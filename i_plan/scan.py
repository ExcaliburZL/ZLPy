# -*- coding: UTF-8 -*-
import tool
import zipfile
import os

'''
    功能描述：
        由系统定时器定时执行扫描。
        获取指定文件夹下的计划文件。将日期不是今天的计划进行压缩打包，并且删除相关压缩过的文本文件
        单个文件打包命名规则是：'时间_我的代办事件.zip'
        多个任务打包命名规则是：'起始时间~结束时间_我的代办事件.zip'
'''

CONFIG = tool.json_config()

def file_zip():
    path = os.path.join(CONFIG["planFolderUrl"],CONFIG["planFolder"])
    all_files = __show_plan_list(path)
    if len(all_files) == 0:
        return
    l = __filter_out_current_plan(all_files)
    if len(l) == 0:
        return
    l.sort()
    zip_name = __zip_name(l)
    try:
        z = zipfile.ZipFile(os.path.join(path, zip_name), 'w')
        for f in l:
            z.write(os.path.join(path, f),f)
    finally:
        z.close()
        del_files(path,l)

def del_files(path,files):
    '''
    删除已经压缩的文本文件
    :param files: 已经压缩文本文件
    :return: 
    '''
    for f in files:
        os.remove(os.path.join(path, f))

def __show_plan_list(path):
    '''
    展示指定文件夹下的所有文件离别
    :param path: 文件夹路径
    :return: [文件名称]
    '''
    list = os.listdir(path)
    if len(list) == 0:
        return []
    return [x for x in list if not tool.is_hidden(x)]

def __zip_name(all_files):
    '''
    获取zip的名称
    :param all_files:[文件] 
    :return: 
    '''
    if len(all_files) == 1:
        return all_files[0:len(all_files) - 6] + CONFIG["compresstionType"]
    begin_t = all_files[0][:10]
    end_t = all_files[len(all_files)-1][:10]
    end = all_files[0][10:len(all_files) - 7] + CONFIG["compresstionType"]
    return begin_t + '~' + end_t + end

#获取除了今天计划外所有非zip的计划列表
def __filter_out_current_plan(all_files):
    if len(all_files) == 0:
        return []
    all_files = __filter_out_zip(all_files)
    return [x for x in all_files if not __is_current_plan(x)]

def __filter_out_zip(all_list):
    #过滤掉zip文件
    return [x for x in all_list if not tool.is_file_type(x,CONFIG["compresstionType"])]

def __is_current_plan(file_name):
    return True if file_name.find(tool.current_date()) != -1 else False

if __name__ == '__main__':
    file_zip()