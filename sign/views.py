from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404


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
    event_list = Event.objects.all()#查询所有发布会对象
    username = request.session.get('user', '')#从浏览器读取session
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})


#发布会搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('name', "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {"user": username,
                                                 'events': event_list})


#嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contracts = paginator.page(page)
    except PageNotAnInteger:
        contracts = paginator.page(1)   #如果page不是整数，取第一页面数据
    except EmptyPage:
        contracts = paginator.page(paginator.num_pages)    #如果page不在范围，取最后一页面
    return render(request, 'guest_manage.html', {"user": username,
                                                 'guests': contracts})


#嘉宾搜索
@login_required
def search_guest_name(request):
    username = request.session.get('user', '')
    guest_realname = request.GET.get('name', "")
    guest_list = Guest.objects.filter(realname__contains=guest_realname)
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contracts = paginator.page(page)
    except PageNotAnInteger:
        contracts = paginator.page(1)   #如果page不是整数，取第一页面数据
    except EmptyPage:
        contracts = paginator.page(paginator.num_pages)    #如果page不在范围，取最后一页面
    return render(request, 'guest_manage.html', {"user": username,
                                                 'guests': contracts})


@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})


@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error.'})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event id or phone error.'})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': "user has signed in"})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'sign in success!',
                                                   'guest': result})


@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response