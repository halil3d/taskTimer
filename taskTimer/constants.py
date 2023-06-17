MICROSECOND_UNIT_LONG = "microsecond"
MILLISECOND_UNIT_LONG = "millisecond"
SECOND_UNIT_LONG = "second"
MINUTE_UNIT_LONG = "minute"
HOUR_UNIT_LONG = "hour"
DAY_UNIT_LONG = "day"
WEEK_UNIT_LONG = "week"
MONTH_UNIT_LONG = "month"
YEAR_UNIT_LONG = "year"

MICROSECOND_UNIT_SHORT = "us"
MILLISECOND_UNIT_SHORT = "ms"
SECOND_UNIT_SHORT = "s"
MINUTE_UNIT_SHORT = "m"
HOUR_UNIT_SHORT = "h"
DAY_UNIT_SHORT = "d"
WEEK_UNIT_SHORT = "w"
MONTH_UNIT_SHORT = "mth"
YEAR_UNIT_SHORT = "y"

MICROSECOND_VALUE = 1.0
MILLISECOND_VALUE = MICROSECOND_VALUE * 1000.0
SECOND_VALUE = MILLISECOND_VALUE * 1000.0
MINUTE_VALUE = SECOND_VALUE * 60.0
HOUR_VALUE = MINUTE_VALUE * 60.0
DAY_VALUE = HOUR_VALUE * 24.0
WEEK_VALUE = DAY_VALUE * 7
MONTH_VALUE = DAY_VALUE * 30.436849917
YEAR_VALUE = MONTH_VALUE * 12

TIME_STRING_TO_MICROSECONDS = {
    MICROSECOND_UNIT_SHORT: MICROSECOND_VALUE,
    MILLISECOND_UNIT_SHORT: MILLISECOND_VALUE,
    SECOND_UNIT_SHORT: SECOND_VALUE,
    MINUTE_UNIT_SHORT: MINUTE_VALUE,
    HOUR_UNIT_SHORT: HOUR_VALUE,
    DAY_UNIT_SHORT: DAY_VALUE,
    WEEK_UNIT_SHORT: WEEK_VALUE,
    MONTH_UNIT_SHORT: MONTH_VALUE,
    YEAR_UNIT_SHORT: YEAR_VALUE,
}

UNIT_VALID_STRING_MAPPING = {
    YEAR_UNIT_SHORT: ("y", "yr", "yrs", "year", "years"),
    MONTH_UNIT_SHORT: ("mon", "mons", "mth", "mths", "mnth", "mnths","month", "months"),
    WEEK_UNIT_SHORT: ("w", "wk", "wks", "week", "weeks"),
    DAY_UNIT_SHORT: ("d", "day", "days"),
    HOUR_UNIT_SHORT: ("h", "hr", "hrs", "hour", "hours"),
    MINUTE_UNIT_SHORT: ("m", "min", "mins", "minute", "minutes"),
    SECOND_UNIT_SHORT: ("s", "sec", "secs", "second", "seconds"),
    MILLISECOND_UNIT_SHORT: ("ms", "millisec", "millisecs", "millisecond", "milliseconds"),
    MICROSECOND_UNIT_SHORT: ("us", "microsec", "microsecs", "microsecond", "microseconds")
}