from datetime import datetime
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")


def execute(argument: dict):
    now = datetime.now(IST)
    return now.strftime("%d-%m-%Y %I:%M:%S %p") + " IST"


if __name__ == "__main__":
    print("Time tool\n")
    print(execute({}))