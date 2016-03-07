from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import auth
from msgBoard.admin import UserCreationForm
from msgBoard.models import *
from .form import ImageForm


def index(request):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            password = request.POST.get('password', '')
            girl_list = Girl.objects.filter(password=password).all()
            if len(girl_list) == 0:
                return render(request, "index.html", {'error': "暗号不对哦",
                                                      'password': password})
            girl = girl_list[0]
            msg_list = Message.objects.filter(girl=girl).all()
            print(msg_list[0].content)
            return render(request, "display.html", {'msg_list': msg_list})
        else:
            render(request, "index.html")
    if not request.user.is_authenticated():
        return render(request, "index.html")
    girls = Girl.objects.all()
    for x in girls:
        msg = Message.objects.filter(sender=request.user, girl=x).all()
        if not len(msg) == 0:
            x.content = msg[0].content
        else:
            x.content = ''
    return render(request, "index.html", {'girl_list': girls})


@require_http_methods(['POST'])
def new_msg(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    user = request.user
    girl_id = int(request.POST.get('id', ''))
    message = request.POST.get('content', '')
    girl = Girl.objects.filter(id=girl_id).all()
    if len(girl) == 0:
        return HttpResponseRedirect('/')
    msg = Message(sender=user, girl=girl[0], content=message)
    msg.save()
    return HttpResponseRedirect('/')


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def login(request, error_msg=""):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, "login.html", {'error': "该用户已经被禁止登陆",
                                                      'username': username})
        else:
            return render(request, "login.html", {'error': "用户名或密码不正确",
                                                  'username': username})
    else:
        return render(request, "login.html", context=error_msg or {})


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid() and request.POST['password1'] and len(request.POST['password1']) >= 6:
            form.save()
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            # auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            username = request.POST['username'] if request.POST['username'] else ""
            password1 = request.POST['password1'] if request.POST['password1'] else ""
            password2 = request.POST['password2'] if request.POST['password2'] else ""
            name = request.POST['name'] if request.POST['name'] else ""
            email = request.POST['email'] if request.POST['email'] else ""
            error_msg = "错误"
            if not username:
                error_msg = "请输入用户名"
            elif not (password1 and password2):
                error_msg = "请输入密码"
            elif not name:
                error_msg = "请输入昵称"
            elif not email:
                error_msg = "请输入邮箱"
            elif password1 != password2:
                error_msg = "两次密码不一致"
            elif len(password1) < 6:
                error_msg = "密码长度小于6位"
            elif User.objects.filter(username=username):
                error_msg = "用户名已经存在"
                username = ""
            elif User.objects.filter(email=email):
                error_msg = "邮箱已经注册"
                email = ""
            elif User.objects.filter(name=name):
                error_msg = "名字已经被使用"
                name = ""
            return render(request, "register.html", {'error': error_msg,
                                                     'username': username,
                                                     'name': name,
                                                     'email': email})
    return render(request, "register.html")


def upload_photo(request):
    return render(request, 'forms/upload-photo.html')


@require_http_methods(["POST"])
def process_img(request):
    user = request.user
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            user.image = form.files['image']
            user.save()
            form = ImageForm(instance=user)
            return render(request, 'forms/process-photo.html', {'form': form})
        else:
            return render(request, 'forms/upload-photo.html', {'error': '请重新上传一张图像。'})


@require_http_methods(["POST"])
def upload_success(request):
    user = request.user
    if request.method == "POST":
        form = ImageForm(request.POST)
        if form.is_valid():
            form = ImageForm(request.POST, instance=user)
            form.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'forms/upload-photo.html', {'error': '发生错误，请重新上传。'})
