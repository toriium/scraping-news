from datetime import datetime


def now_timestamp_str() -> str:
    now = datetime.now()
    return now.strftime("%Y%m%d_%H%M%S")


if __name__ == '__main__':
    print(now_timestamp_str())
