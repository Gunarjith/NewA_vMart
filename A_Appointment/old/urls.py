from django.contrib import admin
from django.urls import path
from A_Appointment import views



urlpatterns =[
    #A_appointment Configuration
    path('Appointment/AppointmentInfo', views.AppointmentInfo, name='AppointmentInfo'),

    path('AppointmentConfig', views.AppointmentConfig, name='AppointmentConfig'),

    path('Appointment/AppointmentMaster/', views.AppointmentMaster , name='AppointmentMaster'),

    path('Appointment/SubmitAppointmentinfo', views.SubmitAppointmentinfo, name='SubmitAppointmentinfo'),

    path('Appointment/editSubmitAppointmentinfo', views.editSubmitAppointmentinfo, name='editSubmitAppointmentinfo'),

    path('Appointment/AddAppointment', views.AddAppointment, name='AddAppointment'),

    path('Appointment/submitConsultantAppointment', views.submitConsultantAppointment, name='submitConsultantAppointment'),

    path('Appointment/ConsultantAvailablity/<int:id>/', views.ConsultantAvailablity, name='ConsultantAvailablity'),

    path('Appointment/consultantHolidays/<int:id>/', views.consultantHolidays, name='consultantHolidays'),

    path('Appointment/submitholiday/<int:id>/', views.submitholiday, name='submitholiday'),

    path('Appointment/submitavailablity/<int:id>/', views.submitavailablity, name='submitavailablity'),

    path('Appointment/editAppointment/<int:id>/', views.editAppointment, name='editAppointment'),

    path('Appointment/deleteAppointment/<int:id>/', views.deleteAppointment, name='deleteAppointment'),

    path('Appointment/updateappointment/<int:id>/', views.updateappointment, name='updateappointment'),

    path('Appointment/editavailablity/<int:id>/', views.editavailablity, name='editavailablity'),

    path('Appointment/updateavailablity/<int:id>/', views.updateavailablity, name='updateavailablity'),

    path('Appointment/deleteavailablity/<int:id>/', views.deleteavailablity, name='deleteavailablity'),

    path('Appointment/deleteholidays/<int:id>/', views.deleteholidays, name='deleteholidays'),
#visitors
    path('Appointment/visitorsinfo', views.visitorsinfo, name='visitorsinfo'),
    #path('Appointment/submitvisitoreinfo', views.submitvisitoreinfo, name='submitvisitoreinfo'),


#Calender
    path('Appointment/Calender', views.Calender, name='Calender'),


]