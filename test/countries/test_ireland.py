#  python-holidays
#  ---------------
#  A fast, efficient Python library for generating country, province and state
#  specific sets of holidays on the fly. It aims to make determining whether a
#  specific date is a holiday as fast and flexible as possible.
#
#  Authors: dr-prodigy <dr.prodigy.github@gmail.com> (c) 2017-2023
#           ryanss <ryanssdev@icloud.com> (c) 2014-2017
#  Website: https://github.com/dr-prodigy/python-holidays
#  License: MIT (see LICENSE file)

from datetime import date
from datetime import timedelta as td

from dateutil.relativedelta import MO
from dateutil.relativedelta import relativedelta as rd

from holidays.constants import FRI
from holidays.countries.ireland import IE, IRL, Ireland

from test.common import TestCase


class TestIreland(TestCase):
    def setUp(self):
        self.holidays = Ireland()
        self.holidays_no_observed = Ireland(observed=False)

    def test_country_aliases(self):
        self.assertCountryAliases(Ireland, IE, IRL)

    def test_2020(self):
        self.assertHoliday("2020-01-01", "New Year's Day")
        self.assertHoliday("2020-03-17", "St. Patrick's Day")
        self.assertHoliday("2020-04-13", "Easter Monday")
        self.assertHoliday("2020-05-04", "May Day")
        self.assertNoHoliday("2020-05-08", "May Day")
        self.assertHoliday("2020-06-01", "June Bank Holiday")
        self.assertHoliday("2020-08-03", "August Bank Holiday")
        self.assertHoliday("2020-10-26", "October Bank Holiday")
        self.assertHoliday("2020-12-25", "Christmas Day")
        self.assertHoliday("2020-12-26", "St. Stephen's Day")
        self.assertHoliday("2020-12-28", "St. Stephen's Day (Observed)")

    def test_2023(self):
        self.assertHoliday("2023-01-01", "New Year's Day")
        self.assertHoliday("2023-02-06", "St. Brigid's Day")
        self.assertHoliday("2023-03-17", "St. Patrick's Day")
        self.assertHoliday("2023-04-10", "Easter Monday")
        self.assertHoliday("2023-05-01", "May Day")
        self.assertHoliday("2023-06-05", "June Bank Holiday")
        self.assertHoliday("2023-08-07", "August Bank Holiday")
        self.assertHoliday("2023-10-30", "October Bank Holiday")
        self.assertHoliday("2023-12-25", "Christmas Day")
        self.assertHoliday("2023-12-26", "St. Stephen's Day")

    def test_st_brigids_day(self):
        # St. Brigid's Day
        self.holidays.observed = False

        for year in range(2023, 2100):
            dt = date(year, 2, 1)

            if dt.weekday() == FRI:
                self.assertHoliday(dt, self.holidays)
            else:
                self.assertNoHoliday(dt, self.holidays)
                self.assertHoliday(dt + rd(weekday=MO), self.holidays)
        self.assertNoHolidayName("St. Brigid's Day", Ireland(years=2022))

    def test_may_day(self):
        # Specific Ireland "May Day"
        for dt in [
            date(1978, 5, 1),
            date(1979, 5, 7),
            date(1980, 5, 5),
            date(1995, 5, 8),
            date(1999, 5, 3),
            date(2000, 5, 1),
            date(2010, 5, 3),
            date(2018, 5, 7),
            date(2019, 5, 6),
            date(2020, 5, 4),
        ]:
            self.assertHoliday(dt, self.holidays)
            self.assertNoHoliday(dt + td(days=-1), self.holidays)
            self.assertNoHoliday(dt + td(days=+1), self.holidays)

    def test_st_stephens_day(self):
        # St. Stephen's Day
        self.holidays.observed = False

        for year in range(1900, 2100):
            dt = date(year, 12, 26)
            self.assertHoliday(dt, self.holidays)
            self.assertNoHoliday(dt + td(days=+1), self.holidays)
        self.assertNoHoliday(date(2009, 12, 28), self.holidays)
        self.assertNoHoliday(date(2010, 12, 27), self.holidays)
        self.holidays.observed = True
        self.assertHoliday(date(2004, 12, 28), self.holidays)
        self.assertHoliday(date(2010, 12, 28), self.holidays)
        for year, day in enumerate(
            [
                26,
                26,
                26,
                28,
                26,
                26,
                26,
                26,
                28,
                28,
                26,
                26,
                26,
                26,
                26,
                26,
                26,
                26,
                26,
                26,
                28,
            ],
            2001,
        ):
            dt = date(year, 12, day)
            self.assertHoliday(dt, self.holidays, dt)
            self.assertHoliday(
                self.holidays[dt],
                [
                    "St. Stephen's Day",
                    "St. Stephen's Day (Observed)",
                    "Christmas Day (Observed); St. Stephen's Day",
                    "St. Stephen's Day; Christmas Day (Observed)",
                ],
            )

    def test_special_holidays(self):
        self.assertHoliday("2022-03-18", self.holidays)
