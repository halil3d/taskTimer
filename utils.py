from collections import OrderedDict


def convertTime(value, src_unit, dst_unit):
    """
    Convert a unit of time from a source unit to a destination unit
    """
    newValue = float(value) * timeMultiplier(src_unit, dst_unit)
    return newValue


def stringToTime(timeStr, unit='us'):
    """
    Convert any time string to the given unit returning a float value.

    Eg:
    stringToTime("1hrs", 'mins')
    >>>60.0
    stringToTime("1d", 'hrs')
    >>>24.0
    stringToTime("0.5y 1w 5d 3.5h 50m 15s 20ms 6us", 'weeks')
    >>>27.8288327
    stringToTime("0.5d 6hrs", 'hrs')
    >>>18.0
    """
    if not isinstance(timeStr, basestring):
        print "Please specify a time string"
        return

    timeDict = _timeStringToDict(timeStr)
    timeValue = 0
    for unitStr, unitValue in timeDict.items():
        timeValue += convertTime(unitValue, unitStr, unit)

    return timeValue


def timeToString(timeValue, inputUnit='ms', minUnit='us'):
    """
    Convert time value to a string
    """
    if not timeValue:
        print "Please specify time and unit."
        return

    timeDict = OrderedDict([
        ('year', 0.0),
        ('month', 0.0),
        ('week', 0.0),
        ('day', 0.0),
        ('hour', 0.0),
        ('minute', 0.0),
        ('second', 0.0),
        ('millisecond', 0.0),
        ('microsecond', 0.0)
    ])

    for timeStr in timeDict:
        unitValue = convertTime(timeValue, inputUnit, timeStr)
        timeDict[timeStr] = float(int(unitValue))  # round to nearest as float
        timeValue = timeValue - convertTime(timeDict[timeStr], timeStr, inputUnit)
        if _unitFromString(timeStr) == _unitFromString(minUnit):
            break

    timeStrTokens = []
    for timeUnit, timeValue in timeDict.items():
        if timeValue:
            plural = "s" if timeValue > 1 else ""
            timeStrTokens.append("%s %s%s" % (
                str(int(timeValue)), str(timeUnit), plural))

    timeStr = ""
    for i, token in enumerate(timeStrTokens, start=1):
        if len(timeStrTokens) > 1 and i < len(timeStrTokens):
            timeStr += "%s, " % token
        else:
            timeStr += token

    return timeStr


def isValidTimeString(timeStr):
    isValid = True
    timeStr = str(timeStr).replace(',', ' ')
    tokens = timeStr.split(' ')
    for token in tokens:
        # Get the value of time within the token, account for decimal places
        timeVal = ''.join([digit for digit in token if digit.isdigit() or digit == '.'])
        if not timeVal:
            isValid = False
            break
        unitStr = token.strip(timeVal)
        try:
            # Get the known equivalent unit string
            unit = _unitFromString(unitStr)
        except Exception:
            isValid = False
            break
    return isValid


def _timeStringToDict(timeStr):
    """
    Parse time strings to dict with separated units:
    >>>_timeStringToDict('5d 3h 50m 15s 20ms 6us')
    {'d':5, 'h':3, 'm':50, 's':15, 'ms':20, 'us':6}
    >>>_timeStringToDict('5day')  # or '5days'
    {'d':5, 'h':0.0, 'm':0.0, 's':0.0, 'ms':0.0, 'us':0.0}
    >>>_timeStringToDict('24hrs,30mins')
    {'h':24, 'm':30,'m':0.0, 's':0.0, 'ms':0.0, 'us':0.0}
    """
    timeDict = OrderedDict([
        ('y', 0.0),
        ('mth', 0.0),
        ('w', 0.0),
        ('d', 0.0),
        ('h', 0.0),
        ('m', 0.0),
        ('s', 0.0),
        ('ms', 0.0),
        ('us', 0.0)
    ])

    timeStr = str(timeStr).replace(',', ' ')
    tokens = timeStr.split(' ')
    for token in tokens:
        # Get the value of time within the token, account for decimal places
        timeVal = ''.join([digit for digit in token if digit.isdigit() or digit == '.'])
        if not timeVal:
            raise ValueError("Missing time digits:", token)
        unitStr = token.strip(timeVal)
        # Get the known equivalent unit string
        unit = _unitFromString(unitStr)
        timeDict[unit] += float(timeVal)

    return timeDict


def timeMultiplier(src_unit='hr', dst_unit='sec'):
    """
    Return a multiplier between two time units.
    """
    ruler = {
        'd': 86400000000.0,
        'h': 3600000000.0,
        'm': 60000000.0,
        's': 1000000.0,
        'ms': 1000.0,
        'us': 1.0
    }
    ruler['w'] = 7.0 * ruler['d']
    ruler['mth'] = 30.436849917 * ruler['d']
    ruler['y'] = 12.0 * ruler['mth']
    scale = ruler[_unitFromString(src_unit)] / ruler[_unitFromString(dst_unit)]
    return scale


def _unitFromString(unit='sec'):
    """
    Return known time unit.
    """
    unit = unit.lower()
    if unit in ('y', 'year', 'yrs', 'years'):
        return 'y'
    elif unit in ('mon', 'mons', 'mth', 'mths', 'month', 'months'):
        return 'mth'
    elif unit in ('w', 'wk', 'wks', 'week', 'weeks'):
        return 'w'
    elif unit in ('d', 'day', 'days'):
        return 'd'
    elif unit in ('h', 'hr', 'hrs', 'hour', 'hours'):
        return 'h'
    elif unit in ('m', 'min', 'mins', 'minute', 'minutes'):
        return 'm'
    elif unit in ('s', 'sec', 'secs', 'second', 'seconds'):
        return 's'
    elif unit in ('ms', 'millisecond', 'milliseconds'):
        return 'ms'
    elif unit in ('us', 'microsecond', 'microseconds'):
        return 'us'
    else:
        raise TypeError("Unknown time unit:", unit)


if __name__ == "__main__":
    print stringToTime("1hrs", 'mins')
    print stringToTime("1d", 'hrs')
    print stringToTime("0.5y 1w 5d 3.5h 50m 15s 20ms 6us", 'w')
    print stringToTime("26weeks 3days 3hours", 'y')
    print stringToTime("0.5d 6hrs", 'hrs')
    print timeToString(360000, 'ms')
    print timeToString(24, 'w')
    print timeToString(360, 'h')
    print timeToString(2, 'h')
    print timeToString(1, 's')

    print "*" * 80
    elapsed = stringToTime('1h 29mins', 'ms')
    print elapsed
    hours, remainder = divmod(elapsed, timeMultiplier('hours', 'ms'))
    halfHour, remainder = divmod(remainder, timeMultiplier('hours', 'ms') / 2)
    print hours
    print halfHour
    print timeMultiplier('hours', 'ms') / 2

    print isValidTimeString(None)
    print isValidTimeString(1)
    print isValidTimeString("1")
    print isValidTimeString("1h")
