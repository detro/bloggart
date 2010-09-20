from datetime import timedelta, tzinfo

class SST(tzinfo):
    """Fixed offset, non-DST."""

    def utcoffset(self, dt):
        return timedelta(hours=8)

    def tzname(self, dt):
        return "Asia/Singapore"

    def dst(self, dt):
        return timedelta(0)
