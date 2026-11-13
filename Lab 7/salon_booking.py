def parse_booking(text):
    try:
        if not isinstance(text, str) or ':' not in text:
            return ("", 0.0)

        service, minutes = text.split(':')
        service = service.strip()

        if not service:
            return ("", 0.0)

        duration = float(minutes)

        if not (0 <= duration < float('inf')):
            return ("", 0.0)

        return service.title(), duration

    except (ValueError, TypeError):
        return ("", 0.0)


def duration_average(durations_csv):
    try:
        if not isinstance(durations_csv, str) or not durations_csv.strip():
            return 0

        values = [int(r.strip()) for r in durations_csv.split(',')]

        if not values or any(v < 0 for v in values):
            return 0

        return sum(values) // len(values)

    except (ValueError, TypeError):
        return 0


def payable_bill(text):
    try:
        if not isinstance(text, str) or '|' not in text:
            return 0.0

        bill, discount = text.split('|')

        bill = float(bill)
        discount = float(discount)

        if not (0 <= bill < float('inf')):
            return 0.0

        if not (0 <= discount < float('inf')):
            return 0.0

        total = bill * 1.18 - discount
        return max(total, 0)

    except (ValueError, TypeError):
        return 0.0


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter service:duration in min (e.g. haircut:45): ")
    result = parse_booking(user_input)
    print("Service and Duration:", result)

    print("\n==== Running duration_average ====")
    user_input = input("Enter durations as CSV (e.g. 30,45,60): ")
    result = duration_average(user_input)
    print("Average Duration:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 800|100): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result)


if __name__ == "__main__":
    main()
