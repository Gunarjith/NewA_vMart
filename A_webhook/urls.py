
from django.contrib import admin
from django.urls import path
from A_webhook import views

urlpatterns = [

    path('',views.vmart,name='home'),
    path('directcommerce',views.directcommerce,name='directcommerce'),
    path('faq',views.faq,name='faq'),
    path('redirectVailo/', views.MY_bOT, name='webhook'),
    path('webhook/<str:pk>', views.BotView.as_view()),
    path('payinfo',views.payinfo,name='payinfo'),
    path('T/<str:refid>/<int:cid>/',views.T,name='T'),
    path('N1/<str:number>/<int:dcid>/',views.N1,name='N1'),
    path('N2/<str:number>/<int:dcid>/',views.N2,name='N2'),
    path('checklink',views.checklink,name='checklink'),
    path('submitdonationdata',views.submitdonationdata,name='submitdonationdata'),
    path('data',views.data,name='data'),
    path('datacheck/',views.datacheck,name='datacheck'),
    path('webhook',views.webhook,name='webhook'),
    path('checkdata/',views.checkdata,name='checkdata'),
    path('testdata',views.testdata,name='testdata'),
    path('appontementdata',views.appontementdata,name='appontementdata'),
    path('mydonationdata',views.mydonationdata,name='mydonationdata'),
    path('specificdata',views.specificdata,name='specificdata'),
    path('specificapptdata',views.specificapptdata,name='specificapptdata'),
    path('myappointmentdata',views.myappointmentdata,name='myappointmentdata'),
    path('surveydata',views.surveydata,name='surveydata'),
    path('specificsurveydata',views.specificsurveydata,name='specificsurveydata'),
    path('mysurveydata',views.mysurveydata,name='mysurveydata'),
    path('campaigndata',views.campaigndata,name='campaigndata'),
    path('mycampaigndata',views.mycampaigndata,name='mycampaigndata'),
    path('finalcheck',views.finalcheck,name='finalcheck')

]
