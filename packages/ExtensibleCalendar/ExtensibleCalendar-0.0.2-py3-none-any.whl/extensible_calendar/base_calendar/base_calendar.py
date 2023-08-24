#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2023/8/21 18:13
# file: base_calendar.py
# author: 孙伟亮
# email: 2849068933@qq.com
from __future__ import absolute_import, unicode_literals

import datetime

from base_calendar.constants import holidays, in_lieu_days, workdays
from base_calendar.solar_terms import (
    SOLAR_TERMS_C_NUMS,
    SOLAR_TERMS_DELTA,
    SOLAR_TERMS_MONTH,
    SolarTerms,
)
from base_calendar.utils import add_state, remove_state, select_all


class BaseCalendar(object):
    """
    万年历类
    """
    def __init__(self, app_name="default", app_path="db"):
        """
        :param app_name: 应用名称，默认为default
        :param app_path: 日期配置文件文件夹，默认在项目启动文件所在目录下db文件夹
        """
        self.app_name = app_name
        self.app_path = app_path
        self.all_workday, self.all_un_workday = select_all(self.app_name, self.app_path)

    def _wrap_date(self, date):
        """
        transform datetime.datetime into datetime.date

        :type date: datetime.date | datetime.datetime
        :rtype: datetime.date
        """
        if isinstance(date, datetime.datetime):
            date = date.date()
        return date

    def _validate_date(self, *dates):
        """
        check if the date(s) is supported

        :type date: datetime.date | datetime.datetime
        :rtype: datetime.date | list[datetime.date]
        """
        if len(dates) != 1:
            return list(map(self._validate_date, dates))
        date = self._wrap_date(dates[0])
        if not isinstance(date, datetime.date):
            raise NotImplementedError("unsupported type {}, expected type is datetime.date".format(type(date)))
        min_year, max_year = min(holidays.keys()).year, max(holidays.keys()).year + 5
        if not (min_year <= date.year <= max_year):
            raise NotImplementedError(
                "no available data for year {}, only year between [{}, {}] supported".format(date.year, min_year,
                                                                                             max_year)
            )
        return date

    def is_holiday(self, date):
        """
        check if one date is holiday in China.
        in other words, Chinese people get rest at that day.

        :type date: datetime.date | datetime.datetime
        :rtype: bool
        """
        return not self.is_workday_(date)

    def is_workday_(self, date):
        """
        check if one date is workday in China.
        in other words, Chinese people works at that day.

        :type date: datetime.date | datetime.datetime
        :rtype: bool
        """
        date = self._validate_date(date)

        weekday = date.weekday()
        return bool(date in workdays.keys() or (weekday <= 4 and date not in holidays.keys()))

    def is_workday(self, date):
        return (self.is_workday_(date) or date in self.all_workday) and (date not in self.all_un_workday)

    def is_in_lieu(self, date):
        """
        check if one date is in lieu in China.
        in other words, Chinese people get rest at that day because of legal holiday.

        :type date: datetime.date | datetime.datetime
        :rtype: bool
        """
        date = self._validate_date(date)

        return date in in_lieu_days

    def get_holiday_detail(self, date):
        """
        check if one date is holiday in China,
        and return the holiday name (None if it's a normal day)

        :type date: datetime.date | datetime.datetime
        :return: holiday bool indicator, and holiday name if it's holiday related day
        :rtype: (bool, str | None)
        """
        date = self._validate_date(date)
        if date in workdays.keys():
            return False, workdays[date]
        elif date in holidays.keys():
            return True, holidays[date]
        else:
            return date.weekday() > 4, None

    def get_dates(self, start, end):
        """
        get dates between start date and end date. (includes start date and end date)

        :type start: datetime.date | datetime.datetime
        :type end:  datetime.date | datetime.datetime
        :rtype: list[datetime.date]
        """
        start, end = map(self._wrap_date, (start, end))
        delta_days = (end - start).days
        return [start + datetime.timedelta(days=delta) for delta in range(delta_days + 1)]

    def get_holidays(self, start, end, include_weekends=True):
        """
        get holidays between start date and end date. (includes start date and end date)

        :type start: datetime.date | datetime.datetime
        :type end:  datetime.date | datetime.datetime
        :type include_weekends: bool
        :param include_weekends: False for excluding Saturdays and Sundays
        :rtype: list[datetime.date]
        """
        start, end = self._validate_date(start, end)
        if include_weekends:
            return list(filter(self.is_holiday, self.get_dates(start, end)))
        return list(filter(lambda x: x in holidays, self.get_dates(start, end)))

    def get_workdays(self, start, end, include_weekends=True):
        """
        get workdays between start date and end date. (includes start date and end date)

        :type start: datetime.date | datetime.datetime
        :type end:  datetime.date | datetime.datetime
        :type include_weekends: bool
        :param include_weekends: False for excluding Saturdays and Sundays
        :rtype: list[datetime.date]
        """
        start, end = self._validate_date(start, end)
        if include_weekends:
            return list(filter(self.is_workday, self.get_dates(start, end)))
        return list(filter(lambda x: self.is_workday(x) and x.weekday() < 5, self.get_dates(start, end)))

    def find_workday(self, delta_days=0, date=None):
        """
        find the workday after {delta_days} days.

        :type delta_days: int
        :param delta_days: 0 means next workday (includes today), -1 means previous workday.
        :type date: datetime.date | datetime.datetime
        :param: the start point
        :rtype: datetime.date
        """
        date = self._wrap_date(date or datetime.date.today())
        if delta_days >= 0:
            delta_days += 1
        sign = 1 if delta_days >= 0 else -1
        for i in range(abs(delta_days)):
            if delta_days < 0 or i:
                date += datetime.timedelta(days=sign)
            while not self.is_workday(date):
                date += datetime.timedelta(days=sign)
        return date

    def get_solar_terms(self, start, end):
        """
        生成 24 节气
        通用寿星公式： https://www.jianshu.com/p/1f814c6bb475

        通式寿星公式：[Y×D+C]-L
        []里面取整数； Y=年数的后2位数； D=0.2422； L=Y/4，小寒、大寒、立春、雨水的 L=(Y-1)/4

        :type start: datetime.date
        :param start: 开始日期
        :type end: datetime.date
        :param end: 结束日期
        :rtype: list[(datetime.date, str)]
        """
        if not 1900 <= start.year <= 2100 or not 1900 <= end.year <= 2100:
            raise NotImplementedError("only year between [1900, 2100] supported")
        D = 0.2422
        result = []
        year, month = start.year, start.month
        while year < end.year or (year == end.year and month <= end.month):
            # 按月计算节气
            for solar_term in SOLAR_TERMS_MONTH[month]:
                nums = SOLAR_TERMS_C_NUMS[solar_term]
                C = nums[0] if year < 2000 else nums[1]
                # 2000 年的小寒、大寒、立春、雨水按照 20 世纪的 C 值来算
                if year == 2000 and solar_term in [
                    SolarTerms.lesser_cold,
                    SolarTerms.greater_cold,
                    SolarTerms.the_beginning_of_spring,
                    SolarTerms.rain_water,
                ]:
                    C = nums[0]
                Y = year % 100
                L = int(Y / 4)
                if solar_term in [
                    SolarTerms.lesser_cold,
                    SolarTerms.greater_cold,
                    SolarTerms.the_beginning_of_spring,
                    SolarTerms.rain_water,
                ]:
                    L = int((Y - 1) / 4)
                day = int(Y * D + C) - L
                # 计算偏移量
                delta = SOLAR_TERMS_DELTA.get((year, solar_term))
                if delta:
                    day += delta
                _date = datetime.date(year, month, day)
                if _date < start or _date > end:
                    continue
                result.append((_date, solar_term.value[1]))
            if month == 12:
                year, month = year + 1, 1
            else:
                month += 1
        return result

    def get_month_info(self, year: int, month: int) -> list:
        """

        :param year:
        :param month:
        :return: 指定月的信息
        """
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        days[1] = 29 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 28
        if year < 1582 and year % 4 == 0:
            days[1] = 29
        month_len = days[month - 1]
        calendar_place_info = [[None for j in range(7)] for i in range(6)]
        now_row = {i: 0 for i in range(7)}
        for day in [{"date": datetime.datetime(year=year, month=month, day=day),
                     "is_workday": self.is_workday(datetime.datetime(year=year, month=month, day=day)),
                     "holiday_info": self.get_holiday_detail(datetime.datetime(year=year, month=month, day=day))[1]} for
                    day
                    in
                    range(1, month_len + 1)]:
            weekday: int = day["date"].weekday()

            calendar_place_info[now_row[weekday]][weekday] = day
            if weekday == 6:
                for i in range(7): now_row[i] += 1
        return calendar_place_info

    def _add_un_workday(self, date: datetime.datetime):
        if self.is_workday_(date):
            self.all_un_workday.add(date)
            add_state(date, 0, self.app_name, self.app_path)
        else:
            self.all_workday.remove(date)
            remove_state(date, self.app_name, self.app_path)

    def _remove_un_workday(self, date: datetime.datetime):
        if self.is_workday_(date):
            self.all_un_workday.remove(date)
            remove_state(date, self.app_name, self.app_path)
        else:
            self.all_workday.add(date)
            add_state(date, 1, self.app_name, self.app_path)

    def after_n_day_is_workday(self,delta_days):
        """
        判断n天后是否是工作日（包含自定义工作日），n>0代表n天后，n<0代表abs(n)天前。
        :param delta_days: 间隔天数
        :return:
        """
        return self.is_workday(datetime.datetime.today()+datetime.timedelta(days=delta_days))

