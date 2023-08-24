#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2023/8/21 16:09
# file: calendar_ui.py
# author: 孙伟亮
# email: 2849068933@qq.com
from __future__ import absolute_import, unicode_literals
import tkinter as tk
from tkinter import ttk  # 导入ttk模块，因为Combobox下拉菜单控件在ttk中
import datetime
from base_calendar import BaseCalendar


class CalendarUi():
    week_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

    def __init__(self, bs_calendar: BaseCalendar):
        self.w, self.h = 600, 500  # 窗口大小
        self.bs_calendar = bs_calendar
        self.today = datetime.date.today()
        self.current_year = self.today.year  # 当前年份
        self.valid_month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.valid_years = list([self.current_year + i for i in range(5)])
        self.year = self.today.year
        self.month = self.today.month
        self.day = self.today.day
        self.formRoot()
        self.design()
        self.root.mainloop()

    def formRoot(self):
        self.root = tk.Tk()
        self.root.title("万年历")
        self.root.geometry(f"{self.w}x{self.h}")  # 窗口大小

    def design(self):
        for idx, name in enumerate(CalendarUi.week_names):
            tk.Label(self.root, text=name, font=("黑体", 12)).place(x=80 + ((self.w - 80 * 2) // 6) * idx, y=100,
                                                                  anchor="center")
        tk.Label(self.root, text=f"应用 : {self.bs_calendar.app_name}", font=("宋体", 12)).place(x=140, y=50,
                                                                                             anchor="center")
        # 年月选择框
        ########################################################
        tk.Label(self.root, text="年份:", font=("宋体", 12)).place(x=100 + 200, y=50, anchor="center")
        self.combobox_year = ttk.Combobox(self.root, width=5)
        self.combobox_year.place(x=150 + 200, y=50, anchor="center")
        self.combobox_year["value"] = self.valid_years
        # 设置下拉菜单的默认值,默认值索引从0开始
        self.combobox_year.current(0)
        self.combobox_year.bind("<<ComboboxSelected>>", self.change_year_or_month)  # <ComboboxSelected>当列表选择时触发绑定函数
        ########################################################
        tk.Label(self.root, text="月份:", font=("宋体", 12)).place(x=250 + 200, y=50, anchor="center")
        self.combobox_month = ttk.Combobox(self.root, width=5)
        self.combobox_month.place(x=300 + 200, y=50, anchor="center")
        self.combobox_month["value"] = self.valid_month
        # 设置下拉菜单的默认值,默认值索引从0开始
        self.combobox_month.current(self.valid_month.index(self.month))
        self.combobox_month.bind("<<ComboboxSelected>>", self.change_year_or_month)  # <ComboboxSelected>当列表选择时触发绑定函数
        ########################################################
        self.render_days()

    def render_days(self):
        self.year = int(self.combobox_year.get())
        self.month = int(self.combobox_month.get())
        self.month_info = self.bs_calendar.get_month_info(year=self.year, month=self.month)
        self.days_info = []
        for row, week_info in enumerate(self.month_info):
            self.days_info.append([])
            for col, day_info in enumerate(week_info):
                if not day_info:
                    self.days_info[row].append(None)
                    continue
                y = 140 + row * 60
                bt = tk.Button(self.root, text=str(day_info["date"].day), font=("Arial Bold", 14), border=False,
                               fg="red" if day_info["is_workday"] else "green",
                               command=self.change_day_state(row=row, col=col))
                bt.place(
                    x=80 + ((self.w - 80 * 2) // 6) * col, y=y,
                    anchor="center")
                lb = tk.Label(self.root, text="班" if day_info["is_workday"] else (
                    "休" if not day_info["holiday_info"] else day_info["holiday_info"]), font=("宋体", 10))
                lb.place(
                    x=80 + ((self.w - 80 * 2) // 6) * col, y=y + 30,
                    anchor="center")
                self.days_info[row].append([bt, lb])

    def change_day_state(self, row, col):
        def change_day_state_():
            old = self.month_info[row][col]["is_workday"]
            if old:
                self.bs_calendar._add_un_workday(self.month_info[row][col]["date"])
            else:
                self.bs_calendar._remove_un_workday(self.month_info[row][col]["date"])
            self.month_info[row][col]["is_workday"] = not old
            self.days_info[row][col][0].configure(fg="red" if not old else "green")
            self.days_info[row][col][1].configure(text="班" if not old else (
                "休" if not self.month_info[row][col]["holiday_info"] else self.month_info[row][col]["holiday_info"]))

        return change_day_state_

    def change_year_or_month(self, event):
        for i in self.days_info:
            for j in i:
                if j:
                    j[0].destroy()
                    j[1].destroy()
        self.render_days()
