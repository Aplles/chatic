from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from .models import Profile


class RegistrationForm(UserCreationForm):

    username = forms.CharField(
        label='Логин',
        help_text='<span class="help-text"><br> - Должен быть уникальным</span>',
    )

    email = forms.EmailField(
        
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'placeholder': 'user@gmail.com'})
    )

    password1 = forms.CharField(
        label='Пароль',
        
        widget=forms.PasswordInput(),
        help_text='<span class="help-text"><br> - Минимальная длина пароля: 8 символов <br> - Пароль не может содержать только цифры</span>',
    )

    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(),
        help_text='<span class="help-text"></span>',
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].label = 'Логин'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100,
                                 label='Имя',
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             label='Email',
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар',widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(label='О себе',widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    hobbies = forms.CharField(label='Хобби',widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    aim = forms.CharField(label='Цели')
    city = forms.CharField(label='Город')
    age = forms.IntegerField(label='Возраст')
    class Meta:
        model = Profile
        fields = ['avatar', 'age', 'hobbies', 'aim', 'bio', 'city']

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        fields = ['avatar', 'age', 'hobbies', 'aim', 'bio', 'city']
        for i in fields:
            self.fields[i].required = False