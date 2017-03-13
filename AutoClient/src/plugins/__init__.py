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

    if not response.status:
        return response

    for k, v in settings.PLUGINS_DICT.items():

        module_path, cls_name = v.rsplit('.', 1)

        # python2.6 中没有 importlib 模块  __import__ 只能够导入目录,不能够导入文件,
        # 在plugins 目录平级的 __init__.py 文件中需要先导入一下各个插件的函数
        cls = getattr(__import__(module_path), cls_name)
        obj = cls(hostname).execute()
        response.data[k] = obj
    return response


if __name__ == '__main__':
    ret = get_server_info()
