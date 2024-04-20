from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
import pytz
import datetime
from vailodb_h.models import Hotel_settings, Hotel_services,Food, Nearby_place, Hotel_facilities, Hotel_rooms,Selfhelp, Information, Hotel_marketplace, Hotel_marketplace_settings ,Hotel_rooms_type, Room_list, Food_Category,Food_catalogue, Food_catalogue_items, Hotel_services_settings,Food_order_header, Food_order_details, Service_order, Guest_info,Hotel_Room_Guest_info, Checkout_questions,\
Checkout_response_header, Checkout_responses, Complaint_settings, Complaint_info


from vailodb.models import admin_permission, Subclient, SubUserPreference, SUBCLIENT_CHOICE, facebook_details
import requests
import json
from django.urls import reverse
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend before importing pyplot
import base64
from io import BytesIO
from django.shortcuts import render

from django.core.files.storage import default_storage
from django.conf import settings
import matplotlib.pyplot as plt
from django.db.models import Count 
import calendar
from .utils import get_monthly_ratings,plot_monthly_ratings_base64,get_monthly_complaints, plot_monthly_complaints
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

# Create your views here.
#marketplace YES
def hotelmarketplacemain(request, delete=None):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    print("delete",delete)
    if delete == 'deleteImage':
        Hotel_marketplace_settings_obj=Hotel_marketplace_settings.objects.get(client_id=request.user.id)
        
        
        
        Hotel_marketplace_settings_obj.marketplace_welcome_image = None
        Hotel_marketplace_settings_obj.save()
    try:
        Hotel_marketplace_settings_obj=Hotel_marketplace_settings.objects.get(client_id=request.user.id)
        
    except:
        Hotel_marketplace_settings_obj=Hotel_marketplace_settings()
        Hotel_marketplace_settings_obj.client_id=request.user.id
        Hotel_marketplace_settings_obj.save()

    if request.method=='POST':
        Hotel_marketplace_settings_obj=Hotel_marketplace_settings.objects.get(client_id=request.user.id)
        if request.FILES['marketplace_welcome_image']:
            Hotel_marketplace_settings_obj.marketplace_welcome_image=request.FILES['marketplace_welcome_image']
        Hotel_marketplace_settings_obj.generic_flow_id=request.POST.get('generic_flow_id')
        Hotel_marketplace_settings_obj.specific_flow_id=request.POST.get("specific_flow_id")
        Hotel_marketplace_settings_obj.my_hotel_flow_id=request.POST.get("my_hotel_flow_id")
        Hotel_marketplace_settings_obj.marketplace_welcome_message_body=request.POST.get("marketplace_welcome_message_body")
        Hotel_marketplace_settings_obj.marketplace_welcome_message_footer=request.POST.get("marketplace_welcome_message_footer")
        Hotel_marketplace_settings_obj.generic_flow_cta_name=request.POST.get("generic_flow_cta_name")
        Hotel_marketplace_settings_obj.specific_flow_cta_name=request.POST.get("specific_flow_cta_name")
        Hotel_marketplace_settings_obj.myhotel_flow_cta_name=request.POST.get("myhotel_flow_cta_name")
        Hotel_marketplace_settings_obj.save()

    return render(request, 'H_hotel/hotelmarketplacemain.html',{'admin_permission_obj':admin_permission_obj,"Hotel_marketplace_settings_obj":Hotel_marketplace_settings_obj})


def groupnameinfo(request):
    request.session.pop('marketplace_id', None)
    request.session.save()
    subclient_id = request.session.get('subclient_id') 
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    listofhotels = Hotel_marketplace.objects.filter(client=request.user.id)
    context ={
        'listofhotels':listofhotels,
        'subclient_preferences':subclient_preferences,
        'admin_permission_obj':admin_permission_obj,
        'id':id,
    }
    return render(request, 'H_hotel/groupnameinfo.html',{'admin_permission_obj':admin_permission_obj, 'listofhotels':listofhotels, 'context':context, 'id':id})


def addhotelgroup(request):
    client_id= request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    print('addhotelgroup mk id', marketplace_id)
    return render(request, 'H_hotel/addhotelgroup.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})


def submitlisthotels(request):
    if request.method == 'POST':
        # marketplace_id = request.POST.get('marketplace_id') 
        # print('submitlisthotel, mk id', marketplace_id)
        
        createlisthotels = Hotel_marketplace()
        createlisthotels.hotel_name = request.POST.get('hotelname')
        createlisthotels.hotel_type = request.POST.get('hoteltype')
        createlisthotels.hotel_category = request.POST.get('hotelcategory')
        createlisthotels.hotel_location = request.POST.get('hotellocation')
        createlisthotels.hotel_description = request.POST.get('HotelDescription')
        createlisthotels.hotel_id = request.POST.get('hotelid')
        createlisthotels.hotel_key = request.POST.get('hotelkey')
        createlisthotels.hotel_contact_number = request.POST.get('hotelContactNumber')
        createlisthotels.client_id = request.user.id
        createlisthotels.save()
        # for i in range(7):
        service_entry = Hotel_services_settings.objects.create(
            marketplace=createlisthotels,
            client_id=request.user.id,
            name="SERVICES",
            key="SERVICES",
            description="Description for service",
            support_number=1234567890,
            escalation_number= 101,
            # escalation_hours = ,
            control="Enable",  
        )
        service_entry = Hotel_services_settings.objects.create(
            marketplace=createlisthotels,
            client_id=request.user.id,
            name="FOOD",
            key="FOOD",
            description=" Description for FOOD",
            support_number=1234567890,
            escalation_number= 102,
            # escalation_hours = ,
            control="Disable",  
    
        )
        service_entry = Hotel_services_settings.objects.create(
            marketplace=createlisthotels,
            client_id=request.user.id,
            name="NEARBY",
            key="NEARBY",
            description=" Description for NEARBY",
            support_number=1234567890,
            escalation_number= 103,
            # escalation_hours = , 
            control="Enable",  
    
        )
        service_entry = Hotel_services_settings.objects.create(
            marketplace=createlisthotels,
            client_id=request.user.id,
            name="ROOM",
            key="ROOM",
            description=" Description for ROOM",
            support_number=1234567890,
            escalation_number= 104,
            # escalation_hours = , 
            control="Enable",  
    
        )
        service_entry = Hotel_services_settings.objects.create(
            marketplace=createlisthotels,
            client_id=request.user.id,
            name="FACILITIES",
            key="FACILITIES",
            description=" Description for FACILITIES",
            support_number=1234567890,
            escalation_number= 105,
            # escalation_hours = , 
            control="Enable",  
    
        )
        service_entry = Hotel_services_settings.objects.create(
            marketplace=createlisthotels,
            client_id=request.user.id,
            name="SELP HELP",
            key="SELP HELP",
            description=" Description for SELP HELP",
            support_number=1234567890,
            escalation_number= 106,
            # escalation_hours = , 
            control="Enable",  
    
        )
        service_entry = Hotel_services_settings.objects.create(
            marketplace=createlisthotels,
            client_id=request.user.id,
            name="FEEDBACK QUESTIONS",
            key="FEEDBACK QUESTIONS",
            description=" Description for FEEDBACK QUESTIONS",
            support_number=1234567890,
            escalation_number= 107,
            # escalation_hours = , 
            control="Enable",  
    
        )
        service_entry = Hotel_services_settings.objects.create(
            marketplace=createlisthotels,
            client_id=request.user.id,
            name="INFORMATION",
            key="INFORMATION",
            description=" Description for INFORMATION",
            support_number=1234567890,
            escalation_number= 107,
            # escalation_hours = , 
            control="Enable",  
        )
        service_entry = Hotel_services_settings.objects.create(
            marketplace=createlisthotels,
            client_id=request.user.id,
            name="Complaints",
            key="COMPLAINTS",
            description=" Description for COMPLAINTS QUESTIONS",
            support_number=1234567890,
            escalation_number= 107,
            # escalation_hours = , 
            control="Enable",  
    
        )
        service_entry.save()
            
        return redirect('groupnameinfo')
    return render(request, 'H_hotel/addhotelgroup.html')



def edithotelsgroups(request, id):
    client_id=request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifyhotelsdata = Hotel_marketplace.objects.filter(client_id=request.user.id, id=id)
    return render(request, 'H_hotel/edithotelsgroups.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'modifyhotelsdata':modifyhotelsdata})


def editsubmitlisthotels(request, id):
    if request.method == 'POST':
        hotel_instance = Hotel_marketplace.objects.get(client_id=request.user.id, id=id)
        hotel_instance.hotel_name = request.POST.get('rehotelname')
        hotel_instance.hotel_type = request.POST.get('rehoteltype')
        hotel_instance.hotel_category = request.POST.get('rehotelcategory')
        hotel_instance.hotel_location = request.POST.get('rehotellocation')
        hotel_instance.hotel_description = request.POST.get('reHotelDescription')
        hotel_instance.hotel_id = request.POST.get('rehotelid')
        hotel_instance.hotel_key = request.POST.get('rehotelkey')
        hotel_instance.hotel_contact_number = request.POST.get('rehotelContactNumber')
        hotel_instance.save()
        return redirect('groupnameinfo')
    else:
        return render(request, 'H_hotel/edithotelsgroups.html')

def deletelisthotels(request,id):
    deletehoteldata = Hotel_marketplace.objects.filter(client_id=request.user.id, pk=id)
    deletehoteldata.delete()
    return redirect('groupnameinfo')


def marketplaceConfig(request):
    return render(request, 'H_hotel/marketplaceConfig.html')



# marketplace no
from django.contrib import messages
from django.shortcuts import get_object_or_404


def hotelmaininfo(request, id=None,deletefile=None):
    print("hotelmaininfo","id",id)
    # image=''
    # if id:
    #     Hotel_settings_obj=Hotel_settings.objects.get(client_id=request.user.id,marketplace_id =int(id))
    #     image_data=f'image_data_{Hotel_settings_obj.id}'
    #     if image_data in request.session:
    #         image=request.session.get(image_data)
            
    
    if  id  and deletefile == 'image':
        Hotel_settings_obj=Hotel_settings.objects.get(client_id=request.user.id,marketplace_id =int(id))
        Hotel_settings_obj.hotel_image=None
        Hotel_settings_obj.save()
    elif id and deletefile== 'video':
        Hotel_settings_obj=Hotel_settings.objects.get(client_id=request.user.id,marketplace_id =int(id))
        Hotel_settings_obj.hotel_video=None
        Hotel_settings_obj.save()
    


    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    
    marketplace_id = request.session.get('marketplace_id')
   
    if id:
        request.session['marketplace_id'] = id
    if 'marketplace_id' not in request.session: 
        request.session['marketplace_id'] = id
        request.session.save()

    marketplace_id = request.session['marketplace_id']
    print(marketplace_id,"marketplace_idin hotelmaininfo")
    referer = request.META.get('HTTP_REFERER', '')
    hotel_settings_id=request.GET.get('hotel_id')
    
    if 'hotelmaininfo' in referer or 'groupnameinfo' in referer:
        request.session.save()
        # messages.success(request, 'Session cleared successfully.')

    if id:
        request.session['marketplace_id'] = id
        # request.session.modified = True
        request.session.save()
        

    hotelDash = Hotel_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)
    # print("hotelDash",hotelDash,marketplace_id)
    modifyservice = Hotel_services_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)
    referer = request.META.get('HTTP_REFERER', '')
    # hotel_settings_id=request.GET.get('hotel_id')
    print("hotel_settings_id",hotel_settings_id)
    if 'hotelmaininfo' in referer or 'groupnameinfo' in referer:
        request.session.save()
        # messages.success(request, 'Session cleared successfully.')

    
        

    hotelDash = Hotel_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)
    print("hotelDash",hotelDash,marketplace_id)
    modifyservice = Hotel_services_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)
    

    if marketplace_id :
        print("veeresh")
        hotelDash_first = Hotel_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id).first()
        allmarketplacehotels=Hotel_settings.objects.filter(client_id=request.user.id).exclude(marketplace__isnull =True)
        print("mouli")
        if hotelDash_first:
            modifyservice = Hotel_services_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)
    
        
            return render(request, 'H_hotel/hotelmaininfo1.html', {'modifyservice': modifyservice, 'hotelDash': hotelDash_first, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id, 'subclient_preferences':subclient_preferences,"allhotels":allmarketplacehotels})
        else:

            return render(request, 'H_hotel/hotelmaininfo.html', {'modifyservice': modifyservice, 'marketplace_id': marketplace_id, 'admin_permission_obj': admin_permission_obj, 'subclient_preferences':subclient_preferences,"allhotels":allmarketplacehotels})
    else:
        if hotelDash.exists():
            hotelDash_first = hotelDash.first()
            print("pakku")
            return render(request, 'H_hotel/hotelmaininfo1.html', {'modifyservice': modifyservice, 'hotelDash': hotelDash_first, 'admin_permission_obj': admin_permission_obj, 'subclient_preferences':subclient_preferences})
        else:
            print("info.html")
            if subclient_preferences:
                if subclient_preferences.marketplace_id:
                    hotelDash_first = Hotel_settings.objects.filter(client_id=request.user.id,marketplace_id= subclient_preferences.marketplace_id).first()
                    modifyservice = Hotel_services_settings.objects.filter(client_id=request.user.id, marketplace_id=subclient_preferences.marketplace_id)
                    # print("modifyservice",modifyservice)
                    return render(request, 'H_hotel/hotelmaininfo1.html', {'modifyservice': modifyservice, 'hotelDash': hotelDash_first, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id, 'subclient_preferences':subclient_preferences})
            
            return render(request, 'H_hotel/hotelmaininfo.html', {'modifyservice': modifyservice, 'admin_permission_obj': admin_permission_obj,'subclient_preferences':subclient_preferences})


def hotelmaininfo1(request, id=None, deletefile=None):
    print("hotelmaininfo1")
    if  id  and deletefile == 'image':
        Hotel_settings_obj=Hotel_settings.objects.get(marketplace_id =id)
        Hotel_settings_obj.hotel_image=None
        Hotel_settings_obj.save()
    elif id and deletefile== 'video':
        Hotel_settings_obj=Hotel_settings.objects.get(marketplace_id =id)
        Hotel_settings_obj.hotel_video=None
        Hotel_settings_obj.save()
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    hotel_settings_id=request.GET.get('hotel_id')
    print("hotel_settings_id",hotel_settings_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    print("admin_permission_obj",admin_permission_obj)
    hotelDash = Hotel_settings.objects.filter(client_id=request.user.id, marketplace_id=True)
    marketplace_id = request.session.get('marketplace_id')
    modifyservice = Hotel_services_settings.objects.filter(client_id=request.user.id, marketplace_id=id).first()
   

    if id:
        request.session['marketplace_id'] = id
        request.session.save()
        
        if marketplace_id:
            modifyservice = Hotel_services_settings.objects.filter(client_id=request.user.id, marketplace_id=id)

            hotelDash = Hotel_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id).first()
            print("hotel_setting Id from session", hotelDash)
        else:
            hotelDash = Hotel_settings.objects.filter(client_id=request.user.id, marketplace_id=id).first()
            print("hotel_setting Id from id parameter", hotelDash)
            modifyservice = Hotel_services_settings.objects.filter(client_id=request.user.id,  marketplace_id=marketplace_id)
        if hotelDash:
            modifyservice = Hotel_services_settings.objects.filter(client_id=request.user.id,  marketplace_id=id)
            # print("modifyservice",modifyservice)
            return render(request, 'H_hotel/hotelmaininfo1.html', {'modifyservice':modifyservice,'hotelDash': hotelDash, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': id, 'subclient_preferences':subclient_preferences})
        else:
            return render(request, 'H_hotel/hotelmaininfo.html', {'marketplace_id': id, 'admin_permission_obj': admin_permission_obj, 'subclient_preferences':subclient_preferences})
    else:
        if hotelDash.exists():
            hotelDash_first = hotelDash.first()
            modifyservice = Hotel_services_settings.objects.filter(client_id=request.user.id,  marketplace_id=id).first()

            return render(request, 'H_hotel/hotelmaininfo1.html', {'modifyservice':modifyservice,'hotelDash': hotelDash_first, 'admin_permission_obj': admin_permission_obj, 'subclient_preferences':subclient_preferences})
        else:
            

            return render(request, 'H_hotel/hotelmaininfo.html', {'admin_permission_obj': admin_permission_obj, 'subclient_preferences':subclient_preferences})




def submithotelmain(request, id=None):
    # marketplace_id = request.GET.get('marketplace_id')
    # info_hotelmain = get_object_or_404(Hotel_settings, client_id=request.user.id, marketplace_id=marketplace_id)
    
    # modifyservice = Hotel_services_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)

    if request.method == 'POST':
        marketplace_id = request.POST.get('marketplace_id')
        print('hotelmain marketplaceid',marketplace_id )
        createhoteldata = Hotel_settings(client_id= request.user.id, id=id)
        createhoteldata.hotel_name = request.POST.get('name')
        createhoteldata.hotel_address = request.POST.get('address')
        createhoteldata.contact_us = request.POST.get('contactus')
        createhoteldata.contact_one = request.POST.get('contactone')
        createhoteldata.contact_two = request.POST.get('contacttwo')
        createhoteldata.contact_three = request.POST.get('contactthree')
        createhoteldata.checkIn = request.POST.get('checkIntime')
        createhoteldata.checkout = request.POST.get('checkouttime')
        if 'hotelImage' in request.FILES:
            createhoteldata.hotel_image = request.FILES['hotelImage']
        if 'hotelvideo' in request.FILES:
            createhoteldata.hotel_video = request.FILES['hotelvideo']
        createhoteldata.client_id=request.user.id


        # for data in modifyservice:
        #     service_id = data.id
        #     name = request.POST.get(f'names_{service_id}')
        #     key = request.POST.get(f'key_{service_id}')
        #     description = request.POST.get(f'discription_{service_id}')
        #     suport_number = request.POST.get(f'support_number_{service_id}')
        #     escalation_number = request.POST.get(f'Escalation_number_{service_id}')
        #     escalation_hours = request.POST.get(f'Escalation_hours_{service_id}')
        #     control = request.POST.get(f'control_{service_id}')
            
        #     service = Hotel_services_settings.objects.get(id=service_id)
        #     if name:
        #         service.name = name
        #     if key:
        #         service.key = key
        #     if description:
        #         service.description = description
        #     if suport_number:
        #         service.suport_number = suport_number
        #     if escalation_number:
        #         service.escalation_number =escalation_number
        #     if escalation_hours:
        #         service.escalation_hours =escalation_hours
        #     if control:
        #         service.control = control

        if marketplace_id:
            createhoteldata.marketplace_id = marketplace_id 

        createhoteldata.save()

        if marketplace_id is not None:
            return redirect(reverse('hotelmaininfo1', kwargs={'id': createhoteldata.id}))
        else:
            return redirect('hotelmaininfo1')


def updatemaindata(request, id=None, resize=None):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    hotelsettings = Hotel_settings.objects.filter(client_id=request.user.id)
    marketplace_id = request.GET.get('marketplace_id')
    print("marketplace_id",marketplace_id)
    info_hotelmain = get_object_or_404(Hotel_settings, client_id=request.user.id, marketplace_id=marketplace_id)
    # print("info_hotelmain",info_hotelmain)
    modifyservice = Hotel_services_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)
    if request.method == 'POST':

       
          
        
            # Handle form data
        info_hotelmain.hotel_name = request.POST.get('rename',None)
        info_hotelmain.hotel_address = request.POST.get('readdress',None)
        info_hotelmain.contact_us = request.POST.get('recontactus', None)  
        info_hotelmain.contact_one = request.POST.get('recontactone',None)
        info_hotelmain.contact_two = request.POST.get('recontacttwo',None)
        info_hotelmain.contact_three = request.POST.get('recontactthree',None)
        info_hotelmain.checkIn = request.POST.get('recheckIntime',None)
        info_hotelmain.checkout = request.POST.get('recheckouttime',None)
        if request.FILES.get('reimage') is not None :
           
           

            response = request.FILES.get('reimage')
            image_name = request.FILES.get('reimage').name

            # Open the original image
            original_image = Image.open(response)

            # Define the desired width and height
            desired_width = 600
            desired_height = 200

            # Resize the image without maintaining aspect ratio
            resized_image = original_image.resize((desired_width, desired_height), Image.ANTIALIAS)

            # Save or use resized_image as needed
            image_buffer = BytesIO()
            resized_image.save(image_buffer, format='PNG')  # Save as JPEG format

            # Create a ContentFile from the BytesIO buffer
            image_content = ContentFile(image_buffer.getvalue())


            # Assign the ContentFile to the model field, specifying the format
            info_hotelmain.hotel_image.save(image_name, image_content, save=False)


        info_hotelmain.save()
    
        for data in modifyservice:
            # print("data",data.support_number)
            service_id = data.id
            name = request.POST.get(f'names_{service_id}')
            key = request.POST.get(f'key_{service_id}')
            description = request.POST.get(f'discription_{service_id}')
            support_number = request.POST.get(f'support_number_{service_id}')
            escalation_number = request.POST.get(f'Escalation_number_{service_id}')
            escalation_hours = request.POST.get(f'Escalation_hours_{service_id}')
            control = request.POST.get(f'control_{service_id}')
            
            service = Hotel_services_settings.objects.get(id=service_id)
            if name:
                service.name = name
            if key:
                service.key = key
            if description:
                service.description = description
            if support_number:
                service.support_number = support_number
            if escalation_number:
                service.escalation_number =escalation_number
            if escalation_hours:
                service.escalation_hours =escalation_hours
            if control:
                service.control = control
            
            service.save()
    
        if marketplace_id is not None:
            print("mmmm")
            return redirect('hotelmaininfo',id=marketplace_id)
        else:
            return redirect('hotelmaininfo')
    
    return render(request, 'H_hotel/hotelmaininfo1.html', message="success")



def hotelConfig(request):
    subclient_id = request.session.get('subclient_id')
    print("subclient_id",subclient_id)  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    return render(request, 'H_hotel/hotelConfig.html',{'admin_permission_obj':admin_permission_obj, 'subclient_preferences':subclient_preferences})

def hotelservice(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    client_id = request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    if marketplace_id:
        servicedata = Hotel_services.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/hotelservice.html',{'servicedata':servicedata, 'admin_permission_obj':admin_permission_obj,'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences })
    else:
        servicedata = Hotel_services.objects.filter(client=request.user.id)
        return render(request, 'H_hotel/hotelservice.html',{'admin_permission_obj':admin_permission_obj, 'servicedata':servicedata, 'subclient_preferences':subclient_preferences})


def addservices(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id =  request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    return render(request, 'H_hotel/addservice.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})

def submitservices(request):
    marketplace_id = request.GET.get('marketplace_id')
    print('submitconsultant_marketplace_id', marketplace_id)
    if request.method =='POST':
        createservicedata = Hotel_services()
        createservicedata.service_name = request.POST.get('name')
        createservicedata.start_time = request.POST.get('starttime')
        createservicedata.end_time = request.POST.get('endtime')
        createservicedata.service_discription = request.POST.get('servicediscription')
        if 'serviceimage' in request.FILES:
            createservicedata.service_image = request.FILES['serviceimage']
        if 'servicevideo' in request.FILES:
            createservicedata.service_video = request.FILES['servicevideo']
        createservicedata.client_id = request.user.id
        if marketplace_id:
            createservicedata.marketplace_id = marketplace_id
        createservicedata.save()
        
        if marketplace_id:
            return redirect(reverse('hotelservice') + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('hotelservice')

def editservicedata(request,id,deletefile=None):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print('editservicedata_marketplace_id', marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifyservicedata = Hotel_services.objects.get(client_id=request.user.id, id=id)
    if deletefile == 'servicevideo':
        print("came to iimage delete")
        modifyservicedata.service_video=  None
        modifyservicedata.save()
    elif deletefile == 'serviceimage':
        modifyservicedata.service_image = None 
        modifyservicedata.save()
    return render(request, 'H_hotel/editservicedata.html',{'marketplace_id':marketplace_id,'admin_permission_obj':admin_permission_obj, 'modifyservicedata':modifyservicedata, 'id':id})

def updateservices(request, id):
    updateservicesdate = Hotel_services.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('updateservices_marketplace_id', marketplace_id)
    if request.method =='POST':
        for i in updateservicesdate:
            updateservicesdate = Hotel_services.objects.filter(client_id=request.user.id, id=id)
            if i in updateservicesdate:
                updateservicesedit = Hotel_services.objects.get(id=i.id)
                updateservicesedit.service_name = request.POST.get('rename')
                updateservicesedit.start_time = request.POST.get('restarttime')
                updateservicesedit.end_time = request.POST.get('reendtime')
                print("request.FILES['reserviceimage']",request.FILES['reserviceimage'])
                updateservicesedit.service_discription = request.POST.get('reservicediscription')
                if 'reserviceimage' in request.FILES and len(request.FILES['reserviceimage']) !=0:
                    print("image")
                    updateservicesedit.service_image = request.FILES['reserviceimage']
                else:
                    updateservicesedit.service_image = i.service_image
                if 'reservicevideo' in request.FILES and len(request.FILES['reservicevideo']) !=0:
                    updateservicesedit.service_video= request.FILES['rehotelservicevideo']
                updateservicesedit.save()
                if marketplace_id:
                    return redirect(reverse('hotelservice') + f'?marketplace_id={marketplace_id}')
                else:
                    return redirect('hotelservice')
    return render(request, 'H_hotel/editservicedata.html')

def deleteservicedata(request, id):
    updateservicedata = Hotel_services.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('deleteservicedata_marketplace_id', marketplace_id)
    deleteservice = Hotel_services.objects.filter(client_id=request.user.id, pk=id)
    deleteservice.delete()
    if marketplace_id:
        return redirect(reverse('hotelservice')+f'?marketplace_id={marketplace_id}')
    return redirect('hotelservice')






def foodconfig(request):
    return render(request , 'H_hotel/foodconfig.html')

def foodtypeinfo(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id=request.user.id
    admin_permission_obj=admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    if marketplace_id:
        foodtypedata = Food_Category.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request,'H_hotel/foodcategoryinfo.html',{'foodtypedata':foodtypedata, 'marketplace_id':marketplace_id, 'admin_permission_obj':admin_permission_obj, 'subclient_preferences':subclient_preferences})
    else:
        foodtypedata = Food_Category.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/foodcategoryinfo.html',{'foodtypedata':foodtypedata, 'marketplace_id':marketplace_id, "admin_permission_obj":admin_permission_obj, 'subclient_preferences':subclient_preferences})

def addcategory(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id=request.user.id
    admin_permission_obj=admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    return render(request, 'H_hotel/addcotegory.html',{'admin_permission_obj':admin_permission_obj,'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})

def submitcategory(request):
    marketplace_id=request.GET.get('marketplace_id')
    if request.method=='POST':
        createcategorydata = Food_Category()
        createcategorydata.category_name = request.POST.get('categoryname')
        createcategorydata.client_id = request.user.id
        if marketplace_id:
            createcategorydata.marketplace_id=marketplace_id
        createcategorydata.save()
        if marketplace_id:
            return redirect(reverse('foodtypeinfo') + f'?marketplace_id={marketplace_id}')
        else:    
            return  redirect('foodtypeinfo')

def deletevalue(request, id):
    deletefood = Food_Category.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('deletefooddata_marketplace_id', marketplace_id)
    deletedata = Food_Category.objects.filter(client_id=request.user.id, pk=id)
    deletedata.delete()
    if marketplace_id:
        return redirect(reverse('foodtypeinfo') + f'?marketplace_id={marketplace_id}')
    return redirect('foodtypeinfo')





def foodinfo(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id = request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    if marketplace_id:
        fooddata = Food.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/foodinfo.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id,'fooddata':fooddata, 'subclient_preferences':subclient_preferences})
    fooddata =Food.objects.filter(client_id=request.user.id)
    return render(request, 'H_hotel/foodinfo.html',{'admin_permission_obj':admin_permission_obj,'fooddata':fooddata, 'subclient_preferences':subclient_preferences})


def addfoodlist(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print("addfoodlist mk id", marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=client_id).first()
    if marketplace_id:
        foodtype = Food_Category.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/addfoodlist.html',{'admin_permission_obj':admin_permission_obj, 'foodtype':foodtype, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})
    else:
        foodtype = Food_Category.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/addfoodlist.html',{'foodtype':foodtype, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})

from django.shortcuts import get_object_or_404

def submitfoodlist(request):
    marketplace_id = request.GET.get('marketplace_id')
    print('submitfoodlist_marketplace_id', marketplace_id)
    
    if request.method == 'POST':
        createfood = Food()
        createfood.food_name = request.POST.get('name')
        createfood.food_price = request.POST.get('foodprice')
        createfood.food_type = request.POST.get('foodtype')
        createfood.food_discription = request.POST.get('fooddiscription')
        createfood.food_cuisine = request.POST.get('foodcuisine')
        
        food_category_id = int(request.POST.get('foodcategory'))
        # Get the Food_Category instance
        food_category_instance = get_object_or_404(Food_Category, pk=food_category_id)

        createfood.food_category = food_category_instance
        
        if 'foodimage' in request.FILES:
            createfood.food_image = request.FILES['foodimage']
        if 'foodvideo' in request.FILES:
            createfood.food_video = request.FILES['foodvideo']
        
        createfood.client_id = request.user.id
        if marketplace_id:
            createfood.marketplace_id = marketplace_id
        
        createfood.save()
        
        if marketplace_id:
            return redirect(reverse('foodinfo') + f'?marketplace_id={marketplace_id}')
        return redirect('foodinfo')
    
    return render(request, 'h_hotel/addfoodlist.html')





def editfoodlist(request,id,deletefile=None):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print('editfoodlist_marketplace_id', marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifyfooddata = Food.objects.get(client_id=request.user.id, id=id)
    if deletefile == 'foodvideo':
        print("came to iimage delete")
        modifyfooddata.food_video=  None
        modifyfooddata.save()
    elif deletefile == 'foodimage':
        modifyfooddata.food_image = None 
        modifyfooddata.save()
    if marketplace_id:
        food_type = Food_Category.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/editfoodlist.html',{'modifyfooddata':modifyfooddata,'food_type':food_type,'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})
    else:
        food_type = Food_Category.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/editfoodlist.html',{'modifyfooddata':modifyfooddata,'food_type':food_type,'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})

    # return render(request, 'H_hotel/editfoodlist.html',{'marketplace_id':marketplace_id,'admin_permission_obj':admin_permission_obj, 'modifyfooddata':modifyfooddata})

def submiteditfoodlist(request, id):
    updatefooddate = Food.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('submiteditfoodlist_marketplace_id', marketplace_id)
    if request.method =='POST':
        for i in updatefooddate:
            updatefooddate = Food.objects.filter(client_id=request.user.id, id=id)
            if i in updatefooddate:
                updatefooddateedit = Food.objects.get(id=i.id)
                updatefooddateedit.food_name = request.POST.get('rename')
                updatefooddateedit.food_price = request.POST.get('refoodprice')
                updatefooddateedit.food_type = request.POST.get('refoodtype')
                updatefooddateedit.food_discription = request.POST.get('refooddiscription')
                updatefooddateedit.food_cuisine =  request.POST.get('refoodcuisine')
                food_category_id = int(request.POST.get('refoodcategory'))
                 # Get the Food_Category instance
                food_category_instance = get_object_or_404(Food_Category, pk=food_category_id)

                updatefooddateedit.food_category = food_category_instance
                if 'refoodimage' in request.FILES and len(request.FILES['refoodimage']) !=0:
                    updatefooddateedit.food_image = request.FILES['refoodimage']
                else:
                    updatefooddateedit.food_image = i.food_image
                if 'refoodvideo' in request.FILES and len(request.FILES['refoodvideo']) !=0:
                    updatefooddateedit.food_video= request.FILES['refoodvideo']

                updatefooddateedit.save()
                if marketplace_id:
                    return redirect(reverse('foodinfo') + f'?marketplace_id={marketplace_id}')
                return redirect('foodinfo')
    return render(request, 'H_hotel/editfoodlist.html')

def deletefooddata(request,id):
    deletefood = Food.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('deletefooddata_marketplace_id', marketplace_id)
    deletedata = Food.objects.filter(client_id=request.user.id, pk=id)
    deletedata.delete()
    if marketplace_id:
        return redirect(reverse('foodinfo') + f'?marketplace_id={marketplace_id}')
    return redirect('foodinfo')


def catalogueinfo(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id= request.user.id
    admin_permission_obj=admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    if marketplace_id:
        cataloguedata = Food_catalogue.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request,'H_hotel/catalogueinfo.html', {'cataloguedata':cataloguedata, 'marketplace_id':marketplace_id, 'admin_permission_obj':admin_permission_obj,'subclient_preferences':subclient_preferences})
    else:
        cataloguedata = Food_catalogue.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/catalogueinfo.html', {'cataloguedata':cataloguedata, 'marketplace_id':marketplace_id, 'admin_permission_obj':admin_permission_obj, 'subclient_preferences':subclient_preferences})

def addcatalogue(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id= request.user.id
    admin_permission_obj=admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    print('addcatalogue_marketplace_id',marketplace_id)
    return render(request, 'H_hotel/addcatalogue.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})

def submitcatelogulist(request):
    marketplace_id=request.GET.get('marketplace_id')
    print('submitcataloguelist_marketplace_id', marketplace_id)
    if request.method == 'POST':
        createcataloguedata = Food_catalogue()
        createcataloguedata.catalogue_name= request.POST.get('name')
        createcataloguedata.catalogue_discription = request.POST.get('cataloguediscription')
        createcataloguedata.catalogue_set_id = request.POST.get('cataloguesetid')
        createcataloguedata.start_time = request.POST.get('starttime')
        createcataloguedata.end_time = request.POST.get('endtime')
        if 'catalogueimage' in request.FILES:
            createcataloguedata.catalogue_image = request.FILES['catalogueimage']
        createcataloguedata.client_id=request.user.id

        if marketplace_id:
            createcataloguedata.marketplace_id=marketplace_id
        createcataloguedata.save()
        if marketplace_id:
            return redirect(reverse('catalogueinfo') + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('catalogueinfo')
    return render(request, 'H_hotel/addcatalogue.html')

def editcataloguelist(request, id):
    client_id=request.user.id
    marketplace_id= request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifycatalogue = Food_catalogue.objects.filter(client_id=request.user.id, id=id)
    return render(request, 'H_hotel/editcataloguelist.html',{'modifycatalogue':modifycatalogue, 'admin_permission_obj':admin_permission_obj,'marketplace_id':marketplace_id})

def submiteditcatelogulist(request, id):
    updatecatelogulist = Food_catalogue.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('updatecatelogulist_marketplace_id', marketplace_id)
    if request.method =='POST':
        for i in updatecatelogulist:
            updatecatelogulist = Food_catalogue.objects.filter(client_id=request.user.id, id=id)
            if i in updatecatelogulist:
                updatecatelogulistedit = Food_catalogue.objects.get(id=i.id)
                updatecatelogulistedit.catalogue_name = request.POST.get('rename')
                updatecatelogulistedit.catalogue_discription = request.POST.get('recataloguediscription')
                updatecatelogulistedit.catalogue_set_id = request.POST.get('recataloguesetid')
                updatecatelogulistedit.start_time = request.POST.get('restarttime')
                updatecatelogulistedit.end_time = request.POST.get('reendtime')
                if 'reImage' in request.FILES and len(request.FILES['reImage']) !=0:
                    updatecatelogulistedit.catalogue_image = request.FILES['reImage']
                else:
                    updatecatelogulistedit.catalogue_image = i.catalogue_image
                updatecatelogulistedit.save()
                if marketplace_id:
                    return redirect(reverse('catalogueinfo') + f'?marketplace_id={marketplace_id}')
                else:
                    return redirect('catalogueinfo')
    return render(request, 'H_hotel/editcataloguelist.html')


def deletecataloguelist(request,id):
    updatecatalogue = Food_catalogue.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('Food_catalogue_marketplace_id', marketplace_id)
    deletevalue =Food_catalogue.objects.filter(client_id=request.user.id, pk=id)
    deletevalue.delete()
    if marketplace_id:
        return redirect(reverse('catalogueinfo') + f'?marketplace_id={marketplace_id}')
    else:
        return redirect('catalogueinfo')


def insertfood(request, id):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    if marketplace_id:
        cataloguedata = Food.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        associated_foods = Food_catalogue_items.objects.filter(Food_catalogue_id=id, client_id=client_id, marketplace_id=marketplace_id).values_list('Food_Item__food_name', flat=True)
        catalogueitemsdata=Food_catalogue_items.objects.filter(Food_catalogue_id=id, client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/insertfood.html', {'catalogueitemsdata':catalogueitemsdata, 'cataloguedata': cataloguedata, 'associated_foods': associated_foods, 'marketplace_id': marketplace_id, 'admin_permission_obj': admin_permission_obj, 'id': id, 'subclient_preferences':subclient_preferences})
    else:

        cataloguedata = Food.objects.filter(client_id=client_id)
        associated_foods = Food_catalogue_items.objects.filter(Food_catalogue_id=id, client_id=client_id).values_list('Food_Item__food_name', flat=True)
        catalogueitemsdata=Food_catalogue_items.objects.filter(Food_catalogue_id=id, client_id=request.user.id)
        return render(request, 'H_hotel/insertfood.html', {'catalogueitemsdata':catalogueitemsdata, 'cataloguedata': cataloguedata, 'associated_foods': associated_foods, 'marketplace_id': marketplace_id, 'admin_permission_obj': admin_permission_obj, 'id': id, 'subclient_preferences':subclient_preferences})


def submitselectedfoods(request, id):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    print('submitselectedfoods mk id', marketplace_id)
    
    if request.method == 'POST':
        selected_food_names = request.POST.getlist('selected_foods')
        objects = Food_catalogue.objects.filter(client_id=request.user.id, id=id)
        catalogue = 0
        for i in objects:
            caltalogueid = i.id
        
        for selected_food_name in selected_food_names:
            try:
                selected_foods = Food.objects.filter(food_name=selected_food_name)
                for selected_food in selected_foods:
                    submitfood = Food_catalogue_items(client_id=request.user.id)
                    submitfood.Food_Item = selected_food
                    submitfood.Food_catalogue_id = caltalogueid
                    submitfood.client_id = request.user.id
                    if marketplace_id:
                        submitfood.marketplace_id = marketplace_id
                    submitfood.save()
            except Food.DoesNotExist:
                pass  
        if marketplace_id:
            return redirect(reverse('insertfood', args=[id]) + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('insertfood', id)
    
    return render(request, 'H_hotel/insertfood.html')


def deletefooditem(request, id):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    deletefooditems = Food_catalogue_items.objects.filter(client_id=request.user.id, pk=id)
    deletevall =0
    for i in deletefooditems:
        deletevall = i.Food_catalogue_id
    deletefooditems.delete()
    if marketplace_id:
        return redirect(reverse('insertfood', args=[deletevall]) + f'?marketplace_id={marketplace_id}')
    else:
        return redirect('insertfood', id=deletevall)



def catalogueitemsinfo(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id= request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    if marketplace_id:
        catalogueitemsdata=Food_catalogue_items.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/catalogueitemsinfo.html',{'catalogueitemsdata':catalogueitemsdata,'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})
    else:
        catalogueitemsdata=Food_catalogue_items.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/catalogueitemsinfo.html',{'catalogueitemsdata':catalogueitemsdata,'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})


def addcatalogueitems(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id=request.user.id
    marketplace_id=request.GET.get('marketplace_id')
    admin_permission_obj=admin_permission.objects.filter(client_id=request.user.id).first()
    if marketplace_id:
        cataloguedata1 = Food_catalogue.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        cataloguedata= Food.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/addcatalogueitems.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'cataloguedata':cataloguedata, 'cataloguedata1':cataloguedata1, 'subclient_preferences':subclient_preferences})
    else:
        cataloguedata= Food.objects.filter(client_id=request.user.id)
        cataloguedata1 = Food_catalogue.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/addcatalogueitems.html',{'cataloguedata':cataloguedata, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'cataloguedata1':cataloguedata1,'subclient_preferences':subclient_preferences})

from django.shortcuts import get_object_or_404

def submitcatalogue(request):
    marketplace_id=request.GET.get('marketplace_id')
    if request.method == 'POST':
        createdata = Food_catalogue_items()
        food_catalogue_id = request.POST.get('Foodcatalogue')
        food_catalogue = get_object_or_404(Food_catalogue, id=food_catalogue_id)
        createdata.Food_catalogue=food_catalogue
        food_id = request.POST.get('FoodItem')
        food_item = get_object_or_404(Food, id=food_id)
        createdata.Food_Item = food_item
        createdata.client_id = request.user.id
        if marketplace_id:
            createdata.marketplace_id = marketplace_id
        createdata.save()
        if marketplace_id:
            return redirect(reverse('catalogueitemsinfo') + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('catalogueitemsinfo')
    return render(request, 'H_hotel/addcatalogueitems.html')

def deletecatalogueitemlist(request, id):
    marketplace_id=request.GET.get('marketplace_id')
    deletecatalogueitem= Food_catalogue_items.objects.filter(client_id=request.user.id, pk=id)
    deletecatalogueitem.delete()
    if marketplace_id:
        return redirect(reverse('catalogueitemsinfo') + f'?marketplace_id={marketplace_id}')
    else:
        return redirect('catalogueitemsinfo')

def editcatalogueitemlist(request, id):
    client_id= request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifycatalogueitem = Food_catalogue_items.objects.filter(client_id=request.user.id, id=id)
    if marketplace_id:
        cataloguedata1 = Food_catalogue.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        cataloguedata= Food.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/editcatalogueitemlist.html',{'modifycatalogueitem':modifycatalogueitem, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'cataloguedata':cataloguedata, 'cataloguedata1':cataloguedata1})
    else:
        cataloguedata= Food.objects.filter(client_id=request.user.id)
        cataloguedata1 = Food_catalogue.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/editcatalogueitemlist.html',{'modifycatalogueitem':modifycatalogueitem,'cataloguedata':cataloguedata, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'cataloguedata1':cataloguedata1})

    # return render(request, 'H_hotel/editcatalogueitemlist.html',{'admin_permission_obj':admin_permission_obj,'marketplace_id':marketplace_id})


def edtsubmitcatalogue(request, id):
    updatecataloguelistdata =Food_catalogue_items.objects.filter(client_id= request.user.id, id=id)
    marketplace_id =  request.GET.get('marketplace_id')
    if request.method=="POST":
        for i in updatecataloguelistdata:
            updatecataloguelistdata = Food_catalogue_items.objects.filter(client_id=request.user.id, id=id)
            if i in updatecataloguelistdata:
                updatecataloguelistdataedit = Food_catalogue_items.objects.get(id=i.id)
                food_catalogue_id = request.POST.get('reFoodcatalogue')
                food_catalogue = get_object_or_404(Food_catalogue, id=food_catalogue_id)
                updatecataloguelistdataedit.Food_catalogue=food_catalogue
                food_id = request.POST.get('reFoodItem')
                food_item = get_object_or_404(Food, id=food_id)
                updatecataloguelistdataedit.Food_Item = food_item
                updatecataloguelistdataedit.save()
                if marketplace_id:
                    return redirect(reverse('catalogueitemsinfo') + f'?marketplace_id={marketplace_id}')
                else:
                    return redirect('catalogueitemsinfo')


def hotelnearbyinfo(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id= request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id=request.GET.get('marketplace_id')
    if marketplace_id:
        placedata = Nearby_place.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request,  'H_hotel/hotenearbyinfo.html',{'admin_permission_obj':admin_permission_obj, 'placedata':placedata, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})
    placedata = Nearby_place.objects.filter(client_id=request.user.id)
    return render(request, 'H_hotel/hotenearbyinfo.html',{'admin_permission_obj':admin_permission_obj, 'placedata':placedata, 'subclient_preferences':subclient_preferences})



def addplaces(request):
    client_id=request.user.id
    marketplace_id=request.GET.get('marketplace_id')
    print('addplaces_marketplace_id',marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    return render(request, 'H_hotel/addplaces.html',{'admin_permission_obj':admin_permission_obj,'marketplace_id':marketplace_id})


def submitplacelist(request):
    marketplace_id = request.GET.get('marketplace_id')
    print('submitplacelist_marketplace_id', marketplace_id)
    if request.method == 'POST':
        createplacelistdata = Nearby_place()
        createplacelistdata.place_name = request.POST.get('name')
        createplacelistdata.place_type = request.POST.get('placetype')
        createplacelistdata.distance = request.POST.get('distance')
        createplacelistdata.distance_unit = request.POST.get('distanceunit') 
        createplacelistdata.Discription = request.POST.get('discription')
        if 'placeimage' in request.FILES:
            createplacelistdata.place_image = request.FILES['placeimage']
        
        if 'placevideo' in request.FILES:
            createplacelistdata.place_video = request.FILES['placevideo']
        createplacelistdata.client_id=request.user.id
        if marketplace_id:
            createplacelistdata.marketplace_id=marketplace_id
        createplacelistdata.save()
        if marketplace_id:
            return redirect(reverse('hotelnearbyinfo') + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('hotelnearbyinfo')
    return render(request, 'H_hotel/addplaces.html')


def editplacelist(request,id,deletefile=None):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print('editplacelist_marketplace_id', marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifyplace = Nearby_place.objects.get(client_id=request.user.id, id=id)

    if deletefile == 'place_video':
        print("came to iimage delete")
        modifyplace.place_video=  None
        modifyplace.save()
    elif deletefile == 'place_image':
        modifyplace.place_image = None 
        modifyplace.save()
    return render(request, 'H_hotel/editplacelist.html',{'admin_permission_obj':admin_permission_obj, 'modifyplace':modifyplace, 'marketplace_id':marketplace_id})

def submiteditplacelist(request,id):
    updateplacedate = Nearby_place.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('submiteditplacelist_marketplace_id', marketplace_id)
    if request.method =='POST':
        for i in updateplacedate:
            updateplacedate = Nearby_place.objects.filter(client_id=request.user.id, id=id)
            if i in updateplacedate:
                updateplacedateedit = Nearby_place.objects.get(id=i.id)
                updateplacedateedit.place_name = request.POST.get('rename')
                updateplacedateedit.place_type = request.POST.get('replacetype')
                updateplacedateedit.distance = request.POST.get('redistance')
                updateplacedateedit.distance_unit = request.POST.get('redistanceunit')
                updateplacedateedit.Discription = request.POST.get('rediscription')
                if 'replaceimage' in request.FILES and len(request.FILES['replaceimage']) !=0:
                    updateplacedateedit.place_image = request.FILES['replaceimage']
                else:
                    updateplacedateedit.place_image = i.place_image
                if 'replacevideo' in request.FILES and len(request.FILES['replacevideo']) !=0:
                    updateplacedateedit.place_video= request.FILES['replacevideo']

                updateplacedateedit.save()
                if marketplace_id:
                    return redirect(reverse('hotelnearbyinfo') + f'?marketplace_id={marketplace_id}')
                else:
                    return redirect('hotelnearbyinfo')
    return render(request, 'H_hotel/editplacelist.html')

def deletenearbyplace(request,id):
    updateplaces = Nearby_place.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('deletenearbyplace_marketplace_id', marketplace_id)
    deletevalue =Nearby_place.objects.filter(client_id=request.user.id, pk=id)
    deletevalue.delete()
    if marketplace_id:
        return redirect(reverse('hotelnearbyinfo') + f'?marketplace_id={marketplace_id}')
    else:
        return redirect('hotelnearbyinfo')


def hotelfacilitesinfo(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id=request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    if marketplace_id:
        facilitydata = Hotel_facilities.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/hotelfacilitesinfo.html',{'admin_permission_obj':admin_permission_obj, 'facilitydata':facilitydata, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})

    facilitydata = Hotel_facilities.objects.filter(client_id=request.user.id)
    return render(request, 'H_hotel/hotelfacilitesinfo.html',{'admin_permission_obj':admin_permission_obj, 'facilitydata':facilitydata, 'subclient_preferences':subclient_preferences})


def addfacilities(request):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print("addfacilities mk id", marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    return render(request, 'H_hotel/addfacilities.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})

def submitfacilitylist(request):
    marketplace_id = request.GET.get('marketplace_id')
    print('submitfacilitylist_marketplace_id', marketplace_id)
    if request.method =='POST':
        createfacilitydata=Hotel_facilities()
        createfacilitydata.facility_name = request.POST.get('name')
        createfacilitydata.start_time = request.POST.get('starttime')
        createfacilitydata.end_time = request.POST.get('endtime')
        createfacilitydata.discription = request.POST.get('discription')
        createfacilitydata.facility_location = request.POST.get('facilitylocation')
        if 'facilityimage' in request.FILES:
            createfacilitydata.image = request.FILES['facilityimage']
        if 'facilityvideo' in request.FILES:
            createfacilitydata.video = request.FILES['facilityvideo']
        createfacilitydata.client_id = request.user.id
        if marketplace_id:
            createfacilitydata.marketplace_id = marketplace_id
        createfacilitydata.save()
        if marketplace_id:
            return redirect(reverse('hotelfacilitesinfo') + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('hotelfacilitesinfo')
    return render(request, 'H_hotel/addfacilities.html')


def editfacilitylist(request, id,deletefile=None):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print('editfacilitylist_marketplace_id', marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifyfacilitydata = Hotel_facilities.objects.get(client_id=request.user.id, id=id)
    if deletefile == 'facilityvideo':
        print("came to iimage delete")
        modifyfacilitydata.video=  None
        modifyfacilitydata.save()
    elif deletefile == 'facilityimage':
        modifyfacilitydata.image = None 
        modifyfacilitydata.save()
    return render(request, 'H_hotel/editfacilitylist.html',{'marketplace_id':marketplace_id, 'admin_permission_obj':admin_permission_obj, 'modifyfacilitydata':modifyfacilitydata})


def submiteditfacilitylist(request, id):
    updatefacilitydate = Hotel_facilities.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('submiteditfacilitylist_marketplace_id', marketplace_id)
    if request.method =='POST':
        for i in updatefacilitydate:
            updatefacilitydate = Hotel_facilities.objects.filter(client_id=request.user.id, id=id)
            if i in updatefacilitydate:
                updatefacilitydateedit = Hotel_facilities.objects.get(id=i.id)
                updatefacilitydateedit.facility_name = request.POST.get('rename')
                updatefacilitydateedit.start_time = request.POST.get('restarttime')
                updatefacilitydateedit.end_time = request.POST.get('reendtime')
                updatefacilitydateedit.discription = request.POST.get('rediscription')
                updatefacilitydateedit.facility_location = request.POST.get('refacilitylocation')
                if 'reimage' in request.FILES and len(request.FILES['reimage']) !=0:
                    print("request.FILES['reimage']",request.FILES['reimage'])
                    updatefacilitydateedit.image = request.FILES['reimage']
                else:
                    updatefacilitydateedit.image = i.image
                if 'revideo' in request.FILES and len(request.FILES['revideo']) !=0:
                    updatefacilitydateedit.video= request.FILES['revideo']

                updatefacilitydateedit.save()
                if marketplace_id:
                    return redirect(reverse('hotelfacilitesinfo') + f'?marketplace_id={marketplace_id}')
                else:
                    return redirect('hotelfacilitesinfo')
    return render(request, 'H_hotel/editfacilitylist.html')

def deletefacility(request,id):
    # updateappointment = Consultant_details.objects.filter(client_id=request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    print('deletefacility_marketplace_id', marketplace_id)
    deletefacility = Hotel_facilities.objects.filter(client_id=request.user.id, pk=id)
    deletefacility.delete()
    if marketplace_id:
        return redirect(reverse('hotelfacilitesinfo') + f'?marketplace_id={marketplace_id}')
    else:
        return redirect('hotelfacilitesinfo')



def roomsinfo(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id=request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    if marketplace_id:
        roomsdata = Hotel_rooms_type.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/roomsinfo.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'roomsdata':roomsdata, 'subclient_preferences':subclient_preferences})
    else:
        roomsdata = Hotel_rooms_type.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/roomsinfo.html',{'admin_permission_obj':admin_permission_obj,'roomsdata':roomsdata, 'subclient_preferences':subclient_preferences})
def roomconfig(request):
    return render(request, 'H_hotel/roomconfig.html')

def addhotelrooms(request):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print('addhotelrooms marketplace_id', marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    return render(request, 'H_hotel/addhotelroom.html',{'admin_permission_obj':admin_permission_obj,'marketplace_id':marketplace_id})

def submitroomlist(request):
    marketplace_id= request.GET.get('marketplace_id')
    
    print("RoomImage",request.FILES['RoomImage'])
    print('submitroomlist marketplace_id', marketplace_id)
    if request.method == 'POST':
        createroomsdata = Hotel_rooms_type()
        createroomsdata.l_room_type = request.POST.get('lroomtype')
        createroomsdata.room_type = request.POST.get('roomtype')
        createroomsdata.bed = request.POST.get('roombed') 
        createroomsdata.room_price = request.POST.get('roomprice')
        createroomsdata.Hotel_room_image= request.FILES['RoomImage']
        createroomsdata.room_price_unit = request.POST.get('roompriceunit')
        createroomsdata.room_info = request.POST.get('roominfo')
        createroomsdata.client_id = request.user.id
        if marketplace_id:
            createroomsdata.marketplace_id=marketplace_id
        createroomsdata.save()
        if marketplace_id:
            return redirect(reverse('roomsinfo') + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('roomsinfo')

    return render(request,  'H_hotel/addhotelroom.html')

def editroomslist(request, id):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifyroomdata = Hotel_rooms_type.objects.filter(client_id= request.user.id, id=id)
    return render(request, 'H_hotel/editroomslist.html',{'admin_permission_obj':admin_permission_obj,'modifyroomdata':modifyroomdata, 'marketplace_id':marketplace_id})

def submiteditroomist(request, id):
    updateroomsdate = Hotel_rooms_type.objects.filter(client_id=request.user.id, id=id)
    marketplace_id= request.GET.get('marketplace_id')
    print("RoomImage",request.FILES['reroomimage'])
    if request.method =='POST':
        for i in updateroomsdate:
            updateroomsdate = Hotel_rooms_type.objects.filter(client_id=request.user.id, id=id)
            if i in updateroomsdate:
                updateroomsdateedit = Hotel_rooms_type.objects.get(id=i.id)
                updateroomsdateedit.bed = request.POST.get('reroombed')
                updateroomsdateedit.room_type = request.POST.get('reroomtype')
                updateroomsdateedit.room_price = request.POST.get('reroomprice')
                updateroomsdateedit.room_price_unit = request.POST.get('reroompriceunit')
                updateroomsdateedit.room_info = request.POST.get('reroominfo')
                updateroomsdateedit.l_room_type = request.POST.get('relroomtype')
                updateroomsdateedit.Hotel_room_image=request.FILES['reroomimage']
                updateroomsdateedit.save()
                if marketplace_id:
                    return redirect(reverse('roomsinfo') + f'?marketplace_id={marketplace_id}')
                else:
                    return redirect('roomsinfo')
    return render(request, 'H_hotel/editroomlist.html')


def deleterooms(request, id):
    marketplace_id = request.GET.get('marketplace_id')
    deleteroomsvalue = Hotel_rooms_type.objects.filter(client_id=request.user.id, pk=id)
    deleteroomsvalue.delete()
    if marketplace_id:
        return redirect(reverse('roomsinfo') + f'?marketplace_id={marketplace_id}')
    else:
        return redirect("roomsinfo")


def listofrooms(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id=request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    if marketplace_id:
        roomslistdatadata = Room_list.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/listofrooms.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'roomslistdatadata':roomslistdatadata, 'subclient_preferences':subclient_preferences})
    else:
        roomslistdatadata = Room_list.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/listofrooms.html',{'admin_permission_obj':admin_permission_obj,'roomslistdatadata':roomslistdatadata, 'subclient_preferences':subclient_preferences})
   

def addhotelroomslist(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    client_id=request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    if marketplace_id:
        room_type = Hotel_rooms_type.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/addroomlist.html',{'room_type':room_type,'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})
    else:
        room_type = Hotel_rooms_type.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/addroomlist.html',{'room_type':room_type,'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})




from django.shortcuts import get_object_or_404

def submitroomlista(request):
    marketplace_id = request.GET.get('marketplace_id')

    if request.method == 'POST':
        createroomlistdata = Room_list()
        createroomlistdata.room_number = request.POST.get('roomnumber')
        createroomlistdata.room_floor = request.POST.get('roomfloor')
        # Convert the string to an integer
        hotel_room_type_id = int(request.POST.get('hotelroomtype'))
        # Get the Hotel_rooms_type instance
        hotel_room_type_instance = get_object_or_404(Hotel_rooms_type, pk=hotel_room_type_id)

        createroomlistdata.hotel_room_type = hotel_room_type_instance
        createroomlistdata.client_id = request.user.id

        if marketplace_id:
            createroomlistdata.marketplace_id = marketplace_id

        createroomlistdata.save()

        if marketplace_id:
            return redirect(reverse('listofrooms') + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('listofrooms')

    return render(request, 'H_hotel/addroomlist.html')

def editlistofrooms(request, id):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifyroomlist = Room_list.objects.filter(client_id=request.user.id, id=id)
    if marketplace_id:
        room_type = Hotel_rooms_type.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/editlistofroom.html',{'modifyroomlist':modifyroomlist,'room_type':room_type,'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})
    else:
        room_type = Hotel_rooms_type.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/editlistofroom.html',{'modifyroomlist':modifyroomlist,'room_type':room_type,'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})


def edisubmitroomlista(request, id):
    updateroomlistdata =Room_list.objects.filter(client_id= request.user.id, id=id)
    marketplace_id =  request.GET.get('marketplace_id')
    if request.method=="POST":
        for i in updateroomlistdata:
            updateroomlistdata = Room_list.objects.filter(client_id=request.user.id, id=id)
            if i in updateroomlistdata:
                updateroomlistdataedit = Room_list.objects.get(id=i.id)
                updateroomlistdataedit.room_number = request.POST.get('reroomnumber')
                updateroomlistdataedit.room_floor = request.POST.get('reroomfloor')
                # Convert the string to an integer
                hotel_room_type_id = int(request.POST.get('rehotelroomtype'))
                # Get the Hotel_rooms_type instance
                hotel_room_type_instance = get_object_or_404(Hotel_rooms_type, pk=hotel_room_type_id)

                updateroomlistdataedit.hotel_room_type = hotel_room_type_instance
                updateroomlistdataedit.save()
                if marketplace_id:
                    return redirect(reverse('listofrooms') + f'?marketplace_id={marketplace_id}')
                else:
                    return redirect('listofrooms')

def deletelistofrooms(request, id):
    marketplace_id = request.GET.get('marketplace_id')
    deletelistroomdata = Room_list.objects.filter(client_id=request.user.id, pk=id)
    deletelistroomdata.delete()
    if marketplace_id:
        return redirect(reverse('listofrooms') + f'?marketplace_id={marketplace_id}')
    else:
        return redirect('listofrooms')



def selfhelpinfo(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id = request.user.id
    marketplace_id=request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    if marketplace_id:
        helplistdata = Selfhelp.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/selfhelpinfo.html',{'admin_permission_obj':admin_permission_obj, 'helplistdata':helplistdata, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})
    else:
        helplistdata = Selfhelp.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/selfhelpinfo.html',{'admin_permission_obj':admin_permission_obj, 'helplistdata':helplistdata, 'subclient_preferences':subclient_preferences})

def addselphelp(request):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    return render(request, 'H_hotel/addhelpservice.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})


def submithelplist(request):
    marketplace_id=request.GET.get('marketplace_id')
    if request.method == 'POST':
        createhelpdata=Selfhelp()
        createhelpdata.selfhelp_name = request.POST.get('selpname')
        createhelpdata.selfhelp_discription = request.POST.get('selfhelpdiscription')
        if 'selfhelpimage' in request.FILES:
            createhelpdata.selfhelp_image = request.FILES['selfhelpimage']
        else:
            createhelpdata.selfhelp_image = i.selfhelp_image
        if 'selfhelpvideo' in request.FILES and len(request.FILES['selfhelpvideo']) !=0:
            createhelpdata.selfhelp_video= request.FILES['selfhelpvideo']
        createhelpdata.client_id=request.user.id
        if marketplace_id:
            createhelpdata.marketplace_id = marketplace_id
        createhelpdata.save()
        if marketplace_id:
            return redirect(reverse('selfhelpinfo') + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('selfhelpinfo')
    return render(request,'H_hotel/addhelpservice.html' )

def edithelplist(request, id):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifyhelp = Selfhelp.objects.filter(client_id=request.user.id, id=id)
    return render(request, 'H_hotel/edithelps.html',{'marketplace_id':marketplace_id, 'admin_permission_obj':admin_permission_obj, 'modifyhelp':modifyhelp})

def submitedithelplist(request,id):
    updatehelpdata =Selfhelp.objects.filter(client_id= request.user.id, id=id)
    marketplace_id = request.GET.get('marketplace_id')
    if request.method=="POST":
        for i in updatehelpdata:
            updatehelpdata = Selfhelp.objects.filter(client_id=request.user.id, id=id)
            if i in updatehelpdata:
                updatehelpdataedit = Selfhelp.objects.get(id=i.id)
                updatehelpdataedit.selfhelp_name = request.POST.get('reselpname')
                updatehelpdataedit.selfhelp_discription = request.POST.get('reselfhelpdiscription')
                if 'reselfhelpimage' in request.FILES and len(request.FILES['reselfhelpimage']) !=0:
                    updatehelpdataedit.selfhelp_image= request.FILES['reselfhelpimage']
                else:
                    updatehelpdataedit.selfhelp_image = i.selfhelp_image
                if 'reselfhelpvideo' in request.FILES and len(request.FILES['reselfhelpvideo']) !=0:
                    updatehelpdataedit.selfhelp_video = request.FILES['reselfhelpvideo']
                updatehelpdataedit.save()
                if marketplace_id:
                    return redirect(reverse('selfhelpinfo') + f'?marketplace_id={marketplace_id}')
                else:
                    return redirect('selfhelpinfo')
    return render(request, 'H_hotel/edithelps.html')


def deletehelpsdata(request, id):
    marketplace_id= request.GET.get('marketplace_id')
    deletehelpvalu = Selfhelp.objects.filter(client_id=request.user.id, id=id)
    deletehelpvalu.delete()
    if marketplace_id:
        return redirect(reverse('selfhelpinfo') + f'?marketplace_id={marketplace_id}')
    else:
        return redirect('selfhelpinfo')


def hotelinformation(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    client_id= request.user.id
    marketplace_id =  request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    if marketplace_id:
        informationdata = Information.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
        return render(request, 'H_hotel/hotelinformation.html',{'admin_permission_obj':admin_permission_obj, 'informationdata':informationdata, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})
    else:    
        informationdata= Information.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/hotelinformation.html',{'admin_permission_obj':admin_permission_obj, 'informationdata':informationdata, 'subclient_preferences':subclient_preferences})

def addinformation(request):
    client_id=request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    return render(request, 'H_hotel/addinformation.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id})

def submitinfolist(request):
    marketplace_id= request.GET.get('marketplace_id')
    if request.method== 'POST':
        createinfodata = Information()
        createinfodata.information_name = request.POST.get('name')
        createinfodata.information_discription = request.POST.get('informationdiscription')
        if 'informationimage' in request.FILES:
            createinfodata.information_image = request.FILES['informationimage']
        if 'informationvideo' in request.FILES:
            createinfodata.information_video = request.FILES['informationvideo']

        createinfodata.client_id = request.user.id
        if marketplace_id:
            createinfodata.marketplace_id=marketplace_id
        createinfodata.save()
        if marketplace_id:
            return redirect(reverse('hotelinformation') + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('hotelinformation')
    return render(request, 'H_hotel/addinformation')

def editinfolist(request, id):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    modifyinfolist = Information.objects.filter(client_id=request.user.id, id=id)
    return render(request, 'H_hotel/editinfo.html',{'admin_permission_obj':admin_permission_obj, 'modifyinfolist':modifyinfolist, 'marketplace_id':marketplace_id})

def submitediinfolist(request,id):
    updateinfodata =Information.objects.filter(client_id= request.user.id, id=id)
    marketplace_id =  request.GET.get('marketplace_id')
    if request.method=="POST":
        for i in updateinfodata:
            updateinfodata = Information.objects.filter(client_id=request.user.id, id=id)
            if i in updateinfodata:
                updateinfodataedit = Information.objects.get(id=i.id)
                updateinfodataedit.information_name = request.POST.get('reinformationname')
                updateinfodataedit.information_discription = request.POST.get('reinformationdiscription')
                if 'reinformationimage' in request.FILES and len(request.FILES['reinformationimage']) !=0:
                    updateinfodataedit.information_image= request.FILES['reinformationimage']
                else:
                    updateinfodataedit.information_image = i.information_image
                if 'reinformationvideo' in request.FILES and len(request.FILES['reinformationvideo']) !=0:
                    updateinfodataedit.information_video = request.FILES['reinformationvideo']
                updateinfodataedit.save()
                if marketplace_id:
                    return redirect(reverse('hotelinformation') + f'?marketplace_id={marketplace_id}')
                else:
                    return redirect('hotelinformation')
    return render('H_hotel/editinfo.html')



def deleteinfodata(request,id):
    marketplace_id = request.GET.get('marketplace_id')
    deleteinfovalue = Information.objects.filter(client_id=request.user.id, id=id)
    deleteinfovalue.delete()
    if marketplace_id:
        return redirect(reverse('hotelinformation') + f'?marketplace_id={marketplace_id}')
    else:
        return redirect('hotelinformation')




def guestinfo(request,  id=None):
    subclient_id = request.session.get('subclient_id')  
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    guest_room_info = Hotel_Room_Guest_info.objects.filter(client_id=request.user.id)
    allhotels=Hotel_settings.objects.filter(client_id=request.user.id).exclude(marketplace__isnull=True)
    
    Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.filter(client_id=request.user.id)
    return render(request, 'H_hotel/guestinfo.html',{'admin_permission_obj':admin_permission_obj, 'subclient_preferences':subclient_preferences, 'guest_room_info':guest_room_info,"allhotels":allhotels,"Hotel_Room_Guest_info_obj":Hotel_Room_Guest_info_obj})

from pytz import timezone

def getguestlist(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    subclient_id = request.session.get('subclient_id')  
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    allhotels=Hotel_settings.objects.filter(client_id=request.user.id).exclude(marketplace__isnull=True)
    

    if request.method == 'POST':
        guest_name = request.POST.get('guest_name')
        room_number= request.POST.get('Room_number')
        hotel_id= request.POST.get('hotels')
        
        phone_number = request.POST.get('phone_number')
        print("phone_number",phone_number)
        government_id = request.POST.get('government_id') 
        address = request.POST.get('address')
        check_in = request.POST.get('check_in') 
        check_out = request.POST.get('check_out')


        # Constructing the query based on received parameters
        # Assuming YourModel is the model you want to query
       
       

        Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.filter(client_id=request.user.id)
        if subclient_preferences:
            Hotel_settings_obj=Hotel_settings.objects.get(client_id=request.user.id,marketplace_id=subclient_preferences.marketplace_id)
            
            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info_obj.filter(Hotel_details_id=Hotel_settings_obj)
           
        if hotel_id and hotel_id !='Select Hotel':
            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.filter(client_id=request.user.id,Hotel_details_id=hotel_id)
        if check_in:
            check_in=check_in.replace('T', ' ')
        
            datetime_obj = datetime.strptime(check_in, '%Y-%m-%d %H:%M')

            # Make the datetime object timezone aware
            timezone_obj = timezone('UTC')
            aware_datetime_obj = timezone_obj.localize(datetime_obj)
            aware_date=aware_datetime_obj.date()
            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info_obj.filter(client_id=request.user.id,Check_In__date=aware_date)
            print(Hotel_Room_Guest_info_obj)
        if check_out:
            check_out=check_out.replace('T', ' ')
        
            datetime_obj = datetime.strptime(check_out, '%Y-%m-%d %H:%M')

            # Make the datetime object timezone aware
            timezone_obj = timezone('UTC')
            aware_datetime_obj = timezone_obj.localize(datetime_obj)
            aware_date=aware_datetime_obj.date()
            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info_obj.filter(client_id=request.user.id,Check_Out__date=aware_date)
            print(Hotel_Room_Guest_info_obj)
            

        if room_number:
            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info_obj.filter(Room_details__room_number__icontains=room_number)
        

        Guest_details=Guest_info.objects.filter(client_id=request.user.id)
        if guest_name:
            Guest_details = Guest_details.filter(Guest_name__icontains=guest_name)
           
        if phone_number:
            Guest_details = Guest_details.filter(Phone_number__icontains=phone_number)

        if government_id:
            Guest_details = Guest_details.filter(GovernmentId__icontains=government_id)

        if address:
            Guest_details = Guest_details.filter(Address__icontains=address)
        Final_Guest_details=Guest_details.all()
        print("Final_Guest_details",Final_Guest_details)
        if Final_Guest_details:
            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info_obj.filter(client_id=request.user.id,Guest_details__in=Final_Guest_details)
            if Hotel_Room_Guest_info_obj:
                return render(request,  'H_hotel/guestinfo.html', {'subclient_preferences':subclient_preferences, 'admin_permission_obj':admin_permission_obj,"Hotel_Room_Guest_info_obj":Hotel_Room_Guest_info_obj,"allhotels":allhotels} )

            else:
                error_message="No matching results found....."
                return render(request,  'H_hotel/guestinfo.html', {'subclient_preferences':subclient_preferences, 'admin_permission_obj':admin_permission_obj,"error_message":error_message,"allhotels":allhotels} )
        else:
            

        
            error_message="No matching results found....."
            return render(request,  'H_hotel/guestinfo.html', {'subclient_preferences':subclient_preferences, 'admin_permission_obj':admin_permission_obj,"error_message":error_message,"allhotels":allhotels})                                                             
        # if check_in:
        #     Guest_details = query.filter(check_in__icontains=check_in)

        # if check_out:
        #     query = query.filter(check_out__icontains=check_out)

        # Execute the final query
          # or query.first() if you expect only one result

        # if not all([guest_name, phone_number, government_id, address, check_in, check_out]):
        #     print("error")
        #     error_message = "Please fill out all required fields."
        #     return render(request,  'H_hotel/guestinfo.html', {'error_message': error_message, 'subclient_preferences':subclient_preferences, 'admin_permission_obj':admin_permission_obj})

        
        
        # guest_info, created = Guest_info.objects.get_or_create(
        #     Guest_name=guest_name,
        #     client=current_user,
        #     defaults={'Phone_number': phone_number, 'GovernmentId': government_id, 'Address': address}
        # )

        # if guest_info:
        #     guest_room_info, created = Hotel_Room_Guest_info.objects.get_or_create(
        #         Guest_details=guest_info,
        #         Check_In=check_in,
        #         defaults={'Check_Out': check_out}
        #     )

        #     if guest_room_info:
        #         return render(request,  'H_hotel/guestinfo.html', {'guest_room_info': guest_room_info, 'subclient_preferences':subclient_preferences, 'admin_permission_obj':admin_permission_obj})
        #     else:
        #         error_message = "Failed to create/update booking."
        # else:
        #     error_message = "Failed to create/update guest information."

        # return render(request,  'H_hotel/guestinfo.html', {'error_message': error_message, 'subclient_preferences':subclient_preferences, 'admin_permission_obj':admin_permission_obj})
    else:
        return render(request,  'H_hotel/guestinfo.html', {'subclient_preferences':subclient_preferences, 'admin_permission_obj':admin_permission_obj} )




# Logic for Display Room Details:
def roominfo(request, id=None):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    subclient_id = request.session.get('subclient_id') 
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    # Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.filter(client_id=request.user.id)
    # guest_room_info = Hotel_Room_Guest_info.objects.all()
    guest_room_info = Hotel_Room_Guest_info.objects.filter(client_id=request.user.id)

    room_guest_info_data=Hotel_Room_Guest_info.objects.filter(client_id=request.user.id)
    
    hotelname = Hotel_settings.objects.filter(client_id=request.user.id, marketplace__isnull = False)
    return render(request, 'H_hotel/roominfo.html',{'admin_permission_obj':admin_permission_obj, 'subclient_preferences':subclient_preferences,'room_guest_info_data':room_guest_info_data,"allhotels":hotelname,'guest_room_info':guest_room_info})


# from datetime import datetime
# Logic For Filter Room Lists:
def getroomlist(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    subclient_id = request.session.get('subclient_id')  
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    hotel = Hotel_settings.objects.filter(client_id=request.user.id, marketplace_id__isnull = False)
    
    if request.method == 'POST':
        guest_name = request.POST.get('guest_name')
        room_number= request.POST.get('Room_number')
        hotel_id= request.POST.get('hotels')
        phone_number = request.POST.get('phone_number')
        room_availability = request.POST.get('room_availability')
        check_in = request.POST.get('check_in') 
        check_out = request.POST.get('check_out')
        
        # Constructing the query based on received parameters
        # Assuming YourModel is the model you want to query
       
        Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.filter(client_id=request.user.id)
        # Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.all()
       
        if subclient_preferences:
            Hotel_settings_obj=Hotel_settings.objects.get(client_id=request.user.id,marketplace_id=subclient_preferences.marketplace_id)
            
            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info_obj.filter(Hotel_details_id=Hotel_settings_obj)
           
        if hotel_id and hotel_id !='Select Hotel':
            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.filter(client_id=request.user.id,Hotel_details_id=hotel_id)


        if check_in:
            check_in=check_in.replace('T', ' ')
        
            datetime_obj = datetime.strptime(check_in, '%Y-%m-%d %H:%M')

            # Make the datetime object timezone aware
            timezone_obj = timezone('UTC')
            start_aware_datetime = timezone_obj.localize(datetime_obj)
            end_aware_datetime = start_aware_datetime + timedelta(minutes=1) 

            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info_obj.filter(client_id=request.user.id,Check_In__range=(start_aware_datetime,end_aware_datetime))
            # print(Hotel_Room_Guest_info_obj)

        if check_out:
            check_out=check_out.replace('T', ' ')
            datetime_obj = datetime.strptime(check_out, '%Y-%m-%d %H:%M')

            # Make the datetime object timezone aware
            timezone_obj = timezone('UTC')
            start_aware_datetime = timezone_obj.localize(datetime_obj)
            end_aware_datetime = start_aware_datetime + timedelta(minutes=1) 

            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info_obj.filter(client_id=request.user.id,Check_Out__range=(start_aware_datetime, end_aware_datetime))

        if room_number:
            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info_obj.filter(Room_details__room_number__icontains=room_number)
            
        if room_availability:
            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info_obj.filter(Room_details__room_availability__icontains=room_availability)
            
        Guest_details=Guest_info.objects.filter(client_id=request.user.id)

        if guest_name:
            Guest_details = Guest_details.filter(Guest_name__icontains=guest_name)
            
        if phone_number:
            Guest_details = Guest_details.filter(Phone_number__icontains=phone_number)

        Final_Guest_details=Guest_details.all()
       
        if Final_Guest_details:
            room_guest_info_data=Hotel_Room_Guest_info_obj.filter(client_id=request.user.id,Guest_details__in=Final_Guest_details)
            
            if Hotel_Room_Guest_info_obj:
                return render(request,'H_hotel/roominfo.html', {'subclient_preferences':subclient_preferences, 'admin_permission_obj':admin_permission_obj,"room_guest_info_data":room_guest_info_data,"allhotels":hotel} )

            else:
                error_message="No matching results found....."
                return render(request,  'H_hotel/roominfo.html', {'subclient_preferences':subclient_preferences, 'admin_permission_obj':admin_permission_obj,"error_message":error_message,"allhotels":hotel} )
        else:
            error_message="No matching results found....."
            return render(request,  'H_hotel/roominfo.html', {'subclient_preferences':subclient_preferences, 'admin_permission_obj':admin_permission_obj,"error_message":error_message,"allhotels":hotel})                                                             
    else:
        return render(request,'H_hotel/roominfo.html', {'subclient_preferences':subclient_preferences, 'admin_permission_obj':admin_permission_obj})


#  fro request come from the user/whatsapp
def viewrequest(request, id=None):
    print("id",id)
    subclient_id = request.session.get('subclient_id') 
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    print("admin_permission_obj",admin_permission_obj,admin_permission_obj.client_marketplace)
    servicerequest = Service_order.objects.filter(marketplace_id=id)
    hotelname = Hotel_settings.objects.filter(client_id=request.user.id, marketplace__isnull = False)
    if subclient_preferences:
        hotelname=[]
        subclient_marketplaces=(subclient_preferences.marketplace_id).split(',')
        print("subclient_marketplaces",subclient_marketplaces)
        for i in subclient_marketplaces:
            hotelname.append(Hotel_marketplace.objects.get(client_id=request.user.id,id=int(i)))

    # servicerequest = Serivce_order.objects.filter(subclient=subclient)
    # if subclient:
    #     return render(request,'H_hotel/viewrequest.html', {'admin_permission_obj':admin_permission_obj, 'servicerequest':servicerequest, 'subclient_preferences':subclient_preferences, 'hotelname':hotelname})
    return render(request, 'H_hotel/viewrequest.html', {'admin_permission_obj':admin_permission_obj, 'servicerequest':servicerequest, 'subclient_preferences':subclient_preferences, 'hotelname':hotelname})


def gethotels(request, id=None):
    if request.method == 'POST':
        subclient_id = request.session.get('subclient_id') 
        subclient = Subclient.objects.filter(id=subclient_id).first()
        subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
        admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
        marketplace_id = request.GET.get('marketplace_id')
        print('marketplace_id', marketplace_id)
        client_id = request.GET.get('client_id')
        hotel_id = request.POST.get('hotelname')
        print("hotel_id",hotel_id)
        Hotel_settings_obj=Hotel_settings.objects.get(client_id=request.user.id,id=hotel_id)
        service = Service_order.objects.filter(client_id=request.user.id,marketplace=Hotel_settings_obj.marketplace)
        hotelname = Hotel_settings.objects.filter(client_id=request.user.id, marketplace__isnull = False)
        if subclient_preferences:
                hotelname=[]
                
                subclient_marketplaces=(subclient_preferences.marketplace_id).split(',')
                print("subclient_marketplaces",subclient_marketplaces)
                for i in subclient_marketplaces:
                     hotelname.append(Hotel_marketplace.objects.get(client_id=request.user.id,id=int(i)))
                #return render(request, 'H_hotel/viewcomplaints.html', {'admin_permission_obj':admin_permission_obj,"Hotel_marketplace_obj":Hotel_marketplace_obj,"subclient_preferences":subclient_preferences})
        return render(request, 'H_hotel/viewrequest.html', {'hotelname':hotelname, 'service': service, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})
    return render(request, 'H_hotel/viewrequest.html', {'hotelname':hotelname, 'service': None, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})


def foodrequest(request, id=None):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    client_id = request.GET.get('client_id')
    subclient_id = request.session.get('subclient_id') 
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    hotelname = Hotel_settings.objects.filter(client_id=request.user.id, marketplace__isnull = False)
    Foodorderheader = Food_order_header.objects.filter(client_id=request.user.id)
    if subclient_preferences:
        hotelname=[]
        subclient_marketplaces=(subclient_preferences.marketplace_id).split(',')
        print("subclient_marketplaces",subclient_marketplaces)
        for i in subclient_marketplaces:
            hotelname.append(Hotel_marketplace.objects.get(client_id=request.user.id,id=int(i)))
    return render(request, 'H_hotel/foodrequest.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'Foodorderheader':Foodorderheader, 'hotelname':hotelname, 'subclient_preferences':subclient_preferences})



def getorders(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    hotelname = Hotel_marketplace.objects.filter(client_id=request.user.id)
    if request.method == 'POST':
        subclient_id = request.session.get('subclient_id') 
        subclient = Subclient.objects.filter(id=subclient_id).first()
        subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
        admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
        marketplace_id = request.GET.get('marketplace_id')
        print('marketplace_id', marketplace_id)
        client_id = request.GET.get('client_id')
        marketplace_id = request.POST.get('marketplacename')
        Foodheader = Food_order_header.objects.filter(marketplace_id=marketplace_id)
        hotelname = Hotel_settings.objects.filter(client_id=request.user.id, marketplace__isnull = False)
        if subclient_preferences:
            hotelname=[]
            subclient_marketplaces=(subclient_preferences.marketplace_id).split(',')
            print("subclient_marketplaces",subclient_marketplaces)
            for i in subclient_marketplaces:
                hotelname.append(Hotel_marketplace.objects.get(client_id=request.user.id,id=int(i)))
        return render(request, 'H_hotel/roodrequest.html', {'hotelname':hotelname ,'Foodheader': Foodheader, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id,'subclient_preferences':subclient_preferences})
    return render(request, 'H_hotel/roodrequest.html',{'hotelname':hotelname, 'Foodheader': None, 'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})



def fooddetails(request, id):
    subclient_id = request.session.get('subclient_id') 
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id = request.GET.get('marketplace_id')
    client_id = request.GET.get('client_id')
    Foodorderdetails=Food_order_details.objects.filter(client_id=request.user.id, Food_order_header=id)
    return render(request, 'H_hotel/fooddetails.html',{'admin_permission_obj':admin_permission_obj, 'Foodorderdetails':Foodorderdetails, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})


def submitfeedbackquestions(request):
    client_id= request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    button=request.POST.get('button')
    print("button",button)
    print("marketplace_idmmmmm",marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    if request.method =='POST':
        
        createdata = Checkout_questions()
        createdata.Question = request.POST.get('Feedback_Question')
        createdata.client_id = request.user.id
        if marketplace_id:
            createdata.marketplace_id=marketplace_id

        createdata.save()
        questions=''
        if marketplace_id:
            questions=Checkout_questions.objects.filter(client_id=request.user.id,marketplace_id=int(marketplace_id))
        else:
            questions=Checkout_questions.objects.filter(client_id=request.user.id)
        return render(request, 'H_hotel/feedbackQuestions.html',{'admin_permission_obj':admin_permission_obj, 'questions':questions,'marketplace_id':marketplace_id})

    return render(request, 'H_hotel/addfeedbackquestion.html')

def editfeedbackquestions(request,id):
    print("id",id)
    marketplace_id=request.GET.get('marketplace_id')
    print("marketplace_id",marketplace_id)
    question = Checkout_questions.objects.get(id=id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    return render(request, 'H_hotel/editfeedbackquestion.html',{'admin_permission_obj':admin_permission_obj, 'question':question, 'marketplace_id':marketplace_id})
    
def submiteditfeedbackquestions(request,id):
    client_id= request.user.id
    print("submiteditfeedbackquestions")
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id=request.GET.get('marketplace_id')
    if request.method =='POST':
        print("id1",id)
        createdata = Checkout_questions.objects.get(id=id)
        createdata.Question = request.POST.get('reFeedback_Question')
        

        createdata.save()
        questions=''
        if marketplace_id:
            questions=Checkout_questions.objects.filter(client_id=request.user.id,marketplace_id=int(marketplace_id))
        else:
            questions=Checkout_questions.objects.filter(client_id=request.user.id)

        return render(request, 'H_hotel/feedbackquestions.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, "questions":questions})


    return render(request, 'H_hotel/editfeedbackquestion.html')

def deletefeedbackquestions(request,id):
    print("id",id)
    marketplace_id = request.GET.get('marketplace_id')
    print("marketplace_id",marketplace_id)
    question = Checkout_questions.objects.get(id=int(id))
    
    
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    questions=''
    if marketplace_id:
        questions=Checkout_questions.objects.filter(client_id=request.user.id,marketplace_id=int(marketplace_id))
    else:
        questions=Checkout_questions.objects.filter(client_id=request.user.id)
    question.delete()
    return render(request, 'H_hotel/feedbackquestions.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, "questions":questions})

def feedbackQuestions(request):
    print("feedback")
    subclient_id = request.session.get('subclient_id') 
    marketplace_id = request.GET.get('marketplace_id')
    print("marketplace_id",marketplace_id)
    questions=Checkout_questions.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    print("subclient_preferences",subclient_preferences)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    return render(request, 'H_hotel/feedbackquestions.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences,"questions":questions})

def addfeedbackquestions(request):
    subclient_id = request.session.get('subclient_id') 
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    print("marketplace_id",marketplace_id)
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    return render(request,  'H_hotel/addfeedbackquestion.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})


def feedbackresponses(request, id=None):
    print("feedbackresponse")
    print("id",id)
    client_id=request.user.id
    subclient_id = request.session.get('subclient_id') 
    marketplace_id = request.GET.get('marketplace_id')
    print("marketplace_id",marketplace_id)
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    print("subclient_preferences",subclient_preferences)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    print("admin_permission_obj",admin_permission_obj,request.user.id)
    marketplace_id = request.GET.get('marketplace_id')
    Rooms=Room_list.objects.filter(client_id=request.user.id, marketplace_id=id)
    print("Rooms",Rooms)
    if admin_permission_obj:
        if admin_permission_obj.client_marketplace  == 'yes' :
            print("if hotelname")
            Hotel_marketplace_ids = Hotel_marketplace.objects.filter(client_id=client_id).values_list('id', flat=True)
            hotelname=Hotel_settings.objects.filter(client_id=client_id,marketplace_id__in=Hotel_marketplace_ids)
        
            if subclient_preferences:
                subclient_marketplaces = [int (x) for x in (subclient_preferences.marketplace_id).split(',')]
                print("subclient_marketplaces",subclient_marketplaces)
                hotelname=Hotel_settings.objects.filter(client_id=client_id,marketplace_id__in=subclient_marketplaces)
            if id :
                particular_hotel = Hotel_settings.objects.get(client_id=request.user.id,id=id)
                return render(request, 'H_hotel/feedbackresponses.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences,'hotelname':hotelname,'particular_hotel':particular_hotel,"Rooms":Rooms})
                 
            return render(request, 'H_hotel/feedbackresponses.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences,'hotelname':hotelname})
        elif admin_permission_obj.client_marketplace  != 'yes' :
            print("elif")
            hotelname = Hotel_settings.objects.filter(client_id=request.user.id).exclude(marketplace_isnull = False)
            
            print("hotelname",hotelname)
            return render(request, 'H_hotel/feedbackresponses.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences,'hotelname':hotelname,"Rooms":Rooms})
    return render(request, 'H_hotel/feedbackresponses.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})
     
def viewfeedbackresponses(request,id=None):
    client_id=request.user.id
    hotel_id=request.POST.get('hotelname')
    print("hotel_id",hotel_id,id)
    hotel_details=''
    hotelname=''
    Rooms=Room_list.objects.filter(client_id=request.user.id, marketplace__isnull=True)
    if hotel_id:
        hotel_details=Hotel_settings.objects.get(client_id=client_id, id=hotel_id)
        Rooms=Room_list.objects.filter(client_id=request.user.id, marketplace_id=hotel_details.marketplace_id)
        
    
    subclient_id = request.session.get('subclient_id') 
    print("subclient_id",subclient_id)
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    room_id=request.POST.get('roomnumber')
    print("room_id",room_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    Room_number=Room_list.objects.get(id=room_id)
    print("Room_number",Room_number)
    if hotel_details:
        if hotel_details.marketplace_id:
            hotelname=Hotel_settings.objects.filter(client_id=client_id).exclude(marketplace__isnull=True)
    else:
        hotel_details=Hotel_settings.objects.get(client_id=client_id, marketplace__isnull=True)

    
    Checkout_response_header_ids=Checkout_response_header.objects.filter(client_id=request.user.id,Hotel_details=hotel_details, Room_details_id=room_id).values_list('id', flat=True)
    print("Checkout_response_header_obj",Checkout_response_header_ids)
    allresponses=Checkout_responses.objects.filter(client_id=request.user.id,Checkout_response_header_id__in=Checkout_response_header_ids)  
    print("Checkout_responses_obj",allresponses)
    return render(request, 'H_hotel/feedbackresponses.html',{'admin_permission_obj':admin_permission_obj,"allresponses":allresponses,"Room_Number":Room_number,"hotelname":hotelname,"subclient_preferences":subclient_preferences,"Rooms":Rooms,"particular_hotel":hotel_details})


def complaintcategories(request):
    admin_permission_obj=admin_permission.objects.get(client_id=request.user.id)
    marketplace_id=request.GET.get('marketplace_id')
    print("marketplace_id",marketplace_id)
    Complaint_settings_obj=Complaint_settings.objects.filter(client_id=request.user.id,marketplace_id=marketplace_id)
    return render(request,'H_hotel/complaintcategories.html',{'admin_permission_obj':admin_permission_obj,'marketplace_id':marketplace_id,"Complaint_settings_obj":Complaint_settings_obj})

def addcomplaintcategories(request):
    subclient_id = request.session.get('subclient_id') 
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    print("marketplace_id",marketplace_id)
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    return render(request,'H_hotel/addcomplaintcategories.html',{'admin_permission_obj':admin_permission_obj, 'marketplace_id':marketplace_id, 'subclient_preferences':subclient_preferences})

def submitcomplaintcaregories(request):
    subclient_id = request.session.get('subclient_id') 
    marketplace_id = request.GET.get('marketplace_id')
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    print("marketplace_id",marketplace_id)
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    Complaint_settings_obj=Complaint_settings()
    Complaint_settings_obj.client_id=request.user.id
    Complaint_settings_obj.marketplace_id=marketplace_id
    Complaint_settings_obj.Complaint_category=request.POST.get('Complaint_Category')
    Complaint_settings_obj.save()
    if marketplace_id:
        return redirect(reverse('complaintcategories') + f'?marketplace_id={marketplace_id}')
    else:
        return redirect('complaintcategories')

def editcomplaintcategories(request,id):
    print("id",id)
    marketplace_id=request.GET.get('marketplace_id')
    print("marketplace_id",marketplace_id)
    Complaint_settings_obj=Complaint_settings.objects.get(id=id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    return render(request, 'H_hotel/editcomplaintcategories.html',{'admin_permission_obj':admin_permission_obj, 'Complaint_settings_obj':Complaint_settings_obj, 'marketplace_id':marketplace_id})

def submiteditcomplaintcategories(request,id):
    client_id= request.user.id
    print("submiteditfeedbackquestions")
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    marketplace_id=request.GET.get('marketplace_id')
    if request.method =='POST':
        print("id1",id)
        Complaint_settings_obj=Complaint_settings.objects.get(id=id)
        Complaint_settings_obj.Complaint_category = request.POST.get('Edit_Complaint_Category')
        Complaint_settings_obj.save()
        if marketplace_id:
            return redirect(reverse('complaintcategories') + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('complaintcategories')

def deletecomplaintcategories(request,id):
    admin_permission_obj=admin_permission.objects.filter(client_id=request.user.id).first()
    Complaint_settings_obj=Complaint_settings.objects.get(id=id)
    Complaint_settings_obj.delete()
    marketplace_id=request.GET.get('marketplace_id')
    if marketplace_id:
            return redirect(reverse('complaintcategories') + f'?marketplace_id={marketplace_id}')
    else:
        return redirect('complaintcategories')
    
def viewcomplaints(request, id=None):
    client_id= request.user.id
    subclient_id = request.session.get('subclient_id') 
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    
    if admin_permission_obj: 
        if admin_permission_obj.client_marketplace == 'yes' :
            Hotel_marketplace_ids = Hotel_marketplace.objects.filter(client_id=client_id).values_list('id', flat=True)
            Hotels=Hotel_settings.objects.filter(client_id=client_id,marketplace_id__in=Hotel_marketplace_ids)
            print("Hotel_settings_obj",Hotels)
            if subclient_preferences:
                subclient_marketplaces = [int (x) for x in (subclient_preferences.marketplace_id).split(',')]
                print("subclient_marketplaces",subclient_marketplaces)
                Hotels=Hotel_settings.objects.filter(client_id=client_id,marketplace_id__in=subclient_marketplaces)
            if id:
                Hotel_settings_obj=Hotel_settings.objects.get(client_id=client_id,id=id)
                complaintdata = Complaint_info.objects.filter(client_id= request.user.id,Hotel_details=Hotel_settings_obj)
                return render(request, 'H_hotel/viewcomplaints.html', {'complaintdata':complaintdata, 'admin_permission_obj':admin_permission_obj,"Hotels":Hotels,"subclient_preferences":subclient_preferences})
            return render(request, 'H_hotel/viewcomplaints.html', {'admin_permission_obj':admin_permission_obj,"Hotels":Hotels,"subclient_preferences":subclient_preferences})
        else:
            Hotel_settings_obj=Hotel_settings.objects.get(client_id=client_id,marketplace__isnull=True)
            complaintdata = Complaint_info.objects.filter(client_id= request.user.id,Hotel_details=Hotel_settings_obj)
            return render(request, 'H_hotel/viewcomplaints.html', {'complaintdata':complaintdata, 'admin_permission_obj':admin_permission_obj,"subclient_preferences":subclient_preferences})
    return render(request, 'H_hotel/viewcomplaints.html', {'admin_permission_obj':admin_permission_obj,"subclient_preferences":subclient_preferences})

from .utils import plot_monthly_ratings_cusper,plot_monthly_complaint_percentage
from django.db.models.functions import ExtractYear
def Dashboard(request):
    client_id=request.user.id
    admin_permission_obj=admin_permission.objects.filter(client_id=request.user.id).first()
    print(admin_permission_obj)
    subclient_id = request.session.get('subclient_id') 
    print("subclient_id",subclient_id)
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    if request.method == 'POST':
        # Capture the selected year from the form
        selected_hotel = request.POST.get('hotel_dropdown')
        selected_year = request.POST.get('year_dropdown')
        selected_option = request.POST.get('dropdown')

    # Extract How many Years:
        years = Checkout_responses.objects.annotate(year=ExtractYear('vailo_record_creation')).values_list('year', flat=True).distinct()
        # hotel = Complaint_info.objects.exclude(Hotel_details=None).values_list('Hotel_details__hotel_name', flat=True).distinct()
        # print(hotel)
        hotel = Hotel_settings.objects.filter(client_id=request.user.id, marketplace_id__isnull = False)

# Fetch data using the selected year
        rating_data = get_monthly_ratings(year=selected_year,hotel_name=selected_hotel)
        complaint_data = get_monthly_complaints(year=selected_year,hotel_name=selected_hotel)

    # Your existing logic to generate graphs
        rating_graph = plot_monthly_ratings_base64(rating_data)
        complaint_graph = plot_monthly_complaints(complaint_data)
        customer_percentage = plot_monthly_ratings_cusper(rating_data)
        complaints_percentage = plot_monthly_complaint_percentage(complaint_data)

    # Deciding which graphs to display based on the selected option
        if selected_option == "Number":
            context = {'rating_graph': rating_graph, 'complaint_graph': complaint_graph,'years':years,'hotels':hotel,"admin_permission_obj":admin_permission_obj}
            return render(request, 'H_hotel/Dashboard.html',context)
        elif selected_option == "Percentage":
            context = {'rating_graph': customer_percentage, 'complaint_graph': complaints_percentage,'years':years,'hotels':hotel,"admin_permission_obj":admin_permission_obj}
            return render(request, 'H_hotel/Dashboard.html',context)
# Fetch data using the selected year
    rating_data = get_monthly_ratings()
    complaint_data = get_monthly_complaints()
    rating_graph = plot_monthly_ratings_base64(rating_data)
    complaint_graph = plot_monthly_complaints(complaint_data)
    #hotel = Complaint_info.objects.exclude(Hotel_details=None).values_list('Hotel_details__hotel_name', flat=True).distinct()
        # Fetch all hotel settings
    hotel = Hotel_settings.objects.filter(client_id=request.user.id, marketplace_id__isnull = False)
    print("hotel",hotel)
    # Use a dictionary to ensure uniqueness of hotel names
    years = Checkout_responses.objects.annotate(year=ExtractYear('vailo_record_creation')).values_list('year', flat=True).distinct()
    return render(request, 'H_hotel/Dashboard.html',{'years':years,'rating_graph':rating_graph,'complaint_graph':complaint_graph,'hotels':hotel,"admin_permission_obj":admin_permission_obj,"subclient_preferences":subclient_preferences})

def process(request):
    return HttpResponse("Response success")