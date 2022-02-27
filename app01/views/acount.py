from io import BytesIO

from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt

from app01.models import User
from app01.utils.bootstrap import BootstrapModelForm, BootstrapForm
from app01 import models
from app01.utils.code import check_code
from app01.utils.encrypt import md5


class LoginForm(BootstrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(),
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(),

    )

    # 钩子方法将输入框所得密码md5方便与数据库对照
    def clean_password(self):
        password_md5 = md5(self.cleaned_data['password'])
        return password_md5


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    # post验证，存入数据库
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 1.验证验证码是否正确
        input_code = form.cleaned_data.pop('code')
        # 超时获得空字符串返回None
        correct_code = request.session.get('code')
        if not correct_code:
            form.add_error('code', '验证码已超时')
            return render(request, 'login.html', {'form': form})
        if input_code.upper() != correct_code.upper():
            form.add_error('code', '验证码输入有误')
            return render(request, 'login.html', {'form': form})

        # 2.去数据库查找用户
        user_obj = models.User.objects.filter(**form.cleaned_data).first()
        if not user_obj:
            # 若没有找到用户
            form.add_error('password', '用户名或密码错误')  # 为form.password追加错误
            return render(request, 'login.html', {'form': form})
        # 用户名和密码正确，写入session
        request.session['info'] = {
            'status': True,
            'id': user_obj.id,
            'username': user_obj.username,
            'level': user_obj.get_level_display(),
        }

        # 设置用户的session时间
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect('/index/')
    # 数据校验失败重新输入
    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码"""
    img, code_string = check_code()
    # print(code_string)
    # 将正确的验证码存到session中，并设置30s有效时间
    request.session['code'] = code_string
    request.session.set_expiry(30)

    # 将验证码写如内存，并返还
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())


def logout(request):
    # 清除用户session并重定向
    request.session.clear()
    return redirect('/login/')


class registerModelform(BootstrapModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True))

    # sms_code  = forms.CharField(label='短信验证码')
    class Meta:
        model = models.User
        fields = ['username', 'password', 'confirm_password', 'number', ]
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    # md5加密
    def clean_password(self):
        password = self.cleaned_data['password']
        return md5(password)

    # 定义钩子方法实现密码确认的验证
    def clean_confirm_password(self):

        password = self.cleaned_data.get('password')
        confirm_password = md5(self.cleaned_data['confirm_password'])
        # print(password, confirm_password)

        if password != confirm_password:
            raise ValidationError('密码不一致')

        return confirm_password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = models.User.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('该用户名已被占用')
        return username


def register(request):
    if request.method == 'GET':
        form = registerModelform()
        return render(request, 'register.html', {'form': form})

    form = registerModelform(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('/login/')
    return render(request, 'register.html', {'form': form})


def my_course(request, nid):
    user_obj = User.objects.filter(id=nid).first()
    course_list = []
    for i in range(7):
        d_list = []
        for j in range(8):
            course = user_obj.course_set.filter(day_no=i, time=j).first()
            if not course:
                d_list.append('')
            else:
                d_list.append(course.title)
        course_list.append(d_list)

    content = {
        'course_list': course_list,
    }
    return render(request, 'my_course.html', content)
