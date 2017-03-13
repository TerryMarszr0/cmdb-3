#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:zhangcong
# Email:zc_92@sina.com

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse

from web.service import asset
from web.service import business


class BusinessListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'business_list.html')


class BusinessJsonView(View):
    def get(self, request):
        obj = business.Business()
        response = obj.fetch_business(request)

        # print(response.__dict__)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = asset.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = asset.Asset.put_assets(request)
        return JsonResponse(response.__dict__)