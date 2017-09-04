# -*- coding: UTF-8 -*-

import os
import datetime
import json

def is_file_type(file_name,file_suffix):
    '''
    判断传入的文件是否是指定后缀名类型
    :param file: 文件名称
    :param file_type: 文件名后缀
    :return: True:匹配 False:不匹配
    '''
    if file_suffix == None or file_suffix == '':
        return False
    # file_suffix = '.' + file_suffix
    return True if os.path.splitext(file_name)[1] == file_suffix else False

def current_date():
    '''
    获取当前日期
    :return: y-m-d
    '''
    return datetime.datetime.now().strftime('%Y-%m-%d')

def current_time():
    '''
    获取当前时间
    :return: 24H:m
    '''
    return datetime.datetime.now().strftime('%H:%M')

def is_hidden(file_name):
    '''
    判断文件是否是隐藏文件
    :param file_name: 文件名称
    :return: True:是隐藏文件 False:不是隐藏文件
    '''
    if file_name == '':
        return
    symbol = file_name[0]
    if symbol == '.':
        return True
    return  False

def json_config():
    try:
        f = open("config.json", encoding='utf-8')
        json_config = json.load(f)
    finally:
        f.close()

    return json_config

