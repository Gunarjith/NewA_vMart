
from django.contrib import admin
from django.urls import path
from G_payment import views



urlpatterns =[
    # path('<int:linkNumber>/<int:linkAmount>/',views.customerPaymentFunction,name='payment_page'),
    # # path('payment-status',views.payment_status,name='payment_status'),
    # path('payment_order',views.payment_order,name='payment_order'),
    # path('payment_success',views.payment_success,name='payment_success'),
    # path('payment_failed',views.payment_failed,name='payment_failed'),
    path('you/',views.payment_page,name='payment_page'),
    path('payment/',views.payment_pageCommon,name='payment_pageCommon'),
    # path('payment-form',views.payment_form,name='payment_form')
    
    
]

