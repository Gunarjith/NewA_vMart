from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from vailodb_a.models import Main_settings, Consultant_settings, Availablity, Holiday_leaves, Visitor, Bookings
import pytz
import datetime

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
    deletehaliday=0
    for i in deleteholidays:
        deletehaliday = i.Consultant_settings_id
    deleteholidays.delete()
    return redirect('consultantHolidays', id=deletehaliday)
    

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
'''
def updateavailablity(request, id):
    print("bbbbbbbbbb")
    updateavailablity  = Availablity.objects.filter(client_id=request.user.id, id=id)
    consultId = 0
    for i in updateavailablity:
        consultId = i.id
    if request.method == 'POST':
        for i in updateavailablity:
            updateavailablity = Availablity.objects.filter(client_id=request.user.id, id=id)
            if i in updateavailablity:
                updateavailablityedit = Availablity.objects.get(id=i.id)
                updateavailablityedit.day_of_week=request.POST.get('reday_of_week')
                updateavailablityedit.start_time=request.POST.get('restart_time')
                updateavailablityedit.end_time=request.POST.get('reend_time')
                
                updateavailablityedit.save()
                return redirect('ConsultantAvailablity', id=consultId)
    return render(request, 'A_Appointment/editavailablity.html')
'''
from django.urls import reverse

def updateavailablity(request, id):
    updateavailablity = Availablity.objects.filter(client_id=request.user.id, id=id)
    consultId = 0
    for i in updateavailablity:
        consultId = i.id
    if request.method == 'POST':
        reday_of_week = request.POST.get('reday_of_week')
        restart_time = request.POST.get('restart_time')
        reend_time = request.POST.get('reend_time')

                # Validate and convert the time format to HH:MM
        try:
            start_time = datetime.strptime(restart_time, '%I:%M %p').strftime('%H:%M')
            end_time = datetime.strptime(reend_time, '%I:%M %p').strftime('%H:%M')
        except ValueError:
            return render(request, 'A_Appointment/editavailablity.html', {'error_message': 'Invalid time format. Please use HH:MM AM/PM format.'})


        for i in updateavailablity:
            updateavailablity = Availablity.objects.filter(client_id=request.user.id, id=id)
            if i in updateavailablity:
                updateavailablityedit = Availablity.objects.get(id=i.id)
                updateavailablityedit.day_of_week = reday_of_week
                updateavailablityedit.start_time = start_time
                updateavailablityedit.end_time = end_time
                # Update availability and save changes
                updateavailablityedit.save()
                
                # Redirect to the consultant's availability page
                return redirect(reverse('ConsultantAvailablity', id=updateavall))

    return render(request, 'A_Appointment/editavailablity.html')




def deleteavailablity(request, id):
    #deleteavailablity=Consultant_settings.objects.filter(client_id=request.user.id, pk=id)
    deleteavailable= Availablity.objects.filter(client_id=request.user.id, pk=id)
    delavall=0
    for i in deleteavailable:
        delavall = i.Consultant_settings_id
    deleteavailable.delete()
    return redirect('ConsultantAvailablity', id=delavall)
    #return render(request, 'A_Appointment/ConsultantAvailablity.html')





#visitore 
def visitorsinfo(request):
    visitorsinfo = Visitor.objects.filter(client_id=request.user.id)
    return render(request, 'A_Appointment/visitorsinfo.html',{'visitorsinfo':visitorsinfo})



from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
import pandas as pd


def Calender(request):
    consultants = Consultant_settings.objects.all()
    return render(request, 'A_Appointment/Calender.html', {'consultants': consultants})


from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
import pandas as pd

def booking_form(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        consultant_id = request.POST.get('consultant_id')
        consultant = get_object_or_404(Consultant_settings, id=consultant_id)
        consultant_name = consultant.consultant_name

        day_of_week = datetime.strptime(selected_date, '%Y-%m-%d').weekday()
        availabilities = Availablity.objects.filter(Consultant_settings=consultant, day_of_week=day_of_week)
        bookings = Bookings.objects.filter(date=selected_date, Consultant_settings=consultant)
        visitore = Visitor.objects.all()
        #visitorsinformation  = Visitor.objects.filter(date=selected_date, Consultant_settings=consultant)
        
        holiday = Holiday_leaves.objects.filter(date=selected_date, Consultant_settings=consultant)

        slot_duration_str = consultant.slot_duration.split(' ')[0]
        slot_duration_minutes = int(slot_duration_str)

        total_slots = 24 * 60 // slot_duration_minutes
        slots_df = pd.DataFrame()
        for i in range(total_slots):
            slot_start = (datetime.strptime('00:00', '%H:%M') + timedelta(minutes=i * slot_duration_minutes)).strftime('%H:%M')
            slot_end = (datetime.strptime('00:00', '%H:%M') + timedelta(minutes=(i + 1) * slot_duration_minutes)).strftime('%H:%M')
            slots_df1 = pd.DataFrame([[slot_start, slot_end, '', '', '', '','']], columns=['Start_Time', 'End_Time', 'Availability', 'online_offline', 'Booking_Notes1', 'Booking_Notes2','visitore_name'])
            slots_df = pd.concat([slots_df, slots_df1], ignore_index=True)

        if not availabilities.exists():
            slots_df['Availability'] = 'This day is Full day is Holiday'
            print('slots_df:', slots_df) 
            return render(request, 'A_Appointment/Calender.html',{'slots_df':slots_df})

        for availability in availabilities:
            consultant_start_time = availability.start_time.strftime('%H:%M')
            consultant_end_time = availability.end_time.strftime('%H:%M')
            
            total_available_slots = (datetime.strptime(consultant_end_time, '%H:%M') - datetime.strptime(consultant_start_time, '%H:%M')).seconds // 60 // slot_duration_minutes
            
            available_slots = []
            for j in range(total_available_slots):
                available_slot_start_time = (datetime.strptime(consultant_start_time, '%H:%M') + timedelta(minutes=j * slot_duration_minutes)).strftime('%H:%M')
                available_slots.append(available_slot_start_time)

            for k in range(len(available_slots)):
                slots_df.loc[slots_df.Start_Time == available_slots[k], 'Availability'] = 'Available'

        # Rest of your code for handling bookings and holidays remains the same
        #slots_df.loc[slots_df.Start_Time != available_slots[k],'Availability'] = 'NOT avalebal',
        #booked_Visitor = []

        booked_slots = []
        visitore_name=[]
        online_offline=[]
        booked_note1 = []
        booked_note2 = []
        for l in bookings:
            for visitore in bookings:
                booked_slot_start_time = l.start_time.strftime('%H:%M')
                print ('booked_slot_start_timeva:', available_slot_start_time)
                print ('l:', l)
                booked_slots.append(booked_slot_start_time)

                online_offline.append(l.online_offline)
                booked_note1.append(l.notes1)
                booked_note2.append(l.notes2)
                #visitore_name.append(l.visitore_name)
                #visitore_name.append(l.name)
                #visitore_email.append(l.email)
                #visitore_phone_num.append(l.num)



        #print ('booked slots:', booked_slots)

        for m in range(len(booked_slots)):
            slots_df.loc[slots_df.Start_Time == booked_slots[m], 'Availability'] = 'Booked',
            #slots_df.loc[slots_df.Start_Time == booked_slots[m], 'visitore_name'] = visitore_name[m],

            slots_df.loc[slots_df.Start_Time == booked_slots[m], 'online_offline'] = online_offline[m]
            slots_df.loc[slots_df.Start_Time == booked_slots[m], 'Booking_Notes1'] = booked_note1[m]
            slots_df.loc[slots_df.Start_Time == booked_slots[m], 'Booking_Notes2'] = booked_note2[m]
                

        holiday_slots=[]
        for n in holiday:
            holiday_slots_strat_time = n.start_time.strftime('%H:%M')
            print('n:',n)
            holiday_slots.append(holiday_slots_strat_time)
            #holiday_slots.append(full_holiday_slot)

        print('holiday_slot:',holiday_slots)

        for o in range(len(holiday_slots)):
            slots_df.loc[slots_df.Start_Time == holiday_slots[o], 'Availability'] = 'Not available',
        


        print('slots_df:',slots_df)

        print('slots_df:', slots_df)  
    return render(request, 'A_Appointment/Calender.html',{'slots_df':slots_df})

