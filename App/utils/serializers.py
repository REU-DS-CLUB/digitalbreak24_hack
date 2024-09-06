import datetime


def datetime_serializer(dt: datetime.datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")
