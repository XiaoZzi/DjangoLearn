from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    return render(request, "index.html")


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        #authenticate接收两个参数并在用户名密码匹配的情况下返回一个user对象，否则返回none
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username#将session信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')#进行路径重定向，如果验证通过就跳转到此页
            # response.set_cookie('user', username, 3600)
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error'})
            #通过render返回数据到页面


#发布会管理
@login_required#限制视图登录后才可以访问，关上窗户
def event_manage(request):
    # username = request.COOKIES.get('user', '')
    # event_list = Event.object.all()#查询所有发布会对象
    username = request.session.get('user', '')#从浏览器读取session
    return render(request, "event_manage.html", {"user": username})
