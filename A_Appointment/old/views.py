from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from vailodb_a.models import Main_settings, Consultant_settings, Availablity, Holiday_leaves, Visitor
import pytz
# Create your views here.


#configuration views

def AppointmentInfo(request):
    if request.method == 'GET':
        AppointmentDash = Main_settings.objects.filter(client_id=request.user.id)
        if len(AppointmentDash) == 0:       
            return render(request, 'A_Appointment/AppointmentInfo.html')
        else:
            return render(request, 'A_Appointment/AppointmentInfo1.html', {'AppointmentDash': AppointmentDash})

def SubmitAppointmentinfo(request):
    if request.method == "POST":
        create_info = Main_settings()

        if 'welcome_image' in request.FILES:
            create_info.welcome_image = request.FILES['welcome_image']

        create_info.welcome_message = request.POST.get('welcome_message')
        create_info.booking_button_name = request.POST.get('booking_button_name')
        create_info.my_bookings_button_name = request.POST.get('my_bookings_button_name')
        create_info.contact_us_button_name = request.POST.get('contact_us_button_name')
        create_info.client_id = request.user.id
        #to save
        create_info.save()
        return redirect('AppointmentInfo')

def editSubmitAppointmentinfo(request):
    Mainsettings = Main_settings.objects.filter(client_id=request.user.id)
    for info_appointment in  Mainsettings:
        if request.method == 'POST':
            if 'rewelcome_image' in request.FILES and len(request.FILES['rewelcome_image']) != 0:
                info_appointment.welcome_image = request.FILES['rewelcome_image']
            else:
                info_appointment.welcome_image = info_appointment.welcome_image
            info_appointment.welcome_message = request.POST.get('rewelcome_message')
            info_appointment.booking_button_name = request.POST.get('rebooking_button_name')
            info_appointment.my_bookings_button_name = request.POST.get('remy_bookings_button_name')
            info_appointment.contact_us_button_name = request.POST.get('recontact_us_button_name')
            info_appointment.client_id = request.user.id
            # to save 
            info_appointment.save()
            return redirect('AppointmentInfo')

def AppointmentConfig(request):
    return render(request, 'A_Appointment/AppointmentConfig.html')

def AppointmentMaster(request):
    Appointmentmaster = Consultant_settings.objects.filter(client_id = request.user.id)
    #print('Appointmentmaster',Appointmentmaster)
    return render(request, 'A_Appointment/AppointmentMaster.html', {'Appointmentmaster':Appointmentmaster})

def AddAppointment(request):
    return render(request, 'A_Appointment/AddAppointment.html')


def ConsultantAvailablity(request, id):
    ConsultantAvailablity = Availablity.objects.filter(client_id=request.user.id, Consultant_settings_id=id)
    return render(request, 'A_Appointment/ConsultantAvailablity.html',{'ConsultantAvailablity':ConsultantAvailablity, 'id':id}) #{'consultants': consultants, 'availability_data': availability_data}) #{'ConsultantAvailablity':ConsultantAvailablity, 'id':id})



def submitavailablity(request,id):
    #submitavailablity =  
    if request.method == 'POST':
        objects=Consultant_settings.objects.filter(client_id=request.user.id, id=id)
        consultId = 0
        for i in objects:
            consultId = i.id
        Submitavailablity = Availablity(client_id=request.user.id)
        Submitavailablity.day_of_week = request.POST.get('day_of_week')
        Submitavailablity.start_time = request.POST.get('start_time')
        Submitavailablity.end_time = request.POST.get('end_time')
        Submitavailablity.Consultant_settings_id = consultId
        Submitavailablity.client_id=request.user.id
        Submitavailablity.save()
        return redirect('ConsultantAvailablity', id)
    return render(request, 'A_Appointment/ConsultantAvailablity.html')



def consultantHolidays(request, id):
    consultantHolidays = Holiday_leaves.objects.filter(client_id = request.user.id, Consultant_settings_id=id)
    return render(request, 'A_Appointment/consultantHolidays.html',{'consultantHolidays':consultantHolidays, 'id':id})


def submitholiday(request, id):
    if request.method == 'POST':
        consultant = Consultant_settings.objects.filter(client_id= request.user.id, id=id)
        consultantId=0
        for i in consultant:
            consultantId = i.id
        Submitholiday = Holiday_leaves()
        Submitholiday.date = request.POST.get('day')
        Submitholiday.start_time = request.POST.get('start_time')
        Submitholiday.end_time = request.POST.get('end_time')
        Submitholiday.Consultant_settings_id = consultantId
        Submitholiday.client_id = request.user.id
        Submitholiday.save()
        return redirect('consultantHolidays', id)
    return render(request, 'A_Appointment/consultantHolidays.html')


def editAppointment(request, id):
    client_id = request.user.id
    modifyAppointment = Consultant_settings.objects.filter(client_id=client_id, id=id)
    return render(request,'A_Appointment/editAppointment.html', {'modifyAppointment':modifyAppointment, 'appointmentIA':id})


def deleteAppointment(request, id):
    deleteAppointment = Consultant_settings.objects.get(client_id=request.user.id, pk=id)
    deleteAppointment.delete()
    return redirect('AppointmentMaster')


def deleteholidays(request, id):
    deleteholidays = Holiday_leaves.objects.filter(client_id=request.user.id, pk=id)
    deleteholidays.delete()
    return redirect('consultantHolidays', id=id)
    

# To Add Consultant
def submitConsultantAppointment(request):
    if request.method =='POST':
        create_consultant = Consultant_settings()
        if 'consultant_photo' in request.FILES:
            create_consultant.consultant_photo = request.FILES['consultant_photo']
        if 'consultant_image' in request.FILES:
            create_consultant.consultant_image=request.FILES['consultant_image']
        create_consultant.consultant_name= request.POST.get('consultant_name')
        create_consultant.consultant_email = request.POST.get('consultant_email')
        create_consultant.consultant_phone = request.POST.get('consultant_phone')
        create_consultant.location_address = request.POST.get('location_address')
        create_consultant.location_name = request.POST.get('location_name')
        create_consultant.slot_duration = request.POST.get('slot_duration')
        create_consultant.consultant_specialization =request.POST.get('consultant_specialization')
        create_consultant.consultant_timezone = request.POST.get('timezone')
        create_consultant.client_id = request.user.id
        #save create_consultant
        create_consultant.save()
        return redirect('AppointmentMaster')
    return render(request, 'A_Appointment/AddAppointment.html' )

#update consultant appointment
def updateappointment(request, id):
    updateappointment = Consultant_settings.objects.filter(client_id=request.user.id, id=id)
    if request.method == 'POST':
        for i in updateappointment:
            updateappointment=Consultant_settings.objects.filter(client_id=request.user.id, id=id)
            if i in updateappointment:
                updateappointmentedit= Consultant_settings.objects.get(id=i.id)
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
#                updateappoinement.client_id = request.user.id
                updateappointmentedit.save()
                return redirect('AppointmentMaster')
    return render(request, 'A_Appointment/editAppointment.html')


def editavailablity(request, id):
    client_id = request.user.id
    modifyAvailablity = Availablity.objects.filter(client_id = client_id, id=id)
    return render(request, 'A_Appointment/editavailablity.html', {'modifyAvailablity':modifyAvailablity, 'availablityId':id})

def updateavailablity(request, id):
    updateavailablity  = Availablity.objects.filter(client_id=request.user.id, id=id)
    if request.method == 'POST':
        for i in updateavailablity:
            updateavailablity = Availablity.objects.filter(client_id=request.user.id, id=id)
            if i in updateavailablity:
                updateavailablityedit = Availablity.objects.get(id=i.id)
                updateavailablityedit.day_of_week=request.POST.get('reday_of_week')
                updateavailablityedit.start_time=request.POST.get('restart_time')
                updateavailablityedit.end_time=request.POST.get('reend_time')
                updateavailablityedit.save()
                return redirect('ConsultantAvailablity', id=id)
    return render(request, 'A_Appointment/editavailablity.html')


def deleteavailablity(request, id):

    deleteavailablity= Availablity.objects.filter(client_id=request.user.id, pk=id)
    
    deleteavailablity.delete()
    return redirect('ConsultantAvailablity')



#visitore 
def visitorsinfo(request):
    visitorsinfo = Visitor.objects.filter(client_id=request.user.id)
    return render(request, 'A_Appointment/visitorsinfo.html',{'visitorsinfo':visitorsinfo})


#calender
def Calender(request):

    return render(request, 'A_Appointment/Calender.html')