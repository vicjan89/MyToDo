import unittest
import main
import datetime

class CrossTest(unittest.TestCase):
    def test_cross1(self):
        ''' time_free ▓▓▓▓
            time_task       ▓▓▓▓'''
        time1 = datetime.datetime(2022, 1, 18, 17)
        timedelta1 = datetime.timedelta(hours=2)
        time2 = datetime.datetime(2022, 1, 18, 6)
        time_task = main.Time_range(time1, timedelta1, 'MyTask', 'Description')
        time_free = main.Time_range(time2, timedelta1)
        self.assertEqual(main.Time_line.cross(time_free, time_task), ([], time_task))

    def test_cross2(self):
        ''' time_free       ▓▓▓▓
            time_task ▓▓▓▓'''
        time1 = datetime.datetime(2022, 1, 18, 6)
        timedelta1 = datetime.timedelta(hours=2)
        time2 = datetime.datetime(2022, 1, 18, 17)
        time_task = main.Time_range(time1, timedelta1, 'MyTask', 'Description')
        time_free = main.Time_range(time2, timedelta1)
        self.assertEqual(main.Time_line.cross(time_free, time_task), ([], None))

    def test_cross3(self):
        ''' time_free ▓▓▓▓
            time_task     ▓▓▓▓'''
        time1 = datetime.datetime(2022, 1, 18, 8)
        timedelta1 = datetime.timedelta(hours=2)
        time2 = datetime.datetime(2022, 1, 18, 6)
        time_task = main.Time_range(time1, timedelta1, 'MyTask', 'Description')
        time_free = main.Time_range(time2, timedelta1)
        self.assertEqual(main.Time_line.cross(time_free, time_task), ([], time_task))

    def test_cross4(self):
        ''' time_free   ▓▓▓▓
            time_task     ▓▓▓▓'''
        time_task = main.Time_range(datetime.datetime(2022, 1, 18, 8), datetime.timedelta(hours=2), 'MyTask', 'Description')
        time_free = main.Time_range(datetime.datetime(2022, 1, 18, 7), datetime.timedelta(hours=2))
        time_test = main.Time_range(datetime.datetime(2022, 1, 18, 9), datetime.timedelta(hours=1), 'MyTask', 'Description')
        self.assertEqual(main.Time_line.cross(time_free, time_task), ([
                                                                          main.Time_range(
                                                                              datetime.datetime(2022, 1, 18, 7),
                                                                              datetime.timedelta(hours=1)),
                                                                          main.Time_range(
                                                                              datetime.datetime(2022, 1, 18, 8),
                                                                              datetime.timedelta(hours=1), 'MyTask', 'Description')
                                                                      ], time_test))

    def test_cross5(self):
        ''' time_free     ▓▓▓▓
            time_task     ▓▓▓▓'''
        time_task = main.Time_range(datetime.datetime(2022, 1, 18, 8), datetime.timedelta(hours=2), 'MyTask', 'Description')
        time_free = main.Time_range(datetime.datetime(2022, 1, 18, 8), datetime.timedelta(hours=2))
        self.assertEqual(main.Time_line.cross(time_free, time_task), ([
                                                                          main.Time_range(
                                                                              datetime.datetime(2022, 1, 18, 8),
                                                                              datetime.timedelta(hours=2), 'MyTask', 'Description')
                                                                      ], None))

    def test_cross6(self):
        ''' time_free       ▓▓▓▓
            time_task     ▓▓▓▓'''
        time_task = main.Time_range(datetime.datetime(2022, 1, 18, 7), datetime.timedelta(hours=2), 'MyTask', 'Description')
        time_free = main.Time_range(datetime.datetime(2022, 1, 18, 8), datetime.timedelta(hours=2))
        self.assertEqual(main.Time_line.cross(time_free, time_task), ([
                                                                          main.Time_range(
                                                                              datetime.datetime(2022, 1, 18, 8),
                                                                              datetime.timedelta(hours=1), 'MyTask', 'Description'),
                                                                          main.Time_range(
                                                                              datetime.datetime(2022, 1, 18, 9),
                                                                              datetime.timedelta(hours=1))
                                                                      ], None))

    def test_cross7(self):
        ''' time_free         ▓▓▓▓
            time_task     ▓▓▓▓'''
        time_task = main.Time_range(datetime.datetime(2022, 1, 18, 7), datetime.timedelta(hours=2), 'MyTask', 'Description')
        time_free = main.Time_range(datetime.datetime(2022, 1, 18, 9), datetime.timedelta(hours=2))
        self.assertEqual(main.Time_line.cross(time_free, time_task), ([], None))

    def test_cross8(self):
        ''' time_free   ▓▓▓▓▓▓
            time_task    ▓▓▓▓'''
        time_task = main.Time_range(datetime.datetime(2022, 1, 18, 8), datetime.timedelta(hours=2), 'MyTask', 'Description')
        time_free = main.Time_range(datetime.datetime(2022, 1, 18, 7), datetime.timedelta(hours=4))
        self.assertEqual(main.Time_line.cross(time_free, time_task), ([
                                                                          main.Time_range(
                                                                              datetime.datetime(2022, 1, 18, 7),
                                                                              datetime.timedelta(hours=1)),
                                                                          main.Time_range(
                                                                              datetime.datetime(2022, 1, 18, 8),
                                                                              datetime.timedelta(hours=2), 'MyTask', 'Description'),
                                                                          main.Time_range(
                                                                              datetime.datetime(2022, 1, 18, 10),
                                                                              datetime.timedelta(hours=1))
                                                                      ], None))

    def test_cross9(self):
        ''' time_free     ▓▓
            time_task    ▓▓▓▓'''
        time_task = main.Time_range(datetime.datetime(2022, 1, 18, 7), datetime.timedelta(hours=4), 'MyTask', 'Description')
        time_free = main.Time_range(datetime.datetime(2022, 1, 18, 8), datetime.timedelta(hours=2))
        time_test = main.Time_range(datetime.datetime(2022, 1, 18, 10), datetime.timedelta(hours=1), 'MyTask', 'Description')
        self.assertEqual(main.Time_line.cross(time_free, time_task), ([
                                                                          main.Time_range(
                                                                              datetime.datetime(2022, 1, 18, 8),
                                                                              datetime.timedelta(hours=2), 'MyTask', 'Description')
                                                                      ], time_test))

if __name__ == '__main__':
    unittest.main()