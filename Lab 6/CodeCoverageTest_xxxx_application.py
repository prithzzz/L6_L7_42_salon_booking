import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


def test_extra_time_charge_within_included_time():
    assert extra_time_charge("haircut", 20, "junior", False) == 0


def test_extra_time_charge_member_haircut():
    assert extra_time_charge("haircut", 40, "junior", True) == 0


def test_extra_time_charge_colour_extra_time():
    assert extra_time_charge("colour", 75, "junior", False) == 150


def test_extra_time_charge_senior_long_extra_time():
    assert extra_time_charge("spa", 160, "senior", False) == 2100


def test_extra_time_charge_unknown_service():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("massage", 30, "junior", False)


def test_extra_time_charge_negative_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -1, "junior", False)


def test_walk_in_booking_allowed():
    assert can_book(2, 3, True) is True


def test_regular_booking_allowed():
    assert can_book(4, 2, False) is True


def test_arrival_status_open():
    assert arrival_status(15, False, False) == "open"


def test_arrival_status_late():
    assert arrival_status(0, False, False) == "late"


def test_arrival_status_closed():
    assert arrival_status(-11, False, False) == "closed"
