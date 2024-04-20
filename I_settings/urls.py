
from django.contrib import admin
from django.urls import path
from I_settings import views



urlpatterns =[

    path('',views.settings,name='settings'),
    path('tables/',views.tables,name='tables'),
    path('linkss/',views.linkss,name='linkss'),
    # path('qrCode',views.qrCode,name='qrCode')
]
