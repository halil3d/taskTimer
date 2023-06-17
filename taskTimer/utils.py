import re
from collections import OrderedDict

from taskTimer import constants


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
        print("Please specify a time string")
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
        print("Please specify time and unit.")
        return

    timeDict = OrderedDict([
        (constants.YEAR_UNIT_LONG, 0.0),
        (constants.MONTH_UNIT_LONG, 0.0),
        (constants.WEEK_UNIT_LONG, 0.0),
        (constants.DAY_UNIT_LONG, 0.0),
        (constants.HOUR_UNIT_LONG, 0.0),
        (constants.MINUTE_UNIT_LONG, 0.0),
        (constants.SECOND_UNIT_LONG, 0.0),
        (constants.MILLISECOND_UNIT_LONG, 0.0),
        (constants.MICROSECOND_UNIT_LONG, 0.0)
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
    if not isinstance(timeStr, basestring):
        return False

    isValid = True
    tokens = re.split(r', |,|(?<=[^\d]) ', timeStr)
    for token in tokens:
        token = token.replace(' ', '')
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
    {'d':0, 'h':24, 'm':30, 's':0.0, 'ms':0.0, 'us':0.0}
    """
    timeDict = OrderedDict([
        (constants.YEAR_UNIT_SHORT, 0.0),
        (constants.MONTH_UNIT_SHORT, 0.0),
        (constants.WEEK_UNIT_SHORT, 0.0),
        (constants.DAY_UNIT_SHORT, 0.0),
        (constants.HOUR_UNIT_SHORT, 0.0),
        (constants.MINUTE_UNIT_SHORT, 0.0),
        (constants.SECOND_UNIT_SHORT, 0.0),
        (constants.MILLISECOND_UNIT_SHORT, 0.0),
        (constants.MICROSECOND_UNIT_SHORT, 0.0)
    ])

    tokens = re.split(r', |,|(?<=[^\d]) ', timeStr)
    for token in tokens:
        token = token.replace(' ', '')
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
    src_unit = _unitFromString(src_unit)
    dst_unit = _unitFromString(dst_unit)
    src_microseconds = constants.TIME_STRING_TO_MICROSECONDS[src_unit]
    dst_microseconds = constants.TIME_STRING_TO_MICROSECONDS[dst_unit]
    multiplier = src_microseconds / dst_microseconds
    return multiplier


def _unitFromString(unit='sec'):
    """
    Return known time unit.
    """
    unit = unit.lower()
    found_unit = None
    for time_unit, time_strings in constants.UNIT_VALID_STRING_MAPPING.items():
        if unit in time_strings:
            found_unit = time_unit
            break
    else:
        raise TypeError("Unknown time unit: {}".format(unit))

    return found_unit
