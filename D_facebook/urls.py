
from django.contrib import admin
from django.urls import path
from D_facebook import views



urlpatterns =[
    path('',views.facebook_info,name='facebook_info')

]
