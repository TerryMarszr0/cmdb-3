#!/usr/bin/env python
# -*- coding:utf-8 -*-
from src.plugins.basic import BasicPlugin
from config import settings


# import importlib


def get_server_info(hostname=None):
    """
    获取服务器基本信息
    :param hostname: agent模式时，hostname为空；salt或ssh模式时，hostname表示要连接的远程服务器
    :return:
    """
    print(hostname)
    response = BasicPlugin(hostname).execute()  # 获取基础数据, 系统平台、系统版本、主机名

    print("response.data", response.data)

    if not response.status:
        return response

    for k, v in settings.PLUGINS_DICT.items():

        module_path, cls_name = v.rsplit('.', 1)
        # v_list = v.split('.')
        # module = v_list[-2]
        # cls_name = v_list[-1]
        print(module_path, cls_name)

        cls = getattr(__import__(module_path), cls_name)    # python2.6 中没有 importlib 模块
        obj = cls(hostname).execute()
        response.data[k] = obj
    return response


if __name__ == '__main__':
    ret = get_server_info()
