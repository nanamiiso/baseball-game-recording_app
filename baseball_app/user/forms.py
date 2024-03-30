from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm


class UserForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())
    
    class Meta():
        model = User 
        fields = ('username', 'email', 'password')


class LoginForm(forms.Form):
    username = forms.CharField(label='名前', max_length=150)
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    # パスワード確認のコードを削除しました
    def clean(self):
        cleaned_data = super().clean()
    
        return cleaned_data
        

class ChangeUsernameForm(UserChangeForm):
    password = None  # パスワードを除外
    
    class Meta:
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''

class ChangeEmailForm(UserChangeForm):
    password = None  # パスワードを除外
    
    class Meta:
        model = User
        fields = ('email',)

class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        model = User
        # PasswordChangeFormにはfields属性は通常不要ですが、カスタマイズが必要な場合はここに追加します。


