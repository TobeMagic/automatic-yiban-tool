#!user/bin/env python
import tkinter as tk
import traceback
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import *
import pywintypes
import logging
import requests
import time
import win32api
import win32con
from lxml import etree

logger = logging.getLogger(__name__)

# 创建GUI
root = tk.Tk()


def selectPath():
    path_ = askdirectory()
    path.set(path_)
    # print()

# 设置标签信息
path = StringVar()  # 路径变量（可变字符串)
label1 = tk.Label(root, text='账号Cookie：')
label1.grid(row=0, column=0)
label2 = tk.Label(root, text='批改链接：')
label2.grid(row=1, column=0)
label3 = tk.Label(root, text='确定下载文件夹')
label3.grid(row=3, column=0)
label4 = tk.Label(root, text='提示框')
label4.grid(row=5, column=0)
root.title("易班课群作业收集软件")
# 创建输入框
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=10, pady=5, ipadx=200)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, padx=10, pady=5, ipadx=200)
Entry(root, textvariable=path).grid(row=3, column=1, ipadx=200)
Button(root, text="路径选择", command=selectPath).grid(row=3, column=2)
# 消息提示框
text = Text(root)
# text.pack(fill=X, side=BOTTOM)
text.grid(row=5, column=1, padx=5, pady=5, sticky=N + W + W + E)

"""
1. 尝试用seleunim解决，但相对没那么熟练，面对登录cookie等 还不知如何下手
"""
# options = webdriver.ChromeOptions()
# options.add_argument(
#     'Cookie=""
# # web = Chrome(executable_path='chromedriver')
# web.add_cookie("")
#
# web.get("https://www.yooc.me/group/6507710/homework/145796/grade")
# print(web.title)

"""
2. 可用爬虫实现（附带cookie很简单就登陆进去了），获取附件下载链接到文件中，随后直接下载到对应文件
"""


# 运行任务
def getTask():
    try:
        # print('账号Cookie：%s' % entry1.get())
        # print('批改链接：%s' % entry2.get())
        text.insert(END, '账号Cookie：%s \n' % entry1.get())
        text.insert(END, '批改链接：%s \n' % entry2.get())
        text.see(END)
        text.update()

        # cookie = entry1.get()
        cookie = entry1.get()
        # list_url = entry2.get()
        list_url = "https://www.yooc.me/group/6828525/homework/162730/grade"
        root_url = "https://www.yooc.me"
        headers = {
            'Cookie': cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }

        session = requests.Session()
        # pages = 5
        attachment_url = []
        attachment_name = []
        student_name = []
        homework_url = []
        # 爬取每一页list
        # for page in range(1, pages + 1):
        # list_url = f"https://www.yooc.me/group/6828525/homework/155044/grade?type=1&keyword=&team=&page=2"  # todo 注意是批改作业页面
        resp = session.get(url=list_url, headers=headers)
        html = etree.HTML(resp.text)
        student_list = html.xpath("/html/body/section/section/section/div[2]/table/tr")  # 获取不到原始信息？（删除掉tbody

        # 爬取每位学生作业url 及 name
        for student in student_list:
            student_name.append(student.xpath("./td[2]/text()")[0])
            homework_url.append(student.xpath("./td[6]/a/@href")[0])
            # student_dict[homework_url[0]] = student_name[0]

        # 爬取附件url
        for i, url in enumerate(homework_url):
            # homework_resp = session.get(url="https://www.yooc.me/group/6507710/homework/145796/grade/hu/7269658?htype=1",headers=headers)
            homework_resp = session.get(url=url, headers=headers)
            # print(student_dict)
            sub_html = etree.HTML(homework_resp.text)
            try:
                attachment_url.append(root_url + sub_html.xpath("//a[@class='downl']/@href")[0])
                attachment_name.append(sub_html.xpath("/html/body/section/section/div[2]/div[1]/div[1]/p/text()")[0])
            except IndexError as e:
                # ("errer: " + student_name[i] + "可能未提交附件")
                # showerror("error", student_name[i] + "可能未提交附件")
                text.insert(END, student_name[i] + "可能未提交附件 \n")
                showinfo(title="警示", message=student_name[i] + "可能未提交附件 \n")
                text.see(END)
                text.update()
        # showinfo(title="提示", message="全部学生：" + " ".join(student_name))
        text.insert(END, "全部学生" + str(len(student_name)) + ":" + " ".join(student_name) + "\n")
        text.see(END)
        text.update()
        # win32api.MessageBox(0, "学生：" + " ".join(student_name),
        #                     "提示！",win32con.MB_OK)
        # print("学生：" + " ".join(student_name))
        showinfo(title="警示", message="附件："
                                     "" + str(len(attachment_url)) + " 学生个数:" + str(len(student_name)) + "" if len(
            attachment_url) == len(student_name) else "附件与学生个数不一致，可能有同学未交附件\n")
        # win32api.MessageBox(0, "附件：" + str(len(attachment_url)) + " 学生个数:" + str(len(student_name)) + "" if len(attachment_url) == len(
        #     student_name) else "可能有同学未交附件",
        #                     "提示！",win32con.MB_OK)
        # print("附件：" + str(len(attachment_url)) + " 学生个数:" + str(len(student_name)) + "" if len(attachment_url) == len(
        #     student_name) else "可能有同学未交附件")
        time.sleep(1)

        # 下载附件
        for attachment, filename in zip(attachment_url, attachment_name):
            # showinfo(title="提示", message=attachment + filename)
            text.insert(END, "正在下载" + attachment + filename + "\n")
            text.see(END)
            text.update()
            # win32api.MessageBox(0, attachment + filename,
            #                     "提示！", win32con.MB_OK)
            # print(attachment, filename)
            # with open(file="./attachments/" + filename, mode="wb") as f:
            print(str(path))
            with open(file=path.get() + "/" + filename, mode="wb") as f:
                f.write(requests.get(attachment).content)
            time.sleep(2)
            # print("over!")
            text.insert(END, attachment + filename + "下载完毕 \n")
            text.see(END)
            text.update()
            # showinfo(title="提示", message="over!")

            # win32api.MessageBox(0, "over!",
            #                         "提示！", win32con.MB_OK)
        # win32api.MessageBox(1, "all over!",
        #                     "提示！", win32con.MB_OK)
        showinfo(title="提示", message="全部采集完毕")
    except Exception as e:
        win32api.MessageBox(0, "Cookie填写错误或链接错误！",
                            "警告！", win32con.MB_OK)
        # e.format_exc()
        print(traceback.format_exc())
        # logger.warning("all over!!")


# selenium 下载实现
# web = Chrome(executable_path='chromedriver')
# web.get(attachment)  # selenium 模拟浏览器直接下载，该页面下载无需登录权限！
# time.sleep(2)  # selenium 问题存在 反复请求之后需要登录，且下载加载缓慢
# web.close()
button1 = tk.Button(root, text='开始收集', command=getTask).grid(row=4, column=0,
                                                             sticky=tk.W, padx=30, pady=5)
button2 = tk.Button(root, text='退出', command=root.quit).grid(row=4, column=1,
                                                             sticky=tk.E, padx=30, pady=5)
tk.mainloop()
# import os
# import sys
# import win32con
# import win32api
# from tkinter import *
#
# root = Tk()
# root.resizable(width=False, height=False)
# text = Text(root)
# text.pack(fill=X, side=BOTTOM)
# text.grid(row=0, padx=2, pady=2)
#
#
# def hello():
#     #    print('hello')
#     text.insert(END, 'hello' + '\n')
#
#
# def about():
#     #    print('ok')
#     text.insert(END, 'ok' + '\n')
#
#
# def change():
#     root.update()
#
#
# def delete():
#     text.delete(1.0, END)
#
#
# def Exit():
#     os._exit(0)
#
#
# def show():
#     try:
#         # 你要的在这里
#         #        f = sys.stdout
#         f = os.popen('a.py')
#         for l in iter(f.readline, ''):
#             #            print(l,end='')
#             text.insert(END, l)
#             text.see(END)
#             text.update()
#
#     except:
#         win32api.MessageBox(0, "文件读写错误！",
#                             "警告！", win32con.MB_OK)
#
#
# menubar = Menu(root)
#
# filemenu = Menu(menubar, tearoff=0)
# filemenu.add_command(label="开始", command=show)
# filemenu.add_command(label="清除", command=delete)
# filemenu.add_command(label="退出", command=Exit)
# menubar.add_cascade(label="文件", menu=filemenu)
#
# helpmenu = Menu(menubar, tearoff=0)
# helpmenu.add_command(label="关于", command=about)
# helpmenu.add_command(label="帮助", command=hello)
# menubar.add_cascade(label="帮助", menu=helpmenu)
#
# root.config(menu=menubar)
#
# mainloop()
