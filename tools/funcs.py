# -*- coding: UTF-8 -*-
import os
import sys
import time
import json
import re
# import MySQLdb
import pymysql
import smtplib
import requests
import redis
from queue import Queue
from typing import List, Dict, Tuple, Any, TypeVar
from collections import namedtuple
from functools import wraps
from datetime import timedelta, datetime
from openpyxl.chart import Series, LineChart, Reference, BarChart
from memory_profiler import profile
from concurrent.futures import ThreadPoolExecutor, as_completed
from line_profiler import LineProfiler
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from openpyxl import Workbook
from tqdm import tqdm


def get_divmod(up, down, minute=False, limit=2):
    """
    获取商
    :param up: 被除数
    :param down: 除数
    :param minute: 换算成分钟单位
    :param limit: 保留小数的位数
    :return: 商
    """
    if up == 0:
        return 0
    if down == 0:
        return 0
    if minute:
        return round(up/down/60.0, limit)
    return round(float(up)/down, limit)


def get_date_list(start_date, end_date):
    """
    获取日期列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return:
    """
    start = None
    if start_date is not None:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date is None:
        end = datetime.now()
    else:
        end = datetime.strptime(end_date, "%Y-%m-%d")
    data = []
    for d in gen_dates(start, ((end-start).days + 1)):
        data.append(d.strftime("%Y-%m-%d"))
    return data


def gen_dates(b_date, days):
    day = timedelta(days=1)
    for i in range(days):
        yield b_date + day*i


def cal_read_time(file_path, date):
    start = time.time()
    user_list = get_new_users(date)
    with open(file_path, "r") as f:
        for line in f:
            line_data = line.strip().split("\t")
            user_id = line_data[0]
            if user_id in user_list:
                pass
    end = time.time()
    return "run in {} seconds".format(end-start)


def get_column_name(column):
    """
    :param column: excel中列的偏移量
    :return: 对应列的字母表示
    """
    prefix = 0
    if column > 90:
        prefix = prefix + (column - 65) // 26
        column = column - 26*prefix
    if prefix:
        pre = chr(64 + prefix)
    else:
        pre = ""
    return "{0}{1}".format(pre, chr(column))


def runTime(func):
    @wraps(func)
    def inner(*args, **kwargs):
        print("{0} start at {1}".format(func.__name__, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        print("{0} end at {1}".format(func.__name__, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print("{0} run succeed in {1} second".format(func.__name__, round(end-start), 3))
        return ret
    return inner


def insert_line_chart(ws, save_cell, data_info):
    """

    :param ws:
    :param save_cell:
    :param data_info: {"title": "", "x_title":"", "y_title": "", "data": [(min_col, min_row, max_row)],
    "cat": (min_col, min_row, max_row)}
    :return:
    """
    chart = LineChart()
    if data_info.get("title"):
        chart.title = data_info.get("title")  # 图的标题
    if data_info.get("y_title"):
        chart.y_axis.title = data_info.get("y_title")  # y坐标的标题
    if data_info.get("x_title"):
        chart.x_axis.title = data_info.get("x_title")  # x坐标的标题
    for data_tuple in data_info.get("data"):
        data_min_col, data_min_row, data_max_row = data_tuple
        data = Reference(ws, min_col=data_min_col, min_row=data_min_row, max_row=data_max_row)
        chart.add_data(data, titles_from_data=True)
    cat_min_col, cat_min_row, cat_max_row = data_info.get("cat")
    cats = Reference(ws, min_col=cat_min_col, min_row=cat_min_row, max_row=cat_max_row)
    chart.set_categories(cats)
    ws.add_chart(chart, save_cell)


def eachLineRuntime(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        func_return = func(*args, **kwargs)
        lp = LineProfiler()
        lp_wrap = lp(func)
        lp_wrap(*args, **kwargs)
        lp.print_stats()
        return func_return
    return decorator


def timestamp_to_date(time_stamp, format_string="%Y-%m-%d"):
    time_array = time.localtime(time_stamp/1000)
    str_date = time.strftime(format_string, time_array)
    return str_date


def str_to_timestamp13(str_time, format='%Y-%m-%d %H:%M:%S.%f'):
    time_tuple = datetime.strptime(str_time, format)
    date_stamp = str(int(time.mktime(time_tuple.timetuple())))
    data_microsecond = str("%06d" % time_tuple.microsecond)[0:3]
    ret_stamp = date_stamp + data_microsecond

    return ret_stamp


@eachLineRuntime
def test():
    a_id = "ea696bdb-8f70-40e6-987c-87f7dd79f1b2"
    a_line = "2020-04-26 00:10:04.711	A:selected:hot_category	30:84:54:d5:d8:27	b754ec51-0ed2-434a-8f8c-c9f2fe1402b0	肇庆市	SHORT_VIDEO	WIFI	15	cd6b6023-474f-404f-b078-1037423c7963,26fda36c-d10c-48fb-90f0-a90613419fff,bd36a5b0-78c7-4780-a987-11caa4efb2b4,fa3ebd6c-3ff8-4edb-a3f5-d15fbe65e9b3,d5edf700-a879-4ae8-be5e-3d803c444205,ec73e360-5388-4fa1-9ae9-3c9538cd55d3,b44f9a17-a97f-4abf-8912-09bb1eb58931,64e4fb02-c589-4cd6-9c1a-22d3f2a4782a,70d9a23a-86e4-440d-848f-82a2a0a2be90,cd96925c-7c81-4485-925b-04a370758c8d,bb2579e8-ec85-4ebf-a5c8-f29cdcbdbf43,f2de6b6b-2a7f-42fa-9b47-c432d15d7c15,0a01b863-4d9a-4fde-a86a-a3f63b4a294f,ea696bdb-8f70-40e6-987c-87f7dd79f1b2,610a7b0e-a92f-451d-9436-72c220225543"
    if a_id in a_line:
        pass
    data = a_line.strip().split("\t")
    if a_id in data[8].split(","):
        pass


def main():
    with ThreadPoolExecutor(max_workers=12) as t:
        obj_list = []
        for page in range(1, 10):
            obj = t.submit(test, page)
            obj_list.append(obj)

        for future in as_completed(obj_list):
            data = future.result()
            print(f"main: {data}")
    print("finish")


def producer_func(file, q):
    with open(file, "r") as f:
        for line in f:
            q.put(line)  # TODO 筛选符合条件的数据放入队列
        q.put("Done")


def consumer_func(result, exit_cnt, q):
    n = 0
    while True:
        if n == exit_cnt:
            break
        if q.empty():
            time.sleep(0.2)
        data = q.get()
        if data == "Done":
            n += 1
        else:
            # TODO 队列数据处理后存入result
            result[1] = 1
            pass


def run_with_threadingPool(file_list):
    producer = producer_func
    consumer = consumer_func
    q = Queue()
    result = {}
    with ThreadPoolExecutor(max_workers=13) as t:
        c = t.submit(consumer, result, len(file_list), q)
        obj_list = [c]
        for file in file_list:
            p = t.submit(producer, file, q)
            obj_list.append(p)

        for future in as_completed(obj_list):
            future.result()
    return result


def send_a_mail(subject, content):
    sender = "websiteyao@163.com"
    receiver = [""]
    password = ""
    message = MIMEText(content, "plain", "utf-8")

    message['Subject'] = subject
    message['To'] = ",".join(receiver)
    message['From'] = sender

    smtp = smtplib.SMTP_SSL("smtp.163.com", 587)
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, message.as_string())
    smtp.close()


def send_a_mail_with_files(subject, content, file_path_list):
    sender = "websiteyao@163.com"
    receiver = [""]
    password = ""
    message = MIMEMultipart()
    part = MIMEText(content, "plain", "utf-8")
    message.attach(part)

    message['Subject'] = subject
    message['To'] = ",".join(receiver)
    message['From'] = sender

    for path in file_path_list:
        part = MIMEApplication(open(path, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=path)
        message.attach(part)

    smtp = smtplib.SMTP_SSL("smtp.163.com", 587)
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, message.as_string())
    smtp.close()



def get_startDate_by_endDate(end_date, recent_day_cnt=240) -> str:
    if isinstance(end_date, datetime):
        start_date = (end_date.date() - timedelta(days=recent_day_cnt)).strftime("%Y-%m-%d")
    elif isinstance(end_date, str):
        try:
            end_date_time = datetime.strptime(end_date, "%Y-%m-%d")
            start_date = (end_date_time.date() - timedelta(days=recent_day_cnt-1)).strftime("%Y-%m-%d")
        except ValueError:
            start_date = None
    else:
        start_date = None
    return start_dat
