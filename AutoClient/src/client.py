#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import time
import hashlib
import requests
from src import plugins
from lib.serialize import Json
from lib.log import Logger
from config import settings




import platform

import threading



class AutoBase(object):
    def __init__(self):
        self.asset_api = settings.ASSET_API         # api url
        self.key = settings.KEY                     # key
        self.key_name = settings.AUTH_KEY_NAME      # key 的名称

    def auth_key(self):
        """
        接口认证
        :return:
        """
        ha = hashlib.md5(self.key.encode('utf-8'))
        time_span = time.time()
        ha.update("%s|%f" % (self.key, time_span))
        # ha.update(bytes("%s|%f" % (self.key, time_span), encoding='utf-8'))
        encryption = ha.hexdigest()
        result = "%s|%f" % (encryption, time_span)
        return {self.key_name: result}

    def get_asset(self):
        """
        get方式向获取未采集的资产
        :return: {"data": [{"hostname": "c1.com"}, {"hostname": "c2.com"}], "error": null, "message": null, "status": true}
        """

        # headers = {}
        # headers.update(self.auth_key())
        # response = requests.get(
        #     url=self.asset_api,
        #     headers=headers
        # )

        try:
            headers = {}
            headers.update(self.auth_key())
            response = requests.get(
                url=self.asset_api,
                headers=headers
            )
        except Exception as e:
            print(e)
            response = e

        return response.json()

    def post_asset(self, msg, callback=None):
        """
        post方式向接口提交资产信息
        :param msg:
        :param callback:
        :return:
        """
        print("msg -----> ", msg)
        status = True
        try:
            headers = {}
            headers.update(self.auth_key())
            response = requests.post(
                url=self.asset_api,
                headers=headers,
                json=msg
            )
        except Exception as e:
            response = e
            status = False
        if callback:
            callback(status, response)

    def process(self):
        """
        派生类需要继承此方法，用于处理请求的入口
        :return:
        """
        raise NotImplementedError('you must implement process method')

    def callback(self, status, response):
        """
        提交资产后的回调函数
        :param status: 是否请求成功
        :param response: 请求成功，则是响应内容对象；请求错误，则是异常对象
        :return:
        """
        print(response)
        if not status:
            Logger().log(str(response), False)
            return
        ret = json.loads(response.text)
        if ret['code'] == 1000:
            Logger().log(ret['message'], True)
        else:
            Logger().log(ret['message'], False)

    @classmethod
    def getPythonVersion(self):
        """查看当前python的版本"""
        version = platform.python_version()
        return version.split('.')[0]


class AutoAgent(AutoBase):
    def __init__(self):
        self.cert_file_path = settings.CERT_FILE_PATH
        super(AutoAgent, self).__init__()

    def load_local_cert(self):
        """
        获取本地以为标识
        :return:
        """
        if not os.path.exists(self.cert_file_path):
            return None
        with open(self.cert_file_path, mode='r') as f:
            data = f.read()
        if not data:
            return None
        cert = data.strip()
        return cert

    def write_local_cert(self, cert):
        """
        写入本地以为标识
        :param cert:
        :return:
        """
        if not os.path.exists(self.cert_file_path):
            os.makedirs(os.path.basename(self.cert_file_path))
        with open(settings.CERT_FILE_PATH, mode='w') as f:
            f.write(cert)

    def process(self):
        """
        获取当前资产信息
        1. 在资产中获取主机名 cert_new
        2. 在本地cert文件中获取主机名 cert_old
        如果cert文件中为空，表示是新资产
            - 则将 cert_new 写入该文件中，发送数据到服务器（新资产）
        如果两个名称不相等
            - 如果 db=new 则，表示应该主动修改，new为唯一ID
            - 如果 db=old 则，表示
        :return:
        """
        server_info = plugins.get_server_info()
        if not server_info.status:
            return
        local_cert = self.load_local_cert()
        if local_cert:
            if local_cert == server_info.data['hostname']:
                pass
            else:
                server_info.data['hostname'] = local_cert
        else:
            self.write_local_cert(server_info.data['hostname'])
        server_json = Json.dumps(server_info.data)
        self.post_asset(server_json, self.callback)


class AutoSSH(AutoBase):
    def process(self):
        """
        根据主机名获取资产信息，将其发送到API
        :return:
        """
        task = self.get_asset()
        if not task['status']:
            Logger().log(task['message'], False)

        pool = ThreadPoolExecutor(10)
        for item in task['data']:
            hostname = item['hostname']
            pool.submit(self.run, hostname)
        pool.shutdown(wait=True)

        # for item in task['data']:
        #     while True:
        #         if threading.active_count() > 10:   # 如果线程数大于10个
        #             time.sleep(2)
        #         else:
        #             hostname = item['hostname']
        #             t = threading.Thread(target=self.run, args=[hostname, ])
        #             t.start()
        #         if item == task[-1]:
        #             break



    def run(self, hostname):
        server_info = plugins.get_server_info(hostname)
        server_json = Json.dumps(server_info.data)
        self.post_asset(server_json, self.callback)


class AutoSalt(AutoBase):
    def process(self):
        """
        根据主机名获取资产信息，将其发送到API
        :return:
        """
        task = self.get_asset()     # 向 api 获取需要采集的资产
        if not task['status']:
            Logger().log(task['message'], False)

        if self.getPythonVersion == 3:
            # python3 线程池执行方法
            from concurrent.futures import ThreadPoolExecutor
            pool = ThreadPoolExecutor(10)
        else:
            # python2 线程池执行方法
            pool = threadPool(10)

        for item in task['data']:
            hostname = item['hostname']
            pool.submit(self.run, hostname)
        pool.shutdown(wait=True)

    def run(self, hostname):
        server_info = plugins.get_server_info(hostname)
        server_json = Json.dumps(server_info.data)
        self.post_asset(server_json, self.callback)


class threadPool(object):
    """线程池"""
    def __init__(self, threadNum):
        """
        :param threadNum: 线程池中的数量
        """
        self.thread_list = []
        self.threadNum = threadNum

    def submit(self, func, *args, **kwargs):
        """
        线程池
        :param func:  需要使用子线程执行的函数名
        :param *args:  函数中的参数
        :return:
        """

        while True:
            if threading.active_count() > self.threadNum:  # 如果线程数大于10个
                continue
            else:
                t = threading.Thread(target=func, args=args)
                t.start()
                self.thread_list.append(t)  # 将线程对象放入列表中
                print("当前线程数: ", threading.active_count())
                break

    def shutdown(self, wait=True):
        """
        是否等待子线程执行完毕
        :param wait: True 表示等待子线程执行完毕在继续, False 表示不等子线程
        :return:
        """
        if wait:
            for t in self.thread_list:  # 循环所有线程对象,判断对象是否处于存活状态,如果是则等待该状态处理完毕
                while True:
                    if t.is_alive():
                        time.sleep(1)
                    else:
                        break