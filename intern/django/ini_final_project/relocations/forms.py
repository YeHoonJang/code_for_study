from django import forms
from django.contrib.auth.models import User

#회원가입
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'password': forms.PasswordInput(attrs={'class': 'forms-control'}),
        }
        labels = {
        'username': '사용자 이름',
        'email': '메일',
        'password': '비밀번호'
        }

    #글자수 제한
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['maxlength'] = 15

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
