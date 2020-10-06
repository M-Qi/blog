import time

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render,reverse
from .forms import ForgetPassword, LoginForm,RegForm,ChangeNicknameForm,BindEmailForm,ChangePassword
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.
def login(request):
    '''
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request,username=username,password=password)

    referer = request.META.get('HTTP_REFERER',reverse('home'))
    if user:
        auth.login(request,user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message': '用户名或者密码不一样'})'''
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            users = login_form.cleaned_data.get('user')
            auth.login(request,users)
            url = request.GET.get('path',reverse('home'))
            return redirect(url)
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    print(login_form.non_field_errors())
    return render(request, 'login.html', context)

def login_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data.get('user')
        auth.login(request,user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'FAIL'
        data['errmsg'] = '用户名或者密码错误'
    return JsonResponse(data)


def register(request):
    context = {}
    if request.method == 'POST':
        reg_form = RegForm(request.POST,request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data.get('username')
            password = reg_form.cleaned_data.get('password')
            email = reg_form.cleaned_data.get('email')
            # 创建用户
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
            del request.session['register']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            url = request.GET.get('path',reverse('home'))
            return redirect(url)
    else:
        reg_form = RegForm()
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)


def user_info(request):



    return render(request,'user_info.html')


def logout(request):
    auth.logout(request)

    return redirect(reverse('home'))


def change_nickname(request):
    full_path = request.GET.get('from',reverse('home'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname = form.cleaned_data.get('nickname_new')
            user = form.cleaned_data.get('user')
            profile,created = Profile.objects.get_or_create(user=user)
            profile.nickname=nickname
            profile.save()
            return redirect(full_path)
    else:

        form = ChangeNicknameForm()
    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['sub_text'] = '修改'
    context['full_path'] = full_path
    return render(request, 'from.html', context)

def change_password(request):
    full_path = request.GET.get('from',reverse('home'))
    if request.method == 'POST':
        form = ChangePassword(request.POST,user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            user = request.user
            user.set_password(new_password)
            user.save()
            return redirect(full_path)
    else:
        form = ChangePassword()
    context = {}
    context['form'] = form
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['sub_text'] = '修改'
    context['full_path'] = full_path
    return render(request, 'from.html', context)



def bind_email(request):
    full_path = request.GET.get('from',reverse('home'))
    context = {}
    if request.method == 'POST':
        form = BindEmailForm(request.POST,request=request)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = request.user
            print('email=',email)
            user.email = email
            user.save()
            del request.session['bind']

            return redirect(full_path)

    else:
        form = BindEmailForm()
    context['form'] = form
    context['form_title'] = '编辑邮箱'
    context['page_title'] = '编辑邮箱'
    context['sub_text'] = '提交'
    context['full_path'] = full_path
    return render(request,'bind_email.html',context)

def forget_password(request):

    full_path = reverse('home')
    context = {}
    if request.method == 'POST':
        form = ForgetPassword(request.POST, request=request)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            email = form.cleaned_data['email']
            print('email=',email)
            user = User.objects.get(email=email)

            user.set_password(new_password)
            user.save()
            del request.session['forget']

            return redirect(full_path)

    else:
        form = ForgetPassword()
    context['form'] = form
    context['form_title'] = '重置密码'
    context['page_title'] = '重置密码'
    context['sub_text'] = '提交'
    context['full_path'] = full_path
    return render(request, 'forget_password.html', context)


# 导入发送邮件的函数
from django.core.mail import send_mail
from django.conf import settings

import random,re

def send_email(request):
    '''
    发送邮件的函数
    :param request:
    :return:
    '''
    data = {}
    email = request.GET.get('email')
    send_for = request.GET.get('send_for','')

    source = 'jnhioj234iojiofnsdmaio32'
    code = ''.join(random.sample(source,4))
    is_email = re.match('.+163\.com',email)
    now = int(time.time())
    send_code_time = request.session.get('now',0)
    if is_email:
        if (now - send_code_time)<30:
            data['status'] = 'error'
        else:
            print(code)
            print(now)
            request.session[send_for] = code
            request.session['now'] = now
            send_mail(
                subject='接受验证码',
                message='<h1>验证码：</h1>%s'%code,
                from_email=settings.EMAIL_FROM,
                recipient_list=[email],
                html_message='<h1>验证码：</h1>%s'%code
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'error'

    return JsonResponse(data)


