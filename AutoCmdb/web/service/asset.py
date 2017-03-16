#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from .base import BaseServiceList
from web.service import forms


class Asset(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'cabinet_num', 'text': '机柜号', 'condition_type': 'input'},
            {'name': 'device_type_id', 'text': '资产类型', 'condition_type': 'select', 'global_name': 'device_type_list'},
            {'name': 'device_status_id', 'text': '资产状态', 'condition_type': 'select', 'global_name': 'device_status_list'},
            {'name': 'tag__id', 'text': '标签名称', 'condition_type': 'select', 'global_name': 'tag_name_list'},
            {'name': 'idc__id', 'text': 'IDC', 'condition_type': 'select', 'global_name': 'idc_list'},
        ]

        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "ID",  # 前段表格中显示的标题
                'display': 0,  # 是否在前端显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前端显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {}  # 自定义属性
            },
            {
                'q': 'device_type_id',
                'title': "资产类型",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@device_type_list'}},  # 两个 @@ 符号表示需要从全局变量名 device_type_list 中获取 device_type_id对应的值
                'attr': {}
            },
            {
                'q': 'server_title',
                'title': "主机名",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@server_title'}},
                'attr': {}
            },
            {
                'q': 'network_title',
                'title': "网络设备标识",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@network_title'}},
                'attr': {}
            },
            {
                'q': 'idc_id',
                'title': "IDC",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@idc_list'}},
                'attr': {'name': 'idc_id', 'id': '@idc_id', 'origin': '@idc_id', 'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'idc_list'}
            },
            {
                'q': 'cabinet_num',
                'title': "机柜号",
                'display': 1,
                'text': {'content': "{cabinet_num}", 'kwargs': {'cabinet_num': '@cabinet_num'}},
                'attr': {'name': 'cabinet_num', 'edit-enable': 'true', 'edit-type': 'input', 'origin': '@cabinet_num', }
            },
            {
                'q': 'cabinet_order',
                'title': "位置",
                'display': 1,
                'text': {'content': "{cabinet_order}", 'kwargs': {'cabinet_order': '@cabinet_order'}},
                'attr': {'name': 'cabinet_order', 'edit-enable': 'true', 'edit-type': 'input',
                         'origin': '@cabinet_order', }
            },
            {
                'q': 'business_unit_id',
                'title': "业务线ID",
                'display': 0,
                'text': {'content': "", 'kwargs': {}},
                'attr': {}
            },
            {
                'q': 'business_unit__name',
                'title': "业务线",
                'display': 1,
                'text': {'content': "{business_unit__name}", 'kwargs': {'business_unit__name': '@business_unit__name'}},
                'attr': {'name': 'business_unit_id', 'id': '@business_unit_id', 'origin': '@business_unit_id',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'business_unit_list'}
            },
            {
                'q': 'device_status_id',
                'title': "资产状态",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@device_status_list'}},
                'attr': {'name': 'device_status_id', 'id': '@device_status_id', 'origin': '@device_status_id',
                         'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'device_status_list'}
            },
            {
                'q': 'id',
                'title': "标签",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@tagName_list'}},
                'attr': {
                    # 'name': 'device_status_id',
                    # 'id': '@device_status_id',
                    # 'origin': '@device_status_id',
                    # 'edit-enable': 'true',
                    # 'edit-type': 'select',
                    # 'global-name': 'device_status_list'
                }
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
        # 额外搜索条件,这个地方也可以放入全局变量, 然后通过 @@ 来获取
        extra_select = {
            'server_title': 'select hostname from repository_server where repository_server.asset_id=repository_asset.id and repository_asset.device_type_id=1',
            'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        super(Asset, self).__init__(condition_config, table_config, extra_select)

    # 全局变量
    @property
    def device_status_list(self):
        """资产状态"""
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.device_status_choices)
        return list(result)

    @property
    def device_type_list(self):
        """资产类型"""
        result = map(lambda x: {'id': x[0], 'name': x[1]}, models.Asset.device_type_choices)
        return list(result)

    @property
    def idc_list(self):
        values = models.IDC.objects.all().values('id', 'name', 'floor')
        idc_values = []
        for i in values:
            if i['floor']:
                idc_values.append({'id': i['id'], 'name': "%s-%s层" % (i['name'], i['floor'])})
            else:
                idc_values.append({'id': i['id'], 'name': i['name']})
        #
        # values = models.IDC.objects.only('id', 'name', 'floor')
        # result = map(lambda x: {'id': x.id, 'name': "%s-%s" % (x.name, x.floor)}, values)
        return idc_values

    def tagName_list(self, asset_list):
        """获取标签"""
        id_list = []

        result = []

        for i in asset_list:
            id_list.append(i['id'])

        obj = models.Asset.objects.filter(id__in=id_list)
        for i in obj:
            tag_text = ""

            for tag in i.tag.all():
                if tag_text:
                    tag_text += (",%s" % str(tag))
                else:
                    tag_text = str(tag)
            result.append(
                {
                    'id': i.id,
                    'name': tag_text,
                }
            )
        return result

    @property
    def tag_name_list(self):
        result = models.Tag.objects.all().values('id', 'name')

        return list(result)

    @property
    def business_unit_list(self):
        values = models.BusinessUnit.objects.values('id', 'name')
        return list(values)

    @staticmethod
    def assets_condition(request):
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

    def fetch_assets(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.assets_condition(request)     # 根据搜索条件构造 q 对象
            asset_count = models.Asset.objects.filter(conditions).count()   # 根据搜索条件统计搜索总数量
            page_info = PageInfo(request.GET.get('pager', None), asset_count)   # 使用 PageInfo 构造 分页
            asset_list = models.Asset.objects.filter(conditions).extra(select=self.extra_select).values(*self.values_list)[page_info.start:page_info.end]

            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(asset_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'device_status_list': self.device_status_list,
                'device_type_list': self.device_type_list,
                'idc_list': self.idc_list,
                'business_unit_list': self.business_unit_list,
                'tagName_list': self.tagName_list(ret['data_list']),   # 用作资产表中 对应的标签名称
                'tag_name_list': self.tag_name_list,   # 用作搜索条件处显示标签名称搜索条件
            }

            response.data = ret
            response.status = True
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
            if device_type_id in ['1', '2']:    # 硬件服务器 或虚拟机
                response.data = models.Server.objects.filter(asset_id=asset_id).select_related('asset').first()
            else:
                response.data = models.NetworkDevice.objects.filter(asset_id=asset_id).select_related('asset').first()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def assets_edit_get(device_type_id, asset_nid):
        """点击资产的编辑按钮,获取资产的信息"""

        response = Asset.assets_detail(device_type_id, asset_nid)  # 获取的数据和资产详情是一样的

        obj = forms.AddAssetForm()
        obj.fields['device_type_id'].initial = response.data.asset.device_type_id
        obj.fields['device_status_id'].initial = response.data.asset.device_status_id
        obj.fields['hostname'].initial = response.data.hostname
        obj.fields['cabinet_num'].initial = response.data.asset.cabinet_num
        obj.fields['cabinet_order'].initial = response.data.asset.cabinet_order
        if response.data.asset.idc:
            obj.fields['idc_id'].initial = response.data.asset.idc.id
        else:
            obj.fields['idc_id'].initial = ""

        if response.data.asset.business_unit:
            obj.fields['business_unit_id'].initial = response.data.asset.business_unit.id
        else:
            obj.fields['business_unit_id'].initial = ""

        if response.data.asset.tag:
            tag_list = []
            for tag in response.data.asset.tag.all().values_list('id'):
                tag_list.append(tag[0])
            obj.fields['tag'].initial = tag_list
        else:
            obj.fields['tag'].initial = ""

        return obj

    @staticmethod
    def assets_edit_post(request, device_type_id, asset_nid):
        print("request.POST: ", request.POST)
        response = BaseResponse()
        if device_type_id in ['1', '2']:  # 硬件服务器 或虚拟机
            data = {
                "device_type_id": request.POST.get('device_type_id'),
                "device_status_id": request.POST.get('device_status_id'),
                "cabinet_order": request.POST.get('cabinet_order'),
                "business_unit_id": request.POST.get('business_unit_id'),
                "idc_id": request.POST.get('idc_id'),
                "cabinet_num": request.POST.get('cabinet_num'),
            }
            hostname = request.POST.get('hostname')

            models.Server.objects.filter(asset_id=asset_nid).update(hostname=hostname)
            Asset_obj = models.Asset.objects.filter(id=asset_nid)
            Asset_obj.update(**data)

            tag_list = request.POST.get('tag')
            if tag_list:
                tag_obj = models.Tag.objects.filter(id__in=tag_list)
                tmp = []
                for i in Asset_obj.first().tag.all().values_list('id'):
                    tmp.append(i[0])
                Asset_obj.first().tag.remove(*tmp)
                Asset_obj.first().tag.add(*tag_obj)


        # except Exception as e:
        #     response.status = False
        #     response.message = str(e)
        return response



    @staticmethod
    def assets_add(request):
        response = BaseResponse()
        obj = forms.AddAssetForm(request.POST)

        if obj.is_valid():
            hostname = obj.cleaned_data.pop('hostname')
            Server_obj = models.Server.objects.filter(hostname=hostname)

            if Server_obj:  # 判断主机名是否存在
                # 主机名已经存在
                obj.errors['hostname'] = ["主机名已存在"]
            else:
                tag_list = obj.cleaned_data.pop('tag')

                Asset_obj = models.Asset.objects.create(**obj.cleaned_data)

                models.Server.objects.create(hostname=hostname, asset_id=obj.id)

                if tag_list:
                    tag_obj = models.Tag.objects.filter(id__in=tag_list)
                    Asset_obj.tag.add(*tag_obj)

                response.status = True
        else:
            response.status = False

        response.data = obj
        return response





