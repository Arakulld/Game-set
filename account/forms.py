from django import forms
from django.core.validators import validate_email
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(required=True, label='Password')
    password_confirm = forms.CharField(required=True, label='Password confirm')
    email = forms.CharField(max_length=75, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == '':
            return self.instance.email
        validate_email(email)
        if not len(User.objects.filter(email=email)) == 0:
            raise forms.ValidationError('This mail is already exists.')
        return email

    def clean_password_confirm(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_confirm']:
            raise forms.ValidationError('Passwords don\'t match')
        return cd['password_confirm']


class EditUserForm(forms.Form):
    old_password = forms.CharField(required=True, label='Password')
    password = forms.CharField(required=False, label='New password')
    verify_password = forms.CharField(required=False, label='Verify password')
    username = forms.CharField(required=False, label='Username')
    email = forms.CharField(required=False, label='Email')

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        super(EditUserForm, self).__init__(*args, **kwargs)

    def save(self, commit=False):
        super(EditUserForm, self).save(commit=commit)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username:
            try:
                User.objects.get(username=username)
                raise (forms.ValidationError('User with this username is already exists.'))
            except User.DoesNotExist:
                return username
        return self.instance.username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            validate_email(email)
            if not len(User.objects.filter(email=email)) == 0:
                raise forms.ValidationError('This mail is already exists.')
            return email
        return self.instance.email

    def clean_old_password(self):
        user: User = self.instance
        if not user.check_password(self.cleaned_data['old_password']):
            raise forms.ValidationError('Wrong old password.')
        return self.cleaned_data['old_password']

    def clean_verify_password(self):
        password = self.cleaned_data['password']
        verify_password = self.cleaned_data['verify_password']
        if password and password != verify_password:
            raise forms.ValidationError('Passwords don\'t match')
        return verify_password


class AccountForm(forms.Form):
    phone_number = forms.CharField(max_length=16, required=False)

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        super(AccountForm, self).__init__(*args, **kwargs)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number:
            return self.instance.phone_number
        return phone_number
