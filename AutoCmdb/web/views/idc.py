#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse

from web.service import idc


class IdcListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'idc_list.html')


class IdcJsonView(View):
    def get(self, request):
        obj = idc.IDC()
        response = obj.fetch_idc(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = idc.IDC.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = idc.IDC.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, device_type_id, asset_nid):
        response = idc.IDC.assets_detail(device_type_id, asset_nid)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class AddAssetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_asset.html')


