
from django.contrib import admin
from django.urls import path, include
from B_profile import views
from django.contrib import admin


urlpatterns =[
    
    path('', views.UpdateProfile, name='UpdateProfile'),
    path('profilepic',views.profilepic, name= 'profilepic'),
    path('color1',views.color1, name= 'color1'),
    path('color2',views.color2, name= 'color2'),
    path('color3', views.color3, name='color3'),
    path('color4',views.color4, name= 'color4'),
    path('color5',views.color5, name= 'color5'),
    path('color6', views.color6, name='color6'),

]