from datetime import timezone, timedelta

utc_beijing = timezone(timedelta(hours=8))


def strftime(datetime, timezone=utc_beijing):
    return datetime.replace(tzinfo=timezone.utc) \
                .astimezone(timezone) \
                .strftime(r'%Y-%m-%d %H:%M:%S')