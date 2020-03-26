from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

from .forms import UserLoginForm, ProfileForm, UserRegisterForm
from .models import Profile


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # cleaned_data 清洗出合法数据
            profile = user_login_form.cleaned_data
            # authenticate 检验账号、密码是否正确匹配数据库,匹配则返回这个user对象
            user = authenticate(username=profile['username'], password=profile['password'])
            if user:
                # 将用户数据保存在session中，即实现了登录动作
                login(request, user)
                return redirect("my_blog:article_list")
            else:
                return HttpResponse("账号或密码输入有误，请重新输入！")

        else:
            return HttpResponse("账号或密码输入不合法")

    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = dict(
            form=user_login_form,
        )
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def user_logout(request):
    logout(request)
    return redirect("my_blog:article_list")


@login_required(login_url='/user/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        # 验证登录用户与待删除用户是否相同
        if request.user == user:
            # 退出登录
            logout(request)
            user.delete()
            return redirect('my_blog:article_list')
        else:
            return HttpResponse("抱歉！您没有删除操作的权限。")
    else:
        return HttpResponse("仅接受POST请求。")


@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    if Profile.objects.filter(user_id=user.id):
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        if request.user != user:
            return HttpResponse('你没有权限修改此用户的信息。')

        profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():

            profile.phone = profile_form.cleaned_data['phone']
            profile.bio = profile_form.cleaned_data['bio']

            # 如果 request.FILES 存在文件，则保存
            if 'avatar' in request.FILES:
                profile.avatar = profile_form.cleaned_data['avatar']
            profile.save()
            # 带参数的 重定向
            return redirect("my_blog:article_list")
        else:
            return HttpResponse("注册表单输入有误，请重新输入。")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = dict(
            profile_form=profile_form,
            profile=profile,
            user=user
        )
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse('请使用GET或POST请求数据')


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password1'])
            new_user.save()
            login(request, new_user)
            return redirect("my_blog:article_list")
        else:
            return HttpResponse("注册表单有误，请重新输入！")

    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = dict(
            form=user_register_form,
        )
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


@login_required(login_url='/userprofile/login')
def edit_password(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        if not user.check_password(request.POST['password1']):
            user.set_password(request.POST['password1'])
            user.save()
            logout(request)
            return redirect("my_blog:article_list")
        else:
            return HttpResponse("密码不能与之前的相同！")

    elif request.method == 'GET':
        return render(request, 'userprofile/edit_password.html')
    else:
        return HttpResponse("请使用GET或POST请求数据")











