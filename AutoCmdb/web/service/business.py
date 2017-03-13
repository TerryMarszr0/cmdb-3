#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:zhangcong
# Email:zc_92@sina.com
import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from .base import BaseServiceList


class Business(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'id', 'text': '业务线', 'condition_type': 'select', 'global_name': "name_list"},
        ]

        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "ID",  # 前段表格中显示的标题
                'display': 1,  # 是否在前端显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前端显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {}  # 自定义属性
            },
            {
                'q': 'name',
                'title': "业务线",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {}
            },
            {
                'q': 'contact__name',
                'title': "业务联系人",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@contact__name'}},
                'attr': {}
            },
            {
                'q': 'manager__name',
                'title': "系统管理员",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@manager__name'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "选项",
                'display': 1,
                'text': {
                    'content': "<a href='/asset-{device_type_id}-{nid}.html'>查看详细</a> | <a href='/edit-asset-{device_type_id}-{nid}.html'>编辑</a>",
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id'}},
                'attr': {}
            },
        ]
        # 额外搜索条件
        # extra_select = {
        #     'server_title': 'select hostname from repository_server where repository_server.asset_id=repository_asset.id and repository_asset.device_type_id=1',
        #     'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        # }
        extra_select = {}
        super(Business, self).__init__(condition_config, table_config, extra_select)

    @property
    def name_list(self):
        result = models.BusinessUnit.objects.all().values('id', 'name')
        # result = map(lambda x: {'id': x[0], 'name': x[1]}, models.BusinessUnit.objects.all().values('name'))
        print(list(result))
        return list(result)

    @staticmethod
    def business_condition(request):
        """根据搜索条件构造 q 对象"""
        con_str = request.GET.get('condition', None)
        if not con_str:
            con_dict = {}
        else:
            con_dict = json.loads(con_str)

        con_q = Q()
        for k, v in con_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item))
            con_q.add(temp, 'AND')

        return con_q

    def fetch_business(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.business_condition(request)     # 根据搜索条件构造 q 对象
            print(conditions)
            asset_count = models.BusinessUnit.objects.filter(conditions).count()   # 根据搜索条件统计搜索总数量
            page_info = PageInfo(request.GET.get('pager', None), asset_count)   # 使用 PageInfo 构造 分页
            asset_list = models.BusinessUnit.objects.filter(conditions).extra(select=self.extra_select).values(*self.values_list)[page_info.start:page_info.end]

            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(asset_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'name_list': self.name_list,
            }
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def delete_assets(request):
        response = BaseResponse()
        try:
            delete_dict = QueryDict(request.body, encoding='utf-8')
            id_list = delete_dict.getlist('id_list')
            models.Asset.objects.filter(id__in=id_list).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def put_assets(request):
        response = BaseResponse()
        try:
            response.error = []
            put_dict = QueryDict(request.body, encoding='utf-8')
            update_list = json.loads(put_dict.get('update_list'))
            error_count = 0
            for row_dict in update_list:
                nid = row_dict.pop('nid')
                num = row_dict.pop('num')
                try:
                    models.Asset.objects.filter(id=nid).update(**row_dict)
                except Exception as e:
                    response.error.append({'num': num, 'message': str(e)})
                    response.status = False
                    error_count += 1
            if error_count:
                response.message = '共%s条,失败%s条' % (len(update_list), error_count,)
            else:
                response.message = '更新成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def assets_detail(device_type_id, asset_id):

        response = BaseResponse()
        try:
            if device_type_id == '1':
                response.data = models.Server.objects.filter(asset_id=asset_id).select_related('asset').first()
            else:
                response.data = models.NetworkDevice.objects.filter(asset_id=asset_id).select_related('asset').first()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response