from django.contrib import auth
from django.shortcuts import redirect, render,reverse
from user.forms import RegForm
from django.views.generic import View
from django.contrib.auth.models import User

class Register(View):

    def get(self,request):
        reg_form = RegForm()
        context = {}
        context['reg_form'] = reg_form
        return render(request, 'register.html', context)

    def post(self,request):

        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data.get('username')
            password = reg_form.cleaned_data.get('password')
            email = reg_form.cleaned_data.get('email')
            #创建用户
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            #登录用户
            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return redirect(request.GET.get('path',reverse('home')))
        else:
            print(reg_form.errors.get_json_data())
            page = request.GET.get('page','/')
            return redirect(reverse('register')+'?page=%s'%page)


