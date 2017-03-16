#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse


from web.service import asset
from repository import models
from web.service import forms

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
        obj = asset.Asset.assets_edit_get(device_type_id, asset_nid)

        return render(request, 'asset_edit.html', {'obj': obj})

    def post(self, request, device_type_id, asset_nid):
        ret = asset.Asset.assets_edit_post(request, device_type_id,  asset_nid)
        return redirect('/asset.html')


class AddAssetView(View):
    """添加资产信息"""
    def get(self, request, *args, **kwargs):
        obj = forms.AddAssetForm()
        return render(request, 'asset_add.html', {'obj': obj})

    def post(self, request, *args, **kwargs):
        response = asset.Asset.assets_add(request)
        if response.status:
            return redirect('/asset.html')
        else:
            return render(request, 'asset_add.html', {'obj': response.data})




