from django.shortcuts import render, redirect
from django.http import HttpResponse
from user.forms import UserForm, LoginForm
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from .forms import ChangeUsernameForm, ChangeEmailForm, ChangePasswordForm
from django.contrib import messages 
import logging



# Create your views here.
def user_list(request):
    return render(request, 'user/user_list.html')

def index(request):
    return render(request, 'user/index.html')

logger = logging.getLogger(__name__)
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            try:
                validate_password(user_form.cleaned_data.get('password', user))
            except ValidationError as e:
                user_form.add_error('password', e)
                return render(request, 'user/register.html', context={'user_form': user_form})
            user.set_password(user.password)
            user.save()  # ユーザーを保存
            messages.success(request, '登録できました')
            logger.info('Registration successful for user: %s', user_form.cleaned_data.get('username'))
            return redirect('user:login')  # ログインページにリダイレクトする
           
    else:
        user_form = UserForm()

    return render(request, 'user/register.html', context={'user_form': user_form})

def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('user:index')
                else:
                    return HttpResponse('アカウントがアクティブでないです')
            else:
                return HttpResponse('ユーザーが存在しません')
    else:
        login_form = LoginForm()  # POSTでない場合は空のフォームを渡す

    return render(request, 'user/login.html', {'login_form': login_form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('user:index')

@login_required
def settings_view(request):
    # ユーザー設定に関連する処理をここに記述
    return render(request, 'user/settings.html')  

@login_required
def change_username_view(request):
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user:settings') 
    else:
        form =  ChangeUsernameForm(instance=request.user)
    return render(request, 'user/change_username.html', {'form': form})

# メールアドレス変更のビュー
@login_required
def change_email_view(request):
    # POSTリクエストを処理するコード
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # メールアドレスを変更した後の追加の処理をここに追加
            return redirect('user:settings') # 設定ページへリダイレクト
    else:
        form = ChangeEmailForm(instance=request.user)  # GETリクエストの場合はフォームを初期化
        return render(request, 'user/change_email.html', {'form': form})  # テンプレートをレンダリング

        

# パスワード変更のビュー
@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)  # POSTリクエストではデータとユーザーを渡す
        if form.is_valid():
            form.save()
            # 必要に応じてセッションのハッシュを更新
            return redirect('user:settings')  # ここはアプリの設定画面へのリダイレクト
    else:
        form = ChangePasswordForm(user=request.user)  # GETリクエストではユーザーのみを渡す
    return render(request, 'user/change_password.html', {'form': form})


 