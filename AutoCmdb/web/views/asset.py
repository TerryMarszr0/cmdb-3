#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from django.forms import Form
from django.forms import widgets
from django.forms import MultipleChoiceField
from django.forms import fields

from utils.response import BaseResponse

from web.service import asset

from repository import models

class AssetListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'asset_list.html')


class AssetJsonView(View):
    def get(self, request):
        obj = asset.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = asset.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = asset.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, device_type_id, asset_nid):
        response = asset.Asset.assets_detail(device_type_id, asset_nid)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class AssetEditlView(View):
    def get(self, request, device_type_id, asset_nid):
        response = asset.Asset.assets_detail(device_type_id, asset_nid)     # 获取的数据和资产详情是一样的

        obj = AddAssetForm()
        print(response.data.asset)
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
            print(tag_list)
            obj.fields['tag'].initial = tag_list
        else:
            obj.fields['tag'].initial = ""


        return render(request, 'asset_edit.html', {'obj': obj})

    def post(self, request):
        print(dir(request))

        return HttpResponse('ok')


class AddAssetForm(Form):
    """新增资产Form表单"""

    device_type_id = fields.ChoiceField(
        choices=models.Asset.device_type_choices,
        widget=widgets.Select(
            attrs={}
        )

    )
    device_status_id = fields.ChoiceField(
        choices=models.Asset.device_status_choices,
        widget=widgets.Select

    )

    hostname = fields.CharField(
        error_messages={
            "required": "主机名不能为空",
        },
        widget=widgets.Input(
            attrs={"class": "form-control", "name": "hostname", "type": "text"})
    )

    cabinet_num = fields.CharField(
        required=False,
        widget=widgets.Input(
            attrs={"class": "form-control", "placeholder": "请输入机柜号,没有可为空", "name": "hostname", "type": "text"})
    )

    cabinet_order = fields.CharField(
        required=False,
        widget=widgets.Input(
            attrs={"class": "form-control", "placeholder": "请输入机柜中所在位置,没有可为空", "name": "hostname", "type": "text"})
    )

    idc_id = fields.ChoiceField(
        required=False,
        choices=[],
        widget=widgets.Select

    )

    business_unit_id = fields.ChoiceField(
        required=False,
        choices=[],
        widget=widgets.Select

    )

    tag = MultipleChoiceField(
        error_messages={
            "required": "标签不能为空",
        },
        choices=models.Tag.objects.all().values_list('id', 'name'),
        widget=widgets.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super(AddAssetForm, self).__init__(*args, **kwargs)

        values = models.IDC.objects.all().values_list('id', 'name', 'floor')
        idc_values = [['', '---------']]
        for i in values:
            idc_values.append([i[0], "%s-%s" % (i[1], i[2])])
        self.fields['idc_id'].choices = idc_values

        values = models.BusinessUnit.objects.values_list('id', 'name')
        business_unit_values = [['', '---------']]
        for i in values:
            business_unit_values.append([i[0], i[1]])
        self.fields['business_unit_id'].choices = business_unit_values


class AddAssetView(View):
    """添加资产信息"""
    def get(self, request, *args, **kwargs):
        obj = AddAssetForm()
        return render(request, 'asset_add.html', {'obj': obj})

    def post(self, request, *args, **kwargs):

        obj = AddAssetForm(request.POST)

        if obj.is_valid():
            hostname = obj.cleaned_data.pop('hostname')
            Server_obj = models.Server.objects.filter(hostname=hostname)

            if Server_obj:  # 判断主机名是否存在
                # 主机名已经存在
                obj.errors['hostname'] = ["主机名已存在"]
            else:
                tag_list = obj.cleaned_data.pop('tag')

                obj = models.Asset.objects.create(**obj.cleaned_data)

                models.Server.objects.create(hostname=hostname, asset_id=obj.id)

                if tag_list:
                    tag_obj = models.Tag.objects.filter(id__in=tag_list)
                    obj.tag.add(*tag_obj)

                return redirect('/asset.html')

        else:
            print(obj.errors)
            # response.status = False
            # response.error = obj.errors
            # print(response.error)

        return render(request, 'asset_add.html', {'obj': obj})




