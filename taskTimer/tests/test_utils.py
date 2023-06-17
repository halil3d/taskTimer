import unittest

from taskTimer import utils, constants


class TestUtils(unittest.TestCase):
    def test_convertTime(self):
        TEST_DATA = [
            {
                "input_value": 60,
                "src_unit": "s",
                "dst_unit": "m",
                "expected_value": 1.0,
            },
            {
                "input_value": 1,
                "src_unit": "week",
                "dst_unit": "days",
                "expected_value": 7.0,
            },
            {
                "input_value": 7,
                "src_unit": "hour",
                "dst_unit": "minutes",
                "expected_value": 420.0,
            },
            {
                "input_value": 0.75,
                "src_unit": "h",
                "dst_unit": "m",
                "expected_value": 45.0,
            },
            {
                "input_value": 1.5,
                "src_unit": "yrs",
                "dst_unit": "months",
                "expected_value": 18.0,
            },
            {
                "input_value": 1000,
                "src_unit": "ms",
                "dst_unit": "sec",
                "expected_value": 1.0,
            },
        ]

        for data in TEST_DATA:
            self.assertEqual(
                utils.convertTime(
                    data["input_value"],
                    data["src_unit"],
                    data["dst_unit"],
                ),
                data["expected_value"])

    def test_stringToTime(self):
        TEST_DATA = []
        for time_unit in constants.UNIT_VALID_STRING_MAPPING:
            TEST_DATA.append(
                {
                    "input_value": "1{}".format(time_unit),
                    "dst_unit": "microseconds",
                    "expected_value": constants.TIME_STRING_TO_MICROSECONDS[time_unit],
                },
            )
            TEST_DATA.append(
                {
                    "input_value": "1 {}".format(time_unit),
                    "dst_unit": "microseconds",
                    "expected_value": constants.TIME_STRING_TO_MICROSECONDS[time_unit],
                },
            )

        TEST_DATA.extend([
            {
                "input_value": "1day",
                "dst_unit": "hr",
                "expected_value": 24.0,
            },
            {
                "input_value": "0.5y, 2mth, 1w, 5d, 3.5h, 50m, 15s, 20ms, 5us",
                "dst_unit": "w",
                "expected_value": 36.525075533458,
            },
            {
                "input_value": "26weeks 3days 3hours",
                "dst_unit": "year",
                "expected_value": 0.5068554523678481,
            },
            {
                "input_value": "26 weeks 3 days 3 hours",
                "dst_unit": "year",
                "expected_value": 0.5068554523678481,
            },
            {
                "input_value": "26 weeks, 3 days, 3 hours",
                "dst_unit": "year",
                "expected_value": 0.5068554523678481,
            },
            {
                "input_value": "26 weeks,3 days,3 hours",
                "dst_unit": "year",
                "expected_value": 0.5068554523678481,
            },
            {
                "input_value": "0.5d 6hr",
                "dst_unit": "hr",
                "expected_value": 18.0,
            },
        ])
        for data in TEST_DATA:
            self.assertEqual(
                utils.stringToTime(
                    data["input_value"],
                    unit=data["dst_unit"]),
                data["expected_value"]
                )

    def test_timeToString(self):
        TEST_DATA = [
            {
                "input_value": 3600,
                "input_unit": "sec",
                "min_unit": "hr",
                "expected_value": "1 hour",
            },
            # {
            #     "input_value": 1000,
            #     "input_unit": "us",
            #     "min_unit": "hr",
            #     "expected_value": "1 hour",
            # },
        ]

        for data in TEST_DATA:
            self.assertEqual(
                utils.timeToString(
                    data["input_value"],
                    inputUnit=data["input_unit"],
                    minUnit=data["min_unit"]),
                data["expected_value"]
                )

    def test_isValidTimeString(self):
        TRUE_TEST_DATA = []
        FALSE_TEST_DATA = []

        # Multiple spaces
        multiple_units_test_1 = ""
        # Multiple no-spaces and comma
        multiple_units_test_2 = ""
        # Multiple spaces and comma
        multiple_units_test_3 = ""
        for time_unit in constants.TIME_STRING_TO_MICROSECONDS:
            # Single unit no spaces
            TRUE_TEST_DATA.append("1{}".format(time_unit))
            # Single unit spaces
            TRUE_TEST_DATA.append("1 {}".format(time_unit))
            # Single unit decimals
            TRUE_TEST_DATA.append("1.5 {}".format(time_unit))
            multiple_units_test_1 += " 1{}".format(time_unit)
            multiple_units_test_2 += "1{},".format(time_unit)
            multiple_units_test_3 += "1{}, ".format(time_unit)
        TRUE_TEST_DATA.append(multiple_units_test_1)
        TRUE_TEST_DATA.append(multiple_units_test_2.strip(","))
        TRUE_TEST_DATA.append(multiple_units_test_3.strip(", "))

        # Multiple no-spaces
        multiple_units_test_1 = ""
        for i, time_unit in enumerate(constants.TIME_STRING_TO_MICROSECONDS):
            # Time unit only
            FALSE_TEST_DATA.append(time_unit)
            # Digit only
            FALSE_TEST_DATA.append(i)
            multiple_units_test_1 += "1{}".format(time_unit)
        FALSE_TEST_DATA.append(multiple_units_test_1)
        # Unhandled time values
        FALSE_TEST_DATA.append("1/2 day")
        FALSE_TEST_DATA.append("half an hr")
        # Unhandled units
        FALSE_TEST_DATA.append("1 centurary")
        FALSE_TEST_DATA.append("1 decade")
        FALSE_TEST_DATA.append("1 fortnight")
        FALSE_TEST_DATA.append("1 millenia")

        for data in TRUE_TEST_DATA:
            self.assertTrue(utils.isValidTimeString(data))

        for data in FALSE_TEST_DATA:
            self.assertFalse(utils.isValidTimeString(data))

    def test__timeStringToDict(self):
        GOOD_TEST_DATA = [
            {
                "input_data": "5d 3h 50m 15s 20ms 6us",
                "expected_value": {"y": 0.0, "mth": 0.0, "w": 0.0, "d":5.0, "h":3.0, "m":50.0, "s":15.0, "ms":20.0, "us":6.0}
            },
            {
                "input_data": "5day",
                "expected_value": {"y": 0.0, "mth": 0.0, "w": 0.0, "d":5.0, "h":0.0, "m":0.0, "s":0.0, "ms":0.0, "us":0.0}
            },
            {
                "input_data": "24hr,30mins",
                "expected_value": {"y": 0.0, "mth": 0.0, "w": 0.0, "d":0.0, "h":24.0, "m":30.0, "s":0.0, "ms":0.0, "us":0.0}
            },
        ]
        BAD_TEST_DATA = [
            "bad data",
            "2 dayz",
            "13random",
        ]
        for data in GOOD_TEST_DATA:
            self.assertEqual(utils._timeStringToDict(data["input_data"]), data["expected_value"])
        for data in BAD_TEST_DATA:
            self.assertRaises((ValueError, TypeError), utils._timeStringToDict, data)

    def test_timeMultiplier(self):
        TEST_DATA = [
            {
                "src_unit": "us",
                "dst_unit": "ms",
                "expected_value": constants.TIME_STRING_TO_MICROSECONDS["us"] / constants.TIME_STRING_TO_MICROSECONDS["ms"],
            },
            {
                "src_unit": "y",
                "dst_unit": "d",
                "expected_value": constants.TIME_STRING_TO_MICROSECONDS["y"] / constants.TIME_STRING_TO_MICROSECONDS["d"],
            },
            {
                "src_unit": "h",
                "dst_unit": "mth",
                "expected_value": constants.TIME_STRING_TO_MICROSECONDS["h"] / constants.TIME_STRING_TO_MICROSECONDS["mth"],
            },
        ]
        for data in TEST_DATA:
            self.assertEqual(utils.timeMultiplier(data["src_unit"], data["dst_unit"]), data["expected_value"])

    def test_unitFromString(self):
        for unit, valid_values in constants.UNIT_VALID_STRING_MAPPING.items():
            for string_value in valid_values:
                self.assertEqual(utils._unitFromString(string_value), unit)

        BAD_DATA = [
            "invalid",
            "fake",
            "bad",
        ]
        for bad_value in BAD_DATA:
            self.assertRaises(TypeError, utils._unitFromString, bad_value)
