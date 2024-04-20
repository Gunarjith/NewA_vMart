#
from django.contrib import admin
from django.urls import path,include

from C_billing import views
#
urlpatterns = [

    # path('',views.billing,name='billing'),
    path('payment',views.payment,name='payment'),
    # path('payment2', views.payment2, name='payment2'),
    # path('paymentdone',views.payment_done,name='paymentdone'),
    # path('paymenthis',views.payment_history,name='paymenthis')

]
