from django import forms
from django.contrib.auth import authenticate
from account.models import User
from django.forms import ValidationError


class SingupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('Username already exists!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('Email already exists!')
        return email

    def clean(self):
        cd = super().clean()
        pass1 = cd.get('pass1')
        pass2 = cd.get('pass2')
        if pass1 != pass2:
            raise ValidationError('Pass1 and Pass2 must not be the same ')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())

    def clean_password(self):
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if user is not None:
            return self.cleaned_data.get('password')
        raise ValidationError("username or password is not same", code="invalid_error")


class EditAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        # help texts
        self.fields[
            'username'].help_text = 'لطفا نام کاربری خود را فارسی بنویسید و از علامت ها ی@ # $@ |/ استفاده نکنید'
        # disabled form
        if not user.is_superuser:
            self.fields['email'].disabled = True
            self.fields['is_superuser'].disabled = True
            self.fields['is_author'].disabled = True
            self.fields['is_staff'].disabled = True
            self.fields['username'].disabled = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_author', 'is_staff')
