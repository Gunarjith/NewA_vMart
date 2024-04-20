from django.contrib import admin
from django.urls import path
from A_Appointment import views



urlpatterns =[
    path('Appointment/AppointmentInfo/', views.AppointmentInfo, name='AppointmentInfo'),
    path('Appointment/ConsultantAvailablity/<int:id>/', views.ConsultantAvailablity, name='ConsultantAvailablity'),
    path('Appointment/ConsultantAvailablity/<int:id>/', views.ConsultantAvailablity, name='ConsultantAvailablity'),
    path('Appointment/marketplacemain', views.marketplacemain, name='marketplacemain'),
    path('Appointment/marketplacesettings', views.marketplacesettings, name='marketplacesettings'),
    
    path('Appointment/submitmarketplacemain', views.submitmarketplacemain, name='submitmarketplacemain'),
    path('Appointment/editmarketplacemain', views.editmarketplacemain, name='editmarketplacemain'),

    #A_appointment Configuration
    path('Appointment/AppointmentInfo/<int:id>/', views.AppointmentInfo, name='AppointmentInfo'),
    path('Appointment/AppointmentInfo1/<int:id>/', views.AppointmentInfo1, name='AppointmentInfo1'),
    path('Appointment/addgroupname/', views.addgroupname, name='addgroupname'),
    path('Appointment/AddGroupsForm', views.AddGroupsForm, name='AddGroupsForm'),
    path('Appointment/submitGroupsForm', views.submitGroupsForm, name='submitGroupsForm'),
    path('Appointment/editgroupname/<int:id>/', views.editgroupname, name='editgroupname'),
    path('Appointment/submiteditgroupname/<int:id>/', views.submiteditgroupname, name='submiteditgroupname'),
    path('Appointment/deletegroupmane/<int:id>/', views.deletegroupmane, name='deletegroupmane'),

    path('AppointmentConfig', views.AppointmentConfig, name='AppointmentConfig'),

    path('Appointment/AppointmentMaster/', views.AppointmentMaster , name='AppointmentMaster'),
    path('Appointment/AppointmentMaster/<int:id>/', views.AppointmentMaster , name='AppointmentMaster'),

    path('Appointment/SubmitAppointmentinfo', views.SubmitAppointmentinfo, name='SubmitAppointmentinfo'),

    path('Appointment/editSubmitAppointmentinfo', views.editSubmitAppointmentinfo, name='editSubmitAppointmentinfo'),
    
    path('Appointment/AddAppointment/<int:marketplace_id>/', views.AddAppointment, name='AddAppointment'),

    path('Appointment/AddAppointment', views.AddAppointment, name='AddAppointment'),

    path('Appointment/submitConsultantAppointment', views.submitConsultantAppointment, name='submitConsultantAppointment'),


    # path('Appointment/ConsultantAvailablity/<int:id>/', views.ConsultantAvailablity, name='ConsultantAvailablity'),

   
    # path('Appointment/AddAvailablity/', views.AddAvailablity, name='AddAvailablity'),
    path('Appointment/AddAvailablity/<int:id>/', views.AddAvailablity, name='AddAvailablity'),
    
    path('Appointment/submitavailable/<int:id>/', views.submitavailable, name='submitavailable'),

    path('Appointment/consultantHolidays/<int:id>/', views.consultantHolidays, name='consultantHolidays'),


    path('Appointment/Addholiday/<int:id>/', views.Addholiday, name='Addholiday'),


    path('Appointment/submitholiday/<int:id>/', views.submitholiday, name='submitholiday'),

#     path('Appointment/submitavailablity/<int:id>/', views.submitavailablity, name='submitavailablity'),

    path('Appointment/editAppointment/<int:id>/', views.editAppointment, name='editAppointment'),

    path('Appointment/deleteAppointment/<int:id>/', views.deleteAppointment, name='deleteAppointment'),

    path('Appointment/updateappointment/<int:id>/', views.updateappointment, name='updateappointment'),

    path('Appointment/editholiday/<int:id>/', views.editholiday, name='editholiday'),

    path('Appointment/editavailablity/<int:id>/', views.editavailablity, name='editavailablity'),
 

    path('Appointment/updateavailablity/<int:id>/', views.updateavailablity, name='updateavailablity'),

    path('Appointment/deleteavailablity/<int:id>/', views.deleteavailablity, name='deleteavailablity'),

    path('Appointment/deleteholidays/<int:id>/', views.deleteholidays, name='deleteholidays'),
   
#     path('Appointment/editholiday/<int:id>/', views.editholiday, name='editholiday'),

    path('Appointment/updatetholidays/<int:id>/', views.updatetholidays, name='updatetholidays'),
# #visitors
    # path('Appointment/visitorsinfo/<int:id>/', views.visitorsinfo, name='visitorsinfo'),

    path('Appointment/visitorsinfo', views.visitorsinfo, name='visitorsinfo'),
    path('Appointment/getmarketplace', views.getmarketplace, name='getmarketplace'),

# #Calender
    path('Appointment/Calender', views.Calender, name='Calender'),
    path('Appointment/booking_form', views.booking_form, name='booking_form'),

    path('get_consultants/', views.get_consultants, name='get_consultants'),

# for payment and paymentgetway
    path('Appointment/Appointmentpayment/<int:id>/',  views.Appointmentpayment, name='Appointmentpayment'),
    path('Appointment/appointmentpayment_page/<int:id>/', views.appointmentpayment_page, name='appointmentpayment_page'),
    # path('Appointment/payment_page', views.payment_page, name='payment_page'),
    path('appointementgeneric',views.appointementgeneric,name='appointementgeneric'),
    path('appointementspecific',views.appointementspecific,name='appointementspecific'),
    path('myappointement',views.myappointement,name='myappointement')
]   