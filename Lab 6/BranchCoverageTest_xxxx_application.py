import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# extra_time_charge: validation, membership, rate and long-duration branches
def test_unknown_service_raises():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("nails", 30, "junior", False)


def test_negative_duration_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("spa", -5, "senior", False)


@pytest.mark.parametrize(
    "service,duration,level,member,expected",
    [
        ("haircut", 30, "junior", False, 0),   # exact included limit
        ("haircut", 45, "junior", True, 0),    # member gets 15 extra minutes
        ("colour", 60, "senior", True, 0),     # membership adds time for colour
        ("spa", 90, "senior", True, 0),        # membership does not add spa time
        ("haircut", 40, "junior", False, 100), # junior rate
        ("haircut", 40, "senior", False, 180),# non-junior rate
        ("haircut", 91, "junior", False, 1098),# >60 extra, non-senior
        ("haircut", 91, "senior", False, 1830),# >60 extra, senior surcharge
    ],
)
def test_extra_time_charge_all_calculation_branches(service, duration, level, member, expected):
    assert extra_time_charge(service, duration, level, member) == expected


# can_book: walk-in and regular booking decisions
@pytest.mark.parametrize(
    "party,services,walkin,expected",
    [
        (1, 5, True, True),   # walk-in ignores service count
        (2, 1, True, True),
        (3, 1, True, False),
        (5, 1, False, False), # party too large
        (4, 2, False, True),
        (4, 3, False, False), # too many services
    ],
)
def test_can_book_branches(party, services, walkin, expected):
    assert can_book(party, services, walkin) is expected


# arrival_status: colour/non-colour cutoffs, weekend adjustment and all outcomes
@pytest.mark.parametrize(
    "minutes,is_colour,weekend,expected",
    [
        (5, False, False, "open"),     # non-colour weekday cutoff
        (4, False, False, "late"),
        (-11, False, False, "closed"),
        (10, True, False, "open"),     # colour weekday cutoff
        (9, True, False, "late"),
        (-6, True, False, "closed"),
        (15, False, True, "open"),     # weekend adds 10
        (14, False, True, "late"),
        (-1, False, True, "closed"),
        (20, True, True, "open"),      # colour weekend cutoff
        (19, True, True, "late"),
        (4, True, True, "closed"),
    ],
)
def test_arrival_status_branches(minutes, is_colour, weekend, expected):
    assert arrival_status(minutes, is_colour, weekend) == expected
