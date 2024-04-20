from django.urls import include, re_path
from django.conf import settings
from django.views.static import serve

from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

from A_vMart import views
from B_profile.views import imageajax
# from I_settings.views import offline,offlineBack

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from D_facebook.views import facebook_info
from django.views.generic import RedirectView


urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('reset_password',auth_views.PasswordResetView.as_view(template_name="Z_forgotpassword/reset_password.html"),name='reset_password'),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name='Z_forgotpassword/password-resent-sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='Z_forgotpassword/password_reset_form.html'),name='password_reset_confirm'),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name='Z_forgotpassword/password_reset_done.html'),name='password_reset_complete'),

    path('clientReset_password',auth_views.PasswordResetView.as_view(template_name="superAdmin/forgotpassword/reset_password.html"),name='clientReset_password'),
    path('clientReset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name='superAdmin/forgotpassword/password-resent-sent.html'),name='clientReset_password_sent'),
    path('clientReset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='superAdmin/forgotpassword/password_reset_form.html'),name='clientPassword_reset_confirm'),
    path('clientReset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name='superAdmin/forgotpassword/password_reset_done.html'),name='clientPassword_reset_complete'),
    
    # path('create-user/', views.create_user, name='create-user'),
    # path('', RedirectView.as_view(url='homeStatic', permanent=False)),
    path(" ",views.homeStatic,name='homeStatic'),
    path('facebook/<int:client_id>/', facebook_info, name='facebook'),
    # path('facebook/', facebook_info, name='facebook'),
    path('facebook', include('D_facebook.urls')),
    path('donation/', include('N_donation.urls')),
    path('survey/', include('s_survey.urls')),
    path('', include('A_Appointment.urls')),
    path('B_campaign/', include('B_campaign.urls')),
    path('admin/', admin.site.urls),
    path('',include('A_webhook.urls')),
    path('',include('E_product.urls')),
    path('',include('H_hotel.urls')),
    
    path('accounts/login/', views.loginPage, name='login'),

    # path('subclient_dashboard/', views.subclient_dashboard_view, name='subclient_dashboard_view_name'),

    path('registerpage/', views.registerpage, name='registerpage'),
    # path('register/', views.registerPage, name='registerPage'),

    path('logout', views.logoutUser, name='logout'),
    path('password/', views.user_change_password.as_view(), name='user_change_password'),
    path('signupdemo',views.demo,name='demo'),

    path('appointmentPage',views.appointmrntPage,name='appointmentPage'),
    path('blogPage', views.blogPage, name='blogPage'),
    path('useCasePage', views.useCasePage, name='useCasePage'),
    path('dipstickPage',views.dipstickPage,name='dipstickPage'),
    path('campaignPage',views.campaignPage,name='campaignPage'),
    path('donationPage',views.donationPage,name='donationPage'),
    path('ticketPage',views.ticketPage,name='ticketPage'),
    path('',views.homeStatic,name='homeStatic'),
    path('healthwatt',views.healthwatt,name='healthwatt'),
    path('digitalPage',views.digitalPage,name='digitalPage'),

    path('Product-Ticket',views.productOne,name='productOne'),
    path('Product-Resto',views.productTwo,name='productTwo'),

    path('aboutUs',views.aboutUs,name='aboutUs'),
    path('salon',views.salon,name='salon'),
    path('servicesPage',views.servicesPage,name='servicesPage'),
    path('serviceNow',views.serviceNow,name='serviceNow'),
    path('hrSystem',views.hrSystem,name='hrSystem'),
    path('reachBillion',views.reachBillion,name='reachBillion'),
    path('pricingPage',views.pricingPage,name='pricingPage'),
    path('reachBillion',views.reachBillion,name='reachBillion'),
    path('donationWebPage',views.donationWebPage,name='donationWebPage'),
    path('scanToMenuWebPage',views.scanToMenuWebPage,name='scanToMenuWebPage'),
    path('ticketMenuWebPage',views.ticketMenuWebPage,name='ticketMenuWebPage'),
    path('directCommerceBlog',views.directCommerceBlog,name='directCommerceBlog'),
    path('partnerPage',views.partnerPage,name='partnerPage'),

    path('Services',views.Services,name='Services'),
    path('help',views.help,name='help'),
    path('termsConditions/',views.termsConditions,name ='termsConditions'),
    path('refundAndCancelation/',views.refundAndCancelation,name ='refundAndCancelation'),
    path('privacyPolicy/',views.privacyPolicy,name ='privacyPolicy'),
    path('eCommerceDashboard/',views.eCommerceDashboard,name='eCommerceDashboard'),
    # path('superAdmin/',views.superAdmin,name='superAdmin'),
    # path('loginSuperAdmin/', views.loginSuperAdminPage, name="loginSuperAdmin"),
    # path('sADashboard/', views.sADashboard, name="sADashboard"),
    # path('admindash/', views.admindash, name="admindash"),
    # path('facebookAdmin/', views.facebookAdmin, name="facebookAdmin"),
    # path('permissions/', views.permissions, name='permissions'),
    path('clientList/', views.clientList, name='clientList'),
    path('edit_client/<int:client_id>/', views.edit_client, name='edit_client'),
    path('update_client/<int:id>/',views.update_client,name= 'update_client'),
    path('updatepermisions/<int:client_id>/',views.updatepermisions,name='updatepermisions'),
    path('scanner/',views.scanner,name='scanner'),
    path('scannerSub/',views.scannerSub,name='scannerSub'),
    
    path('clientscanner',views.clientscanner,name='clientscanner'),
    path('helps',views.helps,name='helps'),
    # path('addfb/<int:client_id>/',views.addfb_client, name='addfb_client'),
    # path('facebook/<int:client_id>/', facebook_info, name='facebook_info'),
    # path('facebook_info/<int:id>/', views.facebook_info, name='facebook_info'),
    # path('facebook_info/<int:pk>/', views.facebook_info, name='facebook_info'),
    path('profile/', include('B_profile.urls')),
    path('avatar',imageajax, name='imageajax'),
    # path('facebook/<int:client_id>/', include('D_facebook.urls')),
    # path('facebook/', views.facebook_view, name='facebook'),
    # path('products/', include('E_product.urls')),
    path('billing/', include('C_billing.urls')),
    # path('order/', include('F_order.urls')),
    path('payments/', include('G_payment.urls')),
    path('setting/', include('I_settings.urls')),
    path('Eventmaster/', include('K_Ticket.urls')),
    path('customer/',views.customer, name='customer'),
    path('clientInfo',views.clientInfo,name='clientInfo'),
    # path('adminDash',include('adminDash.urls')),
    path('generate_bill/', views.generate_bill, name='generate_bill'),
    path('subClient/', views.subclient, name='subClient'),
    path('openSub/',views.openSub,name='openSub'),
    path('openSubClient/', views.openSubClient, name='openSubClient'),
    path('demo1/', views.demo1, name='demo1'),

    


    path('ticketdash/', views.ticketDash, name='ticketDash'),
    path('assignSubClient/<int:id>/', views.assignSubClient, name='assignSubClient'),

    # path('assignSubClient/<int:id>/',views.assignSubClient,name= 'assignSubClient'),
    path('<str:catalog>/<str:newStr>', views.clientView, name='clientView'),
    path('api/<int:pk>/', views.productApi, name='productApi'),
    path('backProduct/<str:pk>/<str:pk1>/<str:pk2>/<str:pk3>/', views.py_addtocart, name='backProduct'),
    # path('<str:client>/<str:clientId>/<str:tableId>',offline,name='offline'),
    # path('<str:client>/<str:clientId>/<str:tableId>/<str:JsId>',offlineBack,name='offlineBack'),
    path('update_ticket',views.update_ticket,name='update_ticket'),
    path('process_expiry',views.process_expiry,name='process_expiry'),
# common 
    path('UpdateProfileCommon/', views.UpdateProfileCommon, name='UpdateProfileCommon'),
    path('closeCommon/', views.closeCommon, name='closeCommon'),
    path('subClientCommon/', views.subclientCommon, name='subClientCommon'),
    path('openSubCommon/',views.openSubCommon,name='openSubCommon'),
    path('openSubClientCommon/', views.openSubClientCommon, name='openSubClientCommon'),
    path('subClientCommon/', views.subclientCommon, name='subClientCommon'), 
    path('subClientCommon/<int:id>/', views.subclientCommon, name='subClientCommon'),

    path('assignSubClientCommon/<int:id>/', views.assignSubClientCommon, name='assignSubClientCommon'),
    path('assignSubClientCommonMarketId/<int:id>/', views.assignSubClientCommonMarketId, name='assignSubClientCommonMarketId'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_header  =  "Vailo.ai Admin"  
admin.site.site_title  =  "Vailo.ai"
admin.site.index_title  =  "All User Info"


handler404="A_vMart.views.error_404"
