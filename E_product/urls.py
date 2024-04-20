
from django.contrib import admin
from django.urls import path
from E_product import views


urlpatterns = [

   path('redirectVmart/',views.bot,name='webhook'),
    # path('',views.vmart,name='home'),
    # path('directcommerce',views.directcommerce,name='directcommerce'),
    # path('faq',views.faq,name='faq'),
    # path('redirectVailo/', views.MY_bOT, name='webhook'),
    # path('webhook/<str:pk>', views.BotView.as_view()),
    # path('payinfo',views.payinfo,name='payinfo'),
    # path('T/<str:refid>/<int:cid>/',views.T,name='T'),
    # path('N1/<str:number>/<int:dcid>/',views.N1,name='N1'),
    # path('N2/<str:number>/<int:dcid>/',views.N2,name='N2'),
    # path('checklink',views.checklink,name='checklink'),
    # path('submitdonationdata',views.submitdonationdata,name='submitdonationdata'),
    path('dataexchange/',views.dataexchange,name='dataexchange'),
    path('hotel_de/',views.hotel_de,name='hotel_de')

]
