import unittest
import time
import datetime

from taskTimer.timer import Timer


class TestTimer(unittest.TestCase):
    def setUp(self):
        self.timer = Timer()

    def test_timer_start(self):
        self.assertFalse(self.timer._started)  # pylint: disable=protected-access

        self.timer.start()
        self.assertTrue(self.timer._started)  # pylint: disable=protected-access

    def test_timer_started(self):
        self.timer.start()
        self.assertEqual(datetime.datetime.now(), self.timer.started())

        time.sleep(1)
        self.assertNotEqual(datetime.datetime.now(), self.timer.started())

    def test_timer_setStarted(self):
        self.timer.start()
        test_datetime = datetime.datetime(year=1, month=1, day=1)
        self.timer.setStarted(test_datetime)

        self.assertNotEqual(datetime.datetime.now(), self.timer.started())
        self.assertEqual(test_datetime, self.timer.started())
        self.assertRaises(ValueError, self.timer.setStarted, "bad value")

    def test_timer_isActive(self):
        self.assertFalse(self.timer.isActive())

        self.timer.start()
        self.assertTrue(self.timer.isActive())

    def test_timer_stop(self):
        self.assertFalse(self.timer._ended)  # pylint: disable=protected-access

        self.timer.start()
        self.timer.stop()
        self.assertTrue(self.timer._ended)  # pylint: disable=protected-access

    def test_timer_ended(self):
        self.timer.start()
        self.timer.stop()
        self.assertEqual(datetime.datetime.now(), self.timer.ended())

        time.sleep(1)
        self.assertNotEqual(datetime.datetime.now(), self.timer.ended())

    def test_timer_setEnded(self):
        self.timer.start()
        self.timer.stop()
        test_datetime = datetime.datetime(year=1, month=1, day=1)
        self.timer.setEnded(test_datetime)

        self.assertNotEqual(datetime.datetime.now(), self.timer.ended())
        self.assertEqual(test_datetime, self.timer.ended())
        self.assertRaises(ValueError, self.timer.setEnded, "bad value")

    def test_timer_elapsed(self):
        elapsed = self.timer.elapsed()
        self.assertFalse(elapsed)
        self.assertTrue(elapsed == datetime.timedelta(seconds=0))

        self.timer.start()
        time.sleep(1)
        elapsed = self.timer.elapsed()
        self.assertTrue(elapsed)
        self.assertTrue(isinstance(elapsed, datetime.timedelta))
        self.assertTrue(elapsed > datetime.timedelta(seconds=1))

    def test_timer_setElapsed(self):
        delta = datetime.timedelta(seconds=999)
        self.timer.setElapsed(delta)
        self.assertTrue(self.timer.elapsed() == delta)
        self.assertEqual(self.timer._timer_start, None)  # pylint: disable=protected-access

        self.timer.start()
        now = datetime.datetime.now()
        time.sleep(1)
        self.timer.setElapsed(delta)
        self.assertTrue(self.timer._timer_start > now)  # pylint: disable=protected-access

        self.assertRaises(ValueError, self.timer.setElapsed, "bad value")

    def test_timer_reset(self):
        self.timer.start()
        delta = datetime.timedelta(seconds=999)
        self.timer.setElapsed(delta)
        self.timer.stop()

        fresh_timer = Timer()
        # pylint: disable=protected-access
        self.assertNotEqual(self.timer._started, fresh_timer._started)
        self.assertNotEqual(self.timer._elapsed_delta, fresh_timer._elapsed_delta)
        self.assertNotEqual(self.timer._timer_start, fresh_timer._timer_start)
        self.assertNotEqual(self.timer._ended, fresh_timer._ended)

        self.timer.reset()
        self.assertEqual(self.timer._started, fresh_timer._started)
        self.assertEqual(self.timer._elapsed_delta, fresh_timer._elapsed_delta)
        self.assertEqual(self.timer._timer_start, fresh_timer._timer_start)
        self.assertEqual(self.timer._ended, fresh_timer._ended)
        # pylint: enable=protected-access

    def test_timer_toggle(self):
        self.assertFalse(self.timer.isActive())
        self.timer.toggle()
        self.assertTrue(self.timer.isActive())
        self.timer.toggle()
        self.assertFalse(self.timer.isActive())


if __name__ == '__main__':
    unittest.main()