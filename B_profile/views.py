from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import secrets



import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from vailodb.models import admin_permission

from A_vMart.settings import AWS_STORAGE_BUCKET_NAME, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID
import requests


# from django.http import HttpResponse,JsonResponse
# from django.views import generic
# from django.contrib.auth.decorators import login_required
# from django.urls import reverse_lazy
# from django.forms.formsets import formset_factory
# from django.views.generic.edit import FormView
# from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
# from .forms import EditProUserForm,MyPasswordChangeForm
# from django.contrib.auth import authenticate,login,logout
#
# from django.contrib import messages
# from django.contrib.auth import update_session_auth_hash
#
# from django.views.generic import TemplateView
# from django.contrib.auth.mixins import LoginRequiredMixin


def UpdateProfile(request):
    adminPermissionObjects = admin_permission.objects.filter(client_id=request.user.id)
    if request.method=="GET":
        user_id=request.user.id
        user_object=User.objects.filter(id=user_id)
        adminPermissionObjects=admin_permission.objects.filter(client_id=request.user.id)

        return render(request, 'B_profile/profileView.html', {'us_obj': user_object,'adminP':adminPermissionObjects})
    elif request.method=="POST":
        print("hhhhhhhhhhh")
        user_id = request.user.id
        user_object = User.objects.get(id=user_id)
        user_object.username=request.POST.get('username')
        user_object.first_name = request.POST.get('first_name')
        user_object.last_name = request.POST.get('last_name')
        user_object.email = request.POST.get('email')
        user_object.save()
        user_id = request.user.id
        user_object1 = User.objects.filter(id=user_id)
        return render(request, 'B_profile/profileView.html', {'us_obj': user_object1,'adminP':adminPermissionObjects})



def generate_authkey(request):

    authKey=secrets.token_urlsafe(16)     # 'zs9XYCbTPKvux46UJckflw'
    authToken=secrets.token_hex(16)      # '6bef18936ac12a9096e9fe7a8fe1f777'
    clientId=request.user.id
    adminPermission=False


def profilepic(request):
    if request.method == 'POST':
        obj = admin_permission.objects.filter(client_id=request.user.id)
        if len(obj)==1:
            for i in obj:
                print(i.client_image)
                print(str(i.client_image))
                if str(i.client_image)=='':
                    obj2 = admin_permission.objects.get(id=i.id)
                    obj2.client_image = request.FILES['profile_pic']
                    obj2.save()

                else:
                    s3_clientMASTER = boto3.client('s3',
                                                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                                                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                                                   )
                    deleteMaster = s3_clientMASTER.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME,
                                                                 Key=str(i.client_image))
                    obj2 = admin_permission.objects.get(id=i.id)
                    obj2.client_image = request.FILES['profile_pic']
                    obj2.save()

    # obj.client_image = request.FILES['profile_pic']
        # obj.save()
    return redirect('home')


def imageajax(request):
    profilepic_object = admin_permission.objects.filter(client_id=request.user.id)
    imagepath = ''
    color1 = ''
    color2 = ''
    color3 = ''
    color4 = ''
    color5 = ''
    # color6 = ''
    for j in profilepic_object:
        if j.client_color1 == False:
            color1 = color1 + '#041E42'
        else:
            color1 = color1 + j.client_color1

        if j.client_color2 == False:
            color2 = color2 + '#041E42'
        else:
            color2 = color2 + j.client_color2

        if j.client_color3 == False:
            color3 = color3 + '#374566'
        else:
            color3 = color3 + j.client_color3

        if j.client_color4 == False:
            color4 = color4 + '#fff'
        else:
            color4 = color4 + j.client_color4

        if j.client_color5 == False:
            color5 = color5 + '#041E42'
        else:
            color5 = color5 + j.client_color5

        # if j.client_color6 == False:
        #     color6 = color6 + '#374566'
        # else:
        #     color6 = color6 + j.client_color6

    for i in profilepic_object:
        if str(i.client_image) == '':
            imagepath = imagepath + 'https://vailo.ai/static/img/testimonailBlankImg.png'
            # color1=color1+'#041E42'
            # color2 = color2 + '#041E42'
            # color3 = color3 + '#374566'
        else:
            imagepath = imagepath + 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(i.client_image)
    list1 = []

    # print(imagepath,'sssss')
    return JsonResponse({"imagepath": imagepath, 'color1': color1, 'color2': color2, 'color3': color3,'color4': color4, 'color5': color5})


def color1(request):
    obj = admin_permission.objects.filter(client_id=request.user.id)
    if request.method == 'POST' and len(obj) == 1:
        editColor1 = admin_permission.objects.get(client_id=request.user.id)
        editColor1.client_color1 = request.POST.get('text1')
        editColor1.save()
        return redirect('home')


def color2(request):
    obj = admin_permission.objects.filter(client_id=request.user.id)
    if request.method == 'POST' and len(obj) == 1:
        editColor2 = admin_permission.objects.get(client_id=request.user.id)
        editColor2.client_color2 = request.POST.get('text2')
        editColor2.save()
        return redirect('home')


def color3(request):
    obj = admin_permission.objects.filter(client_id=request.user.id)
    if request.method == 'POST' and len(obj) == 1:
        editColor3 = admin_permission.objects.get(client_id=request.user.id)
        editColor3.client_color3 = request.POST.get('text3')
        editColor3.save()
        return redirect('home')

def color4(request):
    obj = admin_permission.objects.filter(client_id=request.user.id)
    if request.method == 'POST' and len(obj) == 1:
        editColor4 = admin_permission.objects.get(client_id=request.user.id)
        editColor4.client_color4 = request.POST.get('text4')
        editColor4.save()
        return redirect('home')


def color5(request):
    obj = admin_permission.objects.filter(client_id=request.user.id)
    if request.method == 'POST' and len(obj) == 1:
        editColor5 = admin_permission.objects.get(client_id=request.user.id)
        editColor5.client_color5 = request.POST.get('text5')
        editColor5.save()
        return redirect('home')


def color6(request):
    obj = admin_permission.objects.filter(client_id=request.user.id)
    if request.method == 'POST' and len(obj) == 1:
        editColor6 = admin_permission.objects.get(client_id=request.user.id)
        editColor6.client_color6 = request.POST.get('text6')
        editColor6.save()
        return redirect('home')

