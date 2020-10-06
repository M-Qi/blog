from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=20,label='用户名',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'}))
    password = forms.CharField(max_length=16,label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))

    def clean(self):
        # cleaned_data = super(LoginForm, self).clean()
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')
        user = auth.authenticate(username=username_or_email,password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username,password=password)
                if user:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
                else:
                    raise forms.ValidationError('用户名或者密码错误')
            else:
                raise forms.ValidationError('用户名或者密码错误')
        else:
            self.cleaned_data['user'] = user
            return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(min_length=3,max_length=10,label='用户名',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'}))
    password = forms.CharField(min_length=6,max_length=16,label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))
    password_re = forms.CharField(min_length=6,max_length=16,label='重复密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'重复输入密码'}))
    email = forms.EmailField(label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入邮箱'}))
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "请输入验证码"})
    )
    def __init__(self,*args,**kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args,**kwargs)


    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_obj = User.objects.filter(username=username).exists()
        if user_obj:
            raise forms.ValidationError('该用户已经存在')
        else:
            return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_obj = User.objects.filter(email=email).exists()
        if email_obj:
            raise forms.ValidationError('该邮箱已存在')
        else:
            return email
    def clean(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('password_re')
        if pwd1 != pwd2:
            raise forms.ValidationError('两次输入密码不一致')
        else:
            return self.cleaned_data
    def clean_code(self):
        code = self.cleaned_data.get('code','').strip()
        user_code = self.request.session.get('register','')
        if code == '':
            raise forms.ValidationError('验证码不能为空')
        elif code != user_code:
            raise forms.ValidationError('验证码错误')
        else:
            return code


class ChangeNicknameForm(forms.Form):
    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')

        super(ChangeNicknameForm, self).__init__(*args,**kwargs)
    nickname_new = forms.CharField(
        label='新的昵称',
        max_length=12,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入昵称'})
    )
    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录！')
    def clean_nickname(self):
        # 判断昵称是否为空
        nickname = self.cleaned_data.get('nickname_new','').strip()
        if nickname == '':
            raise forms.ValidationError('新的昵称不能为空！')
        else:
            return nickname


class BindEmailForm(forms.Form):

    def __init__(self,*args,**kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args,**kwargs)


    email = forms.CharField(
        label='新的邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'})
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class':"form-control",'placeholder':"请输入验证码"})
    )
    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户未登录')
        if self.request.user.email !='':
            raise forms.ValidationError('用户邮箱已经绑定')
        return self.cleaned_data


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经被绑定')
        else:
            return email

    def clean_code(self):
        code = self.cleaned_data.get('code','').strip()
        user_code = self.request.session.get('bind','')
        if code == '':
            raise forms.ValidationError('验证码不能为空')
        elif code != user_code:
            raise forms.ValidationError('验证码错误')
        else:
            return code


class ChangePassword(forms.Form):


    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePassword, self).__init__(*args,**kwargs)
    old_password = forms.CharField(max_length=16,label='旧密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"请输入原密码"}))
    password = forms.CharField(max_length=16,label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入新密码'}))
    password2 = forms.CharField(max_length=16,label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请再次输入新密码'}))

    def clean(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('password2')
        if pwd1 != pwd2 or pwd1 =='' or pwd2 == '':
            raise forms.ValidationError('请输入正确新密码')
        return self.cleaned_data

    def clean_old_password(self):
        # 验证旧的密码是否正确
        old_password = self.cleaned_data.get('old_password','')
        if self.user.check_password(old_password):
            return self.cleaned_data
        else:
            raise forms.ValidationError('请输入正确的密码！')

class ForgetPassword(forms.Form):
    def __init__(self,*args,**kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgetPassword, self).__init__(*args,**kwargs)


    email = forms.CharField(
        label='您的邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入您的邮箱'})
    )

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class':"form-control",'placeholder':"请输入验证码"})
    )

    new_password = forms.CharField(
        label='新的密码',
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入新密码'})
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('此邮箱不存在！')
        else:
            return email

    def clean_code(self):
        code = self.cleaned_data.get('code', '').strip()
        user_code = self.request.session.get('forget', '')
        if code == '':
            raise forms.ValidationError('验证码不能为空')
        elif code != user_code:
            raise forms.ValidationError('验证码错误')
        else:
            return code






