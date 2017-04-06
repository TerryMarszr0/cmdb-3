#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect

from repository import models


from django.forms import Form
from django.forms import widgets
from django.forms import fields

import hashlib


# 给密码加密
def str_encrypt(pwd):
    """
    用户输入的密码加密
    :param pwd: 密码
    :return:
    """
    hash = hashlib.md5()
    hash.update(pwd.encode())
    return hash.hexdigest()


# 装饰器 判断是否登录
def is_login(func):
    """判断是否登录"""

    def inner(cls, request, *args, **kwargs):
        print(request)
        username = request.session.get("username")  # 从session中获取用户的username对应的值
        if not username:
            return redirect("/login.html")
        return func(cls, request, *args, **kwargs)
    return inner


# 登录 Form
class loginForm(Form):
    username = fields.CharField(
        error_messages={
            "required": "用户名不能为空！",
        },
        widget=widgets.Input(
            attrs={"class": "form-control", "placeholder": "用户名", "name": "username", "type": "text"})
    )
    password = fields.CharField(
        error_messages={
            "required": "密码不能为空！",
        },
        widget=widgets.PasswordInput(
            attrs={"class": "form-control", "placeholder": "密码", "name": "password", "type": "password"})

    )


class LoginView(View):

    def dispatch(self, request, *args, **kwargs):

        result = super(LoginView, self).dispatch(request, *args, **kwargs)

        return result

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        obj = loginForm(request.POST)

        if obj.is_valid():
            obj.cleaned_data['password'] = str_encrypt(obj.cleaned_data['password'])
            print(obj.cleaned_data['password'])
            AdminInfo_obj = models.AdminInfo.objects.filter(**obj.cleaned_data).first()
            if AdminInfo_obj:
                request.session['username'] = AdminInfo_obj.username
                request.session['user_id'] = AdminInfo_obj.id
                request.session['is_login'] = True
                return redirect('/')
            else:  # 用户名和密码不匹配
                obj.errors["password"] = ["用户名或密码错误"]

        return render(request, 'login.html', {'obj': obj})



class LogoutView(View):
    def get(self, request, *args, **kwargs):
        request.session.clear()
        return redirect('/login.html')