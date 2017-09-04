# -*- coding: UTF-8 -*-

import os
import tool

CONFIG = tool.json_config()

def write(note):
    #建立文件夹
    path = os.path.join(CONFIG["planFolderUrl"], CONFIG["planFolder"])
    if not create_folder(path):
        return
    #首先判断 文件存在否
    file_url = os.path.join(path,plan_title())
    r = os.path.exists(file_url)
    if r:
        #如果存在 需要在跟在文件内容后面继续写，
        update_plan(file_url, note)
    else:
        add_plan(file_url, note)

def add_plan(file_url,note):
    notes = handle_note(note)
    # context = append_context(notes)
    files = open(file_url, "w")
    try:
        files.write(notes)
    finally:
        files.close

def update_plan(file_url,note):
    exist_files = open(file_url, "a")
    try:
        index = current_index(file_url)
        notes = handle_note(note, index)
        # context = append_context(notes, exist_files)
        exist_files.write(notes)
    finally:
        exist_files.close

#如果存在内容。需要计算下一个新的任务的index
def current_index(file_url):
    file = open(file_url, "r")
    try:
        field_context = file.read()
        list = field_context.split(';')
    finally:
        file.close()
        if len(list) == 0:
            return 1
    return len(list) - 1

def handle_note(note,new_key = 0):
    s = note.split(";")
    context = ""
    for (key, value) in enumerate(s):
        if value == "":
            break
        new_key += 1
        #截取空格 获取提醒时间 如果有的话
        note_list = handle_plan_time(value)
        if len(note_list) > 1:
            context += str(new_key) + "." + note_list[0] + "\t" + note_list[1] + "\t" + tool.current_time() + ";" + "\n"
        else:
            context += str(new_key) + "." + value + "\t" + tool.current_time() + "\t" + tool.current_time() + ";" + "\n"
    return context

def handle_plan_time(note):
    l = note.split(" ")
    if len(l) > 1:
        plan = ""
        p_time = l[len(l) - 1]
        del_p = l.pop()
        n_l = [x for x in l if x != del_p]
        for n in n_l:
            plan += n
        return [plan,p_time]
    return [note]

#格式化内容
def append_context(note,context = None):
    if context == None:
        return note
    context += note
    return context

def plan_time(time):
    if time == "":
        return tool.current_time()
    return time

#建立一个计划文件夹 专门放写的执行计划
def create_folder(file_path = os.curdir):
    '''
    根据指定的目录创建一个新的文件夹 专门用于存放自己的计划或者提醒事项。
    :param file_path: 传入的路径，默认是当前目录下
    :return: 
    '''
    if os.path.exists(file_path):
        return True
    os.mkdir(file_path)
    return  True

#获取文件标题
def plan_title():
    return tool.current_date() + CONFIG["fileName"] +  CONFIG["fileSuffix"]

def begin():
    t = input("请输入计划，多个计划用;隔开: ")
    if t == '':
        return
    write(t)


if __name__ == '__main__':
    begin()