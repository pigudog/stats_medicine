#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import psutil
import time
import math
import datetime
from functools import wraps
from io import StringIO
import pandas as pd


def clear_dir(path):
    '''清空chrome用户文件夹 '''
    for file_name in os.listdir(path):
        # 如果是文件则删除
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        # 如果是文件夹则递归删除
        elif os.path.isdir(file_path):
            clear_dir(file_path)
            os.rmdir(file_path)
            

def shutdown_chrome():
    '''强制关闭chrome，chromedriver进程  '''
    XTpid=psutil.pids()
    for pid in XTpid:
        # try要放在for内，否则多个进程的会导致杀不干净
        try:
            jinc = psutil.Process(pid)
            jincname = jinc.name()
            if jincname == 'chrome.exe':
                jinc.terminate()
            if jincname == 'chromedriver.exe':
                jinc.terminate()
        except Exception as e:
            pass
        

def readhtml_to_df(table_ele,index_col=0, header=0,links=None):
    '''
    传入表格element，pandas读取返回dataframe
    table_ele: 表格元素
    index_col： 行索引
    header： 列索引
    links：捕获links的区域
    '''
    #获取所有表el
    table_html = table_ele.get_attribute('outerHTML') 

    html_io = StringIO(table_html)
    table_df = pd.read_html(html_io,index_col=index_col, header=header, displayed_only=False,  extract_links=links)[0]
    return table_df

def merge_excel_to_dir(path):
    '''
    传入表格element，pandas读取返回dataframe
    table_ele: 表格元素
    index_col： 行索引
    header： 列索引
    links：捕获links的区域
    '''
    #获取所有表el
    table_list = []
    excel_files = os.listdir(path)
    for dir in excel_files:
        file_path = os.path.join(path,dir)
        tmp_df = pd.read_excel(file_path,index_col=0)
        table_list.append(tmp_df)

    res_df = pd.concat(table_list, axis=0)
    return res_df


def check_items_in_list(list_1, list_2):
    '''
    判断列表元素是否都包含在另一个列表中
    '''
    return all(item in list_2 for item in list_1)


def create_dir(path):
    '''
    传入的路径不存在则创建
    '''
    if not os.path.exists(path):
        os.makedirs(path)

def timestamp():
    """10位秒级别时间戳"""
    return int(time.time())

def dt_strftime(fmt="%Y%m"):
    """
    datetime格式化时间
    :param fmt "%Y%m%d %H%M%S
    """
    return datetime.datetime.now().strftime(fmt)


def sleep(seconds=1.0):
    """
    睡眠时间
    """
    time.sleep(seconds)

def running_time(func):
    """函数运行时间"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timestamp()
        res = func(*args, **kwargs)
        print("校验元素done！用时%.3f秒！" % (timestamp() - start))
        return res

    return wrapper

def extracting_numbers(text):
    '''
    从文本中提取数字，并将提取的若干数字片段合并
    '''
    res = re.findall(r'\d+', text)
    number = int(''.join(res) )
    return number

def round_up(number):
    '''
    向上取整
    '''
    return math.ceil(number)