#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from web.service import chart

from web.views.account import is_login


class IndexView(View):

    @is_login
    def dispatch(self, request, *args, **kwargs):
        result = super(IndexView, self).dispatch(request, *args, **kwargs)

        return result

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')



class CmdbView(View):
    @is_login
    def dispatch(self, request, *args, **kwargs):
        result = super(CmdbView, self).dispatch(request, *args, **kwargs)

        return result

    def get(self, request, *args, **kwargs):
        return render(request, 'cmdb.html')



class ChartView(View):
    @is_login
    def dispatch(self, request, *args, **kwargs):
        result = super(ChartView, self).dispatch(request, *args, **kwargs)

        return result

    def get(self, request, chart_type):
        if chart_type == 'business':
            response = chart.Business.chart()
            print(response.data)
        if chart_type == 'dynamic':
            last_id = request.GET.get('last_id')
            response = chart.Dynamic.chart(last_id)
        return JsonResponse(response.__dict__, safe=False, json_dumps_params={'ensure_ascii': False})
