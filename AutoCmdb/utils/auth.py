#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import hashlib
from AutoCmdb.settings import ASSET_AUTH_HEADER_NAME
from AutoCmdb.settings import ASSET_AUTH_KEY
from AutoCmdb.settings import ASSET_AUTH_TIME
from django.http import JsonResponse

# 用于存放已经访问过的 加密字符串和时间戳, 这里用列表进行存储,可以直接放入 redis 或 memcache 中
ENCRYPT_LIST = [
    # {'encrypt': encrypt, 'time': timestamp
]


def api_auth_method(request):
    auth_key = request.META.get('HTTP_AUTH_KEY')
    if not auth_key:
        return False
    sp = auth_key.split('|')
    if len(sp) != 2:
        return False
    encrypt, timestamp = sp
    timestamp = float(timestamp)
    limit_timestamp = time.time() - ASSET_AUTH_TIME
    # print(limit_timestamp, timestamp)

    if limit_timestamp > timestamp:
        return False

    # md5 加密
    ha = hashlib.md5(ASSET_AUTH_KEY.encode('utf-8'))
    ha.update(bytes("%s|%f" % (ASSET_AUTH_KEY, timestamp), encoding='utf-8'))
    result = ha.hexdigest()

    # 判断发送过来的加密字符串是否和 md5 加密的字符串相等
    if encrypt != result:
        return False

    exist = False
    del_keys = []   # 存放需要清除的加密字符串和时间戳

    # 循环一下存放已经访问的 加密字符串和时间戳列表
    for k, v in enumerate(ENCRYPT_LIST):
        print(k, v)
        m = v['time']
        n = v['encrypt']
        if m < limit_timestamp:     # 判断时间是否已经过期,如果过期则加入到需要删除的列表中
            del_keys.append(k)
            continue
        if n == encrypt:            # 如果加密字符串已经存在,则将 exist 置为 True
            exist = True

    print(limit_timestamp, ENCRYPT_LIST, del_keys)

    for k in del_keys:              # 清除需要清除的 加密字符串和时间戳
        if len(ENCRYPT_LIST) > 2:
            del ENCRYPT_LIST[k]

    if exist:   # 如果为真,说明加密字符串已经存在
        return False

    # api认证通过, 将加密字符串和时间戳加入 ENCRYPT_LIST 列表
    ENCRYPT_LIST.append({'encrypt': encrypt, 'time': timestamp})
    return True


def api_auth(func):
    def inner(request, *args, **kwargs):
        if not api_auth_method(request):
            return JsonResponse({'code': 1001, 'message': 'API授权失败'}, json_dumps_params={'ensure_ascii': False})
        return func(request, *args, **kwargs)

    return inner