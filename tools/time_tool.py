from datetime import datetime, timedelta, timezone


def execute(argument: dict):
    now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    return now.strftime("%d-%m-%Y %I:%M:%S %p") + " IST"


if __name__ == "__main__":
    print("Time tool\n")
    print(execute({}))