from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.db.models import Q
from django.forms import ModelForm




class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder': 'fbsfd', 'required': 'True', 'name': 'username', 'id': "registerName"})
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Email', 'required': 'True', 'name': 'email'})
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Password', 'required': 'True', 'name': 'password'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Re-password', 'required': 'True', 'name': 'password1',  'id': "id_password"})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

        self.fields['old_password'].widget.attrs.update(
            {'class': '', 'placeholder': "Old Password"})
        self.fields['new_password1'].widget.attrs.update(
            {'class': '', 'placeholder': "New Password"})
        self.fields['new_password2'].widget.attrs.update(
            {'class': '', 'placeholder': "New Password"})

        self.fields['old_password'].label = 'Old Password *'
        self.fields['new_password1'].label = 'New Password *'
        self.fields['new_password2'].label = 'Confirm New Password *'

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
