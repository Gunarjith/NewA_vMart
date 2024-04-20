from django.contrib import admin
from django.urls import path
from N_donation import views



urlpatterns =[
    # path('<int:linkNumber>/<int:linkAmount>/',views.customerPaymentFunction,name='payment_page'),
    # # path('payment-status',views.payment_status,name='payment_status'),
    # path('payment_order',views.payment_order,name='payment_order'),
    # path('payment_success',views.payment_success,name='payment_success'),
    # path('payment_failed',views.payment_failed,name='payment_failed'),
    # path('you/',views.payment_page,name='payment_page'),
    # path('payment-form',views.payment_form,name='payment_form')
   path('subUserDonation/', views.subUserDonation, name='subUserDonation'),
   path('nDonationPayment/',views.nDonationPayment,name='nDonationPayment'),
   path('billingDonation/', views.billingDonation, name='billingDonation'),
   path('helpDonation/',views.helpDonation,name='helpDonation'),
    path('nDonationFacebook/',views.nDonationFacebook,name='nDonationFacebook'),
 path('nDonationResetPass/', views.N_DonationResetPass.as_view(), name='nDonationResetPass'),
 path('UpdateProfileDonation/', views.UpdateProfileDonation, name='UpdateProfileDonation'),
    # path('profilepic',views.profilepic, name= 'profilepic'),
    # path('subUserDonation/', views.subUserDonation, name='subUserDonation'),
path('openSubDonation/',views.openSubDonation,name='openSubDonation'),
path('formsubclient1/', views.formsubclient1, name='formsubclient1'),
  path('assignSubClientDonation/<int:id>/', views.assignSubClientDonation, name='assignSubClientDonation'),
  path('donorDetail/',views.donorDetail,name='donorDetail'),
#  path('donationInfo/', views.donationInfo, name='donationInfo'),
 path('donationInfo/<int:id>/', views.donationInfo, name='donationInfo'),
path('donationInfo1/', views.donationInfo1, name='donationInfo1'),
# path('donationInfo/<int:id>/', views.donationInfo, name='donationInfoWithID'),


 path('settingsDonation/', views.settingsDonation, name='settingsDonation'),
 path('ConfigurationDonation/', views.ConfigurationDonation, name='ConfigurationDonation'),
 path('general-donation-info/', views.generalDonationInfo, name='generalDonationInfo'),
 
 path('donationMaster/', views.donationMaster, name='donationMaster'),
  path('donationMaster/<int:marketplace_id>/', views.donationMaster, name='donationMaster'),
 path('donationMaster/<int:id>/', views.donationMaster, name='donationMaster'),
path('editSettingsDonation/', views.editSettingsDonation, name='editSettingsDonation'),
 path('editSettingsDonation/<int:id>/', views.editSettingsDonation, name='editSettingsDonation'),

    path('addDonation/<int:id>/', views.addDonation, name='addDonation'),
    path('addDonation', views.addDonation, name='addDonation'),
path('submitDonation', views.submitDonation, name='submitDonation'),
 path('editDontion/<int:id>/', views.editDontion, name='editDontion'),
    path('updateDonation/<int:id>/', views.updateDonation, name='updateDonation'),
 path('deleteDontion/<int:id>/', views.deleteDontion, name='deleteDontion'),
path('doantiondashboard/', views.doantiondashboard, name='doantiondashboard'),

path('addNgoMarketPlace/', views.addNgoMarketPlace, name='addNgoMarketPlace'),
path('addNgoForm', views.addNgoForm, name='addNgoForm'),
path('mkSetting', views.mkSetting, name='mkSetting'),
path('submitNgo', views.submitNgo, name='submitNgo'),
 path('editNgoMarketPlace/<int:id>/', views.editNgoMarketPlace, name='editNgoMarketPlace'),
    path('updateNgoMarketPlace/<int:id>/', views.updateNgoMarketPlace, name='updateNgoMarketPlace'),
 path('deleteNgoMarketPlace/<int:id>/', views.deleteNgoMarketPlace, name='deleteNgoMarketPlace'),
path('viewDetail1/<int:id>/', views.viewDetail1, name='viewDetail1'),
path('GenerateId/<int:id>/', views.GenerateId, name='GenerateId'),
path('Generatekey/<int:id>/', views.Generatekey, name='Generatekey'),
path('generateKeyBarcode/<int:id>/', views.generateKeyBarcode, name='generateKeyBarcode'),
path('GenerateIdBar/<int:id>/', views.GenerateIdBar, name='GenerateIdBar'),

path('GenerateLink/<int:id>/', views.GenerateLink, name='GenerateLink'),
path('GenerateBarLink/<int:id>/', views.GenerateBarLink, name='GenerateBarLink'),
path('genericflow',views.genericflow,name='genericflow'),
    path('specificflow',views.specificflow,name='specificflow'),
    path('mydonationflow',views.mydonationflow,name='mydonationflow'),
path('donationInfo', views.donationInfo, name='donationInfo')


]
 




