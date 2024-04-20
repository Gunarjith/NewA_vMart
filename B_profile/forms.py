from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm,PasswordChangeForm

from collections import OrderedDict
from django.forms import ModelForm
from django import forms
# from .models import UserProfile
from django.contrib.auth.models import User



class EditProUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control focused','name':'username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control','name':'email'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control focused','name':'first_name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control','name':'last_name'})

    class Meta:
        model=User
        fields = ['username', 'email','first_name','last_name']

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': "Old Password"})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "New Password"})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "New Password"})

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


# class UserImage(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.fields['avatar'].widget.attrs.update({'class': 'form-control','name':'avatar'})
#     class Meta:
#         model = UserProfile
#         fields=['avatar']
#
#         def save(self, commit=True):
#             user = super(ModelForm, self).save(commit=False)
#             user.avatar = self.cleaned_data['avatar']
#
#             if commit:
#                 user.save()
#                 return user
