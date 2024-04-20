from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
# from vailodb_a.models import Main_settings, Consultant_settings, Availablity, Holiday_leaves, Visitor, 
from vailodb_a.models import appointment_settings, Consultant_details, Consultant_availablity, \
    Consultant_holiday_leaves, appointment_bookings, appointment_visitor, appointment_marketplace, \
    appointment_payment_gateway_details, appointment_marketplace_settings, appointment_group_type, \
    appointment_group_category
import pytz
import datetime
from vailodb.models import admin_permission, Subclient, SubUserPreference, SUBCLIENT_CHOICE, facebook_details

import json
import random

import requests
# Create your views here.


#marketplaceMain page view
def marketplacesettings(request):
    return render(request, 'A_Appointment/marketplacesettings.html')

def marketplacemain(request):
    if request.method == 'GET':
        admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
        MarketplacemainData = appointment_marketplace_settings.objects.filter(client_id=request.user.id)
        if len(MarketplacemainData) == 0:
           return render(request, 'A_Appointment/marketplacemain.html', {'admin_permission_obj':admin_permission_obj})
        else:
            return render(request, 'A_Appointment/marketplacemain1.html', {'MarketplacemainData':MarketplacemainData, 'admin_permission_obj':admin_permission_obj})


def submitmarketplacemain(request):
    if request.method =='POST':
        createdata = appointment_marketplace_settings()
        if 'appointmentmainImage' in request.FILES:
            createdata.marketplace_welcome_image = request.FILES['appointmentmainImage']
        createdata.generic_flow_id= request.POST.get('contactUsAddresName')
        createdata.specific_flow_id = request.POST.get('contactUsButtonName')
        createdata.my_appointment_flow_id = request.POST.get('myappointmentButtonName')
        createdata.marketplace_welcome_message_body = request.POST.get('appointmentwelcomemessage')
        createdata.marketplace_welcome_message_footer = request.POST.get('appointmentDescription')
        createdata.generic_flow_cta_name = request.POST.get('appointmentFooter')
        createdata.specific_flow_cta_name = request.POST.get('appintmentNowButtonName')
        createdata.myappointment_flow_cta_name = request.POST.get('appintmentsupportnumber')
        createdata.client_id = request.user.id
        createdata.save()

        return redirect('marketplacemain')

    return render(request, 'A_Appointment/marketplacemain.html')


def editmarketplacemain(request):
    Mainsettings = appointment_marketplace_settings.objects.filter(client_id=request.user.id)
    for recreatedata in  Mainsettings:
        if request.method == 'POST':
            if  'reappointmentmainImage' in request.FILES and len(request.FILES['reappointmentmainImage']) != 0:
                recreatedata.marketplace_welcome_image = request.FILES['reappointmentmainImage']
            else:
                recreatedata.marketplace_welcome_image = recreatedata.marketplace_welcome_image
            recreatedata.generic_flow_id= request.POST.get('recontactUsAddresName')
            recreatedata.specific_flow_id = request.POST.get('recontactUsButtonName')
            recreatedata.my_appointment_flow_id = request.POST.get('remyappointmentButtonName')
            recreatedata.marketplace_welcome_message_body = request.POST.get('reappointmentwelcomemessage')
            recreatedata.marketplace_welcome_message_footer = request.POST.get('reappointmentDescription')
            recreatedata.generic_flow_cta_name = request.POST.get('reappointmentFooter')
            recreatedata.specific_flow_cta_name = request.POST.get('reappintmentNowButtonName')
            recreatedata.myappointment_flow_cta_name = request.POST.get('reappintmentsupportnumber')
            recreatedata.client_id = request.user.id
            recreatedata.save()
            return redirect('marketplacemain')
    return render(request, 'A_Appointment/marketplacemain.html')


# To add a marketplace_id groups 
def addgroupname(request):
    # Clear the 'marketplace_id' key from the session
    request.session.pop('marketplace_id', None)
    request.session.save()
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    addgroupMarketPlace = appointment_marketplace.objects.filter(client=request.user.id)
    
    context = {
        'addgroupMarketPlace': addgroupMarketPlace, 
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,
        'id': id,
    }

    return render(request, 'A_Appointment/addgroupname.html', {'id':id, 'context':context, 'addgroupMarketPlace':addgroupMarketPlace, 'admin_permission_obj':admin_permission_obj})



def AddGroupsForm(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    return render(request, 'A_Appointment/AddGroupsForm.html', {'admin_permission_obj':admin_permission_obj})

def submitGroupsForm(request):
    # admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    if request.POST:
        create_group = appointment_marketplace()
        create_group.group_name = request.POST.get('groupName')
        create_group.group_type = request.POST.get('groupType')
        create_group.group_category = request.POST.get('groupCategory')
        create_group.group_location = request.POST.get('groupLocation')
        create_group.group_description = request.POST.get('groupDescription')
        create_group.group_contact_number = request.POST.get('groupContactNumber')
        create_group.client_id = request.user.id
        create_group.save()
        return redirect('addgroupname')
    return render(request, 'A_Appointment/AddGroupsForm.html')

def editgroupname(request, id):
    client_id = request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.POST.get('marketplace_id')
    print('editsurveygroup is ', marketplace_id)

    modifygroup = appointment_marketplace.objects.filter(client_id=client_id, id=id)
    return render(request, 'A_Appointment/editgroupname.html', {'modifygroup':modifygroup, 'admin_permission_obj':admin_permission_obj})


def submiteditgroupname(request, id):
    updategroupname = appointment_marketplace.objects.filter(client_id= request.user.id, id=id)
    if request.method == 'POST':
        for group in updategroupname:
            updategroupname = appointment_marketplace.objects.filter(client_id= request.user.id, id=id)
            admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
            if request.method == 'POST':
                for group in updategroupname:
                    updategroupedit = appointment_marketplace.objects.get(id=group.id)
                    updategroupedit.group_name= request.POST.get('regroupName')
                    updategroupedit.group_type = request.POST.get('regroupType')
                    updategroupedit.group_category = request.POST.get('regroupCategory')
                    updategroupedit.group_location = request.POST.get('regroupLocation')
                    updategroupedit.group_description = request.POST.get('regroupDescription')
                    updategroupedit.group_contact_number = request.POST.get('regroupContactNumber')
                    updategroupedit.save()
                return redirect('addgroupname')
            return render(request, 'A_Appointment/AddGroupsForm.html', {'updategroupname':updategroupname, 'admin_permission_obj':admin_permission_obj})

def deletegroupmane(request, id):
    deletegroup=appointment_marketplace.objects.get(client_id = request.user.id, pk=id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    deletegroup.delete()
    return redirect('addgroupname')




# #configuration views

from django.contrib import messages
from django.shortcuts import redirect

def AppointmentInfo(request, id=None):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.session.get('marketplace_id')

    if 'marketplace_id' not in request.session: 
        request.session['marketplace_id'] = id
        request.session.save()

    marketplace_id = request.session['marketplace_id']
    referer = request.META.get('HTTP_REFERER', '')

    if 'AppointmentInfo' in referer or 'addgroupname' in referer:
        request.session.save()
        # messages.success(request, 'Session cleared successfully.')

    if id:
        request.session['marketplace_id'] = id
        request.session.modified = True
        request.session.save()
    AppointmentDash = appointment_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)
    if marketplace_id:
        AppointmentDash_first = appointment_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id).first()
        if AppointmentDash_first:
            return render(request, 'A_Appointment/AppointmentInfo1.html', {'AppointmentDash': AppointmentDash_first, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id})
        else:
            return render(request, 'A_Appointment/AppointmentInfo.html', {'marketplace_id': marketplace_id, 'admin_permission_obj': admin_permission_obj})
    else:
        if AppointmentDash.exists():
            AppointmentDash_first = AppointmentDash.first()
            return render(request, 'A_Appointment/AppointmentInfo1.html', {'AppointmentDash': AppointmentDash_first, 'admin_permission_obj': admin_permission_obj})
        else:
            return render(request, 'A_Appointment/AppointmentInfo.html', {'admin_permission_obj': admin_permission_obj})



def AppointmentInfo1(request, id=None):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    AppointmentDash = appointment_settings.objects.filter(client_id=request.user.id, marketplace_id__is=True)
    marketplace_id = request.session.get('marketplace_id')
    if id:
        request.session['marketplace_id'] = id
        if marketplace_id:
            AppointmentDash = appointment_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id).first()
            print("donation_setting Id from session", AppointmentDash)
        else:
            AppointmentDash = appointment_settings.objects.filter(client_id=request.user.id, marketplace_id=id).first()
            print("donation_setting Id from id parameter", AppointmentDash)

        if AppointmentDash:
            return render(request, 'A_Appointment/AppointmentInfo1.html', {'AppointmentDash': AppointmentDash, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': id})
        else:
            return render(request, 'A_Appointment/AppointmentInfo.html', {'marketplace_id': id, 'admin_permission_obj': admin_permission_obj})
    else:
        if AppointmentDash.exists():
            AppointmentDash_first = AppointmentDash.first()
            return render(request, 'A_Appointment/AppointmentInfo1.html', {'AppointmentDash': AppointmentDash_first, 'admin_permission_obj': admin_permission_obj})
        else:
            return render(request, 'A_Appointment/AppointmentInfo1.html', {'admin_permission_obj': admin_permission_obj})

from django.shortcuts import render, redirect, reverse


def SubmitAppointmentinfo(request, id=None):
    if request.method == "POST":
        marketplace_id = request.POST.get('marketplace_id')
        create_info = appointment_settings(client_id=request.user.id, id=id)

        if 'appointmentImage' in request.FILES:
            create_info.welcome_image = request.FILES['appointmentImage']
        if 'appointmentconatctImage' in request.FILES:
            create_info.contactus_image = request.FILES['appointmentconatctImage']

        create_info.welcome_message = request.POST.get('appointmentwelcomemessage')
        create_info.booking_button_name = request.POST.get('appointmentDescription')
        create_info.my_bookings_button_name = request.POST.get('appointmentFooter')
        create_info.contact_us_button_name = request.POST.get('appintmentNowButtonName')
        create_info.main_support_number = request.POST.get('appintmentsupportnumber')
        create_info.consultant_list_message = request.POST.get('myappointmentButtonName')
        create_info.contactus_address = request.POST.get('contactUsAddresName')
        create_info.Contactus_description = request.POST.get('contactUsdescriptionName')
        create_info.consultant_list_button_name = request.POST.get('contactUsButtonName')

        create_info.client_id = request.user.id

        if marketplace_id:
            create_info.marketplace_id = marketplace_id

        create_info.save()

        if marketplace_id is not None:
            return redirect(reverse('AppointmentInfo1', kwargs={'id': create_info.id}))
        else:
            return redirect('AppointmentInfo1')



from django.urls import reverse
from django.shortcuts import get_object_or_404


def editSubmitAppointmentinfo(request, id=None):
    appointmentsettings = appointment_settings.objects.filter(client_id=request.user.id)
    marketplace_id = id
    user_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    info_appointment = get_object_or_404(appointment_settings, client_id=user_id, marketplace_id=marketplace_id)
    if request.method == 'POST':    
        marketplace_id = request.GET.get('marketplace_id')
        if 'rewelcome_image' in request.FILES and len(request.FILES['rewelcome_image']) != 0:
            info_appointment.welcome_image = request.FILES['rewelcome_image']
        else:
            info_appointment.welcome_image = info_appointment.welcome_image
        if 'recontactus_image' in request.FILES and len(request.FILES['recontactus_image']) != 0:
            info_appointment.contactus_image = request.FILES['recontactus_image']
        else:
            info_appointment.contactus_image = info_appointment.contactus_image
        info_appointment.welcome_message = request.POST.get('reappointmentwelcomemessage')
        info_appointment.booking_button_name = request.POST.get('reappointmentDescription')
        info_appointment.my_bookings_button_name = request.POST.get('reappointmentFooter')
        info_appointment.contact_us_button_name = request.POST.get('reappintmentNowButtonName')
        info_appointment.consultant_list_message = request.POST.get('remyappointmentButtonName')
        info_appointment.consultant_list_button_name = request.POST.get('recontactUsButtonName') 
        info_appointment.main_support_number = request.POST.get('reappintmentsupportnumber')
        info_appointment.contactus_address = request.POST.get('recontactUsAddresName')
        info_appointment.contactus_description = request.POST.get('recontactUsdescriptionName')

        info_appointment.client_id = request.user.id
        # to save 
        info_appointment.save()
        if marketplace_id is not None:
            return redirect(reverse('AppointmentInfo' , kwargs={'id': marketplace_id}))
        else:
            return redirect('AppointmentInfo')


def AppointmentConfig(request):
    return render(request, 'A_Appointment/AppointmentConfig.html')


def AppointmentMaster(request):
    client_id = request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=client_id).first()
    marketplace_id = request.GET.get('marketplace_id')
    if marketplace_id:
        Appointmentmaster = Consultant_details.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'A_Appointment/AppointmentMaster.html', {'Appointmentmaster': Appointmentmaster, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id})

    else:
        Appointmentmaster = Consultant_details.objects.filter(client_id=request.user.id)
    return render(request, 'A_Appointment/AppointmentMaster.html', {'Appointmentmaster': Appointmentmaster, 'admin_permission_obj': admin_permission_obj})






def AddAppointment(request):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print("AddAppointment mk id", marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=client_id).first()
    return render(request, 'A_Appointment/AddAppointment.html', {'marketplace_id': marketplace_id, 'admin_permission_obj': admin_permission_obj})


def submitConsultantAppointment(request):
    marketplace_id = request.GET.get('marketplace_id')
    print('submitconsultant_marketplace_id', marketplace_id)
    if request.method == "POST":
        submitconsultant = Consultant_details()
        if 'consultant_photo' in request.FILES:
            submitconsultant.consultant_photo = request.FILES['consultant_photo']
        if 'consultant_image' in request.FILES:
            submitconsultant.consultant_image = request.FILES['consultant_image']

        submitconsultant.consultant_name = request.POST.get('consultant_name')
        submitconsultant.consultant_email = request.POST.get('consultant_email')
        submitconsultant.consultant_phone = request.POST.get('consultant_phone')
        submitconsultant.location_address = request.POST.get('location_address')
        submitconsultant.location_name = request.POST.get('location_name')
        submitconsultant.slot_duration = request.POST.get('slot_duration')
        submitconsultant.consultant_specialization = request.POST.get('consultant_specialization')
        submitconsultant.consultant_timezone = request.POST.get('timezone')
        submitconsultant.approval_mode = request.POST.get('approval_mode')
        submitconsultant.consultant_support_number = request.POST.get('consultant_support_number')
        submitconsultant.consultant_fee = request.POST.get('consultantFee')
        submitconsultant.consultant_details = request.POST.get('consultantDeatails')
        submitconsultant.client_id = request.user.id
        if marketplace_id:
            submitconsultant.marketplace_id = marketplace_id
        submitconsultant.save()

        if marketplace_id:
            return redirect(reverse('AppointmentMaster') + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('AppointmentMaster')

    return render(request, 'A_Appointment/AppointmentMaster.html')




def editAppointment(request, id):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print('editAppointment_marketplace_id', marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifyAppointment = Consultant_details.objects.filter(client_id=client_id, id=id)
    return render(request,'A_Appointment/editAppointment.html', {'marketplace_id':marketplace_id, 'modifyAppointment':modifyAppointment, 'appointmentIA':id, 'admin_permission_obj':admin_permission_obj})


#update consultant appointment
def updateappointment(request, id):
    updateappointment = Consultant_details.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('updateappointment_marketplace_id', marketplace_id)
    if request.method == 'POST':
        for i in updateappointment:
            updateappointment=Consultant_details.objects.filter(client_id=request.user.id, id=id)
            if i in updateappointment:
                updateappointmentedit= Consultant_details.objects.get(id=i.id)
                updateappointmentedit.consultant_name = request.POST.get('reconsultant_name')
                if  'reconsultant_photo' in request.FILES and len(request.FILES['reconsultant_photo']) != 0:
                    updateappointmentedit.consultant_photo = request.FILES['reconsultant_photo']
                else:
                    updateappointmentedit.consultant_photo = i.consultant_photo
                if  'reconsultant_image'in request.FILES and len(request.FILES['reconsultant_image']) !=0:
                    updateappointmentedit.consultant_image = request.FILES['reconsultant_image']
                else:
                    updateappointmentedit.consultant_image =  i.consultant_image
                updateappointmentedit.consultant_email = request.POST.get('reconsultant_email')
                updateappointmentedit.consultant_phone = request.POST.get('reconsultant_phone')
                updateappointmentedit.location_address = request.POST.get('relocation_address')
                updateappointmentedit.location_name = request.POST.get('relocation_name')
                updateappointmentedit.slot_duration = request.POST.get('reslot_duration')
                updateappointmentedit.consultant_specialization = request.POST.get('reconsultant_specialization')
                updateappointmentedit.consultant_timezone = request.POST.get('retimezone')
                updateappointmentedit.consultant_support_number = request.POST.get('reconsultant_support_number')
                updateappointmentedit.approval_mode =request.POST.get('reapproval_mode')
                updateappointmentedit.consultant_fee = request.POST.get('reconsultantFee')
                updateappointmentedit.consultant_details = request.POST.get('reconsultantDeatails')
#                updateappoinement.client_id = request.user.id
                updateappointmentedit.save()    
                if marketplace_id:
                    return redirect(reverse('AppointmentMaster') + f'?marketplace_id={marketplace_id}')
                else:
                    return redirect('AppointmentMaster')
    return render(request, 'A_Appointment/editAppointment.html')



def deleteAppointment(request, id):
    updateappointment = Consultant_details.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('deleteAppointment_marketplace_id', marketplace_id)
    deleteAppointment = Consultant_details.objects.get(client_id=request.user.id, pk=id)
    deleteAppointment.delete()
    if marketplace_id:
        return redirect(reverse('AppointmentMaster') + f'?marketplace_id={marketplace_id}')
    else:
        return redirect('AppointmentMaster')


def ConsultantAvailablity(request, id):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print("AddAppointment mk id", marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    day_of_week_mapping = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }

    ConsultantAvailablity = Consultant_availablity.objects.filter(client_id=request.user.id, Consultant_settings_id=id)
    for avail in ConsultantAvailablity:
        avail.day_of_week = day_of_week_mapping.get(avail.day_of_week, 'Unknown Day')

    return render(request, 'A_Appointment/ConsultantAvailablity.html',{'id':id,'marketplace_id':marketplace_id, 'admin_permission_obj':admin_permission_obj,'ConsultantAvailablity':ConsultantAvailablity, 'day_of_week_mapping': day_of_week_mapping}) 



def AddAvailablity(request, id):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print("AddAppointment mk id", marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    Availablity = Consultant_availablity.objects.filter(client_id=request.user.id, Consultant_settings_id=id)
    return render(request, 'A_Appointment/AddAvailablity.html',{'marketplace_id':marketplace_id, 'Availablity':Availablity, 'admin_permission_obj':admin_permission_obj,'id':id})


def submitavailable(request,id):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    print('submitavailablitymarketplace_id',marketplace_id)
    if request.method == 'POST':
        objects=Consultant_details.objects.filter(client_id=request.user.id, id=id)
        consultId = 0
        for i in objects:
            consultId = i.id
        Submitavailablity = Consultant_availablity(client_id=request.user.id)
        Submitavailablity.day_of_week = request.POST.get('day_of_week')
        Submitavailablity.start_time = request.POST.get('start_time')
        Submitavailablity.end_time = request.POST.get('end_time')
        #if 
        Submitavailablity.Consultant_settings_id = consultId
        Submitavailablity.client_id=request.user.id
        if marketplace_id:
            Submitavailablity.marketplace_id = marketplace_id
        Submitavailablity.save()
        if marketplace_id:
            return redirect(reverse('ConsultantAvailablity', args=[id]) + f'?marketplace_id={marketplace_id}')

        else:
            return redirect('ConsultantAvailablity', id)
    return render(request, 'A_Appointment/AddAvailablity.html',{'admin_permission_obj':admin_permission_obj,'marketplace_id':marketplace_id})


def editavailablity(request, id):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print('editappointment_marketplace_id', marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifyAvailablity = Consultant_availablity.objects.filter(client_id = client_id, id=id)
    return render(request, 'A_Appointment/editavailablity.html', {'marketplace_id':marketplace_id, 'admin_permission_obj':admin_permission_obj, 'modifyAvailablity':modifyAvailablity, 'availablityId':id})


def deleteavailablity(request, id):
    updateappointment = Consultant_availablity.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('deleteavailablity_marketplace_id', marketplace_id)
    deleteAppointment = Consultant_availablity.objects.get(client_id=request.user.id, pk=id)
    deleteAppointment.delete()
    if marketplace_id:
        return redirect(reverse('ConsultantAvailablity') + f'?marketplace_id={marketplace_id}')
    else:
        return redirect('ConsultantAvailablity',id)




from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse


def updateavailablity(request, id):
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    if request.method == 'POST':
        consultant=Consultant_availablity.objects.filter(client_id=request.user.id, id=id)
        consultId = 0
        for i in consultant:
            consultId = i.Consultant_settings_id
            day_of_week = request.POST.get('reday_of_week')
            start_time = request.POST.get('restart_time')
            end_time = request.POST.get('reend_time')
            if day_of_week and start_time and end_time:
                availability = get_object_or_404(Consultant_availablity, client_id=request.user.id, id=id)
                availability.day_of_week = day_of_week
                availability.start_time = start_time
                availability.end_time = end_time
                # Save the changes
                availability.save()
                if marketplace_id:
                    return redirect(reverse('ConsultantAvailablity', args=[consultId]) + f'?marketplace_id={marketplace_id}')
                else:
                    return redirect('ConsultantAvailablity',id=consultId)
    return render(request, 'A_Appointment/editavailablity.html',{'marketplace_id':marketplace_id, 'admin_permission_obj':admin_permission_obj})


def consultantHolidays(request, id):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print("consultantholiday mk id", marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    consultantHolidays = Consultant_holiday_leaves.objects.filter(client_id = request.user.id, Consultant_settings_id=id)
    return render(request, 'A_Appointment/consultantHolidays.html',{'marketplace_id':marketplace_id,'consultantHolidays':consultantHolidays, 'id':id, 'admin_permission_obj':admin_permission_obj})


def Addholiday(request, id):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print("Addholiday mk id", marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    consultantHolidays = Consultant_holiday_leaves.objects.filter(client_id = request.user.id, Consultant_settings_id=id)
    return render(request, 'A_Appointment/Addholiday.html',{'marketplace_id':marketplace_id, 'admin_permission_obj':admin_permission_obj, 'id':id})



def submitholiday(request, id):
    marketplace_id = request.GET.get('marketplace_id')
    if request.method == 'POST':
        consultant = Consultant_details.objects.filter(client_id= request.user.id, id=id)
        consultantId=0
        for i in consultant:
            consultantId = i.id
        Submitholiday = Consultant_holiday_leaves()
        Submitholiday.date = request.POST.get('day')
        Submitholiday.start_time = request.POST.get('start_time')
        Submitholiday.end_time = request.POST.get('end_time')
        Submitholiday.Consultant_settings_id = consultantId
        Submitholiday.client_id = request.user.id
        if marketplace_id:
            Submitholiday.marketplace_id = marketplace_id
        Submitholiday.save()
        if marketplace_id:
            return redirect(reverse('consultantHolidays', args=[id]) + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('consultantHolidays', id)
    return render(request, 'A_Appointment/consultantHolidays.html')







def deleteholidays(request, id):
    updateappointment = Consultant_holiday_leaves.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('deleteavailablity_marketplace_id', marketplace_id)
    deleteAppointment = Consultant_holiday_leaves.objects.get(client_id=request.user.id, pk=id)
    deleteAppointment.delete()
    if marketplace_id:
        return redirect(reverse('consultantHolidays') + f'?marketplace_id={marketplace_id}')
    else:
        return redirect('consultantHolidays',id)







def editholiday(request, id):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print('editappointment_marketplace_id', marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifyholiday = Consultant_holiday_leaves.objects.filter(client_id = client_id, id=id)
    return render(request, 'A_Appointment/editholiday.html', {'marketplace_id':marketplace_id, 'modifyholiday':modifyholiday, 'admin_permission_obj':admin_permission_obj})


from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse

def updatetholidays(request, id):
    marketplace_id = request.GET.get('marketplace_id')
    if request.method == 'POST':
        consultant = Consultant_holiday_leaves.objects.filter(client_id=request.user.id, id=id)
        consultId = 0
        for i in consultant:
            consultId = i.Consultant_settings_id
            date = request.POST.get('redate')
            start_time = request.POST.get('restart_time')
            end_time = request.POST.get('reend_time')
            if date and start_time and end_time:
                holiday = get_object_or_404(Consultant_holiday_leaves, client_id=request.user.id, id=id)
                holiday.date = date
                holiday.start_time = start_time
                holiday.end_time = end_time
                
                holiday.save()
                if marketplace_id:
                    return redirect(reverse('consultantHolidays', args=[consultId]) + f'?marketplace_id={marketplace_id}')

                else:
                    return redirect('consultantHolidays', id=consultId)

    return HttpResponse("Invalid request method", status=400)
     

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
import pandas as pd

from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
import pandas as pd
import json

def visitorsinfo(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    client_id = request.GET.get('client_id')
    visitores = appointment_visitor.objects.filter(client_id=request.user.id)
    groupname = appointment_marketplace.objects.all()
    return render(request, 'A_Appointment/visitorsinfo.html',{'groupname':groupname,'visitores':visitores, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})

def getmarketplace(request):
    if request.method == 'POST':
        admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
        marketplace_id = request.GET.get('marketplace_id')
        print('marketplace_id', marketplace_id)
        client_id = request.GET.get('client_id')
        marketplace_id = request.POST.get('marketplacename')
        visitors = appointment_visitor.objects.filter(marketplace_id=marketplace_id)
        return render(request, 'A_Appointment/visitorsinfo.html', {'visitors': visitors, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})

    return render(request, 'A_Appointment/visitorsinfo.html', {'visitors': None, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})

# for marketplace_id 
from django.http import JsonResponse

def get_consultants(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    client_id = request.GET.get('client_id')
    selected_group = request.GET.get('group_name', None)
    print(f"Selected Group: {selected_group}")
    if selected_group is not None:
        consultants = Consultant_details.objects.filter(marketplace__group_name=selected_group)
        consultant_list = [
            {'consultant_id': consultant.id, 'consultant_name': consultant.consultant_name}
            for consultant in consultants
        ]
        print(f"Consultant List: {consultant_list}")
        return JsonResponse(consultant_list, safe=False)
    else:
        return JsonResponse([], safe=False)
    return render(request, 'A_Appointment/Calender.html',{'marketplace_id':marketplace_id, 'admin_permission_obj':admin_permission_obj})


def Calender(request):
    client_id = request.user.id
    client_id = request.GET.get('client_id')
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    group_names = appointment_marketplace.objects.values_list('group_name', flat=True).distinct()
    consultants = Consultant_details.objects.all()

    return render(request, 'A_Appointment/Calender.html', {'group_names':group_names, 'marketplace_id':marketplace_id, 'consultants': consultants, 'admin_permission_obj':admin_permission_obj})


def booking_form(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    print('bookingmarketplace_id',marketplace_id)
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        consultant_id = request.POST.get('consultant_id')
        consultantSelect = request.POST.get('consultant_id')
        consultant = get_object_or_404(Consultant_details, id=consultant_id )
        consultant_name = consultant.consultant_name

        day_of_week = datetime.strptime(selected_date, '%Y-%m-%d').weekday()
        availabilities = Consultant_availablity.objects.filter(Consultant_settings=consultant, day_of_week=day_of_week)
        
        bookings = appointment_bookings.objects.filter(date=selected_date, Consultant_settings=consultant)
        visitors = appointment_visitor.objects.all()
        
        holiday = Consultant_holiday_leaves.objects.filter(date=selected_date, Consultant_settings=consultant)

        slot_duration_str = consultant.slot_duration.split(' ')[0]
        slot_duration_minutes = int(slot_duration_str)

        total_slots = 24 * 60 // slot_duration_minutes
        slots_df = pd.DataFrame()
        for i in range(total_slots):
            slot_start = (datetime.strptime('00:00', '%H:%M') + timedelta(minutes=i * slot_duration_minutes)).strftime('%H:%M')
            slot_end = (datetime.strptime('00:00', '%H:%M') + timedelta(minutes=(i + 1) * slot_duration_minutes)).strftime('%H:%M')
            slots_df1 = pd.DataFrame([[slot_start, slot_end, '', '', '', '', '']], columns=['Start_Time', 'End_Time', 'Availability', 'online_offline', 'Booking_Notes1', 'Booking_Notes2', 'Visitor_Name'])
            slots_df = pd.concat([slots_df, slots_df1], ignore_index=True)

        if not availabilities.exists():
            slots_df['Availability'] = "This day is Full day  Holiday"
            print('slots_df:', slots_df)
            return render(request, 'A_Appointment/Calender.html', {'slots_df': slots_df, 'admin_permission_obj':admin_permission_obj})

        for availability in availabilities:
            consultant_start_time = availability.start_time.strftime('%H:%M')
            consultant_end_time = availability.end_time.strftime('%H:%M')

            total_available_slots = (datetime.strptime(consultant_end_time, '%H:%M') - datetime.strptime(consultant_start_time, '%H:%M')).seconds // 60 // slot_duration_minutes

            available_slots = [(datetime.strptime(consultant_start_time, '%H:%M') + timedelta(minutes=j * slot_duration_minutes)).strftime('%H:%M') for j in range(total_available_slots)]
            
            for available_slot_start_time in available_slots:
                slots_df.loc[slots_df.Start_Time == available_slot_start_time, 'Availability'] = 'Available'

        for booking in bookings:
            booked_slot_start_time = booking.start_time.strftime('%H:%M')
            slots_df.loc[slots_df.Start_Time == booked_slot_start_time, 'Availability'] = 'Booked'
            slots_df.loc[slots_df.Start_Time == booked_slot_start_time, 'online_offline'] = booking.online_offline
            slots_df.loc[slots_df.Start_Time == booked_slot_start_time, 'Booking_Notes1'] = booking.notes1
            slots_df.loc[slots_df.Start_Time == booked_slot_start_time, 'Booking_Notes2'] = booking.notes2

        for holidayss in holiday:
            holiday_start_time = holidayss.start_time.strftime('%H:%M')
            holiday_end_time = holidayss.end_time.strftime('%H:%M')

            total_holiday_slots = (datetime.strptime(holiday_end_time, '%H:%M') - datetime.strptime(holiday_start_time, '%H:%M')).seconds // 60 // slot_duration_minutes

            holiday_slots = [(datetime.strptime(holiday_start_time, '%H:%M') + timedelta(minutes=n * slot_duration_minutes)).strftime('%H:%M') for n in range(total_holiday_slots)]

            for holiday_slot in holiday_slots:
                slots_df.loc[slots_df.Start_Time == holiday_slot, 'Availability'] = 'Not available'

        slots_df['Visitor_Info'] = ''

        for booking in bookings:
            visitor_info = {
                'Visitor_Name': booking.visitor.Visitor_Name,
                'Visitor_email': booking.visitor.Visitor_email,
                'Visitor_Phone_Number': booking.visitor.Visitor_Phone_Number
            }
            slots_df.loc[slots_df.Start_Time == booking.start_time.strftime('%H:%M'), 'Visitor_Info'] = json.dumps(visitor_info) if visitor_info else ''

        print('slots_df:', slots_df)

    return render(request, 'A_Appointment/Calender.html', {'admin_permission_obj':admin_permission_obj, 'marketplace_id': marketplace_id, 'slots_df': slots_df})



# paymentmethods 
def Appointmentpayment(request, id):
    client_id = request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    print('marketplace_id', marketplace_id)
    payment_gatewa = appointment_payment_gateway_details.objects.filter(client_id=client_id, marketplace_id=id)
    return render(request, 'A_Appointment/Appointmentpayment.html', {'payment_gatewa':payment_gatewa, 'id':id, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})
from django.shortcuts import get_object_or_404

#submit payment based on the marketplace_id 
def appointmentpayment_page(request, id):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    payment_gatewa = appointment_payment_gateway_details.objects.filter(client_id=request.user.id, marketplace_id=id)

    if request.method == 'POST':
        marketplace, created = appointment_marketplace.objects.get_or_create(client=request.user, id=id)
        
        for gateway in payment_gatewa:
            gateway_id = request.POST.get(f'{gateway.payment_gateway}_gateway_id')
            gateway_key = request.POST.get(f'{gateway.payment_gateway}_gateway_key')
            currency = request.POST.get(f'{gateway.payment_gateway}_currency')

            gateway.gateway_id = gateway_id
            gateway.gateway_key = gateway_key
            gateway.currency = currency
            gateway.marketplace = marketplace  
            gateway.save()

        selected_methods = ['rozorpay', 'cashfree', 'paypal', 'stripe']
        existing_methods = [gateway.payment_gateway for gateway in payment_gatewa]

        new_methods = set(selected_methods) - set(existing_methods)
        for method in new_methods:
            gateway_id = request.POST.get(f'{method}_gateway_id')
            gateway_key = request.POST.get(f'{method}_gateway_key')
            currency = request.POST.get(f'{method}_currency')

            appointment_payment_gateway_details.objects.create(
                client=request.user,
                marketplace=marketplace,
                payment_gateway=method,
                gateway_id=gateway_id,
                gateway_key=gateway_key,
                currency=currency,
            )
        # return redirect('addgroupname')
        
        return redirect('Appointmentpayment', id=id, marketplace_id=marketplace.id)

    return render(request, 'A_Appointment/Appointmentpayment.html', {'payment_gatewa': payment_gatewa, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id, 'id': id})


def appointementgeneric(request):
    facebook_detailsObj = facebook_details.objects.filter(client_id=request.user.id)
    phonenumberID = 0
    facebook_token = ''
    waba_id = 0
    for f_i in facebook_detailsObj:
        phonenumberID = f_i.fb_phone_number_id
        facebook_token = f_i.fb_access_token
        waba_id = f_i.fb_Whatsapp_business_account_id
    print(phonenumberID)
    print(facebook_token)
    print("rrr")
    market_settingsObj = appointment_marketplace_settings.objects.filter(client_id=request.user.id)
    for m_i in market_settingsObj:
        random_number = random.randint(1, 1000)
        print("fffff")
        base_name = 'generic_flow'
        new_name = f'{base_name}{random_number}'
        url = f"https://graph.facebook.com/v18.0/{waba_id}/flows"

        payload = {'name': new_name,
                   'categories': '["OTHER"]'}

        headers = {
            'Authorization': f'Bearer {facebook_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        response_data = json.loads(response.text)
        id_value = response_data.get('id')
        if id_value is not None:
            print("ID:", id_value)
            print("narrri")
            donation_obj = appointment_marketplace_settings.objects.filter(client_id=request.user.id)
            for d_i in donation_obj:
                d_i.generic_flow_id = id_value
                d_i.save()
                print("successfully saved the flow id")
                type_obj = appointment_group_type.objects.filter(client_id=request.user.id)
                group_Type = []
                for r_i in type_obj:
                    group_Type.append(r_i.appointment_group_type)
                list_group_type = []
                for h_i in range(len(group_Type)):
                    list_group_type.append({"id": group_Type[h_i],
                                          "title": group_Type[h_i]
                                          })
                category_obj = appointment_group_category.objects.filter(client_id=request.user.id)
                category_Type = []
                for c_i in category_obj:
                    category_Type.append(c_i.appointment_group_category)

                list_category_type = []
                for j in range(len(category_Type)):
                    list_category_type.append({
                        "id": category_Type[j],
                        "title": category_Type[j]
                    })
                data = {
                    "version": "2.1",
                    "data_api_version":"3.0",
                    "data_channel_uri":"https://vmart.ai/appontementdata",
                    "routing_model": {
                        "DETAILS": [
                            "HOSPITAL_DATA"
                        ],
                        "HOSPITAL_DATA": [
                            "DOCTORS_DATA"
                        ],
                        "DOCTORS_DATA": [
                            "DATES_DATA"

                        ],
                        "DATES_DATA":[
                            "SLOTS_DATA"

                        ]


                    },
                    "screens": [
                        {
                            "id": "DETAILS",
                            "title": "Your details",
                            "layout": {
                                "type": "SingleColumnLayout",
                                "children": [
                                    {
                                        "type": "Form",
                                        "name": "details_form",
                                        "children": [
                                            {
                                                "type": "TextInput",
                                                "label": "Group Name",
                                                "input-type": "text",
                                                "name": "name",
                                                "required": False
                                            },
                                            {
                                                "type": "Dropdown",
                                                "label": "Group Type",
                                                "required": False,
                                                "name": "ngo_type",
                                                "data-source": list_group_type
                                            },
                                            {
                                                "type": "Dropdown",
                                                "label": "Group Category",
                                                "required": False,
                                                "name": "ngo_category",
                                                "data-source": list_category_type
                                            },
                                            {
                                                "type": "TextInput",
                                                "label": "Group Location",
                                                "input-type": "text",
                                                "name": "location",
                                                "required": False
                                            },
                                            {
                                                "type": "Footer",
                                                "label": "Continue",
                                                "on-click-action": {
                                                    "name": "data_exchange",
                                                    "payload": {
                                                        "group_Name": "${form.name}",
                                                        "group_type": "${form.ngo_type}",
                                                        "group_category": "${form.ngo_category}",
                                                        "group_location": "${form.location}"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "id": "HOSPITAL_DATA",
                            "title": "HOSPITAL_DATA",
                            "data": {
                                "options": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {
                                                "type": "string"
                                            },
                                            "title": {
                                                "type": "string"
                                            },
                                            "description": {
                                                "type": "string"
                                            }
                                        }
                                    },

                                    "__example__": [

                                    ]
                                }
                            },
                            "layout": {
                                "type": "SingleColumnLayout",
                                "children": [
                                    {
                                        "type": "Form",
                                        "name": "cover_form",
                                        "children": [
                                            {
                                                "type": "RadioButtonsGroup",
                                                "name": "options",
                                                "data-source": "${data.options}",
                                                "label": "Options",
                                                "required": True
                                            },
                                            {
                                                "type": "Footer",
                                                "label": "Continue",
                                                "on-click-action": {
                                                    "name": "data_exchange",
                                                    "payload": {
                                                        "options": "${form.options}"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "id": "DOCTORS_DATA",
                            "title": "DOCTORS_DATA",
                            "terminal": True,
                            "data": {
                                "options": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {
                                                "type": "string"
                                            },
                                            "title": {
                                                "type": "string"
                                            },
                                            "description": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "__example__": [

                                    ]
                                }
                            },

                            "layout": {
                                "type": "SingleColumnLayout",
                                "children": [
                                    {
                                        "type": "Form",
                                        "name": "cover_form",
                                        "children": [
                                            {
                                                "type": "RadioButtonsGroup",
                                                "name": "options",
                                                "data-source": "${data.options}",
                                                "label": "Options",
                                                "required": True
                                            },
                                            {
                                                "type": "Footer",
                                                "label": "Continue",
                                                "on-click-action": {
                                                    "name": "data_exchange",
                                                    "payload": {
                                                        "options": "${form.options}"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                          {
                            "id": "DATES_DATA",
                            "title": "DATES_DATA",
                            "terminal": True,
                            "data": {
                                "options": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {
                                                "type": "string"
                                            },
                                            "title": {
                                                "type": "string"
                                            }

                                        }
                                    },
                                    "__example__": [

                                    ]
                                }
                            },

                            "layout": {
                                "type": "SingleColumnLayout",
                                "children": [
                                    {
                                        "type": "Form",
                                        "name": "cover_form",
                                        "children": [
                                            {
                                                "type": "RadioButtonsGroup",
                                                "name": "options",
                                                "data-source": "${data.options}",
                                                "label": "Options",
                                                "required": True
                                            },
                                            {
                                                "type": "Footer",
                                                "label": "Continue",
                                                "on-click-action": {
                                                    "name": "data_exchange",
                                                    "payload": {
                                                        "options": "${form.options}"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                         {
                            "id": "SLOTS_DATA",
                            "title": "SLOTS_DATA",
                            "terminal": True,
                            "data": {
                                "options": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {
                                                "type": "string"
                                            },
                                            "title": {
                                                "type": "string"
                                            }

                                        }
                                    },
                                    "__example__": [

                                    ]
                                }
                            },

                            "layout": {
                                "type": "SingleColumnLayout",
                                "children": [
                                    {
                                        "type": "Form",
                                        "name": "cover_form",
                                        "children": [
                                            {
                                                "type": "RadioButtonsGroup",
                                                "name": "options",
                                                "data-source": "${data.options}",
                                                "label": "Options",
                                                "required": True
                                            },
                                            {
                                                "type": "Footer",
                                                "label": "complete",
                                                "on-click-action": {
                                                    "name": "complete",
                                                    "payload": {
                                                        "slots_data": "${form.options}"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        }

                    ]
                }
                file_name = f'{new_name}.json'
                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=2)
                print("succesfully generated the json file..")

                url = f" https://graph.facebook.com/v18.0/{id_value}/assets"

                payload = {'name': 'flow.json',
                           'asset_type': 'FLOW_JSON'}
                file_path = f'C:/Vailo/04-01-2023/A_vMart/A_vMart/{new_name}.json'
                files = [
                    ('file',
                     ('file', open(file_path, 'rb'), 'application/json'))
                ]
                headers = {
                    'Authorization': f'Bearer {facebook_token}'
                }

                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                print("king nag")

                print(response.text)
                print("s successfully updated json asset")

    return HttpResponse("Flow Id generated and Saved")


def appointementspecific(request):
    facebook_detailsObj = facebook_details.objects.filter(client_id=request.user.id)
    phonenumberID = 0
    facebook_token = ''
    waba_id = 0
    for f_i in facebook_detailsObj:
        phonenumberID = f_i.fb_phone_number_id
        facebook_token = f_i.fb_access_token
        waba_id = f_i.fb_Whatsapp_business_account_id
    print(phonenumberID)
    print(facebook_token)
    print(waba_id)
    print("rrr")
    market_settingsObj = appointment_marketplace_settings.objects.filter(client_id=request.user.id)
    for m_i in market_settingsObj:
        random_number = random.randint(1, 1000)
        print("fffff")
        base_name = 'generic_flow'
        new_name = f'{base_name}{random_number}'
        url = f"https://graph.facebook.com/v18.0/{waba_id}/flows"

        payload = {'name': new_name,
                   'categories': '["OTHER"]'}

        headers = {
            'Authorization': f'Bearer {facebook_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        response_data = json.loads(response.text)
        id_value = response_data.get('id')
        if id_value is not None:
            print("ID:", id_value)
            print("narrri")
            donation_obj = appointment_marketplace_settings.objects.filter(client_id=request.user.id)
            for d_i in donation_obj:
                d_i.specific_flow_id = id_value
                d_i.save()
                print("successfully saved the flow id")
                data = {
                  "version": "2.1",
                  "data_api_version": "3.0",
                  "data_channel_uri": "https://vmart.ai/specificapptdata",
                  "routing_model": {
                    "DOCTORS_DATA": [
                      "DATES_DATA"
                    ],
                    "DATES_DATA": [
                      "SLOTS_DATA"
                    ]
                  },
                  "screens": [

                    {
                      "id": "DOCTORS_DATA",
                      "title": "DOCTORS_DATA",
                      "terminal": True,
                      "data": {
                        "options": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "id": {
                                "type": "string"
                              },
                              "title": {
                                "type": "string"
                              },
                              "description": {
                                "type": "string"
                              }
                            }
                          },
                          "__example__": []
                        }
                      },
                      "layout": {
                        "type": "SingleColumnLayout",
                        "children": [
                          {
                            "type": "Form",
                            "name": "cover_form",
                            "children": [
                              {
                                "type": "RadioButtonsGroup",
                                "name": "options",
                                "data-source": "${data.options}",
                                "label": "Options",
                                "required": True
                              },
                              {
                                "type": "Footer",
                                "label": "Continue",
                                "on-click-action": {
                                  "name": "data_exchange",
                                  "payload": {
                                    "options": "${form.options}"
                                  }
                                }
                              }
                            ]
                          }
                        ]
                      }
                    },
                    {
                      "id": "DATES_DATA",
                      "title": "DATES_DATA",
                      "terminal": True,
                      "data": {
                        "options": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "id": {
                                "type": "string"
                              },
                              "title": {
                                "type": "string"
                              }
                            }
                          },
                          "__example__": []
                        }
                      },
                      "layout": {
                        "type": "SingleColumnLayout",
                        "children": [
                          {
                            "type": "Form",
                            "name": "cover_form",
                            "children": [
                              {
                                "type": "RadioButtonsGroup",
                                "name": "options",
                                "data-source": "${data.options}",
                                "label": "Options",
                                "required": True
                              },
                              {
                                "type": "Footer",
                                "label": "Continue",
                                "on-click-action": {
                                  "name": "data_exchange",
                                  "payload": {
                                    "options": "${form.options}"
                                  }
                                }
                              }
                            ]
                          }
                        ]
                      }
                    },
                    {
                      "id": "SLOTS_DATA",
                      "title": "SLOTS_DATA",
                      "terminal": True,
                      "data": {
                        "options": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "id": {
                                "type": "string"
                              },
                              "title": {
                                "type": "string"
                              }
                            }
                          },
                          "__example__": []
                        }
                      },
                      "layout": {
                        "type": "SingleColumnLayout",
                        "children": [
                          {
                            "type": "Form",
                            "name": "cover_form",
                            "children": [
                              {
                                "type": "RadioButtonsGroup",
                                "name": "options",
                                "data-source": "${data.options}",
                                "label": "Options",
                                "required": True
                              },
                              {
                                "type": "Footer",
                                "label": "complete",
                                "on-click-action": {
                                  "name": "complete",
                                  "payload": {
                                    "slots_data": "${form.options}"
                                  }
                                }
                              }
                            ]
                          }
                        ]
                      }
                    }
                  ]
                }
                file_name = f'{new_name}.json'
                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=2)
                print("succesfully generated the json file..")

                url = f" https://graph.facebook.com/v18.0/{id_value}/assets"

                payload = {'name': 'flow.json',
                           'asset_type': 'FLOW_JSON'}
                file_path = f'C:/Vailo/04-01-2023/A_vMart/A_vMart/{new_name}.json'
                files = [
                    ('file',
                     ('file', open(file_path, 'rb'), 'application/json'))
                ]
                headers = {
                    'Authorization': f'Bearer {facebook_token}'
                }

                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                print("king nag")

                print(response.text)
                print("s successfully updated json asset")

    return HttpResponse("Flow Id generated and Saved")


def myappointement(request):
    facebook_detailsObj = facebook_details.objects.filter(client_id=request.user.id)
    phonenumberID = 0
    facebook_token = ''
    waba_id = 0
    for f_i in facebook_detailsObj:
        phonenumberID = f_i.fb_phone_number_id
        facebook_token = f_i.fb_access_token
        waba_id = f_i.fb_Whatsapp_business_account_id
    print(phonenumberID)
    print(facebook_token)
    print(waba_id)
    print("rrr")
    market_settingsObj = appointment_marketplace_settings.objects.filter(client_id=request.user.id)
    for m_i in market_settingsObj:
        random_number = random.randint(1, 1000)
        print("fffff")
        base_name = 'generic_flow'
        new_name = f'{base_name}{random_number}'
        url = f"https://graph.facebook.com/v18.0/{waba_id}/flows"

        payload = {'name': new_name,
                   'categories': '["OTHER"]'}

        headers = {
            'Authorization': f'Bearer {facebook_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        response_data = json.loads(response.text)
        id_value = response_data.get('id')
        if id_value is not None:
            print("ID:", id_value)
            print("narrri")
            donation_obj = appointment_marketplace_settings.objects.filter(client_id=request.user.id)
            for d_i in donation_obj:
                d_i.my_appointment_flow_id = id_value
                d_i.save()
                print("successfully saved the flow id")
                data = {
                  "version": "2.1",
                  "data_api_version": "3.0",
                  "data_channel_uri": "https://vmart.ai/myappointmentdata",
                  "routing_model": {

                    "MYAPOOINTMENT_DETAILS": [

                    ]
                  },
                  "screens": [
                    {
                      "id": "MYAPOOINTMENT_DETAILS",
                      "title": "MYAPOOINTMENT_DETAILS",
                      "terminal": True,
                      "data": {
                        "details": {
                          "type": "string",
                          "__example__": ""
                        },
                        "options": {
                          "type": "array",
                          "items": {
                            "type": "object",
                            "properties": {
                              "id": {
                                "type": "string"
                              },
                              "title": {
                                "type": "string"
                              }
                            }
                          },
                          "__example__": []
                        }
                      },
                      "layout": {
                        "type": "SingleColumnLayout",
                        "children": [
                          {
                            "type": "Form",
                            "name": "cover_form",
                            "children": [
                              {
                                "type":"TextHeading",
                                "text":"${data.details}"
                              },
                              {
                                "type": "RadioButtonsGroup",
                                "name": "options",
                                "data-source": "${data.options}",
                                "label": "Options",
                                "required": True
                              },
                              {
                                "type": "Footer",
                                "label": "complete",
                                "on-click-action": {
                                  "name": "complete",
                                  "payload": {
                                    "MY_data": "${form.options}"
                                  }
                                }
                              }
                            ]
                          }
                        ]
                      }
                    }
                 ]
                }
                file_name = f'{new_name}.json'
                with open(file_name, 'w') as file:
                    json.dump(data, file, indent=2)
                print("succesfully generated the json file..")

                url = f" https://graph.facebook.com/v18.0/{id_value}/assets"

                payload = {'name': 'flow.json',
                           'asset_type': 'FLOW_JSON'}
                file_path = f'C:/Vailo/04-01-2023/A_vMart/A_vMart/{new_name}.json'
                files = [
                    ('file',
                     ('file', open(file_path, 'rb'), 'application/json'))
                ]
                headers = {
                    'Authorization': f'Bearer {facebook_token}'
                }

                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                print("king nag")

                print(response.text)
                print("s successfully updated json asset")

    return HttpResponse("Flow Id generated and Saved")
