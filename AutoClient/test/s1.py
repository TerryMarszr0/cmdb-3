#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:zhangcong
# Email:zc_92@sina.com


# import threading
# import time
# import random
#
#
# def func(n):
#     time.sleep(random.randint(1, 5))
#     print(n)
#
#
# class threadPool(object):
#     def __init__(self, threadNum):
#         """
#         :param threadNum: 线程池中的数量
#         """
#         self.thread_list = []
#         self.threadNum = threadNum
#
#     def submit(self, func, *args, **kwargs):
#         """
#         线程池
#         :param func:  需要使用子线程执行的函数名
#         :param *args:  函数中的参数
#         :return:
#         """
#
#         while True:
#             if threading.active_count() > self.threadNum:  # 如果线程数大于10个
#                 continue
#             else:
#                 t = threading.Thread(target=func, args=args)
#                 t.start()
#                 self.thread_list.append(t)  # 将线程对象放入列表中
#                 print("当前线程数: ", threading.active_count())
#                 break
#
#     def shutdown(self, wait=True):
#         """
#         是否等待子线程执行完毕
#         :param wait: True 表示等待子线程执行完毕在继续, False 表示不等子线程
#         :return:
#         """
#         if wait:
#             for t in self.thread_list:  # 循环所有线程对象,判断对象是否处于存活状态,如果是则等待该状态处理完毕
#                 while True:
#                     if t.is_alive():
#                         time.sleep(1)
#                     else:
#                         break
#
# task = range(20)
# obj = threadPool(10)
# for i in task:
#     obj.submit(func, i)
# obj.shutdown()

from config import settings

for k, v in settings.PLUGINS_DICT.items():
    module_path, cls_name = v.rsplit('.', 1)

    cls = getattr(importlib.import_module(module_path), cls_name)
    obj = cls(hostname).execute()
    response.data[k] = obj
    __import__()