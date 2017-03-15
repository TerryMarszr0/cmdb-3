#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:zhangcong
# Email:zc_92@sina.com

from django.views import View
from django.shortcuts import render
from django.http import JsonResponse

from web.service import tag


class TagListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tag_list.html')


class TagJsonView(View):
    def get(self, request):
        obj = tag.Tag()
        response = obj.fetch_tags(request)

        return JsonResponse(response.__dict__)

    # def delete(self, request):
    #     response = asset.Asset.delete_assets(request)
    #     return JsonResponse(response.__dict__)
    #
    # def put(self, request):
    #     response = asset.Asset.put_assets(request)
    #     return JsonResponse(response.__dict__)