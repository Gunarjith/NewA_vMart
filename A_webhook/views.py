import random
import re
import soundex
from cryptography.hazmat.backends import default_backend
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from vailodb_b.models import campaign_marketplace_settings, campaign_group_types, campaign_group_categorys, \
    campaign_marketplace, template_info, generic_campaign_info, campaign_customer_master, generic_campaign_history, \
    template_info_details, Inflow_Setup_Details, campaign_footprint, Form, campaign_formdata
# from vailodb_a.models import Main_settings, Consultant_settings, Availablity, Holiday_leaves, Bookings, Visitor
from vailodb_n.models import donation_details, donation_settings, donation_types, donation_marketplace, \
    donation_marketplace_settings
from vailodb_s.models import Survey_list, Survey_Question, Survey_Customer, Survey_Customer_Response, \
    Survey_marketplace_settings, Survey_marketplace

from vailodb_a.models import appointment_marketplace,appointment_settings,Consultant_details,Consultant_holiday_leaves,\
Consultant_availablity,appointment_visitor,appointment_bookings,appointment_payment_settings,appointment_payment_gateway_details,\
appointment_marketplace_settings


from A_vMart.settings import DomainName
from vailodb.models import payment_gateway_details,payment_settings
from vailodb.models import event_master, event_slots, event_ticket_category, event_settings, \
    event_ticket_cart_details, event_ticket_cart_header, ticket_information, ticket_customer_master,\
    ticket_billing_details,ticket_billing,Subclient,SubUserPreference

import base64
import PyPDF2
from django.core.files.images import ImageFile
import webbrowser
from django.views.decorators.cache import never_cache
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import time
import stripe
from django.utils import timezone
from datetime import date, timedelta
import phonenumbers
import urllib.parse
from django.shortcuts import redirect
import jinja2
from django.core.files.uploadedfile import InMemoryUploadedFile
from xhtml2pdf import pisa
from io import BytesIO

from django.utils.decorators import method_decorator
from django.views import generic
import json
import ast
import requests
import secrets
import pytz
from datetime import datetime
import uuid
import base64
from django.db import transaction
from django.db.models import Q

import json
import os
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1, hashes
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1, hashes


format = "%Y-%m-%d %H:%M:%S"

converted_tz = pytz.timezone('Asia/Kolkata')

datetime_object = str(datetime.now(converted_tz))

now = datetime_object[:len(datetime_object) - 6]

# Create your views here.
from urllib.parse import urlencode
from vailodb.models import facebook_details

from vailodb.models import admin_permission

import secrets

BotTokenGen = secrets.token_hex(21)

from datetime import datetime, date

# now = datetime.now()
from django.contrib.auth.decorators import login_required


def directcommerce(request):
    return render(request, 'directCommerce.html')


def faq(request):
    return render(request, 'faq.html')


def payinfo(request):
    return render(request,'payinfo.html')


# @never_cache
# @login_required
# def vmart(request):
#     if request.user.is_authenticated:
#         user = request.user  # Get the authenticated user
#
#         # Check if the user is a superuser (admin)
#         if user.is_superuser:
#             return render(request, 'admindash.html')
#
#         # Check if the user is authenticated as a subclient
#         if 'subclient_id' in request.session:
#             subclient_id = request.session['subclient_id']
#             subclient = Subclient.objects.filter(id=subclient_id).first()
#
#             # Check if the subclient is associated with the main client and subclient login is allowed
#             if subclient and subclient.client == user:
#                 # Use subclient details and preferences
#                 subclient_preferences = SubUserPreference.objects.filter(client=user, subclient=subclient).first()
#
#                 # if subclient_preferences and subclient_preferences.scanner:
#                 #     return render(request, 'scanner.html')
#                 # else:
#                 context = {
#                     'subclient': subclient,
#                     'subclient_preferences': subclient_preferences,
#                 }
#                 if subclient_preferences:
#                     if subclient_preferences.preference == 'donation':
#                         return render(request, 'donationDash.html', context)
#                     else:
#                         return render(request, 'ticketDash.html', context)
#
#         # If the user is a main client and not a valid subclient in session, display the main user dashboard
#         # Fetch all associated subclients
#         # subclients = Subclient.objects.filter(client=user)
#
#         # Check if the main client has admin permission
#         admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()
#         if admin_permission_obj is not None and admin_permission_obj.login_allowed:
#             serviceType = admin_permission_obj.client_service_type
#             if serviceType == "commerce":
#                 return render(request, 'vmart.html')
#             elif serviceType == "scanner":
#                 return render(request, 'scanner.html')
#             elif serviceType == "ticket":
#                 return render(request, 'ticketDash.html')
#             elif serviceType == "survey":
#                 return render(request, 'surveyDash.html')
#             elif serviceType == "donation":
#
#                 return render(request, 'donationDash.html')
#             elif serviceType == "Appointment":
#
#                 return render(request, 'appointmentDash.html')
#             elif serviceType == "B_campaign":
#
#                 return render(request, 'Bcampaign.html')
#
#             else:
#                 return HttpResponse("no sunch directory")
#         else:
#             return render(request, 'vmartHome.html')
#
#     else:
#         return render(request, 'vmartHome.html')
#

# @never_cache
# @login_required
# def vmart(request):
#     if request.user.is_authenticated:
#         user = request.user  # Get the authenticated user
#
#         # Check if the user is a superuser (admin)
#         if user.is_superuser:
#             return render(request, 'admindash.html')
#
#         # Check if the user is authenticated as a subclient
#         if 'subclient_id' in request.session:
#             subclient_id = request.session['subclient_id']
#             subclient = Subclient.objects.filter(id=subclient_id).first()
#
#             # Check if the subclient is associated with the main client and subclient login is allowed
#             if subclient and subclient.client == user:
#                 # Use subclient details and preferences
#                 subclient_preferences = SubUserPreference.objects.filter(client=user, subclient=subclient).first()
#
#                 # if subclient_preferences and subclient_preferences.scanner:
#                 #     return render(request, 'scanner.html')
#                 # else:
#                 context = {
#                     'subclient': subclient,
#                     'subclient_preferences': subclient_preferences,
#                 }
#                 if subclient_preferences:
#                     if subclient_preferences.preference == 'donation':
#                         return render(request, 'donationDash.html', context)
#                     else:
#                         return render(request, 'ticketDash.html', context)
#
#         # If the user is a main client and not a valid subclient in session, display the main user dashboard
#         # Fetch all associated subclients
#         # subclients = Subclient.objects.filter(client=user)
#
#         # Check if the main client has admin permission
#         admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()
#         if admin_permission_obj is not None and admin_permission_obj.login_allowed:
#             serviceType = admin_permission_obj.client_service_type
#             admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()
#             if serviceType == "commerce":
#                 return render(request, 'vmart.html')
#             elif serviceType == "scanner":
#                 return render(request, 'scanner.html')
#
#             elif serviceType == "survey":
#
#                 return render(request, 'surveyDash.html')
#
#             elif serviceType == "ticket":
#
#                 return render(request, 'ticketDash.html')
#             elif serviceType == "donation":
#
#                 return render(request, 'donationDash.html', {"admin_permission_obj": admin_permission_obj})
#             elif serviceType == "Appointment":
#
#                 return render(request, 'appointmentDash.html')
#             elif serviceType == "B_campaign":
#
#                 return render(request, 'Bcampaign.html')
#
#
#             else:
#                 return HttpResponse("no sunch directory")
#         else:
#             return render(request, 'vmartHome.html')
#     else:
#         return render(request, 'vmartHome.html')

def vmart(request):
    if request.user.is_authenticated:
        user = request.user  # Get the authenticated user

        # Check if the user is a superuser (admin)
        if user.is_superuser:
            return render(request, 'admindash.html')

        # Check if the user is authenticated as a subclient
        if 'subclient_id' in request.session:
            subclient_id = request.session['subclient_id']
            subclient = Subclient.objects.filter(id=subclient_id).first()
            client = subclient.client
            # Check if the subclient is associated with the main client and subclient login is allowed
            if subclient and subclient.client == user:
                # Use subclient details and preferences
                subclient_preferences = SubUserPreference.objects.filter(client=user, subclient=subclient).first()
                admin_permission_obj = admin_permission.objects.filter(client_id=client.id).first()
                serviceType = admin_permission_obj.client_service_type

                # if subclient_preferences and subclient_preferences.scanner:
                #     return render(request, 'scanner.html')
                # else:
                context = {
                    'subclient': subclient,
                    'subclient_preferences': subclient_preferences,
                }
                if subclient_preferences:
                    subclient_id = request.session['subclient_id']
                    subclient = Subclient.objects.filter(id=subclient_id).first()
                    client = subclient.client
                    admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()

                    serviceType = admin_permission_obj.client_service_type

                    if subclient_preferences.preference == 'donation':
                        return render(request, 'donationDash.html', context)
                    elif serviceType == "donation":
                        subclient_preferences = SubUserPreference.objects.filter(client=client,
                                                                                 subclient=subclient).first()
                        request.session['subclient_id'] = subclient.id
                        # admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()
                        admin_permission_obj = admin_permission.objects.filter(
                            client_id=client.id).first()  # Ensure admin_permission_obj is fetched for subclients
                        sub_user_preference = SubUserPreference.objects.get(client=client, subclient=subclient)
                        print("admin_permission_objsca", admin_permission_obj.client_marketplace)

                        context = {
                            'subclient': subclient,
                            'subclient_preferences': subclient_preferences,
                            'admin_permission_obj': admin_permission_obj,
                            'sub_user_preference': sub_user_preference,
                        }

                        if subclient_preferences and subclient_preferences.preference == 'donation':
                            return render(request, 'donationDash.html', context)
                        else:
                            return redirect('ticketDash')
                    elif serviceType == "campaign":
                        print("usersss")
                        subclient_preferences = SubUserPreference.objects.filter(client=client,
                                                                                 subclient=subclient).first()
                        print("subclient_preferences", subclient_preferences)
                        request.session['subclient_id'] = subclient.id
                        # admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()
                        admin_permission_obj = admin_permission.objects.filter(
                            client_id=client.id).first()  # Ensure admin_permission_obj is fetched for subclients
                        sub_user_preference = SubUserPreference.objects.get(client=client, subclient=subclient)
                        print("admin_permission_objsca", admin_permission_obj.client_marketplace)

                        context = {
                            'subclient': subclient,
                            'subclient_preferences': subclient_preferences,
                            'admin_permission_obj': admin_permission_obj,
                            'sub_user_preference': sub_user_preference,
                        }

                        if subclient_preferences and subclient_preferences.preference == 'campaign':
                            print('with subclient_preferences preference == "campaign"')
                            return render(request, 'Bcampaign.html', context)
                        else:
                            print('escpe')
                            return render(request, 'Bcampaign.html', context)

                    else:
                        return render(request, 'ticketDash.html', context)

        # If the user is a main client and not a valid subclient in session, display the main user dashboard
        # Fetch all associated subclients
        # subclients = Subclient.objects.filter(client=user)

        # Check if the main client has admin permission
        admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()
        if admin_permission_obj is not None and admin_permission_obj.login_allowed:
            serviceType = admin_permission_obj.client_service_type
            admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()
            if serviceType == "commerce":
                return render(request, 'vmart.html')
            elif serviceType == "scanner":
                return render(request, 'scanner.html')

            elif serviceType == "survey":

                return render(request, 'surveyDash.html', {"admin_permission_obj": admin_permission_obj})

            elif serviceType == "ticket":

                return render(request, 'ticketDash.html')
            elif serviceType == "donation":

                return render(request, 'donationDash.html', {"admin_permission_obj": admin_permission_obj})
            elif serviceType == "Appointment":

                return render(request, 'appointmentDash.html', {"admin_permission_obj": admin_permission_obj})
            elif serviceType == "campaign":

                return render(request, 'Bcampaign.html', {"admin_permission_obj": admin_permission_obj})


            else:
                return HttpResponse("no sunch directory")
        else:
            return render(request, 'vmartHome.html')
    else:
        return render(request, 'vmartHome.html')

def donation_count(request,toUser,ClientID,donate_refer_id):
    transaction_type = "Donation"
    transaction_count = 1
    Donar_name = ''
    donation_amount = 0

    today = date.today()
    print(today)
    current_month = today.strftime("%B %Y")
    ticket_billing_record = ticket_billing.objects.filter(client_id=ClientID, month=current_month).first()
    print(ticket_billing_record)
    with transaction.atomic():
        print("rrr")
        if not ticket_billing_record:
            # Create a new record in ticket_billing for the current month
            ticket_billing_record = ticket_billing.objects.create(
                client_id=ClientID,
                month=current_month,
                billed_amount=0,  # Set initial billed_amount to 0 or provide a default value
                paid_amount=0,  # Set initial paid_amount to 0 or provide a default value
                status=0,  # Set initial status or provide a default value
            )
        ticket_billing_id = ticket_billing_record.id

    updateDetailsObj = donation_details.objects.filter(donation_reference_id=donate_refer_id)
    for j in updateDetailsObj:
        Donar_name = Donar_name + j.donar_name
        donation_amount = j.donation_amount

    updateDonation = ticket_billing_details(
        client_id=ClientID,
        ticket_billing_id=ticket_billing_id,
        transaction_type=transaction_type,
        transaction_name=Donar_name,
        transaction_count=transaction_count,
        transaction_amount=donation_amount,
        date=today
    )
    updateDonation.save()







def customer_sent(request, toUser, clientId):
    # Update or create a record in the ticket billing table for sent messages
    transaction_type = "TicketMessageSent"
    transaction_name = toUser

    # Get the current date
    today = date.today()
    print(today)
    current_month = today.strftime("%B %Y")
    ticket_billing_record = ticket_billing.objects.filter(client_id=clientId, month=current_month).first()
    print(ticket_billing_record)
    ticket_billing_id = 0
    if ticket_billing_record:
        ticket_billing_id = ticket_billing_id + ticket_billing_record.id
    
    print(ticket_billing_id)


    matching_sent_records = ticket_billing_details.objects.filter(client_id=clientId, transaction_name=transaction_name, transaction_type=transaction_type)
    
    if matching_sent_records.exists():
        # Find the sent message record sent on the same day
        matching_sent_record = matching_sent_records.latest('date')
        
        if matching_sent_record.date.date() == today:
            # Update the existing record
            matching_sent_record.transaction_count += 1
            matching_sent_record.save()
        else:
            # Create a new record for the customer
            transaction_count = 1
            billing_details = ticket_billing_details(
                client_id=clientId,
                ticket_billing_id = ticket_billing_id,
                transaction_type=transaction_type,
                transaction_name=transaction_name,
                transaction_count=transaction_count,
                date=today
            )
            billing_details.save()
    else:
        # Create a new record for the customer
        transaction_count = 1
        billing_details = ticket_billing_details(
            client_id=clientId,
            ticket_billing_id = ticket_billing_id,
            transaction_type=transaction_type,
            transaction_name=transaction_name,
            transaction_count=transaction_count,
            date=today
        )
        billing_details.save()


def customer_receive(request, toUser, clientId):
    # Update or create a record in the ticket billing table
    transaction_type = "TicketMessageReceived"
    transaction_name = toUser

    # Get the current date
    today = date.today()
    print(today)
    current_month = today.strftime("%B %Y")
    ticket_billing_record = ticket_billing.objects.filter(client_id=clientId, month=current_month).first()
    print(ticket_billing_record)
    with transaction.atomic():
        print("rrr")
        if not ticket_billing_record:
            # Create a new record in ticket_billing for the current month
            ticket_billing_record = ticket_billing.objects.create(
                client_id=clientId,
                month=current_month,
                billed_amount=0,  # Set initial billed_amount to 0 or provide a default value
                paid_amount=0,  # Set initial paid_amount to 0 or provide a default value
                status=0,  # Set initial status or provide a default value
            )
        ticket_billing_id = ticket_billing_record.id
        print(ticket_billing_id)
        
    matching_records = ticket_billing_details.objects.filter(client_id=clientId, ticket_billing_id=ticket_billing_id,transaction_name=transaction_name, transaction_type=transaction_type)
    
    if matching_records.exists():
        # Find the record received on the same day
        matching_record = matching_records.latest('date')
        
        if matching_record.date.date() == today:
            # Update the existing record
            matching_record.transaction_count += 1
            matching_record.save()
        else:
            # Create a new record for the customer
            transaction_count = 1
            billing_details = ticket_billing_details(
                client_id=clientId,
                ticket_billing_id=ticket_billing_id,
                transaction_type=transaction_type,
                transaction_name=transaction_name,
                transaction_count=transaction_count,
                date=today
            )
            billing_details.save()
    else:
        # Create a new record for the customer
        transaction_count = 1
        billing_details = ticket_billing_details(
            client_id=clientId,
            ticket_billing_id=ticket_billing_id,
            transaction_type=transaction_type,
            transaction_name=transaction_name,
            transaction_count=transaction_count,
            date=today
        )
        billing_details.save()

def contact_info(request,url,headers,toUser,clientId,supportNumber):
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "preview_url": True,
        "recipient_type": "individual",
        "to": supportNumber,
        "type": "text",
        "text": {
            "body": toUser + ": is trying to contact"
        }

    })
    response = requests.request("POST", url, headers=headers, data=payload)

def paid_info(request, toUser, url, headers, supportnum, donate_refer_id,ClientID):
    print("yes cursor coming here")
    all_donationInfo = donation_details.objects.filter(client_id=ClientID,donation_reference_id=donate_refer_id)
    print(all_donationInfo)
    for a_i in all_donationInfo:
        print("t")
        dname = a_i.donation_name
        donarName = a_i.donar_name
        demail = a_i.donar_email
        dphone = a_i.donar_phone_number
        damount = str(a_i.donation_amount)
        dcomments = a_i.donation_comments_message
        status = "paid"
        print("x")
        donation_info_text = ""
        print("aa")
        donation_info_text += f"*Donar Details*\nName:{donarName}\nEmail:{demail}\nPhone:{dphone}\n\n*Donation Details*\nName: {dname}\ncomments: {dcomments}\nAmount: {damount}\nStatus: {status}\n\n"
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "preview_url": True,
            "recipient_type": "individual",
            "to": supportnum,
            "type": "text",
            "text": {
                "body": donation_info_text  # Include the formatted donation information here
            }
        })
        response = requests.request("POST", url, headers=headers, data=payload)


def pdf_display(request,donate_refer_id):
    print("wait padf coming")
    donationPaymentCheck = donation_details.objects.filter(donation_reference_id=donate_refer_id)
    print(donationPaymentCheck)
    toUser = ''
    ClientID = 0
    fbToken = ''
    fbPhoneId = ''
    payment_status = 0
    receipient_pdf = ''
    outputfilename = ''
    for pc_i in donationPaymentCheck:
        print("checking")
        toUser = pc_i.donar_phone_number
        ClientID = pc_i.client_id
        payment_status = pc_i.payment_status
        receipient_pdf = pc_i.receipient_pdf

        facebookDetails = facebook_details.objects.filter(client_id=ClientID)
        fbToken = ''
        fbPhoneId = ''
        for fb_i in facebookDetails:
            print("ddcheck")
            fbPhoneId = fb_i.fb_phone_number_id
            fbToken = fb_i.fb_access_token
    filename = receipient_pdf.name
    outputfilename = filename[9:]

    if payment_status == 1:
        print("payment success")
        donation_count(request, toUser, ClientID, donate_refer_id)
        conformMesaage = donation_settings.objects.filter(client_id=ClientID)
        supportnum = ''
        donationConform = ''
        for cm_i in conformMesaage:
            donationConform = donationConform + cm_i.donation_conform_message
            supportnum = cm_i.support_number


        url = "https://graph.facebook.com/v12.0/" + str(fbPhoneId) + "/messages"
        headers = {
            'Authorization': 'Bearer ' + fbToken,
            'Content-Type': 'application/json'
        }
        paid_info(request, toUser, url, headers, supportnum, donate_refer_id,ClientID)
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "text",
            "text": {
                "body": donationConform if donationConform else "."
            }
        })

        response = requests.request("POST", url, headers=headers, data=payload)
        # paid_info(request, toUser, url, headers, supportnum, donate_refer_id)
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "document",
            "document": {
                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
                    receipient_pdf),
                "filename": outputfilename

            }

        })

        response = requests.request("POST", url, headers=headers, data=payload)


def N3(request, donar_refId, dclientID):
    print('coming to N3')
    detailsObject = donation_details.objects.filter(client_id=dclientID,donation_reference_id=donar_refId)
    donationAmount = 0
    for j_i in detailsObject:
        donationAmount = j_i.donation_amount

    facebookDetails = facebook_details.objects.filter(client_id=dclientID)
    clientNumber = ''
    for f_i in facebookDetails:
        clientNumber = f_i.fb_whatsapp_number

    url = "https://api.razorpay.com/v1/payment_links"

    payload = json.dumps({
        "amount": donationAmount * 100,
        "currency": "INR",
        "accept_partial": False,
        "first_min_partial_amount": 0,
        "reference_id": "N" + str(donar_refId),
        "description": "Donation",
        "customer": {
            "name": "Gaurav Kumar",
            "contact": "918494863493",
            "email": "gaurav.kumar@example.com"
        },
        "notify": {
            "sms": True,
            "email": True
        },
        "reminder_enable": True,
        "notes": {
            "polacy_name": "N" + str(donar_refId)
        },
        "callback_url": f"https://wa.me/{clientNumber}",
        "callback_method": "get"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic cnpwX2xpdmVfSU83R0Vyckkyam9RYXQ6aGt2SVhTZkpvM0x2TWhYaGx5VUpoWTBH'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    a = response.text
    json_str = json.dumps(a)
    b = json.loads(json_str)
    c = response.json()
    print(c)
    payment_link = c['short_url']
    print(payment_link)
    dynamic_link = payment_link[17:]

    return JsonResponse({'success':True,'PaymentLink':dynamic_link})





def process_donation_text_message(message, request,url, headers, toUser, clientId):
    if message == 'HI' or message == 'Hi' or message == 'hi' or message == 'hI':
        # if not donation_details.objects.filter(client_id=clientId, donar_phone_number=toUser).exists():
        #     new_customer = donation_details(client_id=clientId, donar_phone_number=toUser)
        #     new_customer.save()
        # else:
        #     print("phone number already exist")

        welcomeobj = donation_settings.objects.filter(client_id=clientId)

        for don_i in welcomeobj:
            if don_i.donation_image:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                (don_i.donation_image)
                            }
                        },

                        "body": {
                            "text": don_i.donation_description if don_i.donation_description else "."
                        },
                        "footer": {
                            "text": don_i.donation_footer
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "I1",
                                        "title": don_i.donation_now_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "I2",
                                        "title": don_i.my_donation_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "I3",
                                        "title": don_i.contact_us_button_name
                                    }
                                },

                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": don_i.donation_description if don_i.donation_description else "."
                        },
                        "footer": {
                            "text": don_i.donation_footer
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "I1",
                                        "title": don_i.donation_now_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "I2",
                                        "title": don_i.my_donation_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "I3",
                                        "title": don_i.contact_us_button_name
                                    }
                                },
                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
    else:
        print('hello')

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "preview_url": True,
            "recipient_type": "individual",
            "to": toUser,
            "type": "text",
            "text": {
                "body": "Please send *Hi* to proceed"
            }

        })
        response = requests.request("POST", url, headers=headers, data=payload)


def process_donation_interactive_message(response_id, request,url, headers, toUser, clientId,whatsAppPhoneNumberId,faceBookToken):
    response_id_type = response_id[0]
    response_id_id = int(response_id[1:])
    print(response_id_type)
    print(response_id_id)

    if response_id_type == 'D':
        print('f')
        response_d_id_id = int(response_id[1])
        if response_d_id_id == 1:
            print('g')
            ngo_id = int(response_id[2:])
            bookinginfoobj = donation_settings.objects.filter(client_id=clientId,marketplace_id=ngo_id)
            print(bookinginfoobj)
            for bd_i in bookinginfoobj:
                donation_name = []
                donation_desc = []
                donation_id = []
                listdonation = donation_types.objects.filter(client_id=clientId,marketplace_id=ngo_id)
                for list_i in listdonation:
                    print(list_i.id)
                    donation_id.append(list_i.id)
                    donation_desc.append(list_i.donation_short_description)
                    donation_name.append(list_i.donation_name)
                print(donation_name)
                donationlist = []
                for i in range(len(donation_name)):
                    donationlist.append({"id": "M" + str(donation_id[i]),
                                         "title": donation_name[i],
                                         "description": donation_desc[i]
                                         })
                if len(donation_name) == 1:
                    payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "button",

                                    "body": {
                                        "text": bd_i.donation_list_body if bd_i.donation_list_body else "."
                                    },
                                    "footer": {
                                        "text": bd_i.donation_list_footer
                                    },
                                    "action": {
                                        "buttons": [
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "M" + str(donation_id[0]),
                                                    "title": list_i.donation_name
                                                }
                                            }

                                        ]
                                    }
                                }
                            })

                    response = requests.request("POST", url, headers=headers, data=payload)

                    print("welcome")
                else:
                    print('else')
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "list",
                            "header": {
                                "type": "text",
                                "text": bd_i.donation_list_header if bd_i.donation_list_header else "."
                            },
                            "body": {
                                "text": bd_i.donation_list_body if bd_i.donation_list_body else "."
                            },
                            "footer": {
                                "text": bd_i.donation_list_footer
                            },
                            "action": {
                                "button": bd_i.donation_list_button_name,
                                "sections": [
                                    {
                                        "title": "Events",
                                        "rows": donationlist
                                    }

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)

        elif response_d_id_id == 2:
            payload = json.dumps({

                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "interactive",
                "interactive": {
                    "type": "button",

                    "body": {
                        "text": 'Please Choose an option'
                    },

                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "Y1",
                                    "title": "Last 5 Donations"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "O2",
                                    "title": "Month Donations"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "K3",
                                    "title": "My All Donations"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)






            # mydonation_list = list(mydonation)
            # for index, my_i in enumerate(mydonation_list, start=1):
            #     donarName = my_i.donar_name
            #     donationName = my_i.donation_name
            #     donationAmount = str(my_i.donation_amount)  # Convert to string
            #     donationDescription = my_i.donation_description
            #     donationDate = my_i.donation_date
            #     comments = my_i.donation_comments_message
            #     paidStatus = 'paid' if my_i.payment_status == 1 else 'notpaid'
            #     bookinginfomobj = donation_settings.objects.filter(client_id=clientId)
            #     for b_i in bookinginfomobj:
            #         payload = {
            #             "messaging_product": "whatsapp",
            #             "recipient_type": "individual",
            #             "to": toUser,
            #             "type": "interactive",
            #             "interactive": {
            #                 "type": "button",
            #                 "body": {
            #                     "text": f' *Donation Details* (ID: {index}) :\n\n'
            #                             f'  DonarName: {donarName}\n\n'
            #                             f' DonationName: {donationName}\n\n'
            #                             f' DonationAmount: {donationAmount}\n\n'
            #                             f' DonationDescription: {donationDescription}\n\n'
            #                             f' DonationDate: {donationDate}\n\n'
            #                             f' Comments: {comments}\n\n'
            #                             f' Paid: {paidStatus}'
            #                 },
            #                 "action": {
            #                     "buttons": [
            #                         {
            #                             "type": "reply",
            #                             "reply": {
            #                                 "id": "R1",
            #                                 "title": b_i.my_donation_details_button_name1
            #                             }
            #                         },
            #                         {
            #                             "type": "reply",
            #                             "reply": {
            #                                 "id": "J1",
            #                                 "title": b_i.my_donation_details_button_name2
            #                             }
            #                         },
            #                         {
            #                             "type": "reply",
            #                             "reply": {
            #                                 "id": "Z1",
            #                                 "title": b_i.my_donation_details_button_name3
            #                             }
            #                         }
            #                     ]
            #                 }
            #             }
            #         }
            #
            #         payload_json = json.dumps(payload)
            #         response = requests.request("POST", url, headers=headers, data=payload_json)
            #
            #

            # for my_i in mydonation_list:
            #     donarName =  my_i.donar_name
            #     donationName = donationName + my_i.donation_name
            #     donationAmount = my_i.donation_amount
            #     donationDescription = donationDescription + my_i.donation_description
            #     donationDate = my_i.donation_date
            #     comments = comments + my_i.donation_comments_message
            #     # paidcheck = 0
            #     paidStatus = ''
            #     paidcheck = my_i.payment_status
            #     if paidcheck == 1:
            #         paidStatus = 'paid'
            #     else:
            #         paidStatus = 'notpaid'
            #
            # bookinginfomobj = donation_settings.objects.filter(client_id=clientId)
            #
            # for b_i in bookinginfomobj:
            #     payload = json.dumps({
            #
            #         "messaging_product": "whatsapp",
            #         "recipient_type": "individual",
            #         "to": toUser,
            #         "type": "interactive",
            #         "interactive": {
            #             "type": "button",
            #
            #             "body": {
            #                 "text": ' *Donation Details* :\n\n' + "  DonarName :" + donarName + '\n\n' + " DonationName : " + donationName + '\n\n' + "DonationAmount:" + donationAmount + '\n\n' + "DonationDescription :" + donationDescription + '\n\n' + 'DonationDate :' + donationDate + '\n\n' + "comments:" + comments + '\n\n' + "Paid" + paidStatus
            #
            #             },
            #
            #             "action": {
            #                 "buttons": [
            #                     {
            #                         "type": "reply",
            #                         "reply": {
            #                             "id": "R",
            #                             "title": b_i.my_donation_details_button_name1
            #                         }
            #                     },
            #                     {
            #                         "type": "reply",
            #                         "reply": {
            #                             "id": "J",
            #                             "title": b_i.my_donation_details_button_name2
            #                         }
            #                     },
            #                     {
            #                         "type": "reply",
            #                         "reply": {
            #                             "id": "Z",
            #                             "title": b_i.my_donation_details_button_name3
            #                         }
            #                     }
            #
            #                 ]
            #             }
            #         }
            #     })
            #
            #     response = requests.request("POST", url, headers=headers, data=payload)
        elif response_d_id_id == 3:
            numberObjectdet = donation_settings.objects.filter(client_id=clientId)
            supportNumber = ''
            for n_i in numberObjectdet:
                supportNumber = n_i.support_number
            contact_info(request, url, headers, toUser, clientId, supportNumber)
            bookingmoreinfoobj = donation_settings.objects.filter(client_id=clientId)
            for m_i in bookingmoreinfoobj:
                if m_i.donation_contact_us_image:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "button",
                            "header": {
                                "type": "image",
                                "image": {
                                    "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                    (m_i.donation_contact_us_image)
                                }
                            },

                            "body": {
                                "text": m_i.donation_contact_us_message if m_i.donation_contact_us_message else "."
                            },
                            "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "C1",
                                            "title": m_i.contact_us_details_button_name
                                        }
                                    }

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)

                else:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "button",
                            "body": {
                                "text": m_i.donation_contact_us_message if m_i.donation_contact_us_message else "."
                            },
                            "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "C1",
                                            "title": m_i.contact_us_details_button_name
                                        }
                                    },

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'I':
        print('f')
        # response_d_id_id = int(response_id[1])
        if response_id_id == 1:
            print('g')
            # ngo_id = int(response_id[2:])
            bookinginfoobj = donation_settings.objects.filter(client_id=clientId)
            print(bookinginfoobj)
            for bd_i in bookinginfoobj:
                donation_name = []
                donation_desc = []
                donation_id = []
                listdonation = donation_types.objects.filter(client_id=clientId)
                for list_i in listdonation:
                    print(list_i.id)
                    donation_id.append(list_i.id)
                    donation_desc.append(list_i.donation_short_description)
                    donation_name.append(list_i.donation_name)
                print(donation_name)
                donationlist = []
                for i in range(len(donation_name)):
                    donationlist.append({"id": "M" + str(donation_id[i]),
                                         "title": donation_name[i],
                                         "description": donation_desc[i]
                                         })
                if len(donation_name) == 1:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "button",

                            "body": {
                                "text": bd_i.donation_list_body if bd_i.donation_list_body else "."
                            },
                            "footer": {
                                "text": bd_i.donation_list_footer
                            },
                            "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "M" + str(donation_id[0]),
                                            "title": list_i.donation_name
                                        }
                                    }

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)

                    print("welcome")
                else:
                    print('else')
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "list",
                            "header": {
                                "type": "text",
                                "text": bd_i.donation_list_header if bd_i.donation_list_header else "."
                            },
                            "body": {
                                "text": bd_i.donation_list_body if bd_i.donation_list_body else "."
                            },
                            "footer": {
                                "text": bd_i.donation_list_footer
                            },
                            "action": {
                                "button": bd_i.donation_list_button_name,
                                "sections": [
                                    {
                                        "title": "Events",
                                        "rows": donationlist
                                    }

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)

        elif response_id_id == 2:
            payload = json.dumps({

                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "interactive",
                "interactive": {
                    "type": "button",

                    "body": {
                        "text": 'Please Choose an option'
                    },

                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "Y1",
                                    "title": "Last 5 Donations"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "O2",
                                    "title": "Last MonthDonations"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "K3",
                                    "title": "My All Donations"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)

            # mydonation_list = list(mydonation)
            # for index, my_i in enumerate(mydonation_list, start=1):
            #     donarName = my_i.donar_name
            #     donationName = my_i.donation_name
            #     donationAmount = str(my_i.donation_amount)  # Convert to string
            #     donationDescription = my_i.donation_description
            #     donationDate = my_i.donation_date
            #     comments = my_i.donation_comments_message
            #     paidStatus = 'paid' if my_i.payment_status == 1 else 'notpaid'
            #     bookinginfomobj = donation_settings.objects.filter(client_id=clientId)
            #     for b_i in bookinginfomobj:
            #         payload = {
            #             "messaging_product": "whatsapp",
            #             "recipient_type": "individual",
            #             "to": toUser,
            #             "type": "interactive",
            #             "interactive": {
            #                 "type": "button",
            #                 "body": {
            #                     "text": f' *Donation Details* (ID: {index}) :\n\n'
            #                             f'  DonarName: {donarName}\n\n'
            #                             f' DonationName: {donationName}\n\n'
            #                             f' DonationAmount: {donationAmount}\n\n'
            #                             f' DonationDescription: {donationDescription}\n\n'
            #                             f' DonationDate: {donationDate}\n\n'
            #                             f' Comments: {comments}\n\n'
            #                             f' Paid: {paidStatus}'
            #                 },
            #                 "action": {
            #                     "buttons": [
            #                         {
            #                             "type": "reply",
            #                             "reply": {
            #                                 "id": "R1",
            #                                 "title": b_i.my_donation_details_button_name1
            #                             }
            #                         },
            #                         {
            #                             "type": "reply",
            #                             "reply": {
            #                                 "id": "J1",
            #                                 "title": b_i.my_donation_details_button_name2
            #                             }
            #                         },
            #                         {
            #                             "type": "reply",
            #                             "reply": {
            #                                 "id": "Z1",
            #                                 "title": b_i.my_donation_details_button_name3
            #                             }
            #                         }
            #                     ]
            #                 }
            #             }
            #         }
            #
            #         payload_json = json.dumps(payload)
            #         response = requests.request("POST", url, headers=headers, data=payload_json)
            #
            #

            # for my_i in mydonation_list:
            #     donarName =  my_i.donar_name
            #     donationName = donationName + my_i.donation_name
            #     donationAmount = my_i.donation_amount
            #     donationDescription = donationDescription + my_i.donation_description
            #     donationDate = my_i.donation_date
            #     comments = comments + my_i.donation_comments_message
            #     # paidcheck = 0
            #     paidStatus = ''
            #     paidcheck = my_i.payment_status
            #     if paidcheck == 1:
            #         paidStatus = 'paid'
            #     else:
            #         paidStatus = 'notpaid'
            #
            # bookinginfomobj = donation_settings.objects.filter(client_id=clientId)
            #
            # for b_i in bookinginfomobj:
            #     payload = json.dumps({
            #
            #         "messaging_product": "whatsapp",
            #         "recipient_type": "individual",
            #         "to": toUser,
            #         "type": "interactive",
            #         "interactive": {
            #             "type": "button",
            #
            #             "body": {
            #                 "text": ' *Donation Details* :\n\n' + "  DonarName :" + donarName + '\n\n' + " DonationName : " + donationName + '\n\n' + "DonationAmount:" + donationAmount + '\n\n' + "DonationDescription :" + donationDescription + '\n\n' + 'DonationDate :' + donationDate + '\n\n' + "comments:" + comments + '\n\n' + "Paid" + paidStatus
            #
            #             },
            #
            #             "action": {
            #                 "buttons": [
            #                     {
            #                         "type": "reply",
            #                         "reply": {
            #                             "id": "R",
            #                             "title": b_i.my_donation_details_button_name1
            #                         }
            #                     },
            #                     {
            #                         "type": "reply",
            #                         "reply": {
            #                             "id": "J",
            #                             "title": b_i.my_donation_details_button_name2
            #                         }
            #                     },
            #                     {
            #                         "type": "reply",
            #                         "reply": {
            #                             "id": "Z",
            #                             "title": b_i.my_donation_details_button_name3
            #                         }
            #                     }
            #
            #                 ]
            #             }
            #         }
            #     })
            #
            #     response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 3:
            numberObjectdet = donation_settings.objects.filter(client_id=clientId)
            supportNumber = ''
            for n_i in numberObjectdet:
                supportNumber = n_i.support_number
            contact_info(request, url, headers, toUser, clientId, supportNumber)
            bookingmoreinfoobj = donation_settings.objects.filter(client_id=clientId)
            for m_i in bookingmoreinfoobj:
                if m_i.donation_contact_us_image:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "button",
                            "header": {
                                "type": "image",
                                "image": {
                                    "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                    (m_i.donation_contact_us_image)
                                }
                            },

                            "body": {
                                "text": m_i.donation_contact_us_message if m_i.donation_contact_us_message else "."
                            },
                            "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "C1",
                                            "title": m_i.contact_us_details_button_name
                                        }
                                    }

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)

                else:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "button",
                            "body": {
                                "text": m_i.donation_contact_us_message if m_i.donation_contact_us_message else "."
                            },
                            "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "C1",
                                            "title": m_i.contact_us_details_button_name
                                        }
                                    },

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)


    elif response_id_type == 'M':
        print(response_id_id)
        # response_id_id_id = int(response_id[1:])
        # donation_ref_id = uuid.uuid4()
        # donation_details.objects.create(client_id=clientId,donation_reference_id=donation_ref_id,donar_phone_number=toUser)

        # detailslink = "https://vmart.ai" + "/N1/" + "N1" + str(donation_ref_id) + str(response_id_id) + '/' + str(clientId)
        donationTypeobj = donation_types.objects.filter(client_id=clientId,id=response_id_id)
        for dh_i in donationTypeobj:
            if dh_i .donation_type_image:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                (dh_i .donation_type_image)
                            }
                        },

                        "body": {
                            "text": dh_i.donation_description if dh_i.donation_description else "."
                        },

                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "N" + str(response_id_id),
                                        "title": "Proceed"
                                    }
                                }


                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",

                        "body": {
                            "text": dh_i.donation_description if dh_i.donation_description else "."
                        },
                        "footer": {
                            "text": dh_i.donation_short_description
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "N" + str(response_id_id),
                                        "title": "Proceed"
                                    }
                                }

                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)



        # detailslink='home/'
        # detailslink = "https://vmart.ai" + "/T/" + str(response_id_id) + "T" + refer_id + '/' + str(clientId)
        # payload = json.dumps({
        #     "messaging_product": "whatsapp",
        #     "to": toUser,
        #     "text": {
        #         # "preview_url": True,
        #         "body": 'Please provide the contact details through this link :' + detailslink
        #      }
        #   })
        # response = requests.request("POST", url, headers=headers, data=payload)
        # url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
        # headers = {
        #     'Authorization': 'Bearer ' + faceBookToken,
        #     'Content-Type': 'application/json'
        # }
    elif response_id_type == "N":

        print(response_id_id)
        # response_n_id = response_id[1:]
        print("please wait downloading")
        donation_ref_id = uuid.uuid4()
        donation_details.objects.create(client_id=clientId, donation_reference_id=donation_ref_id,
                                        donar_phone_number=toUser)
        donation_detailsobj = donation_types.objects.filter(client_id=clientId, id=response_id_id)
        donation_Amount = 0
        donation_Name = ''
        for f_i in donation_detailsobj:
            donation_Amount = f_i.donation_amount
            donation_Name = f_i.donation_name
        if donation_Amount == 0:
            url = "https://graph.facebook.com/v18.0/154279547761501/messages"

            payload = json.dumps({
                "messaging_product": "whatsapp",
                "to": toUser,
                "recipient_type": "individual",
                "type": "interactive",
                "interactive": {
                    "type": "flow",
                    # "header": {
                    #     "type": "image",
                    #     "image": {
                    #         "link": "https://images.moneycontrol.com/static-mcnews/2021/10/donation.jpg?impolicy=website&width=770&height=431"
                    #     }
                    # },
                    "body": {
                        "text": "Thank you for donating us. Please provide your details."
                    },
                    # "footer": {
                    #     "text": "Submit Details"
                    # },
                    "action": {
                        "name": "flow",
                        "parameters": {
                            "flow_message_version": "3",
                            "flow_action": "navigate",
                            "flow_token": str(response_id_id) + "/" + str(donation_ref_id) + "/" + str(
                                whatsAppPhoneNumberId),
                            "flow_id": "645744577509909",
                            "flow_cta": "Submit Details",
                            "flow_action_payload":{
                                "screen": "SIGN_UP",
                                "data": {
                                    "id": "0",
                                    "title": "Yes"
                                }

                            }
                        }
                    }
                }
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer EAAKvTUOoeAMBOzwpF7TIIZBDxWSsYB6qbSa05unZB8BhifHZCfWw1i9NUUikZAtHhZC6tFJYIlN4nTE5r05JGz8MTVz8kxfgG7eUUC83cat3FYmlIOSbMFMZBRzzHhv40qckIjZBixKGEUvfbW6giVMQTNTda3tuZA3NEcAjO6e4NSanGJAJC15CfqBWlwfArt70'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print("s done")
            print(response.text)
        else:
            url = "https://graph.facebook.com/v18.0/154279547761501/messages"

            payload = json.dumps({
                "messaging_product": "whatsapp",
                "to": toUser,
                "recipient_type": "individual",
                "type": "interactive",
                "interactive": {
                    "type": "flow",
                    # "header": {
                    #     "type": "image",
                    #     "image": {
                    #         "link": "https://images.moneycontrol.com/static-mcnews/2021/10/donation.jpg?impolicy=website&width=770&height=431"
                    #     }
                    # },
                    "body": {
                        "text": "Thank you for donating us. Please provide your details."
                    },
                    # "footer": {
                    #     "text": "Submit Details"
                    # },
                    "action": {
                        "name": "flow",
                        "parameters": {
                            "flow_message_version": "3",
                            "flow_action": "data_exchange",
                            "flow_token": str(response_id_id) + "/" + str(donation_ref_id) + "/" + str(
                                whatsAppPhoneNumberId),
                            "flow_id": "374367468320931",
                            "flow_cta": "Submit Details",

                        }
                    }
                }
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer EAAKvTUOoeAMBOzwpF7TIIZBDxWSsYB6qbSa05unZB8BhifHZCfWw1i9NUUikZAtHhZC6tFJYIlN4nTE5r05JGz8MTVz8kxfgG7eUUC83cat3FYmlIOSbMFMZBRzzHhv40qckIjZBixKGEUvfbW6giVMQTNTda3tuZA3NEcAjO6e4NSanGJAJC15CfqBWlwfArt70'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print("s done")
            print(response.text)

        # infolinks = "N1/" + "N1" + str(donation_ref_id) + str(response_id_id) + '/' + str(clientId)
        # print("completed")
        # url = "https://graph.facebook.com/v15.0/" + str(whatsAppPhoneNumberId) + "/messages"
        # headers = {
        #     'Authorization': 'Bearer ' + faceBookToken,
        #     'Content-Type': 'application/json'
        # }
        # payload = json.dumps({
        #     "messaging_product": "whatsapp",
        #     "recipient_type": "individual",
        #     "to": toUser,
        #     "type": "template",
        #     "template": {
        #         "name": "vailo_info_page_mktg",
        #         "language": {
        #             "code": "en_US"
        #         },
        #         "components": [
        #             {
        #                 "type": "body",
        #                 "parameters": []
        #             },
        #             {
        #                 "type": "button",
        #                 "sub_type": "url",
        #                 "index": "0",
        #                 "parameters": [
        #                     {
        #                         "type": "text",
        #                         "text": infolinks
        #                     }
        #                 ]
        #             }
        #         ]
        #     }
        # })
        # response = requests.request("POST", url, headers=headers, data=payload)
        # payload = json.dumps({
        #     "messaging_product": "whatsapp",
        #     "recipient_type": "individual",
        #     "to": toUser,
        #     "type": "template",
        #     "template": {
        #         "name": "vmart_info_page",
        #         "language": {
        #             "code": "en_US"
        #         },
        #         "components": [
        #             {
        #                 "type": "body",
        #                 "parameters": []
        #             },
        #             {
        #                 "type": "button",
        #                 "sub_type": "url",
        #                 "index": "0",
        #                 "parameters": [
        #                     {
        #                         "type": "text",
        #                         "text": infolinks
        #                     }
        #                 ]
        #             }
        #         ]
        #     }
        # })
        # response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == "R":

        mydonationPdf = donation_details.objects.filter(client_id=clientId,id=response_id_id)
        print(mydonationPdf)
        for p_i in mydonationPdf:
            filepath = p_i.receipient_pdf
            print(filepath)
            File = filepath.name	
            file_name = File[9:]
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "document",
                "document": {
                    "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
                        p_i.receipient_pdf),
                    "filename": file_name

                }

            })

            response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == "J":
        welcomeobj = donation_settings.objects.filter(client_id=clientId)

        for don_i in welcomeobj:
            if don_i.donation_image:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                (don_i.donation_image)
                            }
                        },

                        "body": {
                            "text": don_i.donation_description if don_i.donation_description else "."
                        },
                        "footer": {
                            "text": don_i.donation_footer
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D1",
                                        "title": don_i.donation_now_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D2",
                                        "title": don_i.my_donation_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D3",
                                        "title": don_i.contact_us_button_name
                                    }
                                },

                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": don_i.donation_description if don_i.donation_description else "."
                        },
                        "footer": {
                            "text": don_i.donation_footer
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D1",
                                        "title": don_i.donation_now_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D2",
                                        "title": don_i.my_donation_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D3",
                                        "title": don_i.contact_us_button_name
                                    }
                                },
                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == "Z":
        numberObjectData = donation_settings.objects.filter(client_id=clientId)
        supportNumber = ''
        for n_i in numberObjectData:
            supportNumber = n_i.support_number
        contact_info(request, url, headers, toUser, clientId, supportNumber)
        bookingmoreinfoobj = donation_settings.objects.filter(client_id=clientId)
        for m_i in bookingmoreinfoobj:
            if m_i.donation_contact_us_image:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                (m_i.donation_contact_us_image)
                            }
                        },

                        "body": {
                            "text": m_i.donation_contact_us_message if m_i.donation_contact_us_message else "."
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "C1",
                                        "title": m_i.contact_us_details_button_name
                                    }
                                }

                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)

            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": m_i.donation_contact_us_message if m_i.donation_contact_us_message else "."
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "C1",
                                        "title": m_i.contact_us_details_button_name
                                    }
                                },


                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == "C":
        # numberObject = donation_settings.objects.filter(client_id=clientId)
        # supportNumber = ''
        # for n_i in numberObject:
        #     supportNumber = n_i.support_number
        # contact_info(request,url,headers,toUser,clientId,supportNumber)

        welcomeobj = donation_settings.objects.filter(client_id=clientId)

        for don_i in welcomeobj:
            if don_i.donation_image:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                (don_i.donation_image)
                            }
                        },

                        "body": {
                            "text": don_i.donation_description if don_i.donation_description else "."
                        },
                        "footer": {
                            "text": don_i.donation_footer
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D1",
                                        "title": don_i.donation_now_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D2",
                                        "title": don_i.my_donation_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D3",
                                        "title": don_i.contact_us_button_name
                                    }
                                },

                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": don_i.donation_description if don_i.donation_description else "."
                        },
                        "footer": {
                            "text": don_i.donation_footer
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D1",
                                        "title": don_i.donation_now_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D2",
                                        "title": don_i.my_donation_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D3",
                                        "title": don_i.contact_us_button_name
                                    }
                                },
                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'P':
        print("pay again section")
        new_ref_id = uuid.uuid4()
        print(new_ref_id)
        payLinkObj = donation_details.objects.filter(id=response_id_id)
        for pl_i in payLinkObj:
            pl_i.donation_reference_id = new_ref_id
            pl_i.save()





        # clientUnique = 0
        # donationAmount = 0
        # for pl_i in payLinkObj:
        #     donationAmount = pl_i.donation_amount
        #     clientUnique = pl_i.client_id
        #
        # fbdata = facebook_details.objects.filter(client_id=clientUnique)
        # clientNumber = ''
        # for f_i in fbdata:
        #     clientNumber = f_i.fb_whatsapp_number
        infolink = "N2/" + "P2" + str(new_ref_id) + '/' + str(clientId)
        url = "https://graph.facebook.com/v15.0/" + str(whatsAppPhoneNumberId) + "/messages"
        headers = {
            'Authorization': 'Bearer ' + faceBookToken,
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "template",
            "template": {
                "name": "vmart_info_page",
                "language": {
                    "code": "en_US"
                },
                "components": [
                    {
                        "type": "body",
                        "parameters": []
                    },
                    {
                        "type": "button",
                        "sub_type": "url",
                        "index": "0",
                        "parameters": [
                            {
                                "type": "text",
                                "text": infolink
                            }
                        ]
                    }
                ]
            }
        })
        response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'K':
        mydonation = donation_details.objects.filter(donar_phone_number=toUser)
        print(mydonation)
        if mydonation:
            for m_i in mydonation:
                detailsobj = donation_details.objects.filter(id=m_i.id)
                for f in detailsobj:
                    ldate = f.vailo_record_creation
                    fdate = f.vailo_record_last_update
                    print(ldate)
                    print(fdate)
                    payReferId = f.donation_reference_id
                    donarName = f.donar_name
                    donationName = f.donation_name
                    doemail = f.donar_email
                    dophone = f.donar_phone_number
                    donationAmount = str(f.donation_amount)
                    donationDescription = f.donation_comments_message
                    paidStatus = 'paid' if f.payment_status == 1 else 'notpaid'
                    if paidStatus == 'paid':
                        print(paidStatus)
                        bookinginfomobj = donation_settings.objects.filter(client_id=clientId)
                        for b_i in bookinginfomobj:
                            print("ww")
                            payload = json.dumps({

                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "button",

                                    "body": {
                                        "text": f'*Donor Details* :\n'
                                                f' Name: {donarName}\n'
                                                f' Email: {doemail}\n'
                                                f' Phone: {dophone}\n\n'
                                                f'*Donation Details* :\n'
                                                f' Name: {donationName}\n'
                                                f' Amount: {donationAmount}\n'
                                                f' Comments: {donationDescription}\n'
                                                f' PaymentStatus: {paidStatus}'
                                    },

                                    "action": {
                                        "buttons": [
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "R" + str(m_i.id),
                                                    "title": b_i.my_donation_details_button_name1
                                                }
                                            },
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "J1",
                                                    "title": b_i.my_donation_details_button_name2
                                                }
                                            },
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "Z1",
                                                    "title": b_i.my_donation_details_button_name3
                                                }
                                            }

                                        ]
                                    }
                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)
                    else:
                        print(paidStatus)
                        bookinginfomobj = donation_settings.objects.filter(client_id=clientId)
                        for b_i in bookinginfomobj:
                            print("ww")
                            payload = json.dumps({

                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "button",

                                    "body": {
                                        "text": f'*Donor Details* :\n'
                                                f' Name: {donarName}\n'
                                                f' Email: {doemail}\n'
                                                f' Phone: {dophone}\n\n'
                                                f'*Donation Details* :\n'
                                                f' Name: {donationName}\n'
                                                f' Amount: {donationAmount}\n'
                                                f' Comments: {donationDescription}\n'
                                                f' PaymentStatus: {paidStatus}'
                                    },

                                    "action": {
                                        "buttons": [
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "P" + str(m_i.id),
                                                    "title": "Pay Now"
                                                }
                                            },
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "J1",
                                                    "title": b_i.my_donation_details_button_name2
                                                }
                                            },
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "Z1",
                                                    "title": b_i.my_donation_details_button_name3
                                                }
                                            }

                                        ]
                                    }
                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'Y':
        mydonation = donation_details.objects.filter(donar_phone_number=toUser).order_by('-donation_date', '-vailo_record_creation')[:5]
        print(mydonation)
        if mydonation:
            for m_i in mydonation:
                detailsobj = donation_details.objects.filter(id=m_i.id)
                print("sneha")
                print(detailsobj)
                for f in detailsobj:
                    ldate = f.vailo_record_creation
                    fdate = f.vailo_record_last_update
                    print(ldate)
                    print(fdate)
                    payReferId = f.donation_reference_id
                    donarName = f.donar_name
                    print("gfv")
                    print(donarName)
                    donationName = f.donation_name
                    doemail = f.donar_email
                    dophone = f.donar_phone_number
                    donationAmount = str(f.donation_amount)
                    donationDescription = f.donation_comments_message
                    paidStatus = 'paid' if f.payment_status == 1 else 'notpaid'
                    if paidStatus == 'paid':
                        print(paidStatus)
                        bookinginfomobj = donation_settings.objects.filter(client_id=clientId)
                        for b_i in bookinginfomobj:
                            print("ww")
                            payload = json.dumps({

                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "button",

                                    "body": {
                                        "text": f'*Donor Details* :\n'
                                                f' Name: {donarName}\n'
                                                f' Email: {doemail}\n'
                                                f' Phone: {dophone}\n\n'
                                                f'*Donation Details* :\n'
                                                f' Name: {donationName}\n'
                                                f' Amount: {donationAmount}\n'
                                                f' Comments: {donationDescription}\n'
                                                f' PaymentStatus: {paidStatus}'
                                    },

                                    "action": {
                                        "buttons": [
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "R" + str(m_i.id),
                                                    "title": b_i.my_donation_details_button_name1
                                                }
                                            },
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "J1",
                                                    "title": b_i.my_donation_details_button_name2
                                                }
                                            },
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "Z1",
                                                    "title": b_i.my_donation_details_button_name3
                                                }
                                            }

                                        ]
                                    }
                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)
                    else:
                        print(paidStatus)
                        bookinginfomobj = donation_settings.objects.filter(client_id=clientId)
                        for b_i in bookinginfomobj:
                            print("ww")
                            payload = json.dumps({

                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "button",

                                    "body": {
                                        "text": f'*Donor Details* :\n'
                                                f' Name: {donarName}\n'
                                                f' Email: {doemail}\n'
                                                f' Phone: {dophone}\n\n'
                                                f'*Donation Details* :\n'
                                                f' Name: {donationName}\n'
                                                f' Amount: {donationAmount}\n'
                                                f' Comments: {donationDescription}\n'
                                                f' PaymentStatus: {paidStatus}'
                                    },

                                    "action": {
                                        "buttons": [
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "P" + str(m_i.id),
                                                    "title": "Pay Now"
                                                }
                                            },
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "J1",
                                                    "title": b_i.my_donation_details_button_name2
                                                }
                                            },
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "Z1",
                                                    "title": b_i.my_donation_details_button_name3
                                                }
                                            }

                                        ]
                                    }
                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)
        else:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "preview_url": True,
                "recipient_type": "individual",
                "to": toUser,
                "type": "text",
                "text": {
                    "body": "None"
                }

            })
            response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'O':
        current_date = timezone.now()
        first_day_of_current_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        first_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_previous_month = first_day_of_previous_month.replace(day=1)
        previous_month_donations = donation_details.objects.filter(
            donar_phone_number=toUser,
            donation_date__gte=first_day_of_previous_month,
            donation_date__lt=first_day_of_current_month
        ).order_by('-donation_date', '-vailo_record_creation')
        if previous_month_donations:

            for m_i in previous_month_donations:
                detailsobj = donation_details.objects.filter(id=m_i.id)
                for f in detailsobj:
                    ldate = f.vailo_record_creation
                    fdate = f.vailo_record_last_update
                    print(ldate)
                    print(fdate)
                    payReferId = f.donation_reference_id
                    donarName = f.donar_name
                    donationName = f.donation_name
                    doemail = f.donar_email
                    dophone = f.donar_phone_number
                    donationAmount = str(f.donation_amount)
                    donationDescription = f.donation_comments_message
                    paidStatus = 'paid' if f.payment_status == 1 else 'notpaid'
                    if paidStatus == 'paid':
                        print(paidStatus)
                        bookinginfomobj = donation_settings.objects.filter(client_id=clientId)
                        for b_i in bookinginfomobj:
                            print("ww")
                            payload = json.dumps({

                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "button",

                                    "body": {
                                        "text": f'*Donor Details* :\n'
                                                f' Name: {donarName}\n'
                                                f' Email: {doemail}\n'
                                                f' Phone: {dophone}\n\n'
                                                f'*Donation Details* :\n'
                                                f' Name: {donationName}\n'
                                                f' Amount: {donationAmount}\n'
                                                f' Comments: {donationDescription}\n'
                                                f' PaymentStatus: {paidStatus}'
                                    },

                                    "action": {
                                        "buttons": [
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "R" + str(m_i.id),
                                                    "title": b_i.my_donation_details_button_name1
                                                }
                                            },
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "J1",
                                                    "title": b_i.my_donation_details_button_name2
                                                }
                                            },
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "Z1",
                                                    "title": b_i.my_donation_details_button_name3
                                                }
                                            }

                                        ]
                                    }
                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)
                    else:
                        print(paidStatus)
                        bookinginfomobj = donation_settings.objects.filter(client_id=clientId)
                        for b_i in bookinginfomobj:
                            print("ww")
                            payload = json.dumps({

                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "button",

                                    "body": {
                                        "text": f'*Donor Details* :\n'
                                                f' Name: {donarName}\n'
                                                f' Email: {doemail}\n'
                                                f' Phone: {dophone}\n\n'
                                                f'*Donation Details* :\n'
                                                f' Name: {donationName}\n'
                                                f' Amount: {donationAmount}\n'
                                                f' Comments: {donationDescription}\n'
                                                f' PaymentStatus: {paidStatus}'
                                    },

                                    "action": {
                                        "buttons": [
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "P" + str(m_i.id),
                                                    "title": "Pay Now"
                                                }
                                            },
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "J1",
                                                    "title": b_i.my_donation_details_button_name2
                                                }
                                            },
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "Z1",
                                                    "title": b_i.my_donation_details_button_name3
                                                }
                                            }

                                        ]
                                    }
                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)

        else:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "preview_url": True,
                "recipient_type": "individual",
                "to": toUser,
                "type": "text",
                "text": {
                    "body": "None"
                }

            })
            response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'A':
        print("s you are  in A")
        welcomeobj = donation_settings.objects.filter(client_id=clientId,marketplace_id=response_id_id)
        print(welcomeobj)

        for don_i in welcomeobj:
            if don_i.donation_image:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                (don_i.donation_image)
                            }
                        },

                        "body": {
                            "text": don_i.donation_description if don_i.donation_description else "."
                        },
                        "footer": {
                            "text": don_i.donation_footer
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D1"+str(response_id_id),
                                        "title": don_i.donation_now_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D2"+str(response_id_id),
                                        "title": don_i.my_donation_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D3"+str(response_id_id),
                                        "title": don_i.contact_us_button_name
                                    }
                                },

                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": don_i.donation_description if don_i.donation_description else "."
                        },
                        "footer": {
                            "text": don_i.donation_footer
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D1"+str(response_id_id),
                                        "title": don_i.donation_now_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D2"+str(response_id_id),
                                        "title": don_i.my_donation_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D3"+str(response_id_id),
                                        "title": don_i.contact_us_button_name
                                    }
                                },
                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)



def process_ticket_text_message(message, request,url, headers, toUser, clientId):
    if message == 'HI' or message == 'Hi' or message == 'hi' or message == 'hI':

        if not ticket_customer_master.objects.filter(client_id=clientId,Customer_Phone_Number=toUser).exists():
            new_customer = ticket_customer_master(client_id=clientId,Customer_Phone_Number=toUser)
            new_customer.save()
        else:
            print("phone number already exist")

        if not ticket_billing_details.objects.filter(transaction_name=toUser).exists():
            # Update ticket_billing_details for new customer
            transaction_type = 'New Customer Lead'
            transaction_name = toUser
            transaction_count = 1

            billing_details = ticket_billing_details(
                client_id=clientId,
                transaction_type=transaction_type,
                transaction_name=transaction_name,
                transaction_count=transaction_count,

            )
            billing_details.save()
        else:
            print("User Existed")

        customer_receive(request,toUser,clientId)



        welcomeobject = event_settings.objects.filter(client_id=clientId)

        # welcomemessage = ''
        # welcomeheadertype = ''
        for wel_i in welcomeobject:
            # welcomemessage = welcomemessage + wel_i.event_welcome
            # welcomeheadertype = welcomeheadertype + wel_i.welcome_header_type
            if wel_i.welcome_header_image:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                (wel_i.welcome_header_image)
                            }
                        },

                        "body": {
                            "text": wel_i.welcome_message_text if wel_i.welcome_message_text else "."
                        },
                        "footer": {
                            "text": wel_i.welcome_message_footer
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "F1",
                                        "title": wel_i.booking_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "F2",
                                        "title": wel_i.booking_myticket_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "F3",
                                        "title": wel_i.booking_cancel_ticket_button_name
                                    }
                                },

                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
                customer_sent(request, toUser, clientId)
            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": wel_i.welcome_message_text if wel_i.welcome_message_text else "."
                        },
                        "footer": {
                            "text": wel_i.welcome_message_footer
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "F1",
                                        "title": wel_i.booking_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "F2",
                                        "title": wel_i.booking_myticket_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "F3",
                                        "title": wel_i.booking_cancel_ticket_button_name
                                    }
                                },
                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
                customer_sent(request, toUser, clientId)


    elif 'Transfer ticket' in message:
        ticket_start = message.find("Transfer ticket ") + len("Transfer ticket ")
        ticket_end = message.find(" to:")
        phone_start = message.find("to:") + len("to:")

        ticket_numbers = message[ticket_start:ticket_end]
        phone_number = message[phone_start:]

        phone_number = "91"+ phone_number.strip()
        
        ticketupdate = ticket_information.objects.filter(client_id=clientId,ticket_number=ticket_numbers)
        for z_i in ticketupdate:
            z_i.customer_phone_number = phone_number
            z_i.save()
            print("phone number replaced")
            payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "preview_url": True,
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": "Successfully transfered your tickets to this number" + phone_number 
                    }

            })
            response = requests.request("POST", url, headers=headers, data=payload)
            customer_sent(request, toUser, clientId)


            # old_phone_number = z_i.customer_phone_number
            # if old_phone_number == toUser:
            #     z_i.customer_phone_number = phone_number
            #     z_i.save()
            #     payload = json.dumps({
            #         "messaging_product": "whatsapp",
            #         "preview_url": True,
            #         "recipient_type": "individual",
            #         "to": toUser,
            #         "type": "text",
            #         "text": {
            #             "body": "Successfully transfered your tickets to this number" + phone_number 
            #         }

            #     })
            #     response = requests.request("POST", url, headers=headers, data=payload)
            #     customer_sent(request, toUser, clientId)

            # else:
            #     payload = json.dumps({
            #         "messaging_product": "whatsapp",
            #         "preview_url": True,
            #         "recipient_type": "individual",
            #         "to": toUser,
            #         "type": "text",
            #         "text": {
            #             "body": "You are not a authorized person to transfer"
            #         }

            #     })
            #     response = requests.request("POST", url, headers=headers, data=payload)
            #     customer_sent(request, toUser, clientId)


        

        


        # ticketupdate = ticket_information.objects.filter(client_id=clientId,customer_phone_number=toUser)
        # for tc_i in ticketupdate:
        #     tc_i.customer_phone_number = message
        #     tc_i.save()


        
    
    else:
        print('hello')
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "preview_url": True,
            "recipient_type": "individual",
            "to": toUser,
            "type": "text",
            "text": {
                "body": "Please send *Hi* to proceed"
            }

        })
        response = requests.request("POST", url, headers=headers, data=payload)
        customer_sent(request, toUser, clientId)


def update_second_number(request, url, headers, toUser, clientId, secondnumber):
    # print("qq")
    payload = json.dumps({
        "messaging_product": "whatsapp",
        "preview_url": True,
        "recipient_type": "individual",
        "to": secondnumber,
        "type": "text",
        "text": {
            "body": "Tickets Are Not Available Please Upload the tickets.."
        }

    })
    response = requests.request("POST", url, headers=headers, data=payload)
    customer_sent(request, toUser, clientId)

def process_appointement_interactive_message(response_id, request, url, headers, toUser, clientId, whatsAppPhoneNumberId,
                                           faceBookToken,list_title):
    response_id_type = response_id[0]
    resp_id_id = int(response_id[1])
    # response_id_pos = int(response_id[-1])


    print(response_id_type)
    print(resp_id_id)
    if response_id_type == 'T':
        if resp_id_id == 1:
            mainobj = appointment_settings.objects.filter(client_id=clientId)
            for m_i in mainobj:
                consultant_name = []
                consultant_specialization = []
                consultant_id = []
                consultantDetails = Consultant_details.objects.filter(client_id=clientId)
                for c_i in consultantDetails:
                    consultant_id.append(c_i.id)
                    consultant_name.append(c_i.consultant_name)
                    consultant_specialization.append(c_i.consultant_specialization)
                consultantlist = []
                for i in range(len(consultant_name)):
                    consultantlist.append({"id": "N" + str(consultant_id[i]),
                                      "title": consultant_name[i],
                                      "description": consultant_specialization[i]
                                      })

                if len(consultant_name) == 1:
                    # print("gggggg")

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "button",

                            "body": {
                                "text": m_i.consultant_list_message if m_i.consultant_list_message else "."
                            },

                            "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "A" + str(consultant_id[0]),
                                            "title": c_i.consultant_name
                                        }
                                    }

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)

                else:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "list",
                            "body": {
                                "text": m_i.consultant_list_message if m_i.consultant_list_message else "."
                            },

                            "action": {
                                "button": m_i.consultant_list_button_name,
                                "sections": [
                                    {
                                        "title": "Consultants",
                                        "rows": consultantlist
                                    }

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)
        elif resp_id_id == 2:
            myappointements = appointment_bookings.objects.filter(customer_phone_number=toUser)
            if myappointements:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",

                        "body": {
                            "text": "All your appointments with the doctor are listed below. Choose from the below option to see the details."
                        },

                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "E1",
                                        "title": "Upcoming Appointment"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "F1",
                                        "title": "Past Appointments"
                                    }
                                }
                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)

            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": "There in no appointements booked..Please book the appointements."
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
        elif resp_id_id == 3:
            mainobj = appointment_settings.objects.filter(client_id=clientId)
            for f_i in mainobj:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                (f_i.contactus_image)
                            }
                        },

                        "body": {
                            "text": f_i.contactus_description
                        },

                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "Z1",
                                        "title":"LocateUs"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "Z2",
                                        "title":"Call US"
                                    }
                                }

                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)

            # for m_i in mainobj:
            #     consultant_name = []
            #     consultant_specialization = []
            #     consultant_id = []
            #     consultantDetails = Consultant_settings.objects.filter(client_id=clientId)
            #     for c_i in consultantDetails:
            #         consultant_id.append(c_i.id)
            #         consultant_name.append(c_i.consultant_name)
            #         consultant_specialization.append(c_i.consultant_specialization)
            #     consultantlist = []
            #     for i in range(len(consultant_name)):
            #         consultantlist.append({"id": "B" + str(consultant_id[i]),
            #                                "title": consultant_name[i],
            #                                "description": consultant_specialization[i]
            #                                })
            #
            #     if len(consultant_name) == 1:
            #         # print("gggggg")
            #
            #         payload = json.dumps({
            #             "messaging_product": "whatsapp",
            #             "recipient_type": "individual",
            #             "to": toUser,
            #             "type": "interactive",
            #             "interactive": {
            #                 "type": "button",
            #
            #                 "body": {
            #                     "text": m_i.consultant_list_message if m_i.consultant_list_message else "."
            #                 },
            #
            #                 "action": {
            #                     "buttons": [
            #                         {
            #                             "type": "reply",
            #                             "reply": {
            #                                 "id": "M" + str(consultant_id[0]),
            #                                 "title": c_i.consultant_name
            #                             }
            #                         }
            #
            #                     ]
            #                 }
            #             }
            #         })
            #
            #         response = requests.request("POST", url, headers=headers, data=payload)
            #
            #     else:
            #         payload = json.dumps({
            #             "messaging_product": "whatsapp",
            #             "recipient_type": "individual",
            #             "to": toUser,
            #             "type": "interactive",
            #             "interactive": {
            #                 "type": "list",
            #                 "body": {
            #                     "text": m_i.consultant_list_message if m_i.consultant_list_message else "."
            #                 },
            #
            #                 "action": {
            #                     "button": m_i.consultant_list_button_name,
            #                     "sections": [
            #                         {
            #                             "title": "Consultants",
            #                             "rows": consultantlist
            #                         }
            #
            #                     ]
            #                 }
            #             }
            #         })
            #
            #         response = requests.request("POST", url, headers=headers, data=payload)


    elif response_id_type == 'N':
        response_id_id = int(response_id[1:])

        import datetime as dt

        current_date = dt.datetime.now().date()

        current_date += dt.timedelta(days=1)

        dates = []

        for i in range(60):
            new_date = current_date + dt.timedelta(days=i)
            dates.append(new_date)
        print(dates)

        a = 0
        day_of_week = 0
        ex_date = []
        only_dates = []
        formateed_dates = []
        all_available_slots = []
        consultantName = ''
        consultantSpecialization = ''
        for i, date in enumerate(dates, start=ord('a')):
            print("jinja")
            print(date)
            print("lalli")
            ex_date.append(date)
            zformatted_date = date.strftime('%d-%b %a')
            # formatted_date = zformatted_date[:6] + zformatted_date[-5:]
            # print(formatted_date)
            formateed_dates.append(zformatted_date)
            only_date = date.strftime('%d-%m-%Y')
            only_dates.append(only_date)
            day_of_week = int(date.strftime('%w'))
            variable_name = chr(i)
            print(f"{variable_name} = {zformatted_date} {day_of_week}")
            print(formateed_dates)

            duration = None  # Initialize to None or an appropriate default value

            slotDuration = Consultant_details.objects.filter(client_id=clientId, id=response_id_id)
            for s_i in slotDuration:
                duration_str = s_i.slot_duration
                consultantName = s_i.consultant_name
                consultantSpecialization = s_i.consultant_specialization
                numeric_part = int(''.join(filter(str.isdigit, duration_str)))
                duration = numeric_part

            hslots = []
            not_available_slot = []
            holidayDetails = Consultant_holiday_leaves.objects.filter(client_id=clientId, date=date)
            for h_i in holidayDetails:
                not_available_slots = {
                    "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
                    "end_time": h_i.end_time.strftime("%H:%M"),
                }
                not_available_slot.append(not_available_slots)

            for record in not_available_slot:
                start_time_str1 = record["start_time"]
                end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format

                record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
                record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
                current_time1 = record_start_time1
                while current_time1 < record_end_time2:
                    slot_start = current_time1.strftime("%H:%M")
                    current_time1 += timedelta(minutes=duration)
                    slot_end = current_time1.strftime("%H:%M")
                    hslots.append((slot_start, slot_end))
            print("aa")
            print(hslots)
            print("bb")

            all_slots = []
            availability_records = []

            availablityObject = Consultant_availablity.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
                                                           day_of_week=day_of_week)
            print(availablityObject)
            for a_i in availablityObject:
                print(a_i.id)
                availability_record = {
                    "start_time": a_i.start_time.strftime("%H:%M"),
                    "end_time": a_i.end_time.strftime("%H:%M"),
                }
                # print(availability_record)
                # print("mohan")
                availability_records.append(availability_record)

            for record in availability_records:
                start_time_str = record["start_time"]
                end_time_str = record["end_time"]

                record_start_time = datetime.strptime(start_time_str, "%H:%M")
                record_end_time = datetime.strptime(end_time_str, "%H:%M")
                current_time = record_start_time

                while current_time < record_end_time:
                    slot_start = current_time.strftime("%H:%M")
                    current_time += timedelta(minutes=duration)
                    slot_end = current_time.strftime("%H:%M")
                    all_slots.append((slot_start, slot_end))
            final_all_slots = [slot for slot in all_slots if slot not in hslots]
            print("channi")
            print(final_all_slots)
            print(len(final_all_slots))
            print("keshav")

            # bookingObject = Bookings.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
            #                                         date=current_date)
            # booked_slots = set(booking.notes1 for booking in bookingObject)
            # available_slots = [slot for slot in final_all_slots if slot not in booked_slots]

            existing_bookings = appointment_bookings.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
                                                        date=date)
            print("gowda")
            print(existing_bookings)
            print("sekar")

            booked_slots = set()
            for booking in existing_bookings:
                start_time_str = booking.start_time.strftime("%H:%M")
                end_time_str = booking.end_time.strftime("%H:%M")
                booked_slots.add((start_time_str, end_time_str))
            print("vv")
            print(booked_slots)
            print("andhra")
            available_slots = [slot for slot in final_all_slots if slot not in booked_slots]

            all_available_slots.append(available_slots)
            print("guna")
            print(all_available_slots)
            print("shouya")

            # a=len(available_slots)
            # print(a)
            # print(available_slots)
            # print(type(available_slots))
            # print("done very good job")

        # first_position = len(all_available_slots[0])
        # second_position = len(all_available_slots[1])
        # third_position = len(all_available_slots[2])
        # fourth_position = len(all_available_slots[3])
        # fifth_position = len(all_available_slots[4])
        # six_position = len(all_available_slots[5])
        # seventh_position = len(all_available_slots[6])
        # print(seventh_position)

        len_all_slots = []

        for i, date in enumerate(ex_date):
            avlslots = len(all_available_slots[i])
            formateedDate = ''
            if avlslots != 0 and avlslots <= 10:
                formateedDate = date.strftime('%d %b %a')
                len_all_slots.append((i, date, avlslots, formateedDate))
            else:
                print(f"No slots available for {formateedDate}")

        # Now len_all_slots contains tuples of (formatted_date, avlslots)
        print(len_all_slots)
        print("burger")

        show_avl_slots = []
        show_date = []
        total_avl_slots = 0
        for j, (i, date, avlslots, formateedDate) in enumerate(len_all_slots[:8]):
            show_date.append(date)
            total_avl_slots += avlslots
            title = f"{formateedDate} ({avlslots} slots)"
            show_avl_slots.append({"id": "K" + str(response_id_id) + "/" + str(date),
                                   "title": title

                                   })
        print(show_avl_slots)
        first_date = show_date[0]
        last_date = show_date[-1]
        new_first_date = first_date.strftime('%d %b %a')
        new_last_date = last_date.strftime('%d %b %a')
        print(first_date)
        print(last_date)

        print("king")
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": consultantName
                },

                "body": {
                    "text": f"is available from *{new_first_date}* to *{new_last_date}*. Choose your preferred date to proceed. Use previous or next option for other dates"
                },
                "footer": {
                    "text": consultantSpecialization
                },

                "action": {
                    "button": "Choose Date",
                    "sections": [
                        {
                            "title": "<LIST_SECTION_1_TITLE>",
                            "rows": [
                                {
                                    "id": show_avl_slots[0]["id"],
                                    "title": show_avl_slots[0]["title"],

                                },
                                {
                                    "id": show_avl_slots[1]["id"],
                                    "title": show_avl_slots[1]["title"],

                                },
                                {
                                    "id": show_avl_slots[2]["id"],
                                    "title": show_avl_slots[2]["title"],

                                },
                                {
                                    "id": show_avl_slots[3]["id"],
                                    "title": show_avl_slots[3]["title"],
                                },
                                {
                                    "id": show_avl_slots[4]["id"],
                                    "title": show_avl_slots[4]["title"],

                                },
                                {
                                    "id": show_avl_slots[5]["id"],
                                    "title": show_avl_slots[5]["title"],

                                },
                                {
                                    "id": show_avl_slots[6]["id"],
                                    "title": show_avl_slots[6]["title"],

                                },
                                {
                                    "id": show_avl_slots[7]["id"],
                                    "title": show_avl_slots[7]["title"],

                                },
                                {
                                    "id": "P" + str(first_date) + "/" + str(response_id_id),
                                    "title": "Previous",

                                },
                                {
                                    "id": "X" + str(last_date) + "/" + str(response_id_id),
                                    "title": "Next",

                                },

                            ]
                        }

                    ]
                }
            }
        })

        response = requests.request("POST", url, headers=headers, data=payload)





        # payload = json.dumps({
        #     "messaging_product": "whatsapp",
        #     "recipient_type": "individual",
        #     "to": toUser,
        #     "type": "interactive",
        #     "interactive": {
        #         "type": "list",
        #
        #         "body": {
        #             "text": "Avaialability of slots for each date"
        #         },
        #
        #         "action": {
        #             "button": "Choose Date",
        #             "sections": [
        #                 {
        #                     "title": "Date and avl slots",
        #                     "rows": show_avl_slots
        #                 },
        #                 {
        #                     "title": "choose",
        #                     "rows": [
        #                         {
        #                             "id": "P"+str(response_id_id),
        #                             "title": "Previous",
        #
        #                         },
        #                         {
        #                             "id": "X"+str(response_id_id)+"/"+"8-16",
        #                             "title": "Next",
        #
        #                         }
        #
        #                     ]
        #                 }
        #
        #             ]
        #         }
        #     }
        # })
        #
        # response = requests.request("POST", url, headers=headers, data=payload)
        # if len(len_all_slots) == 7:
        #     payload = json.dumps({
        #         "messaging_product": "whatsapp",
        #         "recipient_type": "individual",
        #         "to": toUser,
        #         "type": "interactive",
        #         "interactive": {
        #             "type": "list",
        #
        #             "body": {
        #                 "text": "Avaialability of slots for each date"
        #             },
        #
        #             "action": {
        #                 "button": "Choose Date",
        #                 "sections": [
        #                     {
        #                         "title": "Date and avl slots",
        #                         "rows": show_avl_slots
        #                     }
        #
        #                 ]
        #             }
        #         }
        #     })
        #
        #     response = requests.request("POST", url, headers=headers, data=payload)
        # else:
        #     print("s len is less than 7")
        #     next_dates = []
        #     next_current_date = dates[-1] + dt.timedelta(days=1)
        #     for i in range(24):
        #         new_date = next_current_date + dt.timedelta(days=i)
        #         next_dates.append(new_date)
        #     a = 0
        #     day_of_week = 0
        #     only_dates = []
        #     formateed_dates = []
        #     all_available_slots = []
        #     for i, date in enumerate(next_dates, start=ord('a')):
        #         print("jinja")
        #         print(date)
        #         print("lalli")
        #         zformatted_date = date.strftime('%d-%b %a')
        #         # formatted_date = zformatted_date[:6] + zformatted_date[-5:]
        #         # print(formatted_date)
        #         formateed_dates.append(zformatted_date)
        #         only_date = date.strftime('%d-%m-%Y')
        #         only_dates.append(only_date)
        #         day_of_week = int(date.strftime('%w'))
        #         variable_name = chr(i)
        #         print(f"{variable_name} = {zformatted_date} {day_of_week}")
        #         print(formateed_dates)
        #
        #         duration = None  # Initialize to None or an appropriate default value
        #         slotDuration = Consultant_settings.objects.filter(client_id=clientId, id=response_id_id)
        #         for s_i in slotDuration:
        #             duration_str = s_i.slot_duration
        #             numeric_part = int(''.join(filter(str.isdigit, duration_str)))
        #             duration = numeric_part
        #
        #         hslots = []
        #         not_available_slot = []
        #         holidayDetails = Holiday_leaves.objects.filter(client_id=clientId, date=date)
        #         for h_i in holidayDetails:
        #             not_available_slots = {
        #                 "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
        #                 "end_time": h_i.end_time.strftime("%H:%M"),
        #             }
        #             not_available_slot.append(not_available_slots)
        #
        #         for record in not_available_slot:
        #             start_time_str1 = record["start_time"]
        #             end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format
        #
        #             record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
        #             record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
        #             current_time1 = record_start_time1
        #             while current_time1 < record_end_time2:
        #                 slot_start = current_time1.strftime("%H:%M")
        #                 current_time1 += timedelta(minutes=duration)
        #                 slot_end = current_time1.strftime("%H:%M")
        #                 hslots.append((slot_start, slot_end))
        #         print("aa")
        #         print(hslots)
        #         print("bb")
        #
        #         all_slots = []
        #         availability_records = []
        #
        #         availablityObject = Availablity.objects.filter(client_id=clientId,
        #                                                        Consultant_settings_id=response_id_id,
        #                                                        day_of_week=day_of_week)
        #         print(availablityObject)
        #         for a_i in availablityObject:
        #             print(a_i.id)
        #             availability_record = {
        #                 "start_time": a_i.start_time.strftime("%H:%M"),
        #                 "end_time": a_i.end_time.strftime("%H:%M"),
        #             }
        #             # print(availability_record)
        #             # print("mohan")
        #             availability_records.append(availability_record)
        #
        #         for record in availability_records:
        #             start_time_str = record["start_time"]
        #             end_time_str = record["end_time"]
        #
        #             record_start_time = datetime.strptime(start_time_str, "%H:%M")
        #             record_end_time = datetime.strptime(end_time_str, "%H:%M")
        #             current_time = record_start_time
        #
        #             while current_time < record_end_time:
        #                 slot_start = current_time.strftime("%H:%M")
        #                 current_time += timedelta(minutes=duration)
        #                 slot_end = current_time.strftime("%H:%M")
        #                 all_slots.append((slot_start, slot_end))
        #         final_all_slots = [slot for slot in all_slots if slot not in hslots]
        #         print("channi")
        #         print(final_all_slots)
        #         print(len(final_all_slots))
        #         print("keshav")
        #
        #         # bookingObject = Bookings.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
        #         #                                         date=current_date)
        #         # booked_slots = set(booking.notes1 for booking in bookingObject)
        #         # available_slots = [slot for slot in final_all_slots if slot not in booked_slots]
        #
        #         existing_bookings = Bookings.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
        #                                                     date=date)
        #         print("gowda")
        #         print(existing_bookings)
        #         print("sekar")
        #
        #         booked_slots = set()
        #         for booking in existing_bookings:
        #             start_time_str = booking.start_time.strftime("%H:%M")
        #             end_time_str = booking.end_time.strftime("%H:%M")
        #             booked_slots.add((start_time_str, end_time_str))
        #         print("vv")
        #         print(booked_slots)
        #         print("andhra")
        #         available_slots = [slot for slot in final_all_slots if slot not in booked_slots]
        #
        #         all_available_slots.append(available_slots)
        #         print("guna")
        #         print(all_available_slots)
        #         print("shouya")
        #
        #     for i, formatted_date in enumerate(formateed_dates):
        #         avlslots = len(all_available_slots[i])
        #
        #         if avlslots != 0 and avlslots <= 10:
        #             len_all_slots.append((i, formatted_date, avlslots))
        #         else:
        #             print(f"No slots available for {formatted_date}")
        #
        #     print(len_all_slots)
        #     print("burger")
        #
        #     show_avl_slots = []
        #     for j, (i, formatted_date, avlslots) in enumerate(len_all_slots[:7]):
        #         title = f"{formatted_date} Avl Slots={avlslots}"
        #         show_avl_slots.append({"id": "K" + str(response_id_id) + str(j) + str(i),
        #                                "title": title
        #
        #                                })
        #     print(show_avl_slots)
        #     payload = json.dumps({
        #         "messaging_product": "whatsapp",
        #         "recipient_type": "individual",
        #         "to": toUser,
        #         "type": "interactive",
        #         "interactive": {
        #             "type": "list",
        #
        #             "body": {
        #                 "text": "Avaialability of slots for each date"
        #             },
        #
        #             "action": {
        #                 "button": "Choose Date",
        #                 "sections": [
        #                     {
        #                         "title": "Date and avl slots",
        #                         "rows": show_avl_slots
        #                     }
        #
        #                 ]
        #             }
        #         }
        #     })
        #
        #     response = requests.request("POST", url, headers=headers, data=payload)

        # payload = json.dumps({
        #     "messaging_product": "whatsapp",
        #     "recipient_type": "individual",
        #     "to": toUser,
        #     "type": "interactive",
        #     "interactive": {
        #         "type": "list",
        #
        #         "body": {
        #             "text": "Avaialability of slots for each date"
        #         },
        #
        #         "action": {
        #             "button": "Choose Date",
        #             "sections": [
        #                 {
        #                     "title": formateed_dates[0],
        #                     "rows": [
        #                         {
        #                             "id": "K"+str(response_id_id)+"0",
        #                             "title": "No slots available" if first_position == 0 else str(first_position) + " slots available",
        #
        #                         }
        #
        #                     ]
        #                 },
        #                 {
        #                     "title": formateed_dates[1],
        #                     "rows": [
        #                         {
        #                             "id": "K"+str(response_id_id)+"1",
        #                             "title": "No slots available" if second_position == 0 else str(second_position) + " slots available",
        #
        #                         }
        #
        #                     ]
        #                 },
        #                 {
        #                     "title": formateed_dates[2],
        #                     "rows": [
        #                         {
        #                             "id": "K"+str(response_id_id)+"2",
        #                             "title": "No slots available" if third_position == 0 else str(third_position) + " slots available",
        #
        #                         }
        #
        #                     ]
        #                 },
        #                 {
        #                     "title": formateed_dates[3],
        #                     "rows": [
        #                         {
        #                             "id": "K"+str(response_id_id)+"3",
        #                             "title": "No slots available" if fourth_position == 0 else str(fourth_position) + " slots available",
        #
        #                         }
        #
        #                     ]
        #                 },
        #                 {
        #                     "title": formateed_dates[4],
        #                     "rows": [
        #                         {
        #                             "id": "K"+str(response_id_id)+"4",
        #                             "title": "No slots available" if fifth_position == 0 else str(fifth_position) + " slots available",
        #
        #                         }
        #
        #                     ]
        #                 },
        #                 {
        #                     "title": formateed_dates[5],
        #                     "rows": [
        #                         {
        #                             "id": "K"+str(response_id_id)+"5",
        #                             "title": "No slots available" if six_position == 0 else str(six_position) + " slots available",
        #
        #                         }
        #
        #                     ]
        #                 },
        #                 {
        #                     "title": formateed_dates[6],
        #                     "rows": [
        #                         {
        #                             "id": "K"+str(response_id_id)+"6",
        #                             "title": "No slots available" if seventh_position == 0 else str(seventh_position) + " slots available",
        #
        #                         }
        #
        #                     ]
        #                 }
        #             ]
        #         }
        #     }
        # })
        # response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'K':
        print("tipelinganna")
        print(response_id)
        slash_index = response_id.index('/')

        date=[]
        dates = response_id[slash_index + 1:]
        print("jayamma")
        print(dates)
        print("jayanna")
        dates_new= datetime.strptime(str(dates), '%Y-%m-%d')
        date.append(dates_new)


        consult_id = response_id[1:slash_index]
        print("nagamma")
        print(consult_id)
        print("nagaraj")


        customer = appointment_visitor.objects.filter(client_id=clientId, Visitor_Whatsapp_Number=toUser).first()
        visitor_id = 0
        if customer:
            visitor_id = customer.id

        # import datetime as dt
        #
        # current_date = dt.datetime.now().date()
        #
        # current_date += dt.timedelta(days=1)
        #
        # dates = []
        #
        # for i in range(7):
        #     new_date = current_date + dt.timedelta(days=i)
        #     dates.append(new_date)
        # print(dates)

        a = 0
        day_of_week = 0
        only_dates = []
        sub_dates = []
        finalDates = []
        formateed_dates = []
        all_available_slots = []
        consultantName = ''
        consultantSpecialization = ''
        for i, date in enumerate(date, start=ord('a')):
            zformatted_date = date.strftime('%d/%B/%Y %A')
            sub_date = date.strftime('%d %b %a')
            sub_dates.append(sub_date)
            formatted_date = zformatted_date[:6] + zformatted_date[12:]
            print(formatted_date)
            formateed_dates.append(formatted_date)
            only_date = date.strftime('%d-%m-%Y')
            final_only_date = only_date.replace("-", "")
            finalDates.append(final_only_date)
            day_of_week = int(date.strftime('%w'))
            variable_name = chr(i)
            print(f"{variable_name} = {formatted_date} {day_of_week}")
            print(formateed_dates)

            duration = None  # Initialize to None or an appropriate default value
            slotDuration = Consultant_details.objects.filter(client_id=clientId, id=consult_id)
            for s_i in slotDuration:
                duration_str = s_i.slot_duration
                consultantName = s_i.consultant_name
                consultantSpecialization = s_i.consultant_specialization
                numeric_part = int(''.join(filter(str.isdigit, duration_str)))
                duration = numeric_part

            hslots = []
            not_available_slot = []
            holidayDetails = Consultant_holiday_leaves.objects.filter(client_id=clientId, date=date)
            for h_i in holidayDetails:
                not_available_slots = {
                    "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
                    "end_time": h_i.end_time.strftime("%H:%M"),
                }
                not_available_slot.append(not_available_slots)

            for record in not_available_slot:
                start_time_str1 = record["start_time"]
                end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format

                record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
                record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
                current_time1 = record_start_time1
                while current_time1 < record_end_time2:
                    slot_start = current_time1.strftime("%H:%M")
                    current_time1 += timedelta(minutes=duration)
                    slot_end = current_time1.strftime("%H:%M")
                    hslots.append((slot_start, slot_end))
            print("aa")
            print(hslots)
            print("bb")

            all_slots = []
            availability_records = []

            availablityObject = Consultant_availablity.objects.filter(client_id=clientId,
                                                           Consultant_settings_id=consult_id,
                                                           day_of_week=day_of_week)
            print(availablityObject)
            for a_i in availablityObject:
                print(a_i.id)
                availability_record = {
                    "start_time": a_i.start_time.strftime("%H:%M"),
                    "end_time": a_i.end_time.strftime("%H:%M"),
                }
                print(availability_record)
                print("mohan")
                availability_records.append(availability_record)

            for record in availability_records:
                start_time_str = record["start_time"]
                end_time_str = record["end_time"]

                record_start_time = datetime.strptime(start_time_str, "%H:%M")
                record_end_time = datetime.strptime(end_time_str, "%H:%M")
                current_time = record_start_time

                while current_time < record_end_time:
                    slot_start = current_time.strftime("%H:%M")
                    current_time += timedelta(minutes=duration)
                    slot_end = current_time.strftime("%H:%M")
                    all_slots.append((slot_start, slot_end))
            final_all_slots = [slot for slot in all_slots if slot not in hslots]
            print("channi")
            print(final_all_slots)
            print(len(final_all_slots))
            print("keshav")

            existing_bookings = appointment_bookings.objects.filter(client_id=clientId, Consultant_settings_id=consult_id,
                                                        date=date)
            print("gowda")
            print(existing_bookings)
            print("sekar")

            booked_slots = set()
            for booking in existing_bookings:
                start_time_str = booking.start_time.strftime("%H:%M")
                end_time_str = booking.end_time.strftime("%H:%M")
                booked_slots.add((start_time_str, end_time_str))
            print("vv")
            print(booked_slots)
            print("andhra")
            available_slots = [slot for slot in final_all_slots if slot not in booked_slots]

            all_available_slots.append(available_slots)
        print("jill")
        print(all_available_slots)
        print("jiga")
        slot_data = all_available_slots[0]
        total_time_slots = len(slot_data)

        list_all_data = []
        formatted_slots_details = []
        formatted_duration_details = []
        for slot_start, slot_end in slot_data:
            print(slot_start)
            print(slot_end)
            formatted_duation_create = f"{slot_start}-{slot_end}"
            formatted_slot_create = f"{slot_start}"
            date_formate_slot_create = datetime.strptime(formatted_slot_create, "%H:%M")
            formatted_start_time = date_formate_slot_create.strftime("%I:%M%p")
            formatted_slots_details.append(formatted_start_time)
            formatted_duration_details.append(formatted_duation_create)

        for i in range(len(formatted_slots_details)):
            list_all_data.append({"id": "S" + str(consult_id) + "/" + str(
                visitor_id) + "//" + str(finalDates[0]) + str(formatted_duration_details[i]) + str(i),
                                  "title": str(sub_dates[0]) + " " + str(formatted_slots_details[i])

                                  })

        print("correct")
        print(formatted_slots_details)
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": consultantName
                },

                "body": {
                    "text":
                            f"is available on {sub_dates[0]}. Choose your preferred time slot from {total_time_slots} options available."
                },
                "footer": {
                    "text": consultantSpecialization
                },

                "action": {
                    "button": "Choose Slots",
                    "sections": [
                        {
                            "title": "Slots",
                            "rows": list_all_data
                        }

                    ]
                }
            }
        })

        response = requests.request("POST", url, headers=headers, data=payload)


        # first_position = len(all_available_slots[0])
        # second_position = len(all_available_slots[1])
        # third_position = len(all_available_slots[2])
        # fourth_position = len(all_available_slots[3])
        # fifth_position = len(all_available_slots[4])
        # six_position = len(all_available_slots[5])
        # seventh_position = len(all_available_slots[6])
        # print(seventh_position)
        # slot_data = all_available_slots[response_id_pos]  # Assuming all_available_slots[2] contains the desired data
        # print(slot_data)

        # if len(slot_data) == 0:
        #     print("s zero")
        #     payload = json.dumps({
        #         "messaging_product": "whatsapp",
        #         "preview_url": True,
        #         "recipient_type": "individual",
        #         "to": toUser,
        #         "type": "text",
        #         "text": {
        #             "body": "for this date no slots availble...please choose another date."
        #         }
        #
        #     })
        #     response = requests.request("POST", url, headers=headers, data=payload)
        # else:
        #     list_all_data = []
        #     formatted_slots_details = []
        #     formatted_duration_details = []
        #     for slot_start, slot_end in slot_data:
        #         print(slot_start)
        #         print(slot_end)
        #         formatted_duation_create = f"{slot_start}-{slot_end}"
        #         formatted_slot_create = f"{slot_start}"
        #         date_formate_slot_create = datetime.strptime(formatted_slot_create, "%H:%M")
        #         formatted_start_time = date_formate_slot_create.strftime("%I:%M%p")
        #         formatted_slots_details.append(formatted_start_time)
        #         formatted_duration_details.append(formatted_duation_create)
        #
        #     for i in range(len(formatted_slots_details)):
        #         list_all_data.append({"id": "S" + str(response_id_id) + "/" + str(
        #             visitor_id) + "//" + str(finalDates[0]) + str(formatted_duration_details[i]) + str(i),
        #                               "title": str(sub_dates[0]) + " " + str(formatted_slots_details[i])
        #
        #                               })
        #
        #     print("correct")
        #     print(formatted_slots_details)
        #     payload = json.dumps({
        #         "messaging_product": "whatsapp",
        #         "recipient_type": "individual",
        #         "to": toUser,
        #         "type": "interactive",
        #         "interactive": {
        #             "type": "list",
        #
        #             "body": {
        #                 "text": "Choose Slots"
        #             },
        #
        #             "action": {
        #                 "button": "Choose Slots",
        #                 "sections": [
        #                     {
        #                         "title": "Slots",
        #                         "rows": list_all_data
        #                     }
        #
        #                 ]
        #             }
        #         }
        #     })
        #
        #     response = requests.request("POST", url, headers=headers, data=payload)


    elif response_id_type == 'S':
        print("scoming")
        print(response_id)
        booking_ref_id = uuid.uuid4()
        Components = response_id.split("/")
        ConsultantId = Components[0][1:]  # Remove the leading 's'
        VisitorId = Components[1]
        sdate = Components[3][:8]
        day = sdate[:2]
        month = sdate[2:4]
        year = sdate[4:]
        fdate = f'{day}/{month}/{year}'
        date_obj = datetime.strptime(str(fdate), "%d/%m/%Y")
        gdate = date_obj.strftime("%Y-%m-%d")
        duration = response_id.split(sdate)[1][:-1]
        # dpart = duration[11:]
        # print(dpart)
        start_time_str, end_time_str = duration.split('-')
        start_time = datetime.strptime(start_time_str.strip(), '%H:%M')
        end_time = datetime.strptime(end_time_str.strip(), '%H:%M')
        status_obj = Consultant_details.objects.filter(id=ConsultantId)
        approval_mode = ''
        for a_i in status_obj:
            approval_mode = a_i.approval_mode
        print(approval_mode)

        if approval_mode == 'Automatic' or approval_mode == 'automatic':
            print("s automatic")
            booking = appointment_bookings(
                client_id=clientId,
                Visitor_id=VisitorId,
                Consultant_settings_id=ConsultantId,
                date=gdate,
                start_time=start_time,
                end_time=end_time,
                status=1,
                booking_reference_id=booking_ref_id,
                customer_phone_number=toUser,
                online_offline='offline'

            )
            booking.save()
            print("successfully created one record in bookings")
            showDetails = appointment_bookings.objects.filter(client_id=clientId, booking_reference_id=booking_ref_id)
            for s_i in showDetails:
                duration_start = s_i.start_time
                duration_end = s_i.end_time
                # start_time_obj1 = datetime.strptime(str(duration_start), "%H:%M")
                # end_time_obj1 = datetime.strptime(str(duration_end), "%H:%M")
                formatted_start_time1 = duration_start.strftime("%I:%M%p")
                formatted_end_time1 = duration_end.strftime("%I:%M%p")
                date = s_i.date
                date_obj = datetime.strptime(str(date), '%Y-%m-%d')
                New_date = date_obj.strftime('%d-%b-%Y')
                status = "Booked" if s_i.status == 1 else "blocked"
                detailsObj = Consultant_details.objects.filter(id=s_i.Consultant_settings_id)
                consultantName = ''
                specialization = ''
                consultantImage = ''
                for d_i in detailsObj:
                    consultantName = d_i.consultant_name
                    specialization = d_i.consultant_specialization
                    consultantImage = d_i.consultant_image

                print("print")
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                (consultantImage)
                            }
                        },

                        "body": {
                            "text": f'*Appointement details* :\n'
                                    f' *_Name_*: {consultantName}\n'
                                    f' *_Specialization_*: {specialization}\n'
                                    f' *_From_*: {formatted_start_time1} *_to_* {formatted_end_time1}\n'
                                    f' *_Date_*:{New_date}\n'
                                    f' *_Status_*:{status}\n'

                        },

                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D1",
                                        "title": "Done"
                                    }
                                }

                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
        elif approval_mode == 'Manual' or approval_mode == 'manual':
            print("s it is manual")
            booking = appointment_bookings(
                client_id=clientId,
                Visitor_id=VisitorId,
                Consultant_settings_id=ConsultantId,
                date=gdate,
                start_time=start_time,
                end_time=end_time,
                status=2,
                booking_reference_id=booking_ref_id,
                customer_phone_number=toUser,
                online_offline='offline'

            )
            booking.save()
            print("successfully created one record in bookings")
            showDetails = appointment_bookings.objects.filter(client_id=clientId, booking_reference_id=booking_ref_id)
            for s_i in showDetails:
                duration_start = s_i.start_time
                duration_end = s_i.end_time
                # start_time_obj1 = datetime.strptime(str(duration_start), "%H:%M")
                # end_time_obj1 = datetime.strptime(str(duration_end), "%H:%M")
                formatted_start_time1 = duration_start.strftime("%I:%M%p")
                formatted_end_time1 = duration_end.strftime("%I:%M%p")
                date = s_i.date
                date_obj = datetime.strptime(str(date), '%Y-%m-%d')
                New_date = date_obj.strftime('%d %b %Y')
                status = "Pending confirmation" if s_i.status == 2 else "."
                detailsObj = Consultant_details.objects.filter(id=s_i.Consultant_settings_id)
                consultantName = ''
                specialization = ''
                consultantImage = ''
                for d_i in detailsObj:
                    consultantName = d_i.consultant_name
                    specialization = d_i.consultant_specialization
                    consultantImage = d_i.consultant_image

                print("print")
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                (consultantImage)
                            }
                        },

                        "body": {
                            "text": f'*Appointement details* :\n'
                                    f' *_Name_*: {consultantName}\n'
                                    f' *_Specialization_*: {specialization}\n'
                                    f' *_From_*: {formatted_start_time1} to {formatted_end_time1}\n'
                                    f' *_Date_*:{New_date}\n'
                                    f' *_Status_*:{status}\n'

                        },

                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D1",
                                        "title": "Done"
                                    }
                                }

                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)



    elif response_id_type == 'X':
        print(response_id)

        x = response_id.index('/')
        print(response_id[x + 1:])
        print(response_id[1:x])
        next_date = response_id[1:x]
        consulta_id = response_id[x+1:]
        main_available_slots = []
        next_date = datetime.strptime(str(next_date), "%Y-%m-%d").date()
        next_day = next_date + timedelta(days=1)
        consultantName=''
        consultantSpecialization=''
        import datetime as dt
        while len(main_available_slots) < 8:

            if next_day != dt.date.today():
                a = 0
                day_of_week = 0
                ex_date = []
                only_dates = []
                formateed_dates = []
                all_available_slots = []
                print("jinja")
                print(next_day)
                print("lalli")
                ex_date.append(next_day)
                zformatted_date = next_day.strftime('%d-%b %a')
                # formatted_date = zformatted_date[:6] + zformatted_date[-5:]
                # print(formatted_date)
                formateed_dates.append(zformatted_date)
                only_date = next_day.strftime('%d-%m-%Y')
                only_dates.append(only_date)
                day_of_week = int(next_day.strftime('%w'))

                print(formateed_dates)

                duration = None  # Initialize to None or an appropriate default value
                slotDuration = Consultant_details.objects.filter(client_id=clientId, id=consulta_id)
                for s_i in slotDuration:
                    duration_str = s_i.slot_duration
                    consultantName = s_i.consultant_name
                    consultantSpecialization = s_i.consultant_specialization
                    numeric_part = int(''.join(filter(str.isdigit, duration_str)))
                    duration = numeric_part

                hslots = []
                not_available_slot = []
                holidayDetails = Consultant_holiday_leaves.objects.filter(client_id=clientId, date=next_day)
                for h_i in holidayDetails:
                    not_available_slots = {
                        "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
                        "end_time": h_i.end_time.strftime("%H:%M"),
                    }
                    not_available_slot.append(not_available_slots)

                for record in not_available_slot:
                    start_time_str1 = record["start_time"]
                    end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format

                    record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
                    record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
                    current_time1 = record_start_time1
                    while current_time1 < record_end_time2:
                        slot_start = current_time1.strftime("%H:%M")
                        current_time1 += timedelta(minutes=duration)
                        slot_end = current_time1.strftime("%H:%M")
                        hslots.append((slot_start, slot_end))
                print("aa")
                print(hslots)
                print("bb")

                all_slots = []
                availability_records = []

                availablityObject = Consultant_availablity.objects.filter(client_id=clientId,
                                                               Consultant_settings_id=consulta_id,
                                                               day_of_week=day_of_week)
                print(availablityObject)
                for a_i in availablityObject:
                    print(a_i.id)
                    availability_record = {
                        "start_time": a_i.start_time.strftime("%H:%M"),
                        "end_time": a_i.end_time.strftime("%H:%M"),
                    }
                    # print(availability_record)
                    # print("mohan")
                    availability_records.append(availability_record)

                for record in availability_records:
                    start_time_str = record["start_time"]
                    end_time_str = record["end_time"]

                    record_start_time = datetime.strptime(start_time_str, "%H:%M")
                    record_end_time = datetime.strptime(end_time_str, "%H:%M")
                    current_time = record_start_time

                    while current_time < record_end_time:
                        slot_start = current_time.strftime("%H:%M")
                        current_time += timedelta(minutes=duration)
                        slot_end = current_time.strftime("%H:%M")
                        all_slots.append((slot_start, slot_end))
                final_all_slots = [slot for slot in all_slots if slot not in hslots]
                print("channi")
                print(final_all_slots)
                print(len(final_all_slots))
                print("keshav")

                # bookingObject = Bookings.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
                #                                         date=current_date)
                # booked_slots = set(booking.notes1 for booking in bookingObject)
                # available_slots = [slot for slot in final_all_slots if slot not in booked_slots]

                existing_bookings = appointment_bookings.objects.filter(client_id=clientId, Consultant_settings_id=consulta_id,
                                                            date=next_day)
                print("gowda")
                print(existing_bookings)
                print("sekar")

                booked_slots = set()
                for booking in existing_bookings:
                    start_time_str = booking.start_time.strftime("%H:%M")
                    end_time_str = booking.end_time.strftime("%H:%M")
                    booked_slots.add((start_time_str, end_time_str))
                print("vv")
                print(booked_slots)
                print("andhra")
                available_slots = [slot for slot in final_all_slots if slot not in booked_slots]

                if len(available_slots) > 0 and len(available_slots) <= 10:
                    formattedDate = next_day.strftime('%d %b %a').upper()
                    avlslots = len(available_slots)
                    main_available_slots.append((next_day, avlslots, formattedDate))
                    next_day += dt.timedelta(days=1)
                else:
                    next_day += dt.timedelta(days=1)
            else:
                next_day += dt.timedelta(days=1)
        print("mallana")
        print(main_available_slots)
        print("manjakka")

        show_avl_slots = []
        show_date = []
        total_avl_slots = 0
        for j, (date, avlslots, formateedDate) in enumerate(main_available_slots):
            show_date.append(date)
            total_avl_slots += avlslots
            title = f"{formateedDate} ({avlslots}slots)"
            show_avl_slots.append({"id": "K" + str(consulta_id) + "/" + str(date),
                                   "title": title

                                   })
        print("jagganna")
        print(show_avl_slots)
        print("jaggamma")
        first_date = show_date[0]
        last_date = show_date[-1]
        print(first_date)
        print(last_date)

        print("king")
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": consultantName
                },

                "body": {
                    "text": f"{total_avl_slots} slots are availble from {first_date} to {last_date} choose your date to proceed. choose previous or *next* if you want to opt for _different date_"
                },
                "footer": {
                    "text": consultantSpecialization
                },

                "action": {
                    "button": "Choose Date",
                    "sections": [
                        {
                            "title": "<LIST_SECTION_1_TITLE>",
                            "rows": [
                                {
                                    "id": show_avl_slots[0]["id"],
                                    "title": show_avl_slots[0]["title"],

                                },
                                {
                                    "id": show_avl_slots[1]["id"],
                                    "title": show_avl_slots[1]["title"],

                                },
                                {
                                    "id": show_avl_slots[2]["id"],
                                    "title": show_avl_slots[2]["title"],

                                },
                                {
                                    "id": show_avl_slots[3]["id"],
                                    "title": show_avl_slots[3]["title"],
                                },
                                {
                                    "id": show_avl_slots[4]["id"],
                                    "title": show_avl_slots[4]["title"],

                                },
                                {
                                    "id": show_avl_slots[5]["id"],
                                    "title": show_avl_slots[5]["title"],

                                },
                                {
                                    "id": show_avl_slots[6]["id"],
                                    "title": show_avl_slots[6]["title"],

                                },
                                {
                                    "id": show_avl_slots[7]["id"],
                                    "title": show_avl_slots[7]["title"],

                                },
                                {
                                    "id": "P" + str(first_date) + "/" + str(consulta_id),
                                    "title": "Previous",

                                },
                                {
                                    "id": "X" + str(last_date) + "/" + str(consulta_id),
                                    "title": "Next",

                                },

                            ]
                        }

                    ]
                }
            }
        })

        response = requests.request("POST", url, headers=headers, data=payload)
















        # import datetime as dt
        #
        # current_date = dt.datetime.now().date()
        #
        # current_date += dt.timedelta(days=1)
        #
        # dates = []
        #
        # for i in range(100):
        #     new_date = current_date + dt.timedelta(days=i)
        #     dates.append(new_date)
        # print(dates)
        #
        # a = 0
        # day_of_week = 0
        # ex_date = []
        # only_dates = []
        # formateed_dates = []
        # all_available_slots = []
        # for i, date in enumerate(dates, start=ord('a')):
        #     print("jinja")
        #     print(date)
        #     print("lalli")
        #     ex_date.append(date)
        #     zformatted_date = date.strftime('%d-%b %a')
        #     # formatted_date = zformatted_date[:6] + zformatted_date[-5:]
        #     # print(formatted_date)
        #     formateed_dates.append(zformatted_date)
        #     only_date = date.strftime('%d-%m-%Y')
        #     only_dates.append(only_date)
        #     day_of_week = int(date.strftime('%w'))
        #     variable_name = chr(i)
        #     print(f"{variable_name} = {zformatted_date} {day_of_week}")
        #     print(formateed_dates)
        #
        #     duration = None  # Initialize to None or an appropriate default value
        #     slotDuration = Consultant_settings.objects.filter(client_id=clientId, id=response_id_id)
        #     for s_i in slotDuration:
        #         duration_str = s_i.slot_duration
        #         numeric_part = int(''.join(filter(str.isdigit, duration_str)))
        #         duration = numeric_part
        #
        #     hslots = []
        #     not_available_slot = []
        #     holidayDetails = Holiday_leaves.objects.filter(client_id=clientId, date=date)
        #     for h_i in holidayDetails:
        #         not_available_slots = {
        #             "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
        #             "end_time": h_i.end_time.strftime("%H:%M"),
        #         }
        #         not_available_slot.append(not_available_slots)
        #
        #     for record in not_available_slot:
        #         start_time_str1 = record["start_time"]
        #         end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format
        #
        #         record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
        #         record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
        #         current_time1 = record_start_time1
        #         while current_time1 < record_end_time2:
        #             slot_start = current_time1.strftime("%H:%M")
        #             current_time1 += timedelta(minutes=duration)
        #             slot_end = current_time1.strftime("%H:%M")
        #             hslots.append((slot_start, slot_end))
        #     print("aa")
        #     print(hslots)
        #     print("bb")
        #
        #     all_slots = []
        #     availability_records = []
        #
        #     availablityObject = Availablity.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
        #                                                    day_of_week=day_of_week)
        #     print(availablityObject)
        #     for a_i in availablityObject:
        #         print(a_i.id)
        #         availability_record = {
        #             "start_time": a_i.start_time.strftime("%H:%M"),
        #             "end_time": a_i.end_time.strftime("%H:%M"),
        #         }
        #         # print(availability_record)
        #         # print("mohan")
        #         availability_records.append(availability_record)
        #
        #     for record in availability_records:
        #         start_time_str = record["start_time"]
        #         end_time_str = record["end_time"]
        #
        #         record_start_time = datetime.strptime(start_time_str, "%H:%M")
        #         record_end_time = datetime.strptime(end_time_str, "%H:%M")
        #         current_time = record_start_time
        #
        #         while current_time < record_end_time:
        #             slot_start = current_time.strftime("%H:%M")
        #             current_time += timedelta(minutes=duration)
        #             slot_end = current_time.strftime("%H:%M")
        #             all_slots.append((slot_start, slot_end))
        #     final_all_slots = [slot for slot in all_slots if slot not in hslots]
        #     print("channi")
        #     print(final_all_slots)
        #     print(len(final_all_slots))
        #     print("keshav")
        #
        #     # bookingObject = Bookings.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
        #     #                                         date=current_date)
        #     # booked_slots = set(booking.notes1 for booking in bookingObject)
        #     # available_slots = [slot for slot in final_all_slots if slot not in booked_slots]
        #
        #     existing_bookings = Bookings.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
        #                                                 date=date)
        #     print("gowda")
        #     print(existing_bookings)
        #     print("sekar")
        #
        #     booked_slots = set()
        #     for booking in existing_bookings:
        #         start_time_str = booking.start_time.strftime("%H:%M")
        #         end_time_str = booking.end_time.strftime("%H:%M")
        #         booked_slots.add((start_time_str, end_time_str))
        #     print("vv")
        #     print(booked_slots)
        #     print("andhra")
        #     available_slots = [slot for slot in final_all_slots if slot not in booked_slots]
        #
        #     all_available_slots.append(available_slots)
        #     print("guna")
        #     print(all_available_slots)
        #     print("shouya")
        #
        #     # a=len(available_slots)
        #     # print(a)
        #     # print(available_slots)
        #     # print(type(available_slots))
        #     # print("done very good job")
        #
        # first_position = len(all_available_slots[0])
        # second_position = len(all_available_slots[1])
        # third_position = len(all_available_slots[2])
        # fourth_position = len(all_available_slots[3])
        # fifth_position = len(all_available_slots[4])
        # six_position = len(all_available_slots[5])
        # seventh_position = len(all_available_slots[6])
        # # print(seventh_position)
        #
        # len_all_slots = []
        #
        # for i, date in enumerate(ex_date):
        #     avlslots = len(all_available_slots[i])
        #     formateedDate = ''
        #     if avlslots != 0 and avlslots <= 10:
        #         formateedDate = date.strftime('%d-%b %a')
        #         len_all_slots.append((i, date, avlslots, formateedDate))
        #     else:
        #         print(f"No slots available for {formateedDate}")
        #
        # # Now len_all_slots contains tuples of (formatted_date, avlslots)
        # print(len_all_slots)
        # print("burger")
        #
        # show_avl_slots = []
        # for j, (i, date, avlslots, formateedDate) in enumerate(len_all_slots[int(value1):int(value2)]):
        #     title = f"{formateedDate} Avl Slots={avlslots}"
        #     show_avl_slots.append({"id": "K" + str(response_id_id) + "/" + str(date),
        #                            "title": title
        #
        #                            })
        # print(show_avl_slots)
        #
        # print("king")
        # payload = json.dumps({
        #     "messaging_product": "whatsapp",
        #     "recipient_type": "individual",
        #     "to": toUser,
        #     "type": "interactive",
        #     "interactive": {
        #         "type": "list",
        #
        #         "body": {
        #             "text": "Avaialability of slots for each date"
        #         },
        #
        #         "action": {
        #             "button": "Choose Date",
        #             "sections": [
        #                 {
        #                     "title": "Date and avl slots",
        #                     "rows": show_avl_slots
        #                 },
        #                 {
        #                     "title": "choose",
        #                     "rows": [
        #                         {
        #                             "id": "P" + str(response_id_id),
        #                             "title": "Previous",
        #
        #                         },
        #                         {
        #                             "id": "X" + str(response_id_id) + str(id_value),
        #                             "title": "Next",
        #
        #                         }
        #
        #                     ]
        #                 }
        #
        #             ]
        #         }
        #     }
        # })
        #
        # response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'P':
        print(response_id)
        x = response_id.index('/')
        print(response_id[x + 1:])
        print(response_id[1:x])
        first_date = response_id[1:x]
        consulta_id = response_id[x + 1:]
        reverse_available_slots = []
        main_available_slots = []
        prev_date = datetime.strptime(str(first_date), "%Y-%m-%d").date()
        next_day = prev_date - timedelta(days=1)
        print("minus")
        print(next_day)
        print("meenaksh")
        consultantName = ''
        consultantSpecialization = ''
        import datetime as dt
        while len(main_available_slots) < 8:
            if next_day != dt.date.today():
                a = 0
                day_of_week = 0
                ex_date = []
                only_dates = []
                formateed_dates = []
                all_available_slots = []
                print("jinja")
                print(next_day)
                print("lalli")
                ex_date.append(next_day)
                zformatted_date = next_day.strftime('%d-%b %a')
                # formatted_date = zformatted_date[:6] + zformatted_date[-5:]
                # print(formatted_date)
                formateed_dates.append(zformatted_date)
                only_date = next_day.strftime('%d-%m-%Y')
                only_dates.append(only_date)
                day_of_week = int(next_day.strftime('%w'))

                print(formateed_dates)

                duration = None  # Initialize to None or an appropriate default value
                slotDuration = Consultant_details.objects.filter(client_id=clientId, id=consulta_id)
                for s_i in slotDuration:
                    duration_str = s_i.slot_duration
                    consultantName = s_i.consultant_name
                    consultantSpecialization = s_i.consultant_specialization
                    numeric_part = int(''.join(filter(str.isdigit, duration_str)))
                    duration = numeric_part

                hslots = []
                not_available_slot = []
                holidayDetails = Consultant_holiday_leaves.objects.filter(client_id=clientId, date=next_day)
                for h_i in holidayDetails:
                    not_available_slots = {
                        "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
                        "end_time": h_i.end_time.strftime("%H:%M"),
                    }
                    not_available_slot.append(not_available_slots)

                for record in not_available_slot:
                    start_time_str1 = record["start_time"]
                    end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format

                    record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
                    record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
                    current_time1 = record_start_time1
                    while current_time1 < record_end_time2:
                        slot_start = current_time1.strftime("%H:%M")
                        current_time1 += timedelta(minutes=duration)
                        slot_end = current_time1.strftime("%H:%M")
                        hslots.append((slot_start, slot_end))
                print("aa")
                print(hslots)
                print("bb")

                all_slots = []
                availability_records = []

                availablityObject = Consultant_availablity.objects.filter(client_id=clientId,
                                                               Consultant_settings_id=consulta_id,
                                                               day_of_week=day_of_week)
                print(availablityObject)
                for a_i in availablityObject:
                    print(a_i.id)
                    availability_record = {
                        "start_time": a_i.start_time.strftime("%H:%M"),
                        "end_time": a_i.end_time.strftime("%H:%M"),
                    }
                    # print(availability_record)
                    # print("mohan")
                    availability_records.append(availability_record)

                for record in availability_records:
                    start_time_str = record["start_time"]
                    end_time_str = record["end_time"]

                    record_start_time = datetime.strptime(start_time_str, "%H:%M")
                    record_end_time = datetime.strptime(end_time_str, "%H:%M")
                    current_time = record_start_time

                    while current_time < record_end_time:
                        slot_start = current_time.strftime("%H:%M")
                        current_time += timedelta(minutes=duration)
                        slot_end = current_time.strftime("%H:%M")
                        all_slots.append((slot_start, slot_end))
                final_all_slots = [slot for slot in all_slots if slot not in hslots]
                print("channi")
                print(final_all_slots)
                print(len(final_all_slots))
                print("keshav")

                # bookingObject = Bookings.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
                #                                         date=current_date)
                # booked_slots = set(booking.notes1 for booking in bookingObject)
                # available_slots = [slot for slot in final_all_slots if slot not in booked_slots]

                existing_bookings = appointment_bookings.objects.filter(client_id=clientId, Consultant_settings_id=consulta_id,
                                                            date=next_day)
                print("gowda")
                print(existing_bookings)
                print("sekar")

                booked_slots = set()
                for booking in existing_bookings:
                    if booking is not None:
                        start_time_str = booking.start_time.strftime("%H:%M")
                        end_time_str = booking.end_time.strftime("%H:%M")
                        booked_slots.add((start_time_str, end_time_str))
                print("vv")
                print(booked_slots)
                print("andhra")
                available_slots = [slot for slot in final_all_slots if slot not in booked_slots]

                if len(available_slots) > 0 and len(available_slots) <= 10:
                    formateedDate = next_day.strftime('%d %b %a').upper()
                    avlslots = len(available_slots)
                    main_available_slots.append((next_day, avlslots, formateedDate))
                    next_day -= dt.timedelta(days=1)
                else:
                    next_day -= dt.timedelta(days=1)
            else:
                next_day -= dt.timedelta(days=1)


        print("mallana")
        print(main_available_slots)
        print("manjakka")
        reversed_list = list(reversed(main_available_slots))
        reverse_available_slots.extend(reversed_list)
        print("reverse")
        print(reverse_available_slots)
        print("reversddddddddd")

        show_avl_slots = []
        show_date = []
        total_avl_slots = 0
        for j, (date, avlslots, formateedDate) in enumerate(reverse_available_slots):
            show_date.append(date)
            total_avl_slots += avlslots
            title = f"{formateedDate} ({avlslots}slots)"
            show_avl_slots.append({"id": "K" + str(consulta_id) + "/" + str(date),
                                   "title": title

                                   })
        print("jagganna")
        print(show_avl_slots)
        print("jaggamma")
        first_date = show_date[0]
        last_date = show_date[-1]
        print(first_date)
        print(last_date)

        print("king")
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": consultantName
                },

                "body": {
                    "text": f"{total_avl_slots} slots are availble from {first_date} to {last_date} choose your date to proceed. choose previous or *next* if you want to opt for _different date_"
                },
                "footer": {
                    "text": consultantSpecialization
                },

                "action": {
                    "button": "Choose Date",
                    "sections": [
                        {
                            "title": "<LIST_SECTION_1_TITLE>",
                            "rows": [
                                {
                                    "id": show_avl_slots[0]["id"],
                                    "title": show_avl_slots[0]["title"],

                                },
                                {
                                    "id": show_avl_slots[1]["id"],
                                    "title": show_avl_slots[1]["title"],

                                },
                                {
                                    "id": show_avl_slots[2]["id"],
                                    "title": show_avl_slots[2]["title"],

                                },
                                {
                                    "id": show_avl_slots[3]["id"],
                                    "title": show_avl_slots[3]["title"],
                                },
                                {
                                    "id": show_avl_slots[4]["id"],
                                    "title": show_avl_slots[4]["title"],

                                },
                                {
                                    "id": show_avl_slots[5]["id"],
                                    "title": show_avl_slots[5]["title"],

                                },
                                {
                                    "id": show_avl_slots[6]["id"],
                                    "title": show_avl_slots[6]["title"],

                                },
                                {
                                    "id": show_avl_slots[7]["id"],
                                    "title": show_avl_slots[7]["title"],

                                },
                                {
                                    "id": "P" + str(first_date) + "/" + str(consulta_id),
                                    "title": "Previous",

                                },
                                {
                                    "id": "X" + str(last_date) + "/" + str(consulta_id),
                                    "title": "NEXT",

                                },

                            ]
                        }

                    ]
                }
            }
        })

        response = requests.request("POST", url, headers=headers, data=payload)



    elif response_id_type == 'D':
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "preview_url": True,
            "recipient_type": "individual",
            "to": toUser,
            "type": "text",
            "text": {
                "body": "Thank You for booking an appointement with us."
            }

        })
        response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'U':
        doctors_id = response_id[1:]
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "interactive",
            "interactive": {
                "type": "button",

                "body": {
                    "text": "Please Check Your Appointments."
                },

                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "Q" + str(doctors_id),
                                "title": "Today/Tomorrow Appts"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "W" + str(doctors_id),
                                "title": "Next 7 Days Appts"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "V" + str(doctors_id),
                                "title": "All Appointements"
                            }
                        }
                    ]
                }
            }
        })

        response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'Q':
        consultantId = response_id[1:]
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        print(today)
        print(tomorrow)
        bookings_today = appointment_bookings.objects.filter(Consultant_settings_id=consultantId, date=today)
        print(bookings_today)
        bookings_tomorrow = appointment_bookings.objects.filter(Consultant_settings_id=consultantId, date=tomorrow)
        print(bookings_tomorrow)
        full_booking_list = bookings_today | bookings_tomorrow
        print("choodu")
        print(full_booking_list)
        print("choodu")
        duration_start = ''
        duration_end = ''
        if full_booking_list.exists():
            for b_i in full_booking_list:
                duration_start = b_i.start_time
                duration_end = b_i.end_time
                apt_date = b_i.date
                customer_number = b_i.customer_phone_number
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "preview_url": True,
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": f'*Today and Tomorrow Appointements are * :\n'
                                f' Customer_Number: {customer_number}\n'
                                f' Start_time: {duration_start}\n'
                                f' End_time:{duration_end}\n'
                                f' Date:{apt_date}\n'

                    }

                })
                response = requests.request("POST", url, headers=headers, data=payload)
        else:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "preview_url": True,
                "recipient_type": "individual",
                "to": toUser,
                "type": "text",
                "text": {
                    "body": "Appointements are not booked for today and tomorrow."
                }

            })
            response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'W':
        consultantId = response_id[1:]
        today = datetime.now().date()
        next_7_days = []
        for i in range(7):
            next_day = today + timedelta(days=i)
            next_7_days.append(next_day)

        bookings_for_next_7_days = []
        for day in next_7_days:
            bookings = appointment_bookings.objects.filter(Consultant_settings_id=consultantId,date=day)
            if bookings.exists():
                bookings_for_next_7_days.extend(bookings)
        print(bookings_for_next_7_days)
        print("gowri")
        if bookings_for_next_7_days:
            for b_i in bookings_for_next_7_days:
                duration_start = b_i.start_time
                duration_end = b_i.end_time
                apt_date = b_i.date
                customer_number = b_i.customer_phone_number
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "preview_url": True,
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": f'*Next 7 days Appointements are * :\n'
                                f' Customer_Number: {customer_number}\n'
                                f' Start_time: {duration_start}\n'
                                f' End_time:{duration_end}\n'
                                f' Date:{apt_date}\n'

                    }

                })
                response = requests.request("POST", url, headers=headers, data=payload)
        else:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "preview_url": True,
                "recipient_type": "individual",
                "to": toUser,
                "type": "text",
                "text": {
                    "body": "Next 7 days no appointements are booked."
                }

            })
            response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'V':
        consultantId = response_id[1:]
        today = datetime.now().date()
        bookings_for_all_days = []
        bookings = appointment_bookings.objects.filter(Consultant_settings_id=consultantId)
        for booking in bookings:
            apt_date = booking.date
            if apt_date >= today:
                bookings_for_all_days.append(booking)

        print("ganesh")
        print(bookings_for_all_days)
        if bookings_for_all_days:
            for b_i in bookings_for_all_days:
                duration_start = b_i.start_time
                duration_end = b_i.end_time
                apt_date = b_i.date
                customer_number = b_i.customer_phone_number
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "preview_url": True,
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": f'*All Appointements are * :\n'
                                f' Customer_Number: {customer_number}\n'
                                f' Start_time: {duration_start}\n'
                                f' End_time:{duration_end}\n'
                                f' Date:{apt_date}\n'

                    }

                })
                response = requests.request("POST", url, headers=headers, data=payload)
        else:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "preview_url": True,
                "recipient_type": "individual",
                "to": toUser,
                "type": "text",
                "text": {
                    "body": "There no appointements booked for you."
                }

            })
            response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'O':
        consultantId = response_id[1:]
        today = datetime.now().date()
        bookings_for_all_days = []
        bookings = appointment_bookings.objects.filter(Consultant_settings_id=consultantId)
        for booking in bookings:
            apt_date = booking.date
            if apt_date < today:
                bookings_for_all_days.append(booking)

        print("ganesh")
        print(bookings_for_all_days)
        if bookings_for_all_days:
            for b_i in bookings_for_all_days:
                duration_start = b_i.start_time
                duration_end = b_i.end_time
                apt_date = b_i.date
                customer_number = b_i.customer_phone_number
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "preview_url": True,
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": f'*Old Appointements are * :\n'
                                f' Customer_Number: {customer_number}\n'
                                f' Start_time: {duration_start}\n'
                                f' End_time:{duration_end}\n'
                                f' Date:{apt_date}\n'

                    }

                })
                response = requests.request("POST", url, headers=headers, data=payload)
        else:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "preview_url": True,
                "recipient_type": "individual",
                "to": toUser,
                "type": "text",
                "text": {
                    "body": "There is no Old appointements booked for you."
                }

            })
            response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'E':
        myappointementsobj = appointment_bookings.objects.filter(customer_phone_number=toUser)
        typeofvisit = ''
        for m_i in myappointementsobj:
            duration_start = m_i.start_time
            duration_end = m_i.end_time
            formatted_start_time1 = duration_start.strftime("%I:%M%p")
            formatted_end_time1 = duration_end.strftime("%I:%M%p")
            date = m_i.date
            status = "Booked" if m_i.status == 1 else "blocked"
            date_obj = datetime.strptime(str(date), '%Y-%m-%d')
            New_date = date_obj.strftime('%d %b %Y')
            typeofvisit = m_i.online_offline
            if typeofvisit == 'offline':
                bookingObj = Consultant_details.objects.filter(id=m_i.Consultant_settings_id)
                consultantName = ''
                specialization = ''
                consultantImage = ''
                for d_i in bookingObj:
                    consultantName = d_i.consultant_name
                    specialization = d_i.consultant_specialization
                    consultantImage = d_i.consultant_image
                print("print")
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                (consultantImage)
                            }
                        },

                        "body": {
                            "text": f'*Appointement details* :\n'
                                    f' *_Name:_* {consultantName}\n'
                                    f' *_Specialization:_* {specialization}\n'
                                    f' *_From:_* {formatted_start_time1} *_to_* {formatted_end_time1}\n'
                                    f' *_Date:_* {New_date}\n'
                                    f' *_Status:_* {status}\n'

                        },

                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "L"+str(m_i.Consultant_settings_id),
                                        "title": "Locate Us"
                                    }
                                }

                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
            elif typeofvisit == 'online':
                pass
    elif response_id_type == 'L':
        print(response_id)
        l_consult_id = response_id[1:]
        consultant_info = Consultant_details.objects.filter(id=l_consult_id)
        consultantPhoto = ''
        consultantAddress = ''
        consultan_loc_name = ''
        for c_i in consultant_info:
            consultantPhoto = c_i.consultant_image
            consultantAddress = c_i.location_address
            consultan_loc_name = c_i.location_name

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "header": {
                    "type": "image",
                    "image": {
                        "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                        (consultantPhoto)
                    }
                },

                "body": {
                    "text": f' *Address* : {consultantAddress}'

                },
                "footer": {
                    "text": consultan_loc_name
                },

                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "G"+str(l_consult_id),
                                "title": "Google Map"
                            }
                        }

                    ]
                }
            }
        })

        response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'G':
        google_location_id = response_id[1:]
        locationinfo = Consultant_details.objects.filter(id=google_location_id)
        for l_i in locationinfo:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "location",
                "location": {
                    "latitude": str(l_i.location_latitude),
                    "longitude": str(l_i.location_longitude),
                    "name": l_i.location_name,
                    "address": l_i.location_address
                }
            })
            response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'F':
        today = datetime.now().date()
        bookings_for_all_days = []
        myappointementsobj = appointment_bookings.objects.filter(customer_phone_number=toUser)
        for booking in myappointementsobj:
            apt_date = booking.date
            if apt_date < today:
                bookings_for_all_days.append(booking)

        print("nagendra")
        print(bookings_for_all_days)

        if bookings_for_all_days:
            for b_i in bookings_for_all_days:
                duration_start = b_i.start_time
                duration_end = b_i.end_time
                apt_date = b_i.date
                formatted_start_time1 = duration_start.strftime("%I:%M%p")
                formatted_end_time1 = duration_end.strftime("%I:%M%p")
                c_obj = Consultant_details.objects.filter(id=b_i.Consultant_settings_id)
                consultant_name = ''
                consultant_specialization = ''
                for o_i in c_obj:
                    consultant_name = o_i.consultant_name
                    consultant_specialization = o_i.consultant_specialization
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "preview_url": True,
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": f'*.Your Last appointements Details are* :\n'
                                f' ConsultantName: {consultant_name}\n'
                                f' Specialization: {consultant_specialization}\n'
                                f' Start_time: {formatted_start_time1}\n'
                                f' End_time:{formatted_end_time1}\n'
                                f' Date:{apt_date}\n'

                    }

                })
                response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'B':
        map_consult_id = response_id[1:]
        consultant_info = Consultant_details.objects.filter(id=map_consult_id)
        consultantPhoto = ''
        consultantAddress = ''
        consultan_loc_name = ''
        for c_i in consultant_info:
            consultantPhoto = c_i.consultant_photo
            consultantAddress = c_i.location_address
            consultan_loc_name = c_i.location_name

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "header": {
                    "type": "image",
                    "image": {
                        "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                        (consultantPhoto)
                    }
                },

                "body": {
                    "text": f' Address: {consultantAddress}'

                },
                "footer": {
                    "text": consultan_loc_name
                },

                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "G" + str(map_consult_id),
                                "title": "Google Map"
                            }
                        }

                    ]
                }
            }
        })

        response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'M':
        map_consult_id = response_id[1:]
        consultant_info = Consultant_details.objects.filter(id=map_consult_id)
        consultantPhoto = ''
        consultantAddress = ''
        consultan_loc_name = ''
        for c_i in consultant_info:
            consultantPhoto = c_i.consultant_photo
            consultantAddress = c_i.location_address
            consultan_loc_name = c_i.location_name

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "header": {
                    "type": "image",
                    "image": {
                        "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                        (consultantPhoto)
                    }
                },

                "body": {
                    "text": f' Address: {consultantAddress}'

                },
                "footer": {
                    "text": consultan_loc_name
                },

                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "G" + str(map_consult_id),
                                "title": "Google Map"
                            }
                        }

                    ]
                }
            }
        })

        response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'Z':
        if resp_id_id == 1:
            maindetails = appointment_settings.objects.filter(client_id=clientId)
            for i in maindetails:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "location",
                    "location": {
                        "latitude":"0",
                        "longitude":"0",
                        "address": i.contactus_address
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
        elif resp_id_id == 2:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "text",
                "text": {
                    "body":"Please Call 18001800 to Contact Hospital Management...."
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'b':
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": toUser,
            "recipient_type": "individual",
            "type": "interactive",
            "interactive": {
                "type": "flow",
                "header": {
                    "type": "text",
                    "text": "signup"
                },
                "body": {
                    "text": "complete the sign up to proceed."
                },
                "footer": {
                    "text": "signup"
                },
                "action": {
                    "name": "flow",
                    "parameters": {
                        "flow_message_version": "3",
                        "flow_action": "navigate",
                        "flow_token": "123erwers",
                        "flow_id": "1344195323152518",
                        "flow_cta": "Sign Up",
                        "flow_action_payload": {
                            "screen": "SIGN_UP",
                            "data": {
                                "id": "0",
                                "title": "Yes"
                            }
                        }
                    }
                }
            }
        })
        response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == 'm':
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": toUser,
            "recipient_type": "individual",
            "type": "interactive",
            "interactive": {
                "type": "flow",
                "header": {
                    "type": "text",
                    "text": "signup"
                },
                "body": {
                    "text": "complete the sign up to proceed."
                },
                "footer": {
                    "text": "signup"
                },
                "action": {
                    "name": "flow",
                    "parameters": {
                        "flow_message_version": "3",
                        "flow_action": "navigate",
                        "flow_token": "123erwers",
                        "flow_id": "340945172010788",
                        "flow_cta": "Details",
                        "flow_action_payload": {
                            "screen": "SIGN_UP",
                            "data": {
                                "id": "0",
                                "title": "Yes"
                            }
                        }
                    }
                }
            }
        })
        response = requests.request("POST", url, headers=headers, data=payload)











def process_ticket_interactive_message(response_id, request,url, headers, toUser, clientId,whatsAppPhoneNumberId,faceBookToken):
    # print(response_id)
    # x=response_id
    # y=str(x)

    response_id_type = response_id[0]
    response_id_id = int(response_id[1:])
    print(response_id_type)
    print(response_id_id)
    # print("33")

    if response_id_type == 'F':
        customer_receive(request, toUser, clientId)
        # print("******")
        if response_id_id == 1:
            bookinginformation = event_settings.objects.filter(client_id=clientId)
            # bookingheadertype = ""
            for b in bookinginformation:
                level_info = b.level_settings
                if level_info == 'none':
                    if b.booking_header_image:
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "image",
                            "image": {
                                "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/" + str(
                                    b.booking_header_image)

                            }
                        })
                        response = requests.request("POST", url, headers=headers, data=payload)
                        time.sleep(2)

                        # print("******")
                        event_name = []
                        event_desc = []
                        event_id = []
                        eventobj = event_master.objects.filter(client_id=clientId, status=1)
                        print(eventobj)
                        for e_i in eventobj:
                            # print(e_i.id)
                            # print(e_i.Event_Name)
                            event_id.append(e_i.id)
                            event_name.append(e_i.Event_Name)
                            event_desc.append(e_i.Event_Description)
                            print(event_name)

                        eventlist = []
                        for i in range(len(event_name)):
                            eventlist.append({"id": "E" + str(event_id[i]),
                                              "title": event_name[i],
                                              "description": event_desc[i]
                                              })
                        if len(event_name) == 1:
                            # print("gggggg")

                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "button",

                                    "body": {
                                        "text": b.booking_message_text if b.booking_message_text else "."
                                    },
                                    "footer": {
                                        "text": b.booking_message_footer
                                    },
                                    "action": {
                                        "buttons": [
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "E" + str(event_id[0]),
                                                    "title": e_i.Event_Name
                                                }
                                            }

                                        ]
                                    }
                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)
                            customer_sent(request, toUser, clientId)
                        else:
                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "list",
                                    "header": {
                                        "type": "text",
                                        "text": b.booking_header_text if b.booking_header_text else "."
                                    },
                                    "body": {
                                        "text": b.booking_message_text if b.booking_message_text else "."
                                    },
                                    "footer": {
                                        "text": b.booking_message_footer
                                    },
                                    "action": {
                                        "button": b.event_list_event_button_name,
                                        "sections": [
                                            {
                                                "title": "Events",
                                                "rows": eventlist
                                            }

                                        ]
                                    }
                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)
                            customer_sent(request, toUser, clientId)
                    else:
                        event_name = []
                        event_desc = []
                        event_id = []
                        eventobj = event_master.objects.filter(client_id=clientId, status=1)
                        print(eventobj)
                        for e_i in eventobj:
                            # print(e_i.id)
                            # print(e_i.Event_Name)
                            event_id.append(e_i.id)
                            event_name.append(e_i.Event_Name)
                            event_desc.append(e_i.Event_Description)
                            print(event_name)

                        eventlist = []
                        for i in range(len(event_name)):
                            eventlist.append({"id": "E" + str(event_id[i]),
                                              "title": event_name[i],
                                              "description": event_desc[i]
                                              })
                        if len(event_name) == 1:
                            # print("gggggg")

                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "button",

                                    "body": {
                                        "text": b.booking_message_text if b.booking_message_text else "."
                                    },
                                    "footer": {
                                        "text": b.booking_message_footer
                                    },
                                    "action": {
                                        "buttons": [
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "E" + str(event_id[0]),
                                                    "title": e_i.Event_Name
                                                }
                                            }

                                        ]
                                    }
                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)
                            customer_sent(request, toUser, clientId)
                        else:
                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "list",
                                    "header": {
                                        "type": "text",
                                        "text": b.booking_header_text if b.booking_header_text else "."
                                    },
                                    "body": {
                                        "text": b.booking_message_text if b.booking_message_text else "."
                                    },
                                    "footer": {
                                        "text": b.booking_message_footer
                                    },
                                    "action": {
                                        "button": b.event_list_event_button_name,
                                        "sections": [
                                            {
                                                "title": "Events",
                                                "rows": eventlist
                                            }

                                        ]
                                    }
                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)
                            customer_sent(request, toUser, clientId)



                elif level_info == 'skiplevel1':
                    print("mohan")
                    EventHeaderImage = ''
                    emasterobj = event_master.objects.filter(client_id=clientId)
                    for listslots_i in emasterobj:
                        EventHeaderImage = listslots_i.Event_Message_Header_Image
                        if EventHeaderImage:

                            slot_name = []
                            slot_desc = []
                            slot_id = []
                            eslots = event_slots.objects.filter(client_id=clientId)
                            for s_i in eslots:
                                # print(s_i.id)
                                slot_id.append(s_i.id)
                                slot_name.append(s_i.Slot_Name)
                                slot_desc.append(s_i.Slot_Description)

                            slotlist = []
                            for l_i in range(len(slot_name)):
                                slotlist.append({"id": "S" + str(slot_id[l_i]),
                                                 "title": slot_name[l_i],
                                                 "description": slot_desc[l_i]
                                                 })

                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "image",
                                "image": {
                                    "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/" + str(
                                        EventHeaderImage)

                                }
                            })
                            response = requests.request("POST", url, headers=headers, data=payload)
                            time.sleep(2)

                            if len(slot_name) == 1:
                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "interactive",
                                    "interactive": {
                                        "type": "button",

                                        "body": {
                                            "text": listslots_i.Slot_Message_Body_Text if listslots_i.Slot_Message_Body_Text else "."
                                        },
                                        "footer": {
                                            "text": listslots_i.Event_Message_Footer_Text
                                        },
                                        "action": {
                                            "buttons": [
                                                {
                                                    "type": "reply",
                                                    "reply": {
                                                        "id": "S" + str(slot_id[0]),
                                                        "title": s_i.Slot_Name
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                })

                                response = requests.request("POST", url, headers=headers, data=payload)
                                customer_sent(request, toUser, clientId)
                            else:

                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "interactive",
                                    "interactive": {
                                        "type": "list",
                                        "header": {
                                            "type": "text",
                                            "text": listslots_i.Event_Message_Header_Text if listslots_i.Event_Message_Header_Text else "."
                                        },
                                        "body": {
                                            "text": listslots_i.Event_Message_Body_Text if listslots_i.Event_Message_Body_Text else "."
                                        },
                                        "footer": {
                                            "text": listslots_i.Event_Message_Footer_Text
                                        },
                                        "action": {
                                            "button": listslots_i.Event_slots_button_name,
                                            "sections": [
                                                {
                                                    "title": "Ticket Slots",
                                                    "rows": slotlist
                                                },

                                            ]
                                        }
                                    }
                                })

                                response = requests.request("POST", url, headers=headers, data=payload)
                                customer_sent(request, toUser, clientId)
                        else:
                            slot_name = []
                            slot_desc = []
                            slot_id = []
                            eslots = event_slots.objects.filter(client_id=clientId)
                            for s_i in eslots:
                                # print(s_i.id)
                                slot_id.append(s_i.id)
                                slot_name.append(s_i.Slot_Name)
                                slot_desc.append(s_i.Slot_Description)

                            slotlist = []
                            for l_i in range(len(slot_name)):
                                slotlist.append({"id": "S" + str(slot_id[l_i]),
                                                 "title": slot_name[l_i],
                                                 "description": slot_desc[l_i]
                                                 })


                            if len(slot_name) == 1:
                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "interactive",
                                    "interactive": {
                                        "type": "button",

                                        "body": {
                                            "text": listslots_i.Slot_Message_Body_Text if listslots_i.Slot_Message_Body_Text else "."
                                        },
                                        "footer": {
                                            "text": listslots_i.Event_Message_Footer_Text
                                        },
                                        "action": {
                                            "buttons": [
                                                {
                                                    "type": "reply",
                                                    "reply": {
                                                        "id": "S" + str(slot_id[0]),
                                                        "title": s_i.Slot_Name
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                })

                                response = requests.request("POST", url, headers=headers, data=payload)
                                customer_sent(request, toUser, clientId)
                            else:

                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "interactive",
                                    "interactive": {
                                        "type": "list",
                                        "header": {
                                            "type": "text",
                                            "text": listslots_i.Event_Message_Header_Text if listslots_i.Event_Message_Header_Text else "."
                                        },
                                        "body": {
                                            "text": listslots_i.Event_Message_Body_Text if listslots_i.Event_Message_Body_Text else "."
                                        },
                                        "footer": {
                                            "text": listslots_i.Event_Message_Footer_Text
                                        },
                                        "action": {
                                            "button": listslots_i.Event_slots_button_name,
                                            "sections": [
                                                {
                                                    "title": "Ticket Slots",
                                                    "rows": slotlist
                                                },

                                            ]
                                        }
                                    }
                                })

                                response = requests.request("POST", url, headers=headers, data=payload)
                                customer_sent(request, toUser, clientId)


                elif level_info == 'skiplevel1and2':
                    slotcatobj1 = event_slots.objects.filter(client_id=clientId)
                    for cat_ii in slotcatobj1:
                        if cat_ii.Slot_message_Header_Image:

                            category_name = []
                            category_desc = []
                            category_id = []
                            catlistobj1 = event_ticket_category.objects.filter(
                                client_id=clientId)
                            for ctg_i in catlistobj1:
                                category_id.append(ctg_i.id)
                                category_name.append(ctg_i.Category_Name)
                                category_desc.append(ctg_i.Category_Description)
                            ctglist = []
                            for g_i in range(len(category_name)):
                                ctglist.append({"id": "C" + str(category_id[g_i]),
                                                "title": category_name[g_i],
                                                "description": category_desc[g_i]
                                                })

                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "image",
                                "image": {
                                    "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/" + str(
                                        cat_ii.Slot_message_Header_Image)

                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)
                            time.sleep(2)

                            if len(category_name) == 1:
                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "interactive",
                                    "interactive": {
                                        "type": "button",

                                        "body": {
                                            "text": cat_ii.Slot_Message_Body_Text if cat_ii.Slot_Message_Body_Text else "."
                                        },
                                        "footer": {
                                            "text": cat_ii.Slot_Message_Footer_Text
                                        },
                                        "action": {
                                            "buttons": [
                                                {
                                                    "type": "reply",
                                                    "reply": {
                                                        "id": "C" + str(category_id[0]),
                                                        "title": ctg_i.Category_Name
                                                    }
                                                }

                                            ]
                                        }
                                    }
                                })

                                response = requests.request("POST", url, headers=headers, data=payload)
                                customer_sent(request, toUser, clientId)
                            else:
                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "interactive",
                                    "interactive": {
                                        "type": "list",
                                        "header": {
                                            "type": "text",
                                            "text": cat_ii.Slot_Message_Header_Text if cat_ii.Slot_Message_Header_Text else "."
                                        },
                                        "body": {
                                            "text": cat_ii.Slot_Message_Body_Text if cat_ii.Slot_Message_Body_Text else "."
                                        },
                                        "footer": {
                                            "text": cat_ii.Slot_Message_Footer_Text
                                        },
                                        "action": {
                                            "button": cat_ii.slot_category_button_name,
                                            "sections": [
                                                {
                                                    "title": "Ticket Category",
                                                    "rows": ctglist
                                                },

                                            ]
                                        }
                                    }
                                })

                                response = requests.request("POST", url, headers=headers, data=payload)
                                customer_sent(request, toUser, clientId)
                        else:
                            category_name = []
                            category_desc = []
                            category_id = []
                            catlistobj1 = event_ticket_category.objects.filter(
                                client_id=clientId)
                            for ctg_i in catlistobj1:
                                category_id.append(ctg_i.id)
                                category_name.append(ctg_i.Category_Name)
                                category_desc.append(ctg_i.Category_Description)
                            ctglist = []
                            for g_i in range(len(category_name)):
                                ctglist.append({"id": "C" + str(category_id[g_i]),
                                                "title": category_name[g_i],
                                                "description": category_desc[g_i]
                                                })


                            if len(category_name) == 1:
                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "interactive",
                                    "interactive": {
                                        "type": "button",

                                        "body": {
                                            "text": cat_ii.Slot_Message_Body_Text if cat_ii.Slot_Message_Body_Text else "."
                                        },
                                        "footer": {
                                            "text": cat_ii.Slot_Message_Footer_Text
                                        },

                                        "action": {
                                            "buttons": [
                                                {
                                                    "type": "reply",
                                                    "reply": {
                                                        "id": "C" + str(category_id[0]),
                                                        "title": ctg_i.Category_Name
                                                    }
                                                }

                                            ]
                                        }
                                    }
                                })

                                response = requests.request("POST", url, headers=headers, data=payload)
                                customer_sent(request, toUser, clientId)
                            else:
                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "interactive",
                                    "interactive": {
                                        "type": "list",
                                        "header": {
                                            "type": "text",
                                            "text": cat_ii.Slot_Message_Header_Text if cat_ii.Slot_Message_Header_Text else "."
                                        },
                                        "body": {
                                            "text": cat_ii.Slot_Message_Body_Text if cat_ii.Slot_Message_Body_Text else "."
                                        },
                                        "footer": {
                                            "text": cat_ii.Slot_Message_Footer_Text
                                        },
                                        "action": {
                                            "button": cat_ii.slot_category_button_name,
                                            "sections": [
                                                {
                                                    "title": "Ticket Category",
                                                    "rows": ctglist
                                                },

                                            ]
                                        }
                                    }
                                })

                                response = requests.request("POST", url, headers=headers, data=payload)
                                customer_sent(request, toUser, clientId)

        elif response_id_id == 2:
            customer_receive(request, toUser, clientId)
            print("aa")
            mytickets = ticket_information.objects.filter(customer_phone_number=toUser)
            print(mytickets)
               
            contactbuttonname = ''
            transferbuttonname = ''
            transfer_ticket=''
            my_ticket_info = event_settings.objects.filter(client_id=clientId)
            for my_i in my_ticket_info:
                contactbuttonname = contactbuttonname + my_i.contact_button_name
                transferbuttonname = transferbuttonname + my_i.transfer_button_name
                transfer_ticket = transfer_ticket + my_i.transfer_ticket
            if transfer_ticket == 'yes':
                for m in mytickets:
                    print("chai")
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "button",
                            "header": {
                                "type": "image",
                                "image": {
                                    "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(m.ticket_QR)
                                }
                            },
                            "body": {
                                "text": m.ticket_number
                            },
                            # "footer": {
                            #     "text": "."
                            # },
                            "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "M" + str(m.id),
                                            "title": contactbuttonname
                                        }
                                    },
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "G" + str(m.id),
                                            "title": transferbuttonname
                                        }
                                    }

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)
                    customer_sent(request, toUser, clientId)
            else:
                for mytick_i in mytickets:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "image",
                        "image": {
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/" + str(
                                mytick_i.ticket_QR)

                        }
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    customer_sent(request, toUser, clientId)







        elif response_id_id == 3:
            customer_receive(request, toUser, clientId)
            cancel_information = event_settings.objects.filter(client_id=clientId)
            cancelticketmessagebody = ''
            for cancel in cancel_information:
                cancelticketmessagebody = cancelticketmessagebody + cancel.cancel_ticket_message_body
                if cancel.cancel_ticket_header_image:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "image",
                        "image": {
                            "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
                                cancel.cancel_ticket_header_image)

                        }
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    time.sleep(2)

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "preview_url": True,
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "text",
                        "text": {
                            "body": cancelticketmessagebody if cancelticketmessagebody else "."
                        }

                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    customer_sent(request, toUser, clientId)
                else:

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "preview_url": True,
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "text",
                        "text": {
                            "body": cancelticketmessagebody if cancelticketmessagebody else "."
                        }

                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    customer_sent(request, toUser, clientId)




    elif response_id_type == 'E':
        customer_receive(request, toUser, clientId)
        if event_master.objects.filter(client_id=clientId,
                                       id=response_id_id):
            EventHeaderImage = ''
            emasterobj = event_master.objects.filter(client_id=clientId, id=response_id_id)
            for listslots_i in emasterobj:
                EventHeaderImage = listslots_i.Event_Message_Header_Image
                if EventHeaderImage:
                    slot_name = []
                    slot_desc = []
                    slot_id = []
                    eslots = event_slots.objects.filter(event_master_id=listslots_i.id, client_id=clientId)
                    for s_i in eslots:
                        # print(s_i.id)
                        slot_id.append(s_i.id)
                        slot_name.append(s_i.Slot_Name)
                        slot_desc.append(s_i.Slot_Description)

                    slotlist = []
                    for l_i in range(len(slot_name)):
                        slotlist.append({"id": "S" + str(slot_id[l_i]),
                                         "title": slot_name[l_i],
                                         "description": slot_desc[l_i]
                                         })

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "image",
                        "image": {
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/" + str(EventHeaderImage)

                        }
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    time.sleep(2)

                    if len(slot_name) == 1:
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "button",

                                "body": {
                                    "text": listslots_i.Event_Message_Body_Text if listslots_i.Event_Message_Body_Text else "."
                                },
                                "footer": {
                                    "text": listslots_i.Event_Message_Footer_Text
                                },
                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "S" + str(slot_id[0]),
                                                "title": s_i.Slot_Name
                                            }
                                        }
                                    ]
                                }
                            }
                        })

                        response = requests.request("POST", url, headers=headers, data=payload)
                        customer_sent(request, toUser, clientId)
                    else:

                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "list",
                                "header": {
                                    "type": "text",
                                    "text": listslots_i.Event_Message_Header_Text if listslots_i.Event_Message_Header_Text else "."
                                },
                                "body": {
                                    "text": listslots_i.Event_Message_Body_Text if listslots_i.Event_Message_Body_Text else "."
                                },
                                "footer": {
                                    "text": listslots_i.Event_Message_Footer_Text
                                },
                                "action": {
                                    "button": listslots_i.Event_slots_button_name,
                                    "sections": [
                                        {
                                            "title": "Ticket Slots",
                                            "rows": slotlist
                                        },

                                    ]
                                }
                            }
                        })

                        response = requests.request("POST", url, headers=headers, data=payload)
                        customer_sent(request, toUser, clientId)
                else:
                    slot_name = []
                    slot_desc = []
                    slot_id = []
                    eslots = event_slots.objects.filter(event_master_id=listslots_i.id, client_id=clientId)
                    for s_i in eslots:
                        # print(s_i.id)
                        slot_id.append(s_i.id)
                        slot_name.append(s_i.Slot_Name)
                        slot_desc.append(s_i.Slot_Description)

                    slotlist = []
                    for l_i in range(len(slot_name)):
                        slotlist.append({"id": "S" + str(slot_id[l_i]),
                                         "title": slot_name[l_i],
                                         "description": slot_desc[l_i]
                                         })



                    if len(slot_name) == 1:
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "button",

                                "body": {
                                    "text": listslots_i.Event_Message_Body_Text if listslots_i.Event_Message_Body_Text else "."
                                },
                                "footer": {
                                    "text": listslots_i.Event_Message_Footer_Text
                                },
                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "S" + str(slot_id[0]),
                                                "title": s_i.Slot_Name
                                            }
                                        }
                                    ]
                                }
                            }
                        })

                        response = requests.request("POST", url, headers=headers, data=payload)
                        customer_sent(request, toUser, clientId)
                    else:

                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "list",
                                "header": {
                                    "type": "text",
                                    "text": listslots_i.Event_Message_Header_Text if listslots_i.Event_Message_Header_Text else "."
                                },
                                "body": {
                                    "text": listslots_i.Event_Message_Body_Text if listslots_i.Event_Message_Body_Text else "."
                                },
                                "footer": {
                                    "text": listslots_i.Event_Message_Footer_Text
                                },
                                "action": {
                                    "button": listslots_i.Event_slots_button_name,
                                    "sections": [
                                        {
                                            "title": "Ticket Slots",
                                            "rows": slotlist
                                        },

                                    ]
                                }
                            }
                        })

                        response = requests.request("POST", url, headers=headers, data=payload)
                        customer_sent(request, toUser, clientId)


    elif response_id_type == 'S':
        customer_receive(request, toUser, clientId)
        if event_slots.objects.filter(client_id=clientId, id=response_id_id):
            slotcatobj1  = event_slots.objects.filter(client_id=clientId, id=response_id_id)
            for cat_ii in slotcatobj1 :
                if cat_ii.Slot_message_Header_Image:
                    category_name = []
                    category_desc = []
                    category_id = []
                    catlistobj1 = event_ticket_category.objects.filter(event_slots_id=cat_ii.id,
                                                                       client_id=clientId)
                    for ctg_i in catlistobj1:
                        category_id.append(ctg_i.id)
                        category_name.append(ctg_i.Category_Name)
                        category_desc.append(ctg_i.Category_Description)
                    ctglist = []
                    for g_i in range(len(category_name)):
                        ctglist.append({"id": "C" + str(category_id[g_i]),
                                        "title": category_name[g_i],
                                        "description": category_desc[g_i]
                                        })

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "image",
                        "image": {
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/" + str(
                                cat_ii.Slot_message_Header_Image)

                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)
                    time.sleep(2)

                    if len(category_name) == 1:
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "button",

                                "body": {
                                    "text": cat_ii.Slot_Message_Body_Text if cat_ii.Slot_Message_Body_Text else "."
                                },
                                "footer": {
                                    "text": cat_ii.Slot_Message_Footer_Text
                                },
                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "C" + str(category_id[0]),
                                                "title": ctg_i.Category_Name
                                            }
                                        }

                                    ]
                                }
                            }
                        })

                        response = requests.request("POST", url, headers=headers, data=payload)
                        customer_sent(request, toUser, clientId)
                    else:
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "list",
                                "header": {
                                    "type": "text",
                                    "text": cat_ii.Slot_Message_Header_Text if cat_ii.Slot_Message_Header_Text else "."
                                },
                                "body": {
                                    "text": cat_ii.Slot_Message_Body_Text if cat_ii.Slot_Message_Body_Text else "."
                                },
                                "footer": {
                                    "text": cat_ii.Slot_Message_Footer_Text
                                },
                                "action": {
                                    "button": cat_ii.slot_category_button_name,
                                    "sections": [
                                        {
                                            "title": "Ticket Category",
                                            "rows": ctglist
                                        },

                                    ]
                                }
                            }
                        })

                        response = requests.request("POST", url, headers=headers, data=payload)
                        customer_sent(request, toUser, clientId)
                else:
                    category_name = []
                    category_desc = []
                    category_id = []
                    catlistobj1 = event_ticket_category.objects.filter(event_slots_id=cat_ii.id,
                                                                       client_id=clientId)
                    for ctg_i in catlistobj1:
                        category_id.append(ctg_i.id)
                        category_name.append(ctg_i.Category_Name)
                        category_desc.append(ctg_i.Category_Description)
                    ctglist = []
                    for g_i in range(len(category_name)):
                        ctglist.append({"id": "C" + str(category_id[g_i]),
                                        "title": category_name[g_i],
                                        "description": category_desc[g_i]
                                        })



                    if len(category_name) == 1:
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "button",

                                "body": {
                                    "text": cat_ii.Slot_Message_Body_Text if cat_ii.Slot_Message_Body_Text else "."
                                },
                                "footer": {
                                    "text": cat_ii.Slot_Message_Footer_Text
                                },
                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "C" + str(category_id[0]),
                                                "title": ctg_i.Category_Name
                                            }
                                        }

                                    ]
                                }
                            }
                        })

                        response = requests.request("POST", url, headers=headers, data=payload)
                        customer_sent(request, toUser, clientId)
                    else:
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "list",
                                "header": {
                                    "type": "text",
                                    "text": cat_ii.Slot_Message_Header_Text if cat_ii.Slot_Message_Header_Text else "."
                                },
                                "body": {
                                    "text": cat_ii.Slot_Message_Body_Text if cat_ii.Slot_Message_Body_Text else "."
                                },
                                "footer": {
                                    "text": cat_ii.Slot_Message_Footer_Text
                                },
                                "action": {
                                    "button": cat_ii.slot_category_button_name,
                                    "sections": [
                                        {
                                            "title": "Ticket Category",
                                            "rows": ctglist
                                        },

                                    ]
                                }
                            }
                        })

                        response = requests.request("POST", url, headers=headers, data=payload)
                        customer_sent(request, toUser, clientId)


    elif response_id_type == "C":
        customer_receive(request, toUser, clientId)
        all_descriptions = []
        description_value = event_settings.objects.filter(client_id=clientId)
        for desc_i in description_value:
            all_descriptions.append(desc_i.ticketcount1_desc)
            all_descriptions.append(desc_i.ticketcount2_desc)
            all_descriptions.append(desc_i.ticketcount3_desc)
            all_descriptions.append(desc_i.ticketcount4_desc)
            all_descriptions.append(desc_i.ticketcount5_desc)
            all_descriptions.append(desc_i.ticketcount6_desc)
            all_descriptions.append(desc_i.ticketcount7_desc)
            all_descriptions.append(desc_i.ticketcount8_desc)
            all_descriptions.append(desc_i.ticketcount9_desc)
        if all_descriptions:
            ticketslist = []
            for i in range(1, 10):
                final_descriptions = all_descriptions[i - 1]
                ticketslist.append({"id": "T" + str(i) + str(response_id_id),
                                    "title": i,
                                    "description": final_descriptions
                                    })

            category = event_ticket_category.objects.filter(client_id=clientId, id=response_id_id)
            for j in category:
                if j.Category_Message_Header_Image:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "image",
                        "image": {
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/" + str(
                                j.Category_Message_Header_Image)

                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)
                    time.sleep(1)

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "list",
                            "header": {
                                "type": "text",
                                "text": j.Category_Message_Header_Text if j.Category_Message_Header_Text else "."
                            },
                            "body": {
                                "text": j.Category_Message_Body_Text if j.Category_Message_Body_Text else "."
                            },
                            "footer": {
                                "text": j.Category_Message_Footer_Text
                            },
                            "action": {
                                "button": j.Number_Of_Ticket_Button_Name,
                                "sections": [
                                    {
                                        "rows": ticketslist
                                    },

                                ]
                            }
                        }
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    customer_sent(request, toUser, clientId)
                else:

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "list",
                            "header": {
                                "type": "text",
                                "text": j.Category_Message_Header_Text if j.Category_Message_Header_Text else "."
                            },
                            "body": {
                                "text": j.Category_Message_Body_Text if j.Category_Message_Body_Text else "."
                            },
                            "footer": {
                                "text": j.Category_Message_Footer_Text
                            },
                            "action": {
                                "button": j.Number_Of_Ticket_Button_Name,
                                "sections": [
                                    {
                                        "rows": ticketslist
                                    },

                                ]
                            }
                        }
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    customer_sent(request, toUser, clientId)

        else:
            ticketslist = []
            for i in range(1, 10):
                # final_descriptions = all_descriptions[i - 1]
                ticketslist.append({"id": "T" + str(i) + str(response_id_id),
                                    "title": i,

                                    })

            category = event_ticket_category.objects.filter(client_id=clientId, id=response_id_id)
            for j in category:
                if j.Category_Message_Header_Image:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "image",
                        "image": {
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/" + str(
                                j.Category_Message_Header_Image)

                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)
                    time.sleep(2)

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "list",
                            "header": {
                                "type": "text",
                                "text": j.Category_Message_Header_Text if j.Category_Message_Header_Text else "."
                            },
                            "body": {
                                "text": j.Category_Message_Body_Text if j.Category_Message_Body_Text else "."
                            },
                            "footer": {
                                "text": j.Category_Message_Footer_Text
                            },
                            "action": {
                                "button": j.Number_Of_Ticket_Button_Name,
                                "sections": [
                                    {
                                        "rows": ticketslist
                                    },

                                ]
                            }
                        }
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    customer_sent(request, toUser, clientId)
                else:

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "list",
                            "header": {
                                "type": "text",
                                "text": j.Category_Message_Header_Text if j.Category_Message_Header_Text else "."
                            },
                            "body": {
                                "text": j.Category_Message_Body_Text if j.Category_Message_Body_Text else "."
                            },
                            "footer": {
                                "text": j.Category_Message_Footer_Text
                            },
                            "action": {
                                "button": j.Number_Of_Ticket_Button_Name,
                                "sections": [
                                    {
                                        "rows": ticketslist
                                    },

                                ]
                            }
                        }
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    customer_sent(request, toUser, clientId)



    elif response_id_type == "T":
        customer_receive(request, toUser, clientId)
        response_id_id_n = int(response_id[1])
        response_id_id_c = int(response_id[2:])
        reference_id = uuid.uuid4()
        # print(response_id_id_n)
        # print(response_id_id_c)
        # print(reference_id)

        category_details = event_ticket_category.objects.filter(client_id = clientId,id = response_id_id_c)
        cart_details = event_ticket_cart_details(client_id=clientId)
        cart_header = event_ticket_cart_header(client_id=clientId)
        cart_header.customer_phone_number = str(toUser)
        cart_amount = 0
        ticket_event_name = ""
        for i in category_details:
            cart_header.cart_amount = i.Category_Price * response_id_id_n
            cart_header.total_tickets = response_id_id_n
            cart_header.payment_reference_id = reference_id
            cart_header.save()

            cart_header_detail = event_ticket_cart_header.objects.filter(client_id = clientId,
                                                                         total_tickets = response_id_id_n, payment_reference_id = reference_id)

            header_cart_id = ''
            # cart_amount = ''
            for j in cart_header_detail:
                header_cart_id = j.id
                print(header_cart_id)
                cart_amount = j.cart_amount
                # print(header_cart_id)
                break
            cart_details.cart_id_id = header_cart_id
            cart_details.event_id = i.event_master_id
            cart_details.slot_id = i.event_slots_id
            cart_details.category_id = response_id_id_c
            cart_details.ticket_price = i.Category_Price
            cart_details.number_of_tickets = response_id_id_n
            cart_details.save()
            break



        ticket_cart_details = event_ticket_cart_details.objects.filter(client_id=clientId)
        for t in ticket_cart_details:
            # ticket_event = t.event_id
            event_name = event_ticket_cart_details.objects.filter(client_id = clientId,id = t.id)

            for e in event_name:
                ticket_event = e.event_id
                eventinfo = event_master.objects.filter(client_id = clientId,id=ticket_event)
                for e in eventinfo:
                    ticket_event_name = e.Event_Name
                    break

        phonenumber = facebook_details.objects.filter(client_id=clientId,fb_phone_number_id=whatsAppPhoneNumberId)
        client_number = ''
        for p in phonenumber:
            client_number = p.fb_whatsapp_number

    # ---------------"blocking the tickets"----------------------
        Availbletickets = ticket_information.objects.filter(client_id=clientId,event_ticket_category_id=response_id_id_c,ticket_status=10)
        if Availbletickets.exists():
            selected_tickets = []
            for C_i in Availbletickets[:response_id_id_n]:
                if C_i.ticket_status == 10:
                    C_i.ticket_status = 20
                    C_i.payment_reference_id = reference_id
                    C_i.save()
                    selected_tickets.append(C_i.id)
                else:
                    break
            if len(selected_tickets) < response_id_id_n:
                for S_i in selected_tickets:
                    updatestatus = ticket_information.objects.filter(id=S_i)
                    for U_i in updatestatus:
                        U_i.ticket_status = 10
                        U_i.save()
                updatesettings = event_settings.objects.filter(client_id=clientId)
                ticketsnotavailable = ''
                for US_i in updatesettings:
                    ticketsnotavailable = ticketsnotavailable + US_i.tickets_not_available_message_body
                    secondnumber = US_i.second_number
                    if US_i.tickets_not_availble_header_image:
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "image",
                            "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
                                    US_i.tickets_not_availble_header_image)

                            }
                        })
                        response = requests.request("POST", url, headers=headers, data=payload)
                        time.sleep(2)
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "preview_url": True,
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "text",
                            "text": {
                                "body": US_i.tickets_not_available_message_body if US_i.tickets_not_available_message_body else "."
                            }

                        })
                        response = requests.request("POST", url, headers=headers, data=payload)
                        customer_sent(request, toUser, clientId)
                        print("11111")
                        update_second_number(request, url, headers, toUser, clientId, secondnumber)
                        return
                    else:

                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "preview_url": True,
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "text",
                            "text": {
                                "body": US_i.tickets_not_available_message_body if US_i.tickets_not_available_message_body else "."
                            }

                        })
                        response = requests.request("POST", url, headers=headers, data=payload)
                        customer_sent(request, toUser, clientId)
                        print("11111")
                        update_second_number(request, url, headers, toUser, clientId, secondnumber)
                    return
            else:
                print("tickets booked successfully")
        else:
            updatesettingsnew = event_settings.objects.filter(client_id=clientId)
            ticketsnotavailablecheck = ''
            for n_i in updatesettingsnew:
                # ticketsnotavailable = ticketsnotavailablecheck + n_i.tickets_not_available_message_body
                secondnumber = n_i.second_number
                if n_i.tickets_not_availble_header_image:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "image",
                        "image": {
                            "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
                                n_i.tickets_not_availble_header_image)

                        }
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    time.sleep(2)
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "preview_url": True,
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "text",
                        "text": {
                            "body": n_i.tickets_not_available_message_body if n_i.tickets_not_available_message_body else "."
                        }

                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    customer_sent(request, toUser, clientId)
                    update_second_number(request, url, headers, toUser, clientId, secondnumber)
                    return
                else:
                    print("kolkata")

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "preview_url": True,
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "text",
                        "text": {
                            "body": n_i.tickets_not_available_message_body if n_i.tickets_not_available_message_body else "."
                        }

                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    customer_sent(request, toUser, clientId)
                    update_second_number(request, url, headers, toUser, clientId, secondnumber)
            return
        
        # if Availbletickets.count() < response_id_id_n:
        #     for B_i in Availbletickets[:response_id_id_n]:
        #         B_i.ticket_status = 20
        #         B_i.save()
        # else:
        #     for A_i in Availbletickets[:response_id_id_n]:
        #         A_i.ticket_status = 20
        #         A_i.save()
        # -------testgeneral link---------
        # detailslink = "https://vmart.ai"+ "/infoform/" + toUser + str(clientId) + '/'
        # print("fel")
        
        # payload = json.dumps({
        #     "messaging_product": "whatsapp",
        #     "to": toUser,
        #     "text": {
        #         # "preview_url": True,
        #         "body": 'Please provide the contact details through this link :' + detailslink
        #     }
        # })
        # response = requests.request("POST", url, headers=headers, data=payload)
        # customer_sent(request, toUser, clientId)
        # ---------------------Test Mode------------------------------
        # url = "https://api.razorpay.com/v1/payment_links"

        # payload = json.dumps({
        #     "amount": cart_amount * 100,
        #     # c= cart_amount * 100,
        #     "currency": "INR",
        #     "accept_partial": False,
        #     "first_min_partial_amount": 0,
        #     "expire_by": 1691097057,
        #     "reference_id": str(reference_id),
        #     "description": ticket_event_name,
        #     "customer": {
        #         "name": "Gaurav Kumar",
        #         "contact": "+918494863493",
        #         "email": "gaurav.kumar@example.com"
        #     },
        #     "notify": {
        #         "sms": True,
        #         "email": True
        #     },
        #     "reminder_enable": True,
        #     "notes": {
        #         "policy_name": "Jeevan Bima"
        #     },
        #     "callback_url": f"https://wa.me/{client_number}",
        #     "callback_method": "get"
        # })
        # headers = {
        #     'Authorization': 'Basic cnpwX3Rlc3RfYXg4a2VCcUdZdkkxVzk6dnUzYVZRamE0WlA4Q2FjR0szOWZtMHd1',
        #     'Content-Type': 'application/json'
        # }

        # response = requests.request("POST", url, headers=headers, data=payload)
        # -------------------------Live Mode-----------------------------------------------------
        print(reference_id)
        print(cart_amount)
        url = "https://api.razorpay.com/v1/payment_links"

        payload = json.dumps({
            "amount": cart_amount * 100,
            "currency": "INR",
            "accept_partial": False,
            "first_min_partial_amount":0,
            # "expire_by": 1691097057,
            "reference_id": "T" + str(reference_id),
            "description": str(reference_id),
            "customer": {
                "name": "Gaurav Kumar",
                "contact": "918494863493",
                "email": "gaurav.kumar@example.com"
            },
            "notify": {
                "sms": True,
                "email": True
            },
            "reminder_enable": True,
            "notes": {
                "polacy_name": "T" + str(reference_id)
            },
            "callback_url": f"https://wa.me/{client_number}",
            "callback_method": "get"
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic cnpwX2xpdmVfSU83R0Vyckkyam9RYXQ6aGt2SVhTZkpvM0x2TWhYaGx5VUpoWTBH'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        a = response.text
        json_str = json.dumps(a)
        b = json.loads(json_str)
        c = response.json()
        print(c)
        payment_link = c['short_url']
        razorpay_payment_link = payment_link[17:]
        print(payment_link)

        url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
        headers = {
            'Authorization': 'Bearer ' + faceBookToken,
            'Content-Type': 'application/json'
        }

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "template",
            "template": {
                "name": "vailo_razorpay_link",
                "language": {
                    "code": "en_US"
                },
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": cart_amount
                            }
                        ]
                    },
                    {
                        "type": "button",
                        "sub_type": "url",
                        "index": "0",
                        "parameters": [
                            {
                                "type": "text",
                                "text": razorpay_payment_link
                            }
                        ]
                    }
                ]
            }
        })
        response = requests.request("POST", url, headers=headers, data=payload)
        customer_sent(request, toUser, clientId)

        

        payment_details = payment_gateway_details.objects.filter(client_id=clientId)
        payment_gateway_info = {}
        for payment in payment_details:
            payment_gateway_info[payment.payment_gateway] = {
                'gateway_id': payment.gateway_id,
                'gateway_key': payment.gateway_key
            }
        razorpay_gateway_id = payment_gateway_info['razorpay']['gateway_id']
        razorpay_gateway_key = payment_gateway_info['razorpay']['gateway_key']

        cashfree_gateway_id = payment_gateway_info['cashfree']['gateway_id']
        cashfree_gateway_key = payment_gateway_info['cashfree']['gateway_key']

        paypal_gateway_id = payment_gateway_info['paypal']['gateway_id']
        paypal_gateway_key = payment_gateway_info['paypal']['gateway_key']

        stripe_gateway_id = payment_gateway_info['stripe']['gateway_id']
        stripe_gateway_key = payment_gateway_info['stripe']['gateway_key']






        payment_details = payment_settings.objects.filter(client_id=clientId)
        payementgateway = ''
        for payment_i in payment_details:
            payementgateway = payementgateway + payment_i.payment_gateway



        print(payementgateway)
        if payementgateway == 'razorpay':
            url = "https://api.razorpay.com/v1/payment_links"

            payload = json.dumps({
                "amount": cart_amount * 100,
                # c= cart_amount * 100,
                "currency": "INR",
                "accept_partial": False,
                "first_min_partial_amount": 0,
                "expire_by": 1691097057,
                "reference_id": str(reference_id),
                "description": ticket_event_name,
                "customer": {
                    "name": "Mohan Kumar",
                    "contact": "+918494863493",
                    "email": "gaurav.kumar@example.com"
                },
                "notify": {
                    "sms": True,
                    "email": True
                },
                "reminder_enable": True,
                "notes": {
                    "fail_id": str(reference_id)
                },
                "callback_url": f"https://wa.me/{client_number}",
                "callback_method": "get"
            })
            headers = {
                'Authorization': 'Basic cnpwX3Rlc3RfYXg4a2VCcUdZdkkxVzk6dnUzYVZRamE0WlA4Q2FjR0szOWZtMHd1',
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            a = response.text
            json_str = json.dumps(a)
            b = json.loads(json_str)
            c = response.json()
            print(c)
            payment_link = c['short_url']
            razorpay_payment_link = payment_link[17:]
            print(payment_link)

            url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
            headers = {
                'Authorization': 'Bearer ' + faceBookToken,
                'Content-Type': 'application/json'
            }

            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "template",
                "template": {
                    "name": "vailo_razorpay_link",
                    "language": {
                        "code": "en_US"
                    },
                    "components": [
                        {
                            "type": "body",
                            "parameters": [
                                {
                                    "type": "text",
                                    "text": cart_amount
                                }
                            ]
                        },
                        {
                            "type": "button",
                            "sub_type": "url",
                            "index": "0",
                            "parameters": [
                                {
                                    "type": "text",
                                    "text": razorpay_payment_link
                                }
                            ]
                        }
                    ]
                }
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            customer_sent(request, toUser, clientId)

        elif payementgateway == 'cashfree':
            url = "https://test.cashfree.com/api/v1/order/create"

            payload = {
                "appId": "TEST3931154d6e90b54bfbc3b4946d511393",
                "secretKey": "TEST701a10a8d7389d719903c77dda9fa993fbc0db63",
                "orderId": reference_id,
                "orderAmount": "1",
                "orderCurrency": "INR",
                "orderNote": "pay",
                "customerName": "Mohan",
                "customeremail": "abcd@gmail.com",
                "customerPhone": "8494863493",
                "returnUrl": "https://cashfree.com"
            }

            response = requests.request("POST", url, data=payload)
            data = json.loads(response.text)
            payment_link = data['payment_link']

            url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
            headers = {
                'Authorization': 'Bearer ' + faceBookToken,
                'Content-Type': 'application/json'
            }

            payload = json.dumps({
                "messaging_product": "whatsapp",
                "to": toUser,
                "text": {
                    "preview_url": True,
                    "body": payment_link
                }
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            customer_sent(request, toUser, clientId)

        elif payementgateway == 'paypal':

            client_id = 'ARZXGxv02vGOAL5nflRoCkm0v-cB49sRiFFp5bSM14qWTL62Wyqzr72OuM4kBLD-AjQaorEPvCD4aTYw'

            client_secret = 'EPGRkm46ShkoFxfMhXQ18_yNS_i_I_092ej6WsCs9DoNlklbnRmI8v-5s_jeewYT-4w7OIDfqG_eNAtZ'

            credentials = f'{client_id}:{client_secret}'
            encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

            headers = {
                'Content-Type': 'application/json',
                'PayPal-Request-Id': reference_id,
                'Authorization': f'Basic {encoded_credentials}'
            }

            data = {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "reference_id": reference_id,
                        "amount": {
                            "currency_code": "USD",
                            "value": "100.00"
                        },
                        "shipping": {
                            "address": {
                                "address_line_1": "1234 Shipping Street",
                                "address_line_2": "Apt 5",
                                "admin_area_2": "San Jose",
                                "admin_area_1": "CA",
                                "postal_code": "95131",
                                "country_code": "US"
                            }
                        }
                    }
                ],
                "payment_source": {
                    "paypal": {
                        "experience_context": {
                            "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                            "payment_method_selected": "PAYPAL",
                            "brand_name": "EXAMPLE INC",
                            "locale": "en-US",
                            "landing_page": "LOGIN",
                            "shipping_preference": "SET_PROVIDED_ADDRESS",
                            "user_action": "PAY_NOW",
                            "return_url": "https://vailo.ai",
                            "cancel_url": "https://example.com/cancelUrl"
                        }
                    }
                }
            }

            response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, json=data)
            # print(response.text)
            data = json.loads(response.text)
            paypal_link = data['links'][1]['href']

            url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
            headers = {
                'Authorization': 'Bearer ' + faceBookToken,
                'Content-Type': 'application/json'
            }

            payload = json.dumps({
                "messaging_product": "whatsapp",
                "to": toUser,
                "text": {
                    "preview_url": True,
                    "body": paypal_link
                }
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            customer_sent(request, toUser, clientId)

        elif payementgateway == 'stripe':

            stripe.api_key = 'sk_test_51NIQFXHJyczfKFYaXcrD40gkA78ly5cHuKXemABW915nMfDNnvBwbyK8mgHtfXq7SdCnz0BjaX6PF2ZOhwzkw0fu00Ej9rw296'

            # id = reference_id  # Replace with your unique reference ID logic

            session = stripe.checkout.Session.create(
                success_url='https://vailo.ai',
                cancel_url='https://example.com/cancel',
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': 500,
                            'product_data': {
                                'name': 'Product Name',
                            },
                        },

                        'quantity': 1,
                    },
                ],
                mode='payment',
                metadata={
                    'reference_id': reference_id,
                }
            )

            payment_link_url = session.url
            url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
            headers = {
                'Authorization': 'Bearer ' + faceBookToken,
                'Content-Type': 'application/json'
            }

            payload = json.dumps({
                "messaging_product": "whatsapp",
                "to": toUser,
                "text": {
                    "preview_url": True,
                    "body": payment_link_url
                }
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            customer_sent(request, toUser, clientId)


    elif response_id_type == "M":
         
         customer_receive(request, toUser, clientId)
    #     updateticket = ticket_information.objects.filter(id=response_id_id)
    #     for u_i in updateticket:
    #         u_i.ticket_status = 40
    #         u_i.save()

         updateticketinfo = event_settings.objects.filter(client_id=clientId)
         contactmessagebody = ''
         for t_i in updateticketinfo:
            contactmessagebody = contactmessagebody + t_i.cotact_message_text
            if t_i.contact_header_image:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "image",
                    "image": {
                        "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(t_i.contact_header_image)

                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                time.sleep(2)

                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "preview_url": True,
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": contactmessagebody if contactmessagebody else "."
                    }

                })
                response = requests.request("POST", url, headers=headers, data=payload)
                customer_sent(request, toUser, clientId)
            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "preview_url": True,
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": contactmessagebody if contactmessagebody else "."
                    }

                })
                response = requests.request("POST", url, headers=headers, data=payload)
                customer_sent(request, toUser, clientId)



    elif response_id_type == "G":
        customer_receive(request, toUser, clientId)
        phonenumber = facebook_details.objects.filter(client_id=clientId,fb_phone_number_id=whatsAppPhoneNumberId)
        client_number = ''
        for p in phonenumber:
            client_number = p.fb_whatsapp_number
        updateticket = ticket_information.objects.filter(client_id=clientId,id=response_id_id)
        for u_i in updateticket:
            refer_id = u_i.payment_reference_id
            # message = "Transfer ticket " + ticketnumber + " to: "
            # encoded_message = urllib.parse.quote(message)
            # print("wait")
            # url = "https://api.whatsapp.com/send?phone=84&text=hello"
            # print("bb")
            # detailslink = "https://vmart.ai"+ "/infoform/" + toUser + str(clientId) + '/'+ str(ticketnumber) + '/'
            detailslink = "https://vmart.ai"+ "/T/" +  str(response_id_id) + "T"+ refer_id + '/'+ str(clientId)

            payload = json.dumps({
                    "messaging_product": "whatsapp", 
                    "to": toUser,
                    "text": {
                    # "preview_url": True,
                    "body": 'Transfer Ticket click the link :' + detailslink
                }
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            customer_sent(request, toUser, clientId)

            
            # payload = json.dumps({
            #         "messaging_product": "whatsapp",
            #         "preview_url": False,
            #         "recipient_type": "individual",
            #         "to": toUser,
            #         "type": "text",
            #         "text": {
            #             "preview_url": True,
            #             "body": 'Transfer Ticket click the link:'+ detailslink
                
            #     }

            # })
            # response = requests.request("POST", url, headers=headers, data=payload)
            # customer_sent(request, toUser, clientId)
def process_survey_interactive_message(response_id, request,url, headers, toUser, clientId, whatsAppPhoneNumberId,
                                           faceBookToken):
    response_id_type = response_id[0]
    response_id_id = int(response_id[1:])
    print(response_id_type)
    print(response_id_id)
    random_number = random.randint(1, 1000)
    print("fffff")
    base_name = 'tenth_flow'
    new_name = f'{base_name}{random_number}'

    url = "https://graph.facebook.com/v18.0/135195166348253/flows"

    payload = {'name': new_name,
               'categories': '["OTHER"]'}

    headers = {
        'Authorization': 'Bearer EAAKvTUOoeAMBOzwpF7TIIZBDxWSsYB6qbSa05unZB8BhifHZCfWw1i9NUUikZAtHhZC6tFJYIlN4nTE5r05JGz8MTVz8kxfgG7eUUC83cat3FYmlIOSbMFMZBRzzHhv40qckIjZBixKGEUvfbW6giVMQTNTda3tuZA3NEcAjO6e4NSanGJAJC15CfqBWlwfArt70'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    response_data = json.loads(response.text)
    id_value = response_data.get('id')
    print(id_value)
    data={
      "version": "2.1",
      "screens": [
        {
          "id": "DEMO_SCREEN",
          "title": "Demo Screen",
          "layout": {
            "type": "SingleColumnLayout",
            "children": [
              {
                "type": "EmbeddedLink",
                "text": "Pay Now",
                "on-click-action": {
                  "name": "navigate",
                  "next": {
                    "type": "screen",
                    "name": "FINISH"
                  },
                  "payload": {
                    "test_payload": "https://google.com"
                  }
                }
              }
            ]
          }
        },
        {
          "id": "FINISH",
          "data": {
            "test_payload": {
              "type": "string",
              "__example__": "CTA title"
            }
          },
          "title": "Final screen",
          "terminal": True,
          "layout": {
            "type": "SingleColumnLayout",
            "children": [
              {
                "type": "Footer",
                "label": "${data.test_payload}",
                "on-click-action": {
                  "name": "complete",
                  "payload": {}
                }
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
    # ---------------------upload update json asset api-----------------------
    url = f" https://graph.facebook.com/v18.0/{id_value}/assets"

    payload = {'name': 'flow.json',
               'asset_type': 'FLOW_JSON'}
    file_path = f'C:/Vailo/06-10-2023/A_vMart/A_vMart/{new_name}.json'
    files = [
        ('file',
         ('file', open(file_path, 'rb'), 'application/json'))
    ]
    headers = {
        'Authorization': 'Bearer EAAKvTUOoeAMBOzwpF7TIIZBDxWSsYB6qbSa05unZB8BhifHZCfWw1i9NUUikZAtHhZC6tFJYIlN4nTE5r05JGz8MTVz8kxfgG7eUUC83cat3FYmlIOSbMFMZBRzzHhv40qckIjZBixKGEUvfbW6giVMQTNTda3tuZA3NEcAjO6e4NSanGJAJC15CfqBWlwfArt70'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    print("s successfully updated json asset")
    # ------------------------------------publish flow api------------------
    url = f"https://graph.facebook.com/v18.0/{id_value}/publish"

    payload = {}
    headers = {
        'Authorization': 'Bearer EAAKvTUOoeAMBOzwpF7TIIZBDxWSsYB6qbSa05unZB8BhifHZCfWw1i9NUUikZAtHhZC6tFJYIlN4nTE5r05JGz8MTVz8kxfgG7eUUC83cat3FYmlIOSbMFMZBRzzHhv40qckIjZBixKGEUvfbW6giVMQTNTda3tuZA3NEcAjO6e4NSanGJAJC15CfqBWlwfArt70'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    if response.status_code == 200:
        print("Publish successful")

    url = "https://graph.facebook.com/v18.0/154279547761501/messages"

    payload = json.dumps({
        "messaging_product": "whatsapp",
        "to": "918494863493",
        "recipient_type": "individual",
        "type": "interactive",
        "interactive": {
            "type": "flow",
            "header": {
                "type": "image",
                "image": {
                    "link": "https://img.freepik.com/free-photo/wide-angle-shot-single-tree-growing-clouded-sky-during-sunset-surrounded-by-grass_181624-22807.jpg"
                }
            },
            "body": {
                "text": "<BODY_TEXT>"
            },
            "footer": {
                "text": "<FOOTER_TEXT>"
            },
            "action": {
                "name": "flow",
                "parameters": {
                    "flow_message_version": "3",
                    "flow_action": "navigate",
                    "flow_token": "123erwers",
                    "flow_id": str(id_value),
                    "flow_cta": "Pay Now",
                    "flow_action_payload": {
                        "screen": "DEMO_SCREEN",
                        "data": {
                            "id": "0",
                            "title": "Yes"
                        }
                    }
                }
            }
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer EAAKvTUOoeAMBOzwpF7TIIZBDxWSsYB6qbSa05unZB8BhifHZCfWw1i9NUUikZAtHhZC6tFJYIlN4nTE5r05JGz8MTVz8kxfgG7eUUC83cat3FYmlIOSbMFMZBRzzHhv40qckIjZBixKGEUvfbW6giVMQTNTda3tuZA3NEcAjO6e4NSanGJAJC15CfqBWlwfArt70'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
def process_appointement_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                               clientId, whatsAppPhoneNumberId, faceBookToken,list_title):

    if messageType == 'text':
        if not appointment_visitor.objects.filter(client_id=clientId,Visitor_Whatsapp_Number=toUser).exists():
            new_customer = appointment_visitor(client_id=clientId,Visitor_Whatsapp_Number=toUser)
            new_customer.save()
        else:
            print("phone number already exist")
        clientMarketPlace = ''
        adminpermissionObj = admin_permission.objects.filter(client_id=clientId)
        for a_i in adminpermissionObj:
            clientMarketPlace = a_i.client_marketplace
        if clientMarketPlace == 'YES' or clientMarketPlace == 'yes':
            flow_obj = appointment_marketplace_settings.objects.filter(client_id=clientId)
            flow_id = 0
            appointment_flow_id = 0
            specific_flow_id = 0
            for f_i in flow_obj:
                flow_id = f_i.generic_flow_id
                appointment_flow_id = f_i.my_appointment_flow_id
                specific_flow_id = f_i.specific_flow_id

            print(flow_id)
            print(appointment_flow_id)
            print(specific_flow_id)

            facebookDetails = facebook_details.objects.filter(client_id=clientId)

            clientNumber = ''
            for f_i in facebookDetails:
                clientNumber = f_i.fb_whatsapp_number
            search_data = appointment_marketplace.objects.filter(client_id=clientId)
            search_Id = []
            for r_i in search_data:
                search_Id.append(r_i.group_id)
            message_data = message[:9]

            if message_data == 'Search_Id' or message_data == 'search_Id':
                print("s serch flow")
                search_info = message.split('=')[1]
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        "header": {
                            "type": "text",
                            "text": "Not shown in draft mode"
                        },
                        "body": {
                            "text": "Not shown in draft mode"
                        },
                        "footer": {
                            "text": "Not shown in draft mode"
                        },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "data_exchange",
                                "flow_token": str(whatsAppPhoneNumberId) + str(toUser) + str(search_info),
                                "flow_id": str(specific_flow_id),
                                "flow_cta": "Not shown in draft mode",
                                "mode": "draft"
                            }
                        }
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "text": {
                        # "preview_url": True,
                        # "body": f"https://wa.me/918792011415/?text=Search_Id=ISKCON421"
                        "body": f"https://wa.me/{clientNumber}/?text=Search_Id={search_Id[0]}"
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        "header": {
                            "type": "text",
                            "text": "Not shown in draft mode"
                        },
                        "body": {
                            "text": "Not shown in draft mode"
                        },
                        "footer": {
                            "text": "Not shown in draft mode"
                        },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "data_exchange",
                                "flow_token": str(whatsAppPhoneNumberId) + str(toUser),
                                "flow_id": str(flow_id),
                                "flow_cta": "Not shown in draft mode",
                                "mode": "draft"
                            }
                        }
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                myappointementsobj = appointment_bookings.objects.filter(client_id=clientId,customer_phone_number=toUser)
                if myappointementsobj:

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "to": toUser,
                        "recipient_type": "individual",
                        "type": "interactive",
                        "interactive": {
                            "type": "flow",
                            "header": {
                                "type": "text",
                                "text": "Not shown in draft mode"
                            },
                            "body": {
                                "text": "Not shown in draft mode"
                            },
                            "footer": {
                                "text": "Not shown in draft mode"
                            },
                            "action": {
                                "name": "flow",
                                "parameters": {
                                    "flow_message_version": "3",
                                    "flow_action": "data_exchange",
                                    "flow_token": str(whatsAppPhoneNumberId) + str(toUser),
                                    "flow_id": str(appointment_flow_id),
                                    "flow_cta": "Not shown in draft mode",
                                    "mode": "draft"
                                }
                            }
                        }
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                else:
                    print("no records present")



        else:
            consultantDetails = Consultant_details.objects.filter(client_id=clientId,
                                                                  consultant_support_number=toUser)
            if consultantDetails.exists():
                consultant_id = 0
                for c_i in consultantDetails:
                    consultant_id = c_i.id
                print(consultant_id)
                print("payload")
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",

                        "body": {
                            "text": "Please Check Your Appointments."
                        },

                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "U" + str(consultant_id),
                                        "title": "Next Appointements"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "O" + str(consultant_id),
                                        "title": "Old Appointments"
                                    }
                                }
                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)

            else:
                print("No matching consultant settings found for phone number:", toUser)
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        "header": {
                            "type": "text",
                            "text": "signup"
                        },
                        "body": {
                            "text": "complete the sign up to proceed."
                        },
                        "footer": {
                            "text": "signup"
                        },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "navigate",
                                "flow_token": "123erwers",
                                "flow_id": "1344195323152518",
                                "flow_cta": "Sign Up",
                                "flow_action_payload": {
                                    "screen": "SIGN_UP",
                                    "data": {
                                        "id": "0",
                                        "title": "Yes"
                                    }
                                }
                            }
                        }
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                if response.status_code == 200:
                    print("Request was successful")
                    a = response.text
                    json_str = json.dumps(a)
                    b = json.loads(json_str)
                    print(b)








    elif messageType == 'interactive':
        process_appointement_interactive_message(response_id, request, url, headers, toUser, clientId, whatsAppPhoneNumberId,
                                           faceBookToken,list_title)
        
def process_survey_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                                     clientId, whatsAppPhoneNumberId, faceBookToken, list_title):
    if messageType == 'text':
        if not Survey_Customer.objects.filter(client_id=clientId,customer_whatsapp_number=toUser).exists():
            new_customer = Survey_Customer(client_id=clientId,customer_whatsapp_number=toUser)
            new_customer.save()
        else:
            print("phone number already exist")
        print("s its survey")
        clientMarketPlace = ''
        adminpermissionObj = admin_permission.objects.filter(client_id=clientId)
        for a_i in adminpermissionObj:
            clientMarketPlace = a_i.client_marketplace
        if clientMarketPlace == 'YES' or clientMarketPlace == 'yes':
            flow_obj = Survey_marketplace_settings.objects.filter(client_id=clientId)
            flow_id = 0
            survey_flow_id = 0
            specific_flow_id = 0
            for f_i in flow_obj:
                flow_id = f_i.generic_flow_id
                survey_flow_id = f_i.my_survey_flow_id
                specific_flow_id = f_i.specific_flow_id

            print(flow_id)
            print(survey_flow_id)
            print(specific_flow_id)
            facebookDetails = facebook_details.objects.filter(client_id=clientId)

            clientNumber = ''
            for f_i in facebookDetails:
                clientNumber = f_i.fb_whatsapp_number

            search_data = Survey_marketplace.objects.filter(client_id=clientId)
            search_Id = []
            for r_i in search_data:
                search_Id.append(r_i.survey_id)
            message_data = message[:9]
            if message_data == 'Search_Id' or message_data == 'search_Id':
                print("s serch flow")
                search_info = message.split('=')[1]
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        "header": {
                            "type": "text",
                            "text": "Not shown in draft mode"
                        },
                        "body": {
                            "text": "Not shown in draft mode"
                        },
                        "footer": {
                            "text": "Not shown in draft mode"
                        },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "data_exchange",
                                "flow_token": str(whatsAppPhoneNumberId) + str(toUser) + str(search_info),
                                "flow_id": str(specific_flow_id),
                                "flow_cta": "Not shown in draft mode",
                                "mode": "draft"
                            }
                        }
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "text": {
                        # "preview_url": True,
                        # "body": f"https://wa.me/918792011415/?text=Search_Id=ISKCON421"
                        "body": f"https://wa.me/{clientNumber}/?text=Search_Id={search_Id[0]}"
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        "header": {
                            "type": "text",
                            "text": "Not shown in draft mode"
                        },
                        "body": {
                            "text": "Not shown in draft mode"
                        },
                        "footer": {
                            "text": "Not shown in draft mode"
                        },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "data_exchange",
                                "flow_token": str(whatsAppPhoneNumberId) + str(toUser),
                                "flow_id": str(flow_id),
                                "flow_cta": "Not shown in draft mode",
                                "mode": "draft"
                            }
                        }
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                survey_name = ''
                responseobj = Survey_Customer.objects.filter(client_id=clientId,customer_whatsapp_number=toUser)
                if responseobj:
                    for r in responseobj:
                        customer_res_obj = Survey_Customer_Response.objects.filter(client_id=clientId,Survey_Customer_id=r.id)
                        if customer_res_obj:
                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "to": toUser,
                                "recipient_type": "individual",
                                "type": "interactive",
                                "interactive": {
                                    "type": "flow",
                                    "header": {
                                        "type": "text",
                                        "text": "Not shown in draft mode"
                                    },
                                    "body": {
                                        "text": "Not shown in draft mode"
                                    },
                                    "footer": {
                                        "text": "Not shown in draft mode"
                                    },
                                    "action": {
                                        "name": "flow",
                                        "parameters": {
                                            "flow_message_version": "3",
                                            "flow_action": "data_exchange",
                                            "flow_token": str(whatsAppPhoneNumberId) + str(toUser),
                                            "flow_id": str(survey_flow_id),
                                            "flow_cta": "Not shown in draft mode",
                                            "mode": "draft"
                                        }
                                    }
                                }
                            })
                            response = requests.request("POST", url, headers=headers, data=payload)





        else:
            flowinfo = Survey_list.objects.filter(client_id=clientId)
            print(flowinfo)
            for i in flowinfo:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/" + str(
                                    i.survey_image)

                            }
                        },
                        "body": {
                            "text": i.survey_message
                        },
                        "footer": {
                            "text": i.survey_footer
                        },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "navigate",
                                "flow_token": "123erwers",
                                "flow_id": str(i.flow_id),
                                "flow_cta": "Vote",
                                "flow_action_payload": {
                                    "screen": "DEMO_SCREEN",
                                    "data": {
                                        "id": "0",
                                        "title": "Yes"
                                    }
                                }
                            }
                        }
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                if response.status_code == 200:
                    print("Request was successful")
            # payload = json.dumps({
            #     "messaging_product": "whatsapp",
            #     "recipient_type": "individual",
            #     "to": toUser,
            #     "type": "interactive",
            #     "interactive": {
            #         "type": "button",
            #         "header": {
            #             "type": "image",
            #             "image": {
            #                 "link": 'https://thumbs.dreamstime.com/b/environment-earth-day-hands-trees-growing-seedlings-bokeh-green-background-female-hand-holding-tree-nature-field-gra-130247647.jpg'
            #             }
            #         },
            #
            #         "body": {
            #             "text": "Payment Option"
            #         },
            #         "footer": {
            #             "text": "Payment Option"
            #         },
            #         "action": {
            #             "buttons": [
            #                 {
            #                     "type": "reply",
            #                     "reply": {
            #                         "id": "S1",
            #                         "title": "Pay Now"
            #                     }
            #                 },
            #                 {
            #                     "type": "reply",
            #                     "reply": {
            #                         "id": "S2",
            #                         "title": "Other Payment"
            #                     }
            #                 }
            #
            #
            #             ]
            #         }
            #     }
            # })
            #
            # response = requests.request("POST", url, headers=headers, data=payload)


    elif messageType == 'interactive':
         process_survey_interactive_message(response_id, request,url, headers, toUser, clientId, whatsAppPhoneNumberId,
                                           faceBookToken)

def process_default_campaign_interactive_message(response_id, request, url, headers, toUser, clientId,
                                             whatsAppPhoneNumberId,faceBookToken,list_title):
    import datetime
    indian_timezone = pytz.timezone('Asia/Kolkata')
    current_date_time = datetime.datetime.now(indian_timezone)
    # Format the date and time
    formatted_datetime = current_date_time.strftime('%d-%m-%y %H:%M:%S')
    print("Current Date and Time in Indian Standard Time (IST):", formatted_datetime)
    date_part, time_part = formatted_datetime.split(' ')
    date_object = datetime.datetime.strptime(date_part, '%d-%m-%y').date()
    formatted_date_obj = date_object.strftime('%Y-%m-%d')
    new_record = campaign_footprint.objects.create(
        client_id=clientId,
        button=list_title,
        From_number=toUser,
        date=formatted_date_obj,
        time=time_part,
        campaign_name='inflow'
    )
    new_record.save()
    new_key_value = {
        'Date': date_part,
        'Time': time_part,
        'Button': list_title,
        'From': toUser,
        'Campaign_Name': 'Inflow'
    }

    update_info = generic_campaign_history.objects.filter(client_id=clientId, Customer_Whatsapp_Number=toUser,Campaign_Status='inflow')
    if update_info:
        print('vaisakh')
        print(update_info)
        for u_i in update_info:
            if u_i.Campaign_Foot_Print:
                print("zzzzzooooo")
                existing_campaign_footprint = u_i.Campaign_Foot_Print
                if isinstance(existing_campaign_footprint, list):
                    # Append the new dictionary to the list
                    existing_campaign_footprint.append(new_key_value)
                else:
                    # Create a list and add both dictionaries
                    existing_campaign_footprint = [existing_campaign_footprint, new_key_value]

                u_i.Campaign_Foot_Print = existing_campaign_footprint

            else:
                u_i.Campaign_Foot_Print = new_key_value

            u_i.save()

        print("s all buttons saved successfully")

    response_id_type = response_id[0]
    response_id_id = int(response_id[1:])
    print(response_id_type)
    print(response_id_id)
    button_type = ''
    if response_id_type == 'I':
        detailsInfo = Inflow_Setup_Details.objects.filter(client_id=clientId,id=response_id_id)
        for d_i in detailsInfo:
            button_type = d_i.open_button_type

        if button_type.lower() == 'chain':
            parentInfoObj = Inflow_Setup_Details.objects.filter(client_id=clientId, Parent_ID=response_id_id)
            print("s second level of interactive chain")
            second_info_id = []
            second_info_button_name = []
            second_info_description = []
            for s_i in parentInfoObj:
                second_info_id.append(s_i.id)
                second_info_button_name.append(s_i.short_title)
                second_info_description.append(s_i.short_description)
            list_second_details = []
            for i in range(len(second_info_button_name)):
                list_second_details.append({
                    "id":"I"+str(second_info_id[i]),
                    "title":second_info_button_name[i],
                    "description":second_info_description[i]

                })
            infoObjDetails = Inflow_Setup_Details.objects.filter(client_id=clientId,id=response_id_id)
            for n_i in infoObjDetails:
                if n_i.inflow_header_type.lower() == 'text':
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "list",
                            "header": {
                                "type": "text",
                                "text": n_i.inflow_header_text
                            },
                            "body": {
                                "text": n_i.inflow_body_text
                            },
                            # "footer": {
                            #     "text": n_i.inflow_footer_text
                            # },
                            "action": {
                                "button": n_i.open_button_name,
                                "sections": [
                                    {
                                        "title": "Locations",
                                        "rows": list_second_details
                                    }

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)
                else:
                    print("image code please wait soon it came.")


        elif button_type.lower() == 'phone':
            detailsInfoObject = Inflow_Setup_Details.objects.filter(client_id=clientId, id=response_id_id)
            for m_i in detailsInfoObject:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "type": "contacts",
                    "contacts": [
                        {
                            "name": {
                                "formatted_name": m_i.additional_info1,
                                "first_name": "Mohan"
                            },
                            "phones": [
                                {
                                    "phone": m_i.additional_info,
                                    "type": "HOME"
                                }
                            ]
                        }
                    ]
                })
                response = requests.request("POST", url, headers=headers, data=payload)
        elif button_type.lower() == 'image':
            otherInfoObject = Inflow_Setup_Details.objects.filter(client_id=clientId, id=response_id_id)
            for b_i in otherInfoObject:
                all_file_path = b_i.additional_file_path
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "image",
                    "image": {
                        "link": f'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/{all_file_path}',

                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
        elif button_type.lower() == 'video':
            otherInfoObject = Inflow_Setup_Details.objects.filter(client_id=clientId, id=response_id_id)
            for b_i in otherInfoObject:
                all_file_path = b_i.additional_file_path
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "video",
                    "video": {
                        "link": f'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/{all_file_path}',
                        "caption":b_i.additional_info

                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
        elif button_type.lower() == 'document':
            otherInfoObject = Inflow_Setup_Details.objects.filter(client_id=clientId, id=response_id_id)
            for b_i in otherInfoObject:
                all_file_path = b_i.additional_file_path
                out_name = all_file_path.name
                File_Name = out_name.split("/")
                Output_File_Name = File_Name[-1]
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "document",
                    "document": {
                        "link": f'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/{all_file_path}',
                        "filename": Output_File_Name

                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
        elif button_type.lower() == 'url':
            detailsInfoObject = Inflow_Setup_Details.objects.filter(client_id=clientId, id=response_id_id)
            for m_i in detailsInfoObject:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "text": {
                        "preview_url": True,
                        "body": m_i.inflow_body_text
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
        elif button_type.lower() == 'form':
            detailsInfoObject = Inflow_Setup_Details.objects.filter(client_id=clientId, id=response_id_id)
            for d_i in detailsInfoObject:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        "body": {
                            "text": "Please fill out the following form to receive a call from our executive."
                        },
                        # "footer": {
                        #     "text": "Submit your details"
                        # },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "navigate",
                                "flow_token": "123refg",
                                "flow_id": d_i.additional_info,
                                "flow_cta": "Enter Details",
                                "flow_action_payload": {
                                    "screen": "campaign_flow",
                                    "data": {
                                        "id": "0",
                                        "title": "Yes"
                                    }
                                }
                            }
                        }
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
        elif button_type.lower() == 'cards':
            print("s cards")
            parentInfoObj = Inflow_Setup_Details.objects.filter(client_id=clientId, Parent_ID=response_id_id)
            print("len is----->",len(parentInfoObj))
            All_cards = []

            for index,p_i in enumerate(parentInfoObj):
                All_cards.append(
                    {
                        "card_index": index,
                        "components": [
                            {
                                "type": "HEADER",
                                "parameters": [
                                    {
                                        "type": "IMAGE",
                                        "image": {
                                            "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
                                                p_i.additional_file_path)
                                        }
                                    }
                                ]
                            },
                            {
                                "type": "BODY",
                                "parameters": [

                                    {
                                        "type": "TEXT",
                                        "text": p_i.inflow_body_text
                                    }

                                ]
                            },
                            {
                                "type": "BUTTON",
                                "sub_type": "QUICK_REPLY",
                                "index": "0",
                                "parameters": [
                                    {
                                        "type": "PAYLOAD",
                                        "payload": f"C{p_i.id}"
                                    }
                                ]
                            },

                        ]
                    },
                )
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "template",
                "template": {
                    "name": f"campaign_cards_list_set_{len(parentInfoObj)}",
                    "language": {
                        "code": "en_US"
                    },
                    "components": [
                        {
                            "type": "BODY",
                            "parameters": [
                                {
                                    "type": "TEXT",
                                    "text": "A villa plot with modern amenities"
                                }

                            ]
                        },
                        {
                            "type": "CAROUSEL",
                            "cards":All_cards
                        }
                    ]
                }
            }

            response = requests.post(url, json=data, headers=headers)

            print(response.status_code)
            print(response.json())
            print("s carousel sent successfully")

















def process_default_campaign_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                                     clientId, whatsAppPhoneNumberId, faceBookToken,list_title):
    if messageType == 'text':
        if not campaign_customer_master.objects.filter(client_id=clientId,Customer_Whatsapp_Number=toUser).exists():
            new_customer = campaign_customer_master(client_id=clientId,Customer_Whatsapp_Number=toUser)
            new_customer.save()
        else:
            print("phone number already exist")

        existing_record = generic_campaign_history.objects.filter(
            client_id=clientId,
            Customer_Whatsapp_Number=toUser,
            Campaign_Status='inflow'
        ).exists()
        if not existing_record:
            customer_history_obj = generic_campaign_history.objects.create(
                client_id=clientId,
                Customer_Whatsapp_Number=toUser,
                marketplace_id=None,
                generic_campaign_info_id=None,
                Campaign_Status='inflow'

            )
            customer_history_obj.save()
            print("first time")
        else:
            print("second time already record is there")


        clientMarketPlace = ''
        adminpermissionObj = admin_permission.objects.filter(client_id=clientId)
        for a_i in adminpermissionObj:
            clientMarketPlace = a_i.client_marketplace
        if clientMarketPlace == 'NO' or clientMarketPlace == 'no':
            print("s inflow messages")
            inflow_details_obj = Inflow_Setup_Details.objects.filter(client_id=clientId,Parent_ID="0")
            print(inflow_details_obj)
            for n_i in inflow_details_obj:
                parentInfoDetails = Inflow_Setup_Details.objects.filter(client_id=clientId,Parent_ID=n_i.id)
                print("parent",parentInfoDetails)
                info_id = []
                info_description = []
                info_button_name = []
                for p_i in parentInfoDetails:
                    info_id.append(p_i.id)
                    info_description.append(p_i.short_description)
                    info_button_name.append(p_i.short_title)
                print(info_button_name)
                list_all_buttons = []
                for h_i in range(len(info_button_name)):
                    list_all_buttons.append({
                        "id":"I"+str(info_id[h_i]),
                        "title":info_button_name[h_i],
                        "description":info_description[h_i]
                    })

                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "list",
                        "header": {
                            "type": "text",
                            "text": n_i.inflow_header_text
                        },
                        "body": {
                            "text": n_i.inflow_body_text
                        },
                        "footer": {
                            "text": n_i.inflow_footer_text
                        },
                        "action": {
                            "button": n_i.open_button_name,
                            "sections": [
                                {
                                    "title": "Locations",
                                    "rows": list_all_buttons
                                }

                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)





        else:
            print("s mp no")
            template_Name = ''
            header_type = ''
            first_value = ''
            second_value = ''
            third_value = ''
            camapaign_Name = ''
            camapign_Message = ''
            campaign_image = ''
            default_campaignInfo = generic_campaign_info.objects.filter(client_id=clientId,default_campaign='yes')
            for d_i in default_campaignInfo:
                camapaign_Name = d_i.Campaign_Name
                camapign_Message = d_i.Campaign_message
                campaign_image = d_i.Campaign_Image
                templateData = template_info.objects.filter(client_id=clientId,generic_campaign_info_id=d_i.id)
                for t_i in templateData:
                    template_Name = t_i.template_name
                    header_type = t_i.template_header_type
            campaign_values = [value.strip() for value in camapign_Message.split(',')]
            if len(campaign_values) >= 1:
                first_value = campaign_values[0]  # end of May
            if len(campaign_values) >= 2:
                second_value = campaign_values[1]  # 250OFF
            if len(campaign_values) >= 3:
                third_value = campaign_values[2]

            if header_type == 'text' or header_type == 'TEXT':

                url = f"https://graph.facebook.com/v15.0/{whatsAppPhoneNumberId}/messages"

                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "template",
                    "template": {
                        "name": template_Name,
                        "language": {
                            "code": "en_Us"
                        },
                        "components": [
                            {
                                "type": "header",
                                "parameters": [
                                    {
                                        "type": "text",
                                        "text": camapaign_Name
                                    }
                                ]
                            },
                            {
                                "type": "body",
                                "parameters": [
                                    {
                                        "type": "text",
                                        "text": first_value
                                    },
                                    {
                                        "type": "text",
                                        "text": second_value
                                    },
                                    {
                                        "type": "text",
                                        "text": third_value
                                    }
                                ]
                            },
                            {
                                "type": "button",
                                "sub_type": "url",
                                "index": "3",
                                "parameters": [
                                    {
                                        "type": "text",
                                        "text": "admin"
                                    }
                                ]
                            },
                            {
                                "type": "button",
                                "sub_type": "quick_reply",
                                "index": "1",
                                "parameters": [
                                    {
                                        "type": "payload",
                                        "payload": "9rwnB8RbYmPF5t2Mn09x4h"
                                    }
                                ]
                            },
                            {
                                "type": "button",
                                "sub_type": "quick_reply",
                                "index": "2",
                                "parameters": [
                                    {
                                        "type": "payload",
                                        "payload": "aGlzIHRoaXMgaXMgY29v"
                                    }
                                ]
                            }
                        ]
                    }
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {faceBookToken}'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
            else:
                url = f"https://graph.facebook.com/v15.0/{whatsAppPhoneNumberId}/messages"

                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to":toUser,
                    "type": "template",
                    "template": {
                        "name": template_Name,
                        "language": {
                            "code": "en_Us"
                        },
                        "components": [
                            {
                                "type": "header",
                                "parameters": [
                                    {
                                        "type": "image",
                                        "image": {
                                            "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                            (campaign_image)
                                        }
                                    }
                                ]
                            },
                            {
                                "type": "body",
                                "parameters": [
                                    {
                                        "type": "text",
                                        "text": first_value
                                    },
                                    {
                                        "type": "text",
                                        "text": second_value
                                    },
                                    {
                                        "type": "text",
                                        "text": third_value
                                    }
                                ]
                            },
                            {
                                "type": "button",
                                "sub_type": "url",
                                "index": "3",
                                "parameters": [
                                    {
                                        "type": "text",
                                        "text": "admin"
                                    }
                                ]
                            },
                            {
                                "type": "button",
                                "sub_type": "quick_reply",
                                "index": "1",
                                "parameters": [
                                    {
                                        "type": "payload",
                                        "payload": "9rwnB8RbYmPF5t2Mn09x4h"
                                    }
                                ]
                            },
                            {
                                "type": "button",
                                "sub_type": "quick_reply",
                                "index": "2",
                                "parameters": [
                                    {
                                        "type": "payload",
                                        "payload": "aGlzIHRoaXMgaXMgY29v"
                                    }
                                ]
                            }
                        ]
                    }
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {faceBookToken}'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
    elif messageType == 'interactive':

        process_default_campaign_interactive_message(response_id, request, url, headers, toUser, clientId,
                                             whatsAppPhoneNumberId,
                                             faceBookToken,list_title)








def process_campaign_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                                     clientId, whatsAppPhoneNumberId, faceBookToken):
    if messageType == 'text':
        if not campaign_customer_master.objects.filter(client_id=clientId,Customer_Whatsapp_Number=toUser).exists():
            new_customer = campaign_customer_master(client_id=clientId,Customer_Whatsapp_Number=toUser)
            new_customer.save()
        else:
            print("phone number already exist")
        clientMarketPlace = ''
        adminpermissionObj = admin_permission.objects.filter(client_id=clientId)
        for a_i in adminpermissionObj:
            clientMarketPlace = a_i.client_marketplace
        if clientMarketPlace == 'YES' or clientMarketPlace == 'yes':
            flow_obj = campaign_marketplace_settings.objects.filter(client_id=clientId)
            flow_id = 0
            campaign_flow_id = 0
            specific_flow_id = 0
            for f_i in flow_obj:
                flow_id = f_i.generic_flow_id
                campaign_flow_id = f_i.my_campaign_flow_id
                specific_flow_id = f_i.specific_flow_id

            print(flow_id)
            print(campaign_flow_id)
            print(specific_flow_id)

            facebookDetails = facebook_details.objects.filter(client_id=clientId)

            clientNumber = ''
            for f_i in facebookDetails:
                clientNumber = f_i.fb_whatsapp_number

            search_data = campaign_marketplace.objects.filter(client_id=clientId)
            search_Id = []
            for r_i in search_data:
                search_Id.append(r_i.campaign_id)
            print(search_Id)
            message_data = message[:9]
            if message_data == 'Search_Id' or message_data == 'search_Id':
                print("s serch flow")
                search_info = message.split('=')[1]
                print(search_info)
                template_Name = ''
                first_value = ''
                second_value = ''
                third_value = ''
                camapaign_Name = ''
                camapign_Message = ''
                campaign_image = ''
                header_type = ''
                campaign_obj = campaign_marketplace.objects.filter(client_id=clientId,campaign_id=search_info)
                for a_i in campaign_obj:
                    campaigndata = generic_campaign_info.objects.filter(client_id=clientId,marketplace_id=a_i.id)
                    for campaign in campaigndata:
                        camapaign_Name = campaign.Campaign_Name
                        camapign_Message = campaign.Campaign_message
                        campaign_image = campaign.Campaign_Image

                    campaign_values = [value.strip() for value in camapign_Message.split(',')]
                    if len(campaign_values) >= 1:
                        first_value = campaign_values[0]  # end of May
                    if len(campaign_values) >= 2:
                        second_value = campaign_values[1]  # 250OFF
                    if len(campaign_values) >= 3:
                        third_value = campaign_values[2]
                    templateobj = template_info.objects.filter(client_id=clientId,marketplace_id=a_i.id)
                    for temp in templateobj:
                        template_Name = temp.template_name
                        header_type = temp.template_header_type

                print("please wait template is display")
                if header_type == 'text' or header_type == 'TEXT':
                    url = f"https://graph.facebook.com/v15.0/{whatsAppPhoneNumberId}/messages"

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "template",
                        "template": {
                            "name": template_Name,
                            "language": {
                                "code": "en_Us"
                            },
                            "components": [
                                {
                                    "type": "header",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": camapaign_Name
                                        }
                                    ]
                                },
                                {
                                    "type": "body",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": first_value
                                        },
                                        {
                                            "type": "text",
                                            "text": second_value
                                        },
                                        {
                                            "type": "text",
                                            "text": third_value
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "url",
                                    "index": "3",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": "admin"
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "quick_reply",
                                    "index": "1",
                                    "parameters": [
                                        {
                                            "type": "payload",
                                            "payload": "9rwnB8RbYmPF5t2Mn09x4h"
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "quick_reply",
                                    "index": "2",
                                    "parameters": [
                                        {
                                            "type": "payload",
                                            "payload": "aGlzIHRoaXMgaXMgY29v"
                                        }
                                    ]
                                }
                            ]
                        }
                    })
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {faceBookToken}'
                    }

                    response = requests.request("POST", url, headers=headers, data=payload)

                    print(response.text)
                else:
                    url = f"https://graph.facebook.com/v15.0/{whatsAppPhoneNumberId}/messages"

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "template",
                        "template": {
                            "name": template_Name,
                            "language": {
                                "code": "en_Us"
                            },
                            "components": [
                                {
                                    "type": "header",
                                    "parameters": [
                                        {
                                            "type": "image",
                                            "image": {
                                                "link":'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                                    (campaign_image)
                                            }
                                        }
                                    ]
                                },
                                {
                                    "type": "body",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": first_value
                                        },
                                        {
                                            "type": "text",
                                            "text": second_value
                                        },
                                        {
                                            "type": "text",
                                            "text": third_value
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "url",
                                    "index": "3",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": "admin"
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "quick_reply",
                                    "index": "1",
                                    "parameters": [
                                        {
                                            "type": "payload",
                                            "payload": "9rwnB8RbYmPF5t2Mn09x4h"
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "quick_reply",
                                    "index": "2",
                                    "parameters": [
                                        {
                                            "type": "payload",
                                            "payload": "aGlzIHRoaXMgaXMgY29v"
                                        }
                                    ]
                                }
                            ]
                        }
                    })
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {faceBookToken}'
                    }

                    response = requests.request("POST", url, headers=headers, data=payload)

                    print(response.text)



            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "text": {
                        # "preview_url": True,
                        # "body": f"https://wa.me/918792011415/?text=Search_Id=ISKCON421"
                        "body": f"https://wa.me/{clientNumber}/?text=Search_Id={search_Id[0]}"
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                print("cccccc")
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        "header": {
                            "type": "text",
                            "text": "Not shown in draft mode"
                        },
                        "body": {
                            "text": "Not shown in draft mode"
                        },
                        "footer": {
                            "text": "Not shown in draft mode"
                        },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "data_exchange",
                                "flow_token": str(whatsAppPhoneNumberId) + str(toUser),
                                "flow_id": str(flow_id),
                                "flow_cta": "Not shown in draft mode",
                                "mode": "draft"
                            }
                        }
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)

                responseobj = campaign_customer_master.objects.filter(client_id=clientId,Customer_Whatsapp_Number=toUser)
                if responseobj:
                    print("s")
                    for r in responseobj:
                        customer_res_obj = generic_campaign_history.objects.filter(client_id=clientId,
                                                                                   campaign_customer_master_id=r.id)
                        if customer_res_obj:
                            print("ss")
                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "to": toUser,
                                "recipient_type": "individual",
                                "type": "interactive",
                                "interactive": {
                                    "type": "flow",
                                    "header": {
                                        "type": "text",
                                        "text": "Not shown in draft mode"
                                    },
                                    "body": {
                                        "text": "Not shown in draft mode"
                                    },
                                    "footer": {
                                        "text": "Not shown in draft mode"
                                    },
                                    "action": {
                                        "name": "flow",
                                        "parameters": {
                                            "flow_message_version": "3",
                                            "flow_action": "data_exchange",
                                            "flow_token": str(whatsAppPhoneNumberId) + str(toUser),
                                            "flow_id": str(campaign_flow_id),
                                            "flow_cta": "Not shown in draft mode",
                                            "mode": "draft"
                                        }
                                    }
                                }
                            })
                            response = requests.request("POST", url, headers=headers, data=payload)

        else:
            pass
        # Code for my campaign button creation in frontend
        # else:
        #     facebook_detailsObj = facebook_details.objects.filter(client_id=clientId)
        #     phonenumberID = 0
        #     facebook_token = ''
        #     waba_id = 0
        #     for f_i in facebook_detailsObj:
        #         phonenumberID = f_i.fb_phone_number_id
        #         facebook_token = f_i.fb_access_token
        #         waba_id = f_i.fb_Whatsapp_business_account_id
        #     print(phonenumberID)
        #     print(facebook_token)
        #     print("rrr")
        #     market_settingsObj = campaign_marketplace_settings.objects.filter(client_id=clientId)
        #     for m_i in market_settingsObj:
        #         random_number = random.randint(1, 1000)
        #         print("fffff")
        #         base_name = 'campaign_flow'
        #         new_name = f'{base_name}{random_number}'
        #         url = f"https://graph.facebook.com/v18.0/{waba_id}/flows"
        #
        #         payload = {'name': new_name,
        #                    'categories': '["OTHER"]'}
        #
        #         headers = {
        #             'Authorization': f'Bearer {facebook_token}'
        #         }
        #
        #         response = requests.request("POST", url, headers=headers, data=payload)
        #         print(response.text)
        #         response_data = json.loads(response.text)
        #         id_value = response_data.get('id')
        #         if id_value is not None:
        #             print("ID:", id_value)
        #             print("narrri")
        #             donation_obj = campaign_marketplace_settings.objects.filter(client_id=clientId)
        #             for d_i in donation_obj:
        #                 d_i.my_campaign_flow_id = id_value
        #                 d_i.save()
        #                 print("successfully saved the flow id")
        #
        #                 data = {
        #                   "version": "2.1",
        #                   "data_api_version": "3.0",
        #                   "data_channel_uri": "https://vmart.ai/mycampaigndata",
        #                   "routing_model": {
        #                     "CAMPAIGN_DATA": [
        #
        #                     ]
        #                   },
        #                   "screens": [
        #                     {
        #                       "id": "CAMPAIGN_DATA",
        #                       "title": "CAMPAIGN_DATA",
        #                       "terminal": True,
        #                       "data": {
        #                         "details_info": {
        #                           "type": "string",
        #                           "__example__": ""
        #                         },
        #                         "details": {
        #                           "type": "string",
        #                           "__example__": ""
        #                         },
        #                         "options": {
        #                           "type": "array",
        #                           "items": {
        #                             "type": "object",
        #                             "properties": {
        #                               "id": {
        #                                 "type": "string"
        #                               },
        #                               "title": {
        #                                 "type": "string"
        #                               }
        #                             }
        #                           },
        #                           "__example__": []
        #                         }
        #                       },
        #                       "layout": {
        #                         "type": "SingleColumnLayout",
        #                         "children": [
        #                           {
        #                             "type": "Form",
        #                             "name": "cover_form",
        #                             "children": [
        #                               {
        #                                 "type": "Image",
        #                                 "src": "${data.details_info}",
        #                                 "width": 300,
        #                                 "height": 300
        #                               },
        #                               {
        #                                 "type": "TextHeading",
        #                                 "text": "${data.details}"
        #                               },
        #                               {
        #                                 "type": "RadioButtonsGroup",
        #                                 "name": "options",
        #                                 "data-source": "${data.options}",
        #                                 "label": "Options",
        #                                 "required": True
        #                               },
        #                               {
        #                                 "type": "Footer",
        #                                 "label": "complete",
        #                                 "on-click-action": {
        #                                   "name": "complete",
        #                                   "payload": {
        #                                     "my_campaign_data_info": "${form.options}"
        #                                   }
        #                                 }
        #                               }
        #                             ]
        #                           }
        #                         ]
        #                       }
        #                     }
        #                   ]
        #                 }
        #
        #                 file_name = f'{new_name}.json'
        #                 with open(file_name, 'w') as file:
        #                     json.dump(data, file, indent=2)
        #                 print("succesfully generated the json file..")
        #
        #                 url = f" https://graph.facebook.com/v18.0/{id_value}/assets"
        #
        #                 payload = {'name': 'flow.json',
        #                            'asset_type': 'FLOW_JSON'}
        #                 file_path = f'C:/Vailo/17-01-2024 new dashboard/A_vMart/A_vMart/{new_name}.json'
        #                 files = [
        #                     ('file',
        #                      ('file', open(file_path, 'rb'), 'application/json'))
        #                 ]
        #                 headers = {
        #                     'Authorization': f'Bearer {facebook_token}'
        #                 }
        #
        #                 response = requests.request("POST", url, headers=headers, data=payload, files=files)
        #                 print("king nag")
        #
        #                 print(response.text)
        #                 print("s successfully updated json asset")





def process_donation_bot_message(message, response_id, messageType, request,url, headers, toUser, clientId,whatsAppPhoneNumberId,faceBookToken):
    if messageType == 'text':
        # if not donation_details.objects.filter(client_id=clientId,donar_phone_number=toUser).exists():
        #     new_customer = donation_details(client_id=clientId,donar_phone_number=toUser)
        #     new_customer.save()
        # else:
        #     print("phone number already exist")


        clientMarketPlace = ''
        adminpermissionObj = admin_permission.objects.filter(client_id=clientId)
        for a_i in adminpermissionObj:
            clientMarketPlace = a_i.client_marketplace

        if clientMarketPlace == 'YES' or clientMarketPlace == 'yes':
            donation_ref_id = uuid.uuid4()
            donation_details.objects.create(client_id=clientId, donation_reference_id=donation_ref_id,
                                            donar_phone_number=toUser)
            print("s successfully generated and saved the reference id")
            print(donation_ref_id)
            print("s text")
            flow_obj = donation_marketplace_settings.objects.filter(client_id=clientId)
            flow_id = 0
            donation_flow_id = 0
            specific_flow_id = 0
            for f_i in flow_obj:
                flow_id = f_i.generic_flow_id
                donation_flow_id = f_i.my_donation_flow_id
                specific_flow_id = f_i.specific_flow_id

            print(flow_id)
            print(donation_flow_id)
            print(specific_flow_id)


            facebookDetails = facebook_details.objects.filter(client_id=clientId)

            clientNumber = ''
            for f_i in facebookDetails:
                clientNumber = f_i.fb_whatsapp_number

            search_data = donation_marketplace.objects.filter(client_id=clientId)
            search_Id = ''
            for r_i in search_data:
                search_Id = r_i.ngo_id
            message_data = message[:9]
            if message_data == 'Search_Id' or message_data == 'search_Id':
                print("s serch flow")
                search_info = message.split('=')[1]
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        "header": {
                            "type": "text",
                            "text": "Not shown in draft mode"
                        },
                        "body": {
                            "text": "Not shown in draft mode"
                        },
                        "footer": {
                            "text": "Not shown in draft mode"
                        },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "data_exchange",
                                "flow_token": str(whatsAppPhoneNumberId) + str(donation_ref_id)+str(search_info),
                                "flow_id": str(specific_flow_id),
                                "flow_cta": "Not shown in draft mode",
                                "mode": "draft"
                            }
                        }
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "text": {
                        # "preview_url": True,
                        # "body": f"https://wa.me/918792011415/?text=Search_Id=ISKCON421"
                        "body": f"https://wa.me/{clientNumber}/?text=Search_Id={search_Id}"
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                print("cccccc")
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        "header": {
                            "type": "text",
                            "text": "Not shown in draft mode"
                        },
                        "body": {
                            "text": "Not shown in draft mode"
                        },
                        "footer": {
                            "text": "Not shown in draft mode"
                        },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "data_exchange",
                                "flow_token": str(whatsAppPhoneNumberId) + str(donation_ref_id),
                                "flow_id": str(flow_id),
                                "flow_cta": "Not shown in draft mode",
                                "mode": "draft"
                            }
                        }
                    }
                })
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)

                donation_info_obj = donation_details.objects.filter(client_id=clientId,donar_phone_number=toUser,
                                                                    payment_status=1)
                if donation_info_obj:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "to": toUser,
                        "recipient_type": "individual",
                        "type": "interactive",
                        "interactive": {
                            "type": "flow",
                            "header": {
                                "type": "text",
                                "text": "Not shown in draft mode"
                            },
                            "body": {
                                "text": "Not shown in draft mode"
                            },
                            "footer": {
                                "text": "Not shown in draft mode"
                            },
                            "action": {
                                "name": "flow",
                                "parameters": {
                                    "flow_message_version": "3",
                                    "flow_action": "data_exchange",
                                    "flow_token": str(whatsAppPhoneNumberId) + str(toUser),
                                    "flow_id": str(donation_flow_id),
                                    "flow_cta": "Not shown in draft mode",
                                    "mode": "draft"
                                }
                            }
                        }
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                else:
                    print("no records present")



                # payload = json.dumps({
                #     "messaging_product": "whatsapp",
                #     "to": toUser,
                #     "recipient_type": "individual",
                #     "type": "interactive",
                #     "interactive": {
                #         "type": "flow",
                #         "header": {
                #             "type": "image",
                #             "image": {
                #                 "link": "https://vakilsearch.com/blog/wp-content/uploads/2021/05/VS_Blog-Images_3-05.png"
                #             }
                #         },
                #         "body": {
                #             "text": "Engage devotional service"
                #         },
                #         "footer": {
                #             "text": "Search the Ngo details"
                #         },
                #         "action": {
                #             "name": "flow",
                #             "parameters": {
                #                 "flow_message_version": "3",
                #                 "flow_action": "navigate",
                #                 "flow_token": "123erwers",
                #                 "flow_id": "861496255624613",
                #                 "flow_cta": "Search",
                #                 "flow_action_payload": {
                #                     "screen": "SIGN_UP",
                #                     "data": {
                #                         "id": "0",
                #                         "title": "Yes"
                #                     }
                #                 }
                #             }
                #         }
                #     }
                # })
                # response = requests.request("POST", url, headers=headers, data=payload)




        else:
            print("ccccccchennai")
            welcomeobj = donation_settings.objects.filter(client_id=clientId)
            print(welcomeobj)
            print("ddevra")
            for don_i in welcomeobj:
                if don_i.donation_image:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "button",
                            "header": {
                                "type": "image",
                                "image": {
                                    "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                    (don_i.donation_image)
                                }
                            },

                            "body": {
                                "text": don_i.donation_description if don_i.donation_description else "."
                            },
                            "footer": {
                                "text": don_i.donation_footer
                            },
                            "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "I1",
                                            "title": don_i.donation_now_button_name
                                        }
                                    },
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "I2",
                                            "title": don_i.my_donation_button_name
                                        }
                                    },
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "I3",
                                            "title": don_i.contact_us_button_name
                                        }
                                    },

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)
                else:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "button",
                            "body": {
                                "text": don_i.donation_description if don_i.donation_description else "."
                            },
                            "footer": {
                                "text": don_i.donation_footer
                            },
                            "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "I1",
                                            "title": don_i.donation_now_button_name
                                        }
                                    },
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "I2",
                                            "title": don_i.my_donation_button_name
                                        }
                                    },
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "I3",
                                            "title": don_i.contact_us_button_name
                                        }
                                    },
                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)

       # process_donation_text_message(message, request, url, headers, toUser, clientId)
    elif messageType == 'interactive':
        process_donation_interactive_message(response_id, request, url, headers, toUser, clientId, whatsAppPhoneNumberId,
                                           faceBookToken)



def process_ticket_bot_message(message, response_id, messageType, request,url, headers, toUser, clientId,whatsAppPhoneNumberId,faceBookToken):
    if messageType == 'text':
       process_ticket_text_message(message, request, url, headers, toUser, clientId)
    elif messageType == 'interactive':
       process_ticket_interactive_message(response_id, request, url, headers, toUser, clientId,whatsAppPhoneNumberId,faceBookToken)







class BotView(generic.View):

    def get(self, request, *args, **kwargs):
        #         # print(request.build_absolute_uri(), '11111111111111111111111111')
        urlThis = str(request.build_absolute_uri())
        #         # print('>>>>>',urlThis,'<<<<<')
        b = urlThis.split('?')
        c = b[0]
        #         # print(b[0])
        #         # print(c[-22:])
        vMartCilentId = c[-22:]
        clientCallbackUrlObjects = admin_permission.objects.filter(client_auth_key=vMartCilentId)
        print('--------------------------------', urlThis)
        vMartCilentsecretKey = ''

        for i in clientCallbackUrlObjects:
            vMartCilentsecretKey = vMartCilentsecretKey + i.client_auth_secret
        #         # print(vMartCilentId,'=============')
        #         # print(vMartCilentsecretKey,'================')
        if self.request.GET['hub.verify_token'] == vMartCilentsecretKey:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)  # Post function to handle Facebook messages

    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        print("booooooooooooommmmmmikkkkkkkk")
        print(incoming_message)
        print("ccchhhhaaaaaannnnniii")

        # url = DomainName + 'redirectVailo/'
        #
        # # url='https://0937-116-75-94-183.ngrok.io/re/'
        # # print('iiiiiiiiii',incoming_message)
        # payload = json.dumps(incoming_message)
        # headers = {
        #
        #     'Content-Type': 'application/json'
        # }
        # response = requests.request("POST", url, headers=headers, data=payload)
        phone_number_id = incoming_message['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
        if phone_number_id == '129405560258915':
            url = DomainName + 'redirectVmart/'

            # url='https://0937-116-75-94-183.ngrok.io/re/'
            # print('iiiiiiiiii',incoming_message)
            payload = json.dumps(incoming_message)
            headers = {

                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
        else:
            print("mohan coming")
            url = DomainName + 'redirectVailo/'

            # url='https://0937-116-75-94-183.ngrok.io/re/'
            # print('iiiiiiiiii',incoming_message)
            payload = json.dumps(incoming_message)
            headers = {

                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)

        return HttpResponse()
def check(request,link):
    return redirect(link)


def decrypt_request_check2(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQItTLWm6Vc654CAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECIvFEoBWEGMFBIIEyHH6IlqdS0g3
9jhMFdyd1JBYuXJZP33tp3YMDarSLi4Aj1nui9BI23w5sHS5GcNidBGC507vq2iw
M8ckVUUOoB3wDqj0H6Uec0aOaHeFQLFDa++CGWZTx0+T6dTG4HCbC/G7VBQmgE1j
rsJ6LGkfq/85NpuNNImwKPHZreAZCxGB/4X3sEFcNYrEMqWhnsz6oGssVGV3uV3M
MPTmv9S8oWUz3GzOZVhP3vwLnpXbyD5pyFf0FPEGBvRjG2UUs9sWHHUTTjF11MtH
TxEmdAVA79Vw2RSx1bLNp5+ItAidfAfFMmIZM7W+LjbZ8DWLDp4sDw+ZpLIg+egZ
PnD/VCjTej37TZIwz8FFeIOs7FcwLX/pqjD6+nPPYUO9PYqIygG4BMndoNrGQT+d
GQjWZIMdofUiwFHsjNupSOde/uQ/JDe5pKvVHaf/+zSYfnjSIjPYELj3OeOSCZaK
A8SZ0HHuwnJeNi733C/BvNh0uh6xJtwdKq3kQSR62/UQRzxxbbRTjcBMjYucf0vY
67eqLmc2aBUyRfnOpQisRTOPaUGYADFrX9i08jM9wWGxXWx5LEDi907HvGAAtZf1
+v4nVAEl7SG5EhEZpCcvOMZaUurwStn4ve+nyD5w73aJzrINdLOuqDz0P/BRsFQF
+gPy1xMtaw/G2E+xSsvyu01t9WzPDDWAqrGI9pzqXQpotpeS4nIuAdVYlM3C/0WZ
L4hQvCfYhlCMnBFiv9X9eQQfTSGAN2gFsuDwZoLk2dVLnTZoJFtwT7+kyYN3G6kJ
bgeegQ9dA2eTIf54j4Xmh4MbozMise9wSCtRkHWylN5QCOLaiMAUx2k5tW8PD7ti
QzVyZmC1mEQgX8OUFw4xz5ikKZhP0aHrd/btTpR1B5Y7+XqBGrIJwPN9+OltmPNx
RWdRkqi2JfFwB9/RmUsKWtALf43TCCanBAvjfsghsKxCQQcFGgHwvND/3c8beVK4
XlN1quweC6mKXXfE4BZdeaIHF+1NGKahfQYDmNQ23mzRmSJydg3KeYlaUCs4BA4e
k5UFeFAWxQ2NN6DIRotOydt3iDiJk4cgoPcM3798pQre+WOa59L/aX9gXxRo0JXK
AE0ups8chhwsfe/zJjCjqOnH6DF7bten2aS6/3LiTjRLu2fGcv67uETeGyJw7TPE
lUvMh/lpiamA7lgQbI69176vF9E3H2smSVt6YsYp7FL8UjaxGMOIXyNR10Rkp82b
sqHgYkcrGZuD/l8IiUMSINqxxZjOSWm83v0wkEpRZGzufdhFJxHcRBq0Y5r/nyXE
OJ3KcCykqIV3dPtV3jpY+6lSTKpquK87gWyNN2YuUjvhEWWcN6wFeZwUiUfxhI+A
S4ZIEa/g5EjLE6CddXXxUitb6ySOnefP7LS2uAxv8sav0+57PtYQwGsWrLjMuhgA
ZDqs0VbDIqpFRgCY4Tb6KADlP+66Cg3re+PkQQ0HQHYXdyYnUPfqcJxrK9FcaWwn
QPn2IfZ/R6/pg5fgd2ARg2YX0/aSkpQ5eOd6HBqG25L6fbcLBNTIVocNRSrlWWOI
LajjtATKktVRm9fNX18XX1Ea2TWS9jZeHg8fERDOe3wR61nD8VEMYLAbVKjkospI
xdKEEsEHiaFkdjuiYbuRIg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check2(response, aes_key, iv):
    # Flip the initialization vector
        flipped_iv = bytearray()
        for byte in iv:
            flipped_iv.append(byte ^ 0xFF)

        # Encrypt the response data
        encryptor = Cipher(algorithms.AES(aes_key),
                           modes.GCM(flipped_iv)).encryptor()
        return b64encode(
            encryptor.update(json.dumps(response).encode("utf-8")) +
            encryptor.finalize() +
            encryptor.tag
        ).decode("utf-8")


def autopayment(request):
    print("ssss auto payment")

    return render(request,'auto.html')


@csrf_exempt
def MY_bOT(request):
    # print("*******",request.data)
    request_data = json.loads(request.body)
    received_message = request_data
    print(received_message)

    try:
        if 'nfm_reply' in received_message['entry'][0]['changes'][0]['value']['messages'][0]['interactive']:
            print("yes you are in flows")
            whatsAppPhoneNumberId = received_message['entry'][0]['changes'][0]['value']['metadata'][
                'phone_number_id']
            toUser = received_message['entry'][0]['changes'][0]['value']['messages'][0]['from']
            print(whatsAppPhoneNumberId)
            print(toUser)
            response_json = \
                received_message['entry'][0]['changes'][0]['value']['messages'][0]['interactive'][
                    'nfm_reply'][
                    'response_json']

            response_data = json.loads(response_json)
            flow_token = response_data['flow_token']


            if all(key in response_data for key in ['firstName', 'lastName', 'email']):
                first_name = response_data.get('firstName')
                last_name = response_data.get('lastName')
                email = response_data.get('email')
                print(first_name)
                print(last_name)
                print(email)

                existing_visitor = appointment_visitor.objects.filter(Visitor_Whatsapp_Number=toUser).first()

                if existing_visitor:
                    # Update the existing record
                    existing_visitor.Visitor_Name = f'{first_name} {last_name}'  # Combine first and last names
                    existing_visitor.Visitor_email = email
                    existing_visitor.save()
                else:
                    # Create a new record
                    new_visitor = appointment_visitor(
                        Visitor_Whatsapp_Number=toUser,
                        Visitor_Name=f'{first_name} {last_name}',  # Combine first and last names
                        Visitor_email=email
                    )
                    new_visitor.save()

                facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                faceBookToken = ''
                # businessName = ''
                clientId = 0
                for tok in facebookObjects:
                    faceBookToken = faceBookToken + tok.fb_access_token
                    # businessName = businessName + tok.fb_name
                    clientId = clientId + tok.client_id

                url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + faceBookToken,
                    'Content-Type': 'application/json'
                }
                welcomeobj = appointment_settings.objects.filter(client_id=clientId)

                for don_i in welcomeobj:
                    if don_i.welcome_image:
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "button",
                                "header": {
                                    "type": "image",
                                    "image": {
                                        "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                        (don_i.welcome_image)
                                    }
                                },

                                "body": {
                                    "text": don_i.welcome_message if don_i.welcome_message else "."
                                },

                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "T123",
                                                "title": don_i.booking_button_name
                                            }
                                        },
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "T2",
                                                "title": don_i.my_bookings_button_name
                                            }
                                        },
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "T3",
                                                "title": don_i.contact_us_button_name
                                            }
                                        },

                                    ]
                                }
                            }
                        })

                        response = requests.request("POST", url, headers=headers, data=payload)
            elif 'radiobuttonsgroup' in response_data:

                print("s it is coming to survey flow")
                poll_answer = response_data.get('radiobuttonsgroup')
                position = poll_answer.find("R")
                servey_question_id = poll_answer[:position]
                print(servey_question_id)
                poll_response_id = poll_answer[position:]
                print(poll_response_id)
                question_info = Survey_Question.objects.filter(id=servey_question_id)
                response_value = ''
                survey_id = 0
                for q_i in question_info:
                    survey_id = q_i.Survey_list_id
                    if poll_response_id == "R1":
                        response_value = q_i.response_option1
                    elif poll_response_id == "R2":
                        response_value = q_i.response_option2
                    elif poll_response_id == "R3":
                        response_value = q_i.response_option3
                    elif poll_response_id == "R4":
                        response_value = q_i.response_option4
                print(response_value)
                print(survey_id)
                facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                faceBookToken = ''
                # businessName = ''
                clientId = 0
                for tok in facebookObjects:
                    faceBookToken = faceBookToken + tok.fb_access_token
                    # businessName = businessName + tok.fb_name
                    clientId = clientId + tok.client_id
                print(clientId)
                customer_info = Survey_Customer.objects.filter(customer_whatsapp_number=toUser)
                customer_id = 0
                for c_i in customer_info:
                    customer_id = c_i.id
                print(customer_id)
                print("s printed all the ids please check once")
                survey_customer_response = Survey_Customer_Response(
                    client_id = clientId,
                    Survey_list_id = survey_id,
                    Survey_Question_id = servey_question_id,
                    Survey_Customer_id = customer_id,
                    Survey_Response = response_value

                )
                survey_customer_response.save()
                print("succcesfully saved all the data")
                url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + faceBookToken,
                    'Content-Type': 'application/json'
                }
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": "Thank you for Voting"
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
            elif 'paybutton' in response_data:
                print("s payment link")
                link = response_data.get('paybutton')
                print(link)
                check(request,link)
            elif any(key in response_data for key in ['ngo_Name', 'ngo_location', 'ngo_category', 'ngo_type']):
                print("You are searching for NGO details. Please wait while it updates.")

                keys_to_check = ['ngo_Name', 'ngo_location', 'ngo_category', 'ngo_type']
                filters = {}

                # Mapping keys to corresponding model column names
                column_mapping = {
                    'ngo_Name': 'ngo_name',
                    'ngo_location': 'ngo_location',
                    'ngo_category': 'ngo_category',
                    'ngo_type': 'ngo_type'
                }

                for key in keys_to_check:
                    value = response_data.get(key)
                    if value:
                        db_column_name = column_mapping.get(key)
                        filters[f'{db_column_name}__icontains'] = value

                facebook_objects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                facebook_token = ''
                client_id = 0

                for tok in facebook_objects:
                    facebook_token += tok.fb_access_token
                    client_id += tok.client_id

                url = f"https://graph.facebook.com/v12.0/{whatsAppPhoneNumberId}/messages"
                headers = {
                    'Authorization': 'Bearer ' + facebook_token,
                    'Content-Type': 'application/json'
                }

                # Using Q objects to dynamically construct the query
                query = Q(client_id=client_id)
                for key, value in filters.items():
                    query |= Q(**{key: value})

                # Apply the constructed query to the donation_marketplace model
                donationObj = donation_marketplace.objects.filter(query)

                Ngo_Name = []
                Ngo_location = []
                Ngo_id = []

                if donationObj:
                    for l_i in donationObj:
                        Ngo_id.append(l_i.id)
                        Ngo_Name.append(l_i.ngo_name)
                        Ngo_location.append(l_i.ngo_location)

                    Ngo_list = [{"id": "A" + str(Ngo_id[i]),
                                 "title": Ngo_Name[i],
                                 "description": Ngo_location[i]}
                                for i in range(len(Ngo_Name))]

                    payload = {
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "list",
                            "body": {"text": "Please select the Ngo"},
                            "action": {
                                "button": "Ngos",
                                "sections": [{
                                    "title": "Ngos",
                                    "rows": Ngo_list
                                }]
                            }
                        }
                    }

                    response = requests.post(url, headers=headers, json=payload)
                else:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "preview_url": True,
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "text",
                        "text": {
                            "body": "No Search found."
                        }

                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
            elif any(key in response_data for key in ['amount', 'comments', 'name', 'email']):
                print("s exact way")
                d_amount = response_data.get('amount')
                d_comments = response_data.get('comments')
                d_name = response_data.get('name')
                d_email = response_data.get('email')
                flow_token = response_data.get('flow_token')
                print(flow_token)
                donation_ref_id = flow_token[15:51]
                donation_type_id = response_data.get('excess')
                donationId = donation_type_id[0]['id']
                print(donationId)
                facebook_objects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                facebook_token = ''
                client_id = 0
                for tok in facebook_objects:
                    facebook_token += tok.fb_access_token
                    client_id += tok.client_id
                donation_detailsobj = donation_types.objects.filter(client_id=client_id, id=donationId)
                print(donation_detailsobj)
                donationName = ''
                donationshortdesc = ''
                donationdesc = ''
                donationImage = ''
                market_placeId = 0
                donationAmount = 0
                Ngo_url = ''
                Ngo_text = ''
                for dj_i in donation_detailsobj:
                    market_placeId = dj_i.marketplace_id
                    donationName = dj_i.donation_name
                    donationshortdesc = dj_i.donation_short_description
                    donationdesc = dj_i.donation_description
                    donationImage = dj_i.donation_type_image
                    donationAmount = dj_i.donation_amount
                    infoobj = donation_marketplace.objects.filter(client_id=client_id, id=dj_i.marketplace_id)
                    for i in infoobj:
                        Ngo_url = i.ngo_url
                        Ngo_text = i.ngo_link_text
                donar_details = donation_details.objects.filter(client_id=client_id, donation_reference_id=donation_ref_id)
                print("bb")
                for dd_i in donar_details:
                    dd_i.donar_name = d_name
                    dd_i.donar_email = d_email
                    dd_i.donation_amount = donationAmount
                    dd_i.donation_name = donationName
                    dd_i.donation_short_description = donationshortdesc
                    dd_i.donation_description = donationdesc
                    dd_i.donation_type_image = donationImage
                    dd_i.donation_date = timezone.now().date()
                    dd_i.donation_comments_message = d_comments
                    dd_i.marketplace_id = market_placeId
                    dd_i.save()
                print("succeefylly saved")
                facebookDetails = facebook_details.objects.filter(client_id=client_id)
                clientNumber = ''
                for f_i in facebookDetails:
                    clientNumber = f_i.fb_whatsapp_number

                autopayment(request)

                # url = "https://api.razorpay.com/v1/payment_links"
                #
                # payload = json.dumps({
                #     "amount": donationAmount * 100,
                #     "currency": "INR",
                #     "accept_partial": False,
                #     "first_min_partial_amount": 0,
                #     "reference_id": "N" + str(donation_ref_id),
                #     "description": "Donation",
                #     "customer": {
                #         "name": "Gaurav Kumar",
                #         "contact": "918494863493",
                #         "email": "gaurav.kumar@example.com"
                #     },
                #     "notify": {
                #         "sms": True,
                #         "email": True
                #     },
                #     "reminder_enable": True,
                #     "notes": {
                #         "polacy_name": "N" + str(donation_ref_id)
                #     },
                #     "callback_url": f"https://wa.me/{clientNumber}",
                #     "callback_method": "get"
                # })
                # headers = {
                #     'Content-Type': 'application/json',
                #     'Authorization': 'Basic cnpwX2xpdmVfSU83R0Vyckkyam9RYXQ6aGt2SVhTZkpvM0x2TWhYaGx5VUpoWTBH'
                # }
                #
                # response = requests.request("POST", url, headers=headers, data=payload)
                #
                # a = response.text
                # json_str = json.dumps(a)
                # b = json.loads(json_str)
                # c = response.json()
                # print(c)
                # payment_link = c['short_url']
                # print(payment_link)

                # url = f"https://graph.facebook.com/v12.0/{whatsAppPhoneNumberId}/messages"
                # headers = {
                #     'Authorization': 'Bearer ' + facebook_token,
                #     'Content-Type': 'application/json'
                # }
                # print("hello")
                #
                # payload = json.dumps({
                #     "messaging_product": "whatsapp",
                #     "to": toUser,
                #
                #     "text": {
                #         "preview_url": True,
                #         "body": f"{Ngo_url}\n\n{Ngo_text}\n{payment_link}"
                #     }
                # })
                # response = requests.request("POST", url, headers=headers, data=payload)


            elif any(key in response_data for key in ['donar_Name', 'donar_Email', 'donar_Amount', 'donar_Comments']):
                print("s exact second way")
                d_amount = int(response_data.get('donar_Amount'))
                d_comments = response_data.get('donar_Comments')
                d_name = response_data.get('donar_Name')
                d_email = response_data.get('donar_Email')
                flow_token = response_data.get('flow_token')
                print(flow_token)
                donation_ref_id = flow_token[15:51]
                donation_type_id = response_data.get('excess_id')
                donationId = donation_type_id[0]['id']
                print(donationId)
                facebook_objects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                facebook_token = ''
                client_id = 0
                for tok in facebook_objects:
                    facebook_token += tok.fb_access_token
                    client_id += tok.client_id
                donation_detailsobj = donation_types.objects.filter(client_id=client_id, id=donationId)
                print(donation_detailsobj)
                donationName = ''
                donationshortdesc = ''
                donationdesc = ''
                donationImage = ''
                market_placeId = 0
                Ngo_url = ''
                Ngo_text = ''
                for dj_i in donation_detailsobj:
                    market_placeId = dj_i.marketplace_id
                    donationName = dj_i.donation_name
                    donationshortdesc = dj_i.donation_short_description
                    donationdesc = dj_i.donation_description
                    donationImage = dj_i.donation_type_image
                    infoobj = donation_marketplace.objects.filter(client_id=client_id, id=dj_i.marketplace_id)
                    for i in infoobj:
                        Ngo_url = i.ngo_url
                        Ngo_text = i.ngo_link_text

                donar_details = donation_details.objects.filter(client_id=client_id,
                                                                donation_reference_id=donation_ref_id)
                print("bb")
                for dd_i in donar_details:
                    dd_i.donar_name = d_name
                    dd_i.donar_email = d_email
                    dd_i.donation_amount = d_amount
                    dd_i.donation_name = donationName
                    dd_i.donation_short_description = donationshortdesc
                    dd_i.donation_description = donationdesc
                    dd_i.donation_type_image = donationImage
                    dd_i.donation_date = timezone.now().date()
                    dd_i.donation_comments_message = d_comments
                    dd_i.marketplace_id = market_placeId
                    dd_i.save()
                print("succeefylly saved second one")
                facebookDetails = facebook_details.objects.filter(client_id=client_id)
                clientNumber = ''
                for f_i in facebookDetails:
                    clientNumber = f_i.fb_whatsapp_number

                url = "https://api.razorpay.com/v1/payment_links"

                payload = json.dumps({
                    "amount": d_amount * 100,
                    "currency": "INR",
                    "accept_partial": False,
                    "first_min_partial_amount": 0,
                    "reference_id": "N" + str(donation_ref_id),
                    "description": "Donation",
                    "customer": {
                        "name": "Gaurav Kumar",
                        "contact": "918494863493",
                        "email": "gaurav.kumar@example.com"
                    },
                    "notify": {
                        "sms": True,
                        "email": True
                    },
                    "reminder_enable": True,
                    "notes": {
                        "polacy_name": "N" + str(donation_ref_id)
                    },
                    "callback_url": f"https://wa.me/{clientNumber}",
                    "callback_method": "get"
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic cnpwX2xpdmVfSU83R0Vyckkyam9RYXQ6aGt2SVhTZkpvM0x2TWhYaGx5VUpoWTBH'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                a = response.text
                json_str = json.dumps(a)
                b = json.loads(json_str)
                c = response.json()
                print(c)
                payment_link = c['short_url']
                print(payment_link)

                # url = f"https://graph.facebook.com/v12.0/{whatsAppPhoneNumberId}/messages"
                # headers = {
                #     'Authorization': 'Bearer ' + facebook_token,
                #     'Content-Type': 'application/json'
                # }
                # print("hello")
                #
                # payload = json.dumps({
                #     "messaging_product": "whatsapp",
                #     "to": toUser,
                #
                #     "text": {
                #         "preview_url": True,
                #         "body": f"{Ngo_url}\n\n{Ngo_text}\n{payment_link}"
                #     }
                # })
                # response = requests.request("POST", url, headers=headers, data=payload)
            elif any(key in response_data for key in ['User_Name', 'User_Email', 'User_Amount', 'User_Comments']):
                print("s after proceed")
                user_name = response_data.get('User_Name')
                user_email = response_data.get('User_Email')
                user_amount = int(response_data.get('User_Amount'))
                user_comments = response_data.get('User_Comments')
                flow_token = response_data.get('flow_token')
                parts = flow_token.split('/')
                donationId = parts[0]
                donation_ref_id = parts[1]
                facebook_objects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                facebook_token = ''
                client_id = 0
                for tok in facebook_objects:
                    facebook_token += tok.fb_access_token
                    client_id += tok.client_id
                donation_detailsobj = donation_types.objects.filter(client_id=client_id, id=donationId)
                print(donation_detailsobj)
                donationName = ''
                donationshortdesc = ''
                donationdesc = ''
                donationImage = ''
                # market_placeId = 0
                Ngo_url = ''
                Ngo_text = ''
                for dj_i in donation_detailsobj:
                    # market_placeId = dj_i.marketplace_id
                    donationName = dj_i.donation_name
                    donationshortdesc = dj_i.donation_short_description
                    donationdesc = dj_i.donation_description
                    donationImage = dj_i.donation_type_image
                    infoobj = donation_marketplace.objects.filter(client_id=client_id,id=dj_i.marketplace_id)

                    for i in infoobj:
                        Ngo_url = i.ngo_url
                        Ngo_text = i.ngo_link_text






                donar_details = donation_details.objects.filter(client_id=client_id,
                                                                donation_reference_id=donation_ref_id)
                print("bb")
                for dd_i in donar_details:
                    dd_i.donar_name = user_name
                    dd_i.donar_email = user_email
                    dd_i.donation_amount = user_amount
                    dd_i.donation_name = donationName
                    dd_i.donation_short_description = donationshortdesc
                    dd_i.donation_description = donationdesc
                    dd_i.donation_type_image = donationImage
                    dd_i.donation_date = timezone.now().date()
                    dd_i.donation_comments_message = user_comments
                    # dd_i.marketplace_id = market_placeId
                    dd_i.save()
                print("succeefylly saved second one")
                facebookDetails = facebook_details.objects.filter(client_id=client_id)
                clientNumber = ''
                for f_i in facebookDetails:
                    clientNumber = f_i.fb_whatsapp_number

                url = "https://api.razorpay.com/v1/payment_links"

                payload = json.dumps({
                    "amount": user_amount * 100,
                    "currency": "INR",
                    "accept_partial": False,
                    "first_min_partial_amount": 0,
                    "reference_id": "N" + str(donation_ref_id),
                    "description": "Donation",
                    "customer": {
                        "name": "Gaurav Kumar",
                        "contact": "918494863493",
                        "email": "gaurav.kumar@example.com"
                    },
                    "notify": {
                        "sms": True,
                        "email": True
                    },
                    "reminder_enable": True,
                    "notes": {
                        "polacy_name": "N" + str(donation_ref_id)
                    },
                    "callback_url": f"https://wa.me/{clientNumber}",
                    "callback_method": "get"
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic cnpwX2xpdmVfSU83R0Vyckkyam9RYXQ6aGt2SVhTZkpvM0x2TWhYaGx5VUpoWTBH'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                a = response.text
                json_str = json.dumps(a)
                b = json.loads(json_str)
                c = response.json()
                print(c)
                payment_link = c['short_url']
                print(payment_link)

                url = f"https://graph.facebook.com/v12.0/{whatsAppPhoneNumberId}/messages"
                headers = {
                    'Authorization': 'Bearer ' + facebook_token,
                    'Content-Type': 'application/json'
                }
                print("hello")
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "preview_url": True,
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "preview_url": True,
                        "body": f'{Ngo_url}\n\n{Ngo_text}\n\n{payment_link}'
                    }

                })
                response = requests.request("POST", url, headers=headers, data=payload)
            elif any(key in response_data for key in ['info_amount', 'info_comments', 'info_name', 'info_email']):
                print("s after proceed")
                user_name = response_data.get('info_name')
                user_email = response_data.get('info_email')
                # user_amount = int(response_data.get('info_amount'))
                user_comments = response_data.get('info_comments')
                flow_token = response_data.get('flow_token')
                parts = flow_token.split('/')
                donationId = parts[0]
                donation_ref_id = parts[1]
                facebook_objects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                facebook_token = ''
                client_id = 0
                for tok in facebook_objects:
                    facebook_token += tok.fb_access_token
                    client_id += tok.client_id
                donation_detailsobj = donation_types.objects.filter(client_id=client_id, id=donationId)
                print(donation_detailsobj)
                donationName = ''
                donationshortdesc = ''
                donationdesc = ''
                donationImage = ''
                # market_placeId = 0
                donation_Amount = 0
                Ngo_url = ''
                Ngo_text = ''
                for dj_i in donation_detailsobj:
                    # market_placeId = dj_i.marketplace_id
                    donationName = dj_i.donation_name
                    donationshortdesc = dj_i.donation_short_description
                    donationdesc = dj_i.donation_description
                    donationImage = dj_i.donation_type_image
                    donation_Amount = dj_i.donation_amount
                    infoobj = donation_marketplace.objects.filter(client_id=client_id, id=dj_i.marketplace_id)

                    for i in infoobj:
                        Ngo_url = i.ngo_url
                        Ngo_text = i.ngo_link_text

                donar_details = donation_details.objects.filter(client_id=client_id,
                                                                donation_reference_id=donation_ref_id)
                print("bb")
                for dd_i in donar_details:
                    dd_i.donar_name = user_name
                    dd_i.donar_email = user_email
                    # dd_i.donation_amount = user_amount
                    dd_i.donation_name = donationName
                    dd_i.donation_short_description = donationshortdesc
                    dd_i.donation_description = donationdesc
                    dd_i.donation_type_image = donationImage
                    dd_i.donation_date = timezone.now().date()
                    dd_i.donation_comments_message = user_comments
                    # dd_i.marketplace_id = market_placeId
                    dd_i.save()
                print("succeefylly saved second one")
                facebookDetails = facebook_details.objects.filter(client_id=client_id)
                clientNumber = ''
                for f_i in facebookDetails:
                    clientNumber = f_i.fb_whatsapp_number

                url = "https://api.razorpay.com/v1/payment_links"

                payload = json.dumps({
                    "amount": donation_Amount * 100,
                    "currency": "INR",
                    "accept_partial": False,
                    "first_min_partial_amount": 0,
                    "reference_id": "N" + str(donation_ref_id),
                    "description": "Donation",
                    "customer": {
                        "name": "Gaurav Kumar",
                        "contact": "918494863493",
                        "email": "gaurav.kumar@example.com"
                    },
                    "notify": {
                        "sms": True,
                        "email": True
                    },
                    "reminder_enable": True,
                    "notes": {
                        "polacy_name": "N" + str(donation_ref_id)
                    },
                    "callback_url": f"https://wa.me/{clientNumber}",
                    "callback_method": "get"
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic cnpwX2xpdmVfSU83R0Vyckkyam9RYXQ6aGt2SVhTZkpvM0x2TWhYaGx5VUpoWTBH'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                a = response.text
                json_str = json.dumps(a)
                b = json.loads(json_str)
                c = response.json()
                print(c)
                payment_link = c['short_url']
                print(payment_link)

                url = f"https://graph.facebook.com/v12.0/{whatsAppPhoneNumberId}/messages"
                headers = {
                    'Authorization': 'Bearer ' + facebook_token,
                    'Content-Type': 'application/json'
                }
                print("hello")
                payload = json.dumps({
                    "messaging_product": "whatsapp",

                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "preview_url": True,
                        "body": f'{Ngo_url}\n\n{Ngo_text}\n\n{payment_link}'
                    }

                })
                response = requests.request("POST", url, headers=headers, data=payload)
            elif any(key in response_data for key in ['group_Name', 'group_type', 'group_category', 'group_location']):
                print("You are searching for Hospital details. Please wait while it updates.")

                keys_to_check = ['group_Name', 'group_location', 'group_category', 'group_type']
                filters = {}

                # Mapping keys to corresponding model column names
                column_mapping = {
                    'group_Name': 'group_name',
                    'group_location': 'group_location',
                    'group_category': 'group_category',
                    'group_type': 'group_type'
                }

                for key in keys_to_check:
                    value = response_data.get(key)
                    if value:
                        db_column_name = column_mapping.get(key)
                        filters[f'{db_column_name}__icontains'] = value

                facebook_objects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                facebook_token = ''
                client_id = 0

                for tok in facebook_objects:
                    facebook_token += tok.fb_access_token
                    client_id += tok.client_id

                url = f"https://graph.facebook.com/v12.0/{whatsAppPhoneNumberId}/messages"
                headers = {
                    'Authorization': 'Bearer ' + facebook_token,
                    'Content-Type': 'application/json'
                }

                # Using Q objects to dynamically construct the query
                query = Q(client_id=client_id)
                for key, value in filters.items():
                    query |= Q(**{key: value})
            elif 'slots_data' in response_data:
                print("s slot info")
                response_id = response_data.get('slots_data')
                facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                faceBookToken = ''
                # businessName = ''
                clientId = 0
                for tok in facebookObjects:
                    faceBookToken = faceBookToken + tok.fb_access_token
                    # businessName = businessName + tok.fb_name
                    clientId = clientId + tok.client_id

                url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + faceBookToken,
                    'Content-Type': 'application/json'
                }

                print("scoming")
                print(response_id)
                booking_ref_id = uuid.uuid4()
                Components = response_id.split("/")
                ConsultantId = Components[0][1:]  # Remove the leading 's'
                VisitorId = Components[1]
                sdate = Components[3][:8]
                day = sdate[:2]
                month = sdate[2:4]
                year = sdate[4:]
                fdate = f'{day}/{month}/{year}'
                date_obj = datetime.strptime(str(fdate), "%d/%m/%Y")
                gdate = date_obj.strftime("%Y-%m-%d")
                duration = response_id.split(sdate)[1][:-1]
                # dpart = duration[11:]
                # print(dpart)
                start_time_str, end_time_str = duration.split('-')
                start_time = datetime.strptime(start_time_str.strip(), '%H:%M')
                end_time = datetime.strptime(end_time_str.strip(), '%H:%M')
                status_obj = Consultant_details.objects.filter(id=ConsultantId)
                approval_mode = ''
                market_place_ID = 0
                for a_i in status_obj:
                    approval_mode = a_i.approval_mode
                    market_place_ID = a_i.marketplace_id
                print(approval_mode)
                print(market_place_ID)
                print("s market place")
                if approval_mode == 'Automatic' or approval_mode == 'automatic':
                    print("s automatic")
                    booking = appointment_bookings(
                        client_id=clientId,
                        Visitor_id=VisitorId,
                        Consultant_settings_id=ConsultantId,
                        date=gdate,
                        start_time=start_time,
                        end_time=end_time,
                        status=1,
                        booking_reference_id=booking_ref_id,
                        customer_phone_number=toUser,
                        online_offline='offline',
                        marketplace_id=market_place_ID


                    )
                    booking.save()
                    print("successfully created one record in bookings")
                    showDetails = appointment_bookings.objects.filter(client_id=clientId,
                                                                      booking_reference_id=booking_ref_id)
                    for s_i in showDetails:
                        duration_start = s_i.start_time
                        duration_end = s_i.end_time
                        # start_time_obj1 = datetime.strptime(str(duration_start), "%H:%M")
                        # end_time_obj1 = datetime.strptime(str(duration_end), "%H:%M")
                        formatted_start_time1 = duration_start.strftime("%I:%M%p")
                        formatted_end_time1 = duration_end.strftime("%I:%M%p")
                        date = s_i.date
                        date_obj = datetime.strptime(str(date), '%Y-%m-%d')
                        New_date = date_obj.strftime('%d-%b-%Y')
                        status = "Booked" if s_i.status == 1 else "blocked"
                        detailsObj = Consultant_details.objects.filter(id=s_i.Consultant_settings_id)
                        consultantName = ''
                        specialization = ''
                        consultantImage = ''
                        for d_i in detailsObj:
                            consultantName = d_i.consultant_name
                            specialization = d_i.consultant_specialization
                            consultantImage = d_i.consultant_image

                        print("print")
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "button",
                                "header": {
                                    "type": "image",
                                    "image": {
                                        "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                        (consultantImage)
                                    }
                                },

                                "body": {
                                    "text": f'*Appointement details* :\n'
                                            f' *_Name_*: {consultantName}\n'
                                            f' *_Specialization_*: {specialization}\n'
                                            f' *_From_*: {formatted_start_time1} *_to_* {formatted_end_time1}\n'
                                            f' *_Date_*:{New_date}\n'
                                            f' *_Status_*:{status}\n'

                                },

                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "D1",
                                                "title": "Done"
                                            }
                                        }

                                    ]
                                }
                            }
                        })

                        response = requests.request("POST", url, headers=headers, data=payload)
                elif approval_mode == 'Manual' or approval_mode == 'manual':
                    print("s it is manual")
                    booking = appointment_bookings(
                        client_id=clientId,
                        Visitor_id=VisitorId,
                        Consultant_settings_id=ConsultantId,
                        date=gdate,
                        start_time=start_time,
                        end_time=end_time,
                        status=2,
                        booking_reference_id=booking_ref_id,
                        customer_phone_number=toUser,
                        online_offline='offline'

                    )
                    booking.save()
                    print("successfully created one record in bookings")
                    showDetails = appointment_bookings.objects.filter(client_id=clientId,
                                                                      booking_reference_id=booking_ref_id)
                    for s_i in showDetails:
                        duration_start = s_i.start_time
                        duration_end = s_i.end_time
                        # start_time_obj1 = datetime.strptime(str(duration_start), "%H:%M")
                        # end_time_obj1 = datetime.strptime(str(duration_end), "%H:%M")
                        formatted_start_time1 = duration_start.strftime("%I:%M%p")
                        formatted_end_time1 = duration_end.strftime("%I:%M%p")
                        date = s_i.date
                        date_obj = datetime.strptime(str(date), '%Y-%m-%d')
                        New_date = date_obj.strftime('%d %b %Y')
                        status = "Pending confirmation" if s_i.status == 2 else "."
                        detailsObj = Consultant_details.objects.filter(id=s_i.Consultant_settings_id)
                        consultantName = ''
                        specialization = ''
                        consultantImage = ''
                        for d_i in detailsObj:
                            consultantName = d_i.consultant_name
                            specialization = d_i.consultant_specialization
                            consultantImage = d_i.consultant_image

                        print("print")
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "button",
                                "header": {
                                    "type": "image",
                                    "image": {
                                        "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                        (consultantImage)
                                    }
                                },

                                "body": {
                                    "text": f'*Appointement details* :\n'
                                            f' *_Name_*: {consultantName}\n'
                                            f' *_Specialization_*: {specialization}\n'
                                            f' *_From_*: {formatted_start_time1} to {formatted_end_time1}\n'
                                            f' *_Date_*:{New_date}\n'
                                            f' *_Status_*:{status}\n'

                                },

                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "D1",
                                                "title": "Done"
                                            }
                                        }

                                    ]
                                }
                            }
                        })

                        response = requests.request("POST", url, headers=headers, data=payload)
            elif 's_data_info' in response_data:
                print("s it is coming to survey response  flow")
                poll_answer = response_data.get('s_data_info')
                print(poll_answer)
                position = poll_answer.find("R")
                servey_question_id = poll_answer[:position]
                print(servey_question_id)
                poll_response_id = poll_answer[position:]
                print(poll_response_id)
                question_info = Survey_Question.objects.filter(id=servey_question_id)
                response_value = ''
                survey_id = 0
                for q_i in question_info:
                    survey_id = q_i.marketplace_id
                    if poll_response_id == "R0":
                        response_value = q_i.response_option1
                    elif poll_response_id == "R1":
                        response_value = q_i.response_option2
                    elif poll_response_id == "R2":
                        response_value = q_i.response_option3
                    elif poll_response_id == "R3":
                        response_value = q_i.response_option4
                print(response_value)
                print(survey_id)
                facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                faceBookToken = ''
                # businessName = ''
                clientId = 0
                for tok in facebookObjects:
                    faceBookToken = faceBookToken + tok.fb_access_token
                    # businessName = businessName + tok.fb_name
                    clientId = clientId + tok.client_id
                print(clientId)
                customer_info = Survey_Customer.objects.filter(customer_whatsapp_number=toUser)
                customer_id = 0
                for c_i in customer_info:
                    customer_id = c_i.id
                print(customer_id)
                print("s printed all the ids please check once")
                survey_customer_response = Survey_Customer_Response(
                    client_id=clientId,
                    marketplace_id=survey_id,
                    Survey_Question_id=servey_question_id,
                    Survey_Customer_id=customer_id,
                    Survey_Response=response_value

                )
                survey_customer_response.save()
                print("succcesfully saved all the data")
                url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + faceBookToken,
                    'Content-Type': 'application/json'
                }
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": "Thank you for Voting"
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
            elif 'MY_data' in response_data:
                print("s it is coming to survey response  flow")
                poll_answer = response_data.get('MY_data')
                print(poll_answer)
                position = poll_answer.find("R")
                servey_question_id = poll_answer[:position]
                print(servey_question_id)
                poll_response_id = poll_answer[position:]
                print(poll_response_id)
                question_info = Survey_Question.objects.filter(id=servey_question_id)
                response_value = ''
                survey_id = 0
                for q_i in question_info:
                    survey_id = q_i.marketplace_id
                    if poll_response_id == "R0":
                        response_value = q_i.response_option1
                    elif poll_response_id == "R1":
                        response_value = q_i.response_option2
                    elif poll_response_id == "R2":
                        response_value = q_i.response_option3
                    elif poll_response_id == "R3":
                        response_value = q_i.response_option4
                print(response_value)
                print(survey_id)
                facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                faceBookToken = ''
                # businessName = ''
                clientId = 0
                for tok in facebookObjects:
                    faceBookToken = faceBookToken + tok.fb_access_token
                    # businessName = businessName + tok.fb_name
                    clientId = clientId + tok.client_id
                print(clientId)
                customer_info = Survey_Customer.objects.filter(customer_whatsapp_number=toUser)
                customer_id = 0
                for c_i in customer_info:
                    customer_id = c_i.id
                print(customer_id)
                print("s printed all the ids please check once")
                survey_customer_response = Survey_Customer_Response(
                    client_id=clientId,
                    marketplace_id=survey_id,
                    Survey_Question_id=servey_question_id,
                    Survey_Customer_id=customer_id,
                    Survey_Response=response_value

                )
                survey_customer_response.save()
                print("succcesfully saved all the data")
                url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + faceBookToken,
                    'Content-Type': 'application/json'
                }
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": "Thank you for Voting"
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
            elif 'campaign_data_info' in response_data:
                response_id = response_data.get('campaign_data_info')
                facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                faceBookToken = ''
                # businessName = ''
                clientId = 0
                for tok in facebookObjects:
                    faceBookToken = faceBookToken + tok.fb_access_token
                    # businessName = businessName + tok.fb_name
                    clientId = clientId + tok.client_id

                url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + faceBookToken,
                    'Content-Type': 'application/json'
                }
                print(response_id)
                campaign_marketplace_id = response_id[1:]
                template_infoobj = template_info.objects.filter(client_id=clientId,marketplace_id=campaign_marketplace_id)
                campaign_data = generic_campaign_info.objects.filter(client_id=clientId,marketplace_id=campaign_marketplace_id)
                print("rr")
                first_value = ''
                second_value = ''
                third_value = ''
                camapaign_Name = ''
                camapign_Message = ''
                campaign_image = ''
                for campaign in campaign_data:
                    camapaign_Name = campaign.Campaign_Name
                    camapign_Message = campaign.Campaign_message
                    campaign_image = campaign.Campaign_Image

                campaign_values = [value.strip() for value in camapign_Message.split(',')]
                if len(campaign_values) >= 1:
                    first_value = campaign_values[0]  # end of May
                if len(campaign_values) >= 2:
                    second_value = campaign_values[1]  # 250OFF
                if len(campaign_values) >= 3:
                    third_value = campaign_values[2]
                template_Name = ''
                header_type = ''
                for t_i in template_infoobj:
                    template_Name = t_i.template_name
                    header_type = t_i.template_header_type
                # Important code dynamic button taking in json
                # button_componets = []
                # details_infoobj = template_info_details.objects.filter(client_id=clientId,marketplace_id=campaign_marketplace_id)
                # for d_i in details_infoobj:
                #     if d_i.template_button_type == 'URL' or d_i.template_button_type == 'url':
                #         url_button = {
                #             "type": "button",
                #             "sub_type": "url",
                #             "index": "3",
                #             "parameters": [
                #                 {
                #                     "type": "text",
                #                     "text": "admin"
                #                 }
                #             ]
                #         }
                #         button_componets.append(url_button)
                #     elif d_i.template_button_type == 'QUICK_REPLY' or d_i.template_button_type == 'quick_reply':
                #         reply_button = {
                #             "type": "button",
                #             "sub_type": "quick_reply",
                #             "index": "1",
                #             "parameters": [
                #                 {
                #                     "type": "payload",
                #                     "payload": "9rwnB8RbYmPF5t2Mn09x4h"
                #                 }
                #             ]
                #         }
                #         button_componets.append(reply_button)
                #     elif d_i.template_button_type == 'PHONE_NUMBER' or d_i.template_button_type == 'phone_number':
                #         phone_reply = {
                #
                #                 "type": "PHONE_NUMBER",
                #                 "text": "Call",
                #                 "phone_number": "15550051310"
                #
                #         }
                #         button_componets.append(phone_reply)
                #
                if header_type == 'text' or header_type == 'TEXT':
                    url = f"https://graph.facebook.com/v15.0/{whatsAppPhoneNumberId}/messages"

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "template",
                        "template": {
                            "name": template_Name,
                            "language": {
                                "code": "en_Us"
                            },
                            "components": [
                                {
                                    "type": "header",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": camapaign_Name
                                        }
                                    ]
                                },
                                {
                                    "type": "body",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": first_value
                                        },
                                        {
                                            "type": "text",
                                            "text": second_value
                                        },
                                        {
                                            "type": "text",
                                            "text": third_value
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "url",
                                    "index": "3",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": "admin"
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "quick_reply",
                                    "index": "1",
                                    "parameters": [
                                        {
                                            "type": "payload",
                                            "payload": "9rwnB8RbYmPF5t2Mn09x4h"
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "quick_reply",
                                    "index": "2",
                                    "parameters": [
                                        {
                                            "type": "payload",
                                            "payload": "aGlzIHRoaXMgaXMgY29v"
                                        }
                                    ]
                                }
                            ]
                        }
                    })
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {faceBookToken}'
                    }

                    response = requests.request("POST", url, headers=headers, data=payload)

                    print(response.text)
                else:
                    url = f"https://graph.facebook.com/v15.0/{whatsAppPhoneNumberId}/messages"

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "template",
                        "template": {
                            "name": template_Name,
                            "language": {
                                "code": "en_Us"
                            },
                            "components": [
                                {
                                    "type": "header",
                                    "parameters": [
                                        {
                                            "type": "image",
                                            "image": {
                                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                                (campaign_image)
                                            }
                                        }
                                    ]
                                },
                                {
                                    "type": "body",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": first_value
                                        },
                                        {
                                            "type": "text",
                                            "text": second_value
                                        },
                                        {
                                            "type": "text",
                                            "text": third_value
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "url",
                                    "index": "3",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": "admin"
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "quick_reply",
                                    "index": "1",
                                    "parameters": [
                                        {
                                            "type": "payload",
                                            "payload": "9rwnB8RbYmPF5t2Mn09x4h"
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "quick_reply",
                                    "index": "2",
                                    "parameters": [
                                        {
                                            "type": "payload",
                                            "payload": "aGlzIHRoaXMgaXMgY29v"
                                        }
                                    ]
                                }
                            ]
                        }
                    })
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {faceBookToken}'
                    }

                    response = requests.request("POST", url, headers=headers, data=payload)

                    print(response.text)


            elif 'my_campaign_data_info' in response_data:
                response_id = response_data.get('my_campaign_data_info')
                facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                faceBookToken = ''
                # businessName = ''
                clientId = 0
                for tok in facebookObjects:
                    faceBookToken = faceBookToken + tok.fb_access_token
                    # businessName = businessName + tok.fb_name
                    clientId = clientId + tok.client_id

                url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + faceBookToken,
                    'Content-Type': 'application/json'
                }
                print(response_id)
                campaign_id = response_id[1:]
                template_Name = ''
                header_type = ''
                template_det = template_info.objects.filter(client_id=clientId,generic_campaign_info_id=campaign_id)
                for t_i in template_det:
                    template_Name = t_i.template_name
                    header_type = t_i.template_header_type

                campaign_data = generic_campaign_info.objects.filter(client_id=clientId,
                                                                     id=campaign_id)
                print("rr")
                first_value = ''
                second_value = ''
                third_value = ''
                camapaign_Name = ''
                camapign_Message = ''
                campaign_image = ''
                for campaign in campaign_data:
                    camapaign_Name = campaign.Campaign_Name
                    camapign_Message = campaign.Campaign_message
                    campaign_image = campaign.Campaign_Image

                campaign_values = [value.strip() for value in camapign_Message.split(',')]
                if len(campaign_values) >= 1:
                    first_value = campaign_values[0]  # end of May
                if len(campaign_values) >= 2:
                    second_value = campaign_values[1]  # 250OFF
                if len(campaign_values) >= 3:
                    third_value = campaign_values[2]

                if header_type == 'text' or header_type == 'TEXT':
                    url = f"https://graph.facebook.com/v15.0/{whatsAppPhoneNumberId}/messages"

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "template",
                        "template": {
                            "name": template_Name,
                            "language": {
                                "code": "en_Us"
                            },
                            "components": [
                                {
                                    "type": "header",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": camapaign_Name
                                        }
                                    ]
                                },
                                {
                                    "type": "body",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": first_value
                                        },
                                        {
                                            "type": "text",
                                            "text": second_value
                                        },
                                        {
                                            "type": "text",
                                            "text": third_value
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "url",
                                    "index": "3",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": "admin"
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "quick_reply",
                                    "index": "1",
                                    "parameters": [
                                        {
                                            "type": "payload",
                                            "payload": "9rwnB8RbYmPF5t2Mn09x4h"
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "quick_reply",
                                    "index": "2",
                                    "parameters": [
                                        {
                                            "type": "payload",
                                            "payload": "aGlzIHRoaXMgaXMgY29v"
                                        }
                                    ]
                                }
                            ]
                        }
                    })
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {faceBookToken}'
                    }

                    response = requests.request("POST", url, headers=headers, data=payload)

                    print(response.text)
                else:
                    url = f"https://graph.facebook.com/v15.0/{whatsAppPhoneNumberId}/messages"

                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "template",
                        "template": {
                            "name": template_Name,
                            "language": {
                                "code": "en_Us"
                            },
                            "components": [
                                {
                                    "type": "header",
                                    "parameters": [
                                        {
                                            "type": "image",
                                            "image": {
                                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                                (campaign_image)
                                            }
                                        }
                                    ]
                                },
                                {
                                    "type": "body",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": first_value
                                        },
                                        {
                                            "type": "text",
                                            "text": second_value
                                        },
                                        {
                                            "type": "text",
                                            "text": third_value
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "url",
                                    "index": "3",
                                    "parameters": [
                                        {
                                            "type": "text",
                                            "text": "admin"
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "quick_reply",
                                    "index": "1",
                                    "parameters": [
                                        {
                                            "type": "payload",
                                            "payload": "9rwnB8RbYmPF5t2Mn09x4h"
                                        }
                                    ]
                                },
                                {
                                    "type": "button",
                                    "sub_type": "quick_reply",
                                    "index": "2",
                                    "parameters": [
                                        {
                                            "type": "payload",
                                            "payload": "aGlzIHRoaXMgaXMgY29v"
                                        }
                                    ]
                                }
                            ]
                        }
                    })
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {faceBookToken}'
                    }

                    response = requests.request("POST", url, headers=headers, data=payload)

                    print(response.text)
            elif any(re.match(r'\b(text|password|number|email|phone|radio|checkbox|select)_\d+\b', key) for key in response_data):
                print("s dynamic way")
                print(response_data)
                flow_token = response_data.get('flow_token')
                print(flow_token)
                t_infodetails = flow_token.split('/')
                formID = t_infodetails[0]
                tempInfoDetID = t_infodetails[1]
                print(tempInfoDetID)
                facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                faceBookToken = ''
                # businessName = ''
                clientId = 0
                campaignID = 0
                additionalInfo1data = ''
                marketplaceId = 0
                for tok in facebookObjects:
                    faceBookToken = faceBookToken + tok.fb_access_token
                    # businessName = businessName + tok.fb_name
                    clientId = clientId + tok.client_id


                campaignObj = template_info_details.objects.filter(client_id=clientId,id=tempInfoDetID)
                for r_i in campaignObj:
                    campaignID = r_i.generic_campaign_info_id
                    template_button_types = r_i.template_button_type
                    additionalInfo1data = r_i.template_additional_info1
                    marketplaceId = r_i.marketplace_id
                    campaign_NameObj = generic_campaign_info.objects.filter(client_id=clientId,
                                                                            id=r_i.generic_campaign_info_id)
                    for g_i in campaign_NameObj:
                        campaign_Name = g_i.Campaign_Name

                update_info = generic_campaign_history.objects.filter(client_id=clientId,
                                                                      Customer_Whatsapp_Number=toUser,
                                                                      generic_campaign_info_id=campaignID).order_by( '-vailo_record_creation').first()
                if update_info:
                    print("s form data collecting")
                    update_info.Campaign_Form_data = response_data
                    update_info.save()
                    print("succssfully saved form data")


                updateFormDataObj = campaign_formdata.objects.create(
                    client_id=clientId,
                    marketplace_id=marketplaceId,
                    generic_campaign_info_id=campaignID,
                    Campaign_Form_data=response_data,
                    Form_id=formID
                )
                updateFormDataObj.save()
                print("successfully created one new recods in formdata table")


                url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + faceBookToken,
                    'Content-Type': 'application/json'
                }

                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": additionalInfo1data
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
            # elif any(key in response_data for key in ['Call Back time', 'Preffered Language', 'Mobile Number', 'Email','Name']):
            #     print("s this is hardcode way")
            #     facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
            #     faceBookToken = ''
            #     # businessName = ''
            #     clientId = 0
            #     for tok in facebookObjects:
            #         faceBookToken = faceBookToken + tok.fb_access_token
            #         # businessName = businessName + tok.fb_name
            #         clientId = clientId + tok.client_id
            #
            #     url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
            #     headers = {
            #         'Authorization': 'Bearer ' + faceBookToken,
            #         'Content-Type': 'application/json'
            #     }
            #
            #     payload = json.dumps({
            #         "messaging_product": "whatsapp",
            #         "recipient_type": "individual",
            #         "to": toUser,
            #         "type": "text",
            #         "text": {
            #             "body": "Your details have been successfully submitted. Our executive will contact you soon. Thank you."
            #         }
            #     })
            #
            #     response = requests.request("POST", url, headers=headers, data=payload)
            elif 'campaign' in flow_token:
                print("s ur in same direction")

                flow_token = response_data['flow_token']
                print(flow_token)
                print("ffftoken")
                all_values = flow_token.split('/')
                formID = all_values[1]
                tempInfoDetID = all_values[2]
                print(formID)
                print(tempInfoDetID)

                facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                faceBookToken = ''
                # businessName = ''
                clientId = 0
                campaignID = 0
                additionalInfo1data = ''
                marketplaceId = 0
                for tok in facebookObjects:
                    faceBookToken = faceBookToken + tok.fb_access_token
                    # businessName = businessName + tok.fb_name
                    clientId = clientId + tok.client_id
                campaignObj = template_info_details.objects.filter(client_id=clientId,id=tempInfoDetID)
                print("ss")
                print(campaignObj)
                for r_i in campaignObj:
                    campaignID = r_i.generic_campaign_info_id
                    template_button_types = r_i.template_button_type
                    additionalInfo1data = r_i.template_additional_info1
                    # marketplaceId = r_i.marketplace_id
                    # campaign_NameObj = generic_campaign_info.objects.filter(client_id=clientId,
                    #                                                         id=r_i.generic_campaign_info_id)
                    # for g_i in campaign_NameObj:
                    #     campaign_Name = g_i.Campaign_Name
                print("dd")

                update_info = generic_campaign_history.objects.filter(client_id=clientId,
                                                                      Customer_Whatsapp_Number=toUser,
                                                                      generic_campaign_info_id=campaignID).order_by('-vailo_record_creation').first()
                print("ll")
                print(update_info)
                if update_info:
                    print("s form data collecting")
                    update_info.Campaign_Form_data = response_data
                    update_info.save()
                    print("succssfully saved form data")

                updateFormDataObj = campaign_formdata.objects.create(
                    client_id=clientId,
                    # marketplace_id=marketplaceId,
                    generic_campaign_info_id=campaignID,
                    Campaign_Form_data=response_data,
                    form_info=formID
                )
                updateFormDataObj.save()
                print("successfully created one new recods in formdata table")

                url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + faceBookToken,
                    'Content-Type': 'application/json'
                }

                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": additionalInfo1data
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)








    except KeyError as e:
        print(f"KeyError occurred: {e}")

    first_key_from_meesage,first_value_from_message = next(iter(received_message.items()))
    # print(first_key_from_meesage,first_value_from_message)

    if first_key_from_meesage == "object" and first_value_from_message == "whatsapp_business_account":

        url_for_domain = DomainName[:-1]
        # url_for_domain='https://0937-116-75-94-183.ngrok.io'
        b = ''
        for i in request:
            b = b + str(i)[2:-1]

        x = b.replace('true', 'True')
        y = x.replace('false', 'False')
        res = ast.literal_eval(y)

        # print("+++++++++",res)
        key_var = res['entry'][0]['changes'][0]['value'].keys()
        condition_list = list(key_var)

        if 'messages' in condition_list:
            if 'button' in res['entry'][0]['changes'][0]['value']['messages'][0]:
                text_value =res['entry'][0]['changes'][0]['value']['messages'][0]['button']['payload']
                textinfo = res['entry'][0]['changes'][0]['value']['messages'][0]['button']['text']
                whatsAppPhoneNumberId = res['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
                toUser = res['entry'][0]['changes'][0]['value']['messages'][0]['from']
                first_letter = text_value[0]
                if first_letter == 'B' or first_letter == 'b':
                    print("s b")
                    t_ID = text_value[1:]
                    print(text_value)
                    print("ss")
                    facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                    faceBookToken = ''
                    # businessName = ''
                    clientId = 0
                    for tok in facebookObjects:
                        faceBookToken = faceBookToken + tok.fb_access_token
                        # businessName = businessName + tok.fb_name
                        clientId = clientId + tok.client_id

                    print(clientId)
                    # ____________________________________API URL and HEADERS__________________________________

                    url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
                    headers = {
                        'Authorization': 'Bearer ' + faceBookToken,
                        'Content-Type': 'application/json'
                    }
                    campaignID = 0
                    campaign_Name = ''
                    template_button_types = ''

                    campaignObj = template_info_details.objects.filter(client_id=clientId, id=t_ID)
                    for r_i in campaignObj:
                        campaignID = r_i.generic_campaign_info_id
                        template_button_types = r_i.template_button_type
                        campaign_NameObj = generic_campaign_info.objects.filter(client_id=clientId,
                                                                                id=r_i.generic_campaign_info_id)
                        for g_i in campaign_NameObj:
                            campaign_Name = g_i.Campaign_Name
                    import datetime
                    indian_timezone = pytz.timezone('Asia/Kolkata')
                    current_date_time = datetime.datetime.now(indian_timezone)
                    # Format the date and time
                    formatted_datetime = current_date_time.strftime('%d-%m-%y %H:%M:%S')
                    print("Current Date and Time in Indian Standard Time (IST):", formatted_datetime)
                    date_part, time_part = formatted_datetime.split(' ')
                    date_object = datetime.datetime.strptime(date_part, '%d-%m-%y').date()
                    formatted_date_obj = date_object.strftime('%Y-%m-%d')
                    new_record = campaign_footprint.objects.create(
                        From_number=toUser,
                        button=textinfo,
                        campaign_name=campaign_Name,
                        date=formatted_date_obj,
                        time=time_part,
                        client_id=clientId
                    )
                    new_record.save()
                    print("successfully created a new record")
                    new_key_value = {
                        'Date': date_part,
                        'Time': time_part,
                        'Button': textinfo,
                        'From': toUser,
                        'Campaign_Name': campaign_Name
                    }

                    update_info = generic_campaign_history.objects.filter(client_id=clientId,
                                                                          Customer_Whatsapp_Number=toUser,
                                                                          generic_campaign_info_id=campaignID).order_by(
                        '-vailo_record_creation').first()
                    if update_info:
                        print('vaisakh')
                        print(update_info)
                        if update_info.Campaign_Foot_Print:
                            print("zzzzzooooo")
                            existing_campaign_footprint = update_info.Campaign_Foot_Print
                            if isinstance(existing_campaign_footprint, list):
                                # Append the new dictionary to the list
                                existing_campaign_footprint.append(new_key_value)
                            else:
                                # Create a list and add both dictionaries
                                existing_campaign_footprint = [existing_campaign_footprint, new_key_value]

                            update_info.Campaign_Foot_Print = existing_campaign_footprint
                        else:
                            update_info.Campaign_Foot_Print = new_key_value

                        update_info.save()
                        print("s archith")
                    else:
                        new_record = generic_campaign_history.objects.create(
                            client_id=clientId,
                            Customer_Whatsapp_Number=toUser,
                            generic_campaign_info_id=campaignID,
                            Campaign_Foot_Print=new_key_value
                        )
                        new_record.save()
                    if template_button_types.lower() == 'video':
                        print("s video  coming")
                        video_file_path = ''
                        tempDetails = template_info_details.objects.filter(client_id=clientId, id=t_ID)
                        print(tempDetails)
                        for j in tempDetails:
                            video_file_path = j.template_file_path
                            print(video_file_path)
                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "video",
                                "video": {
                                    "link": f'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/{video_file_path}',
                                    "caption": j.template_additional_info
                                }
                            })
                            response = requests.request("POST", url, headers=headers, data=payload)



                    elif template_button_types.lower() == 'document':
                        video_file_path = ''
                        template_infoDetails = template_info_details.objects.filter(client_id=clientId, id=t_ID)
                        for t_i in template_infoDetails:
                            video_file_path = t_i.template_file_path
                            out_name = video_file_path.name
                            File_Name = out_name.split("/")
                            Output_File_Name = File_Name[-1]
                            print("file name is", Output_File_Name)
                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "document",
                                "document": {
                                    "link": f'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/{video_file_path}',
                                    "filename": Output_File_Name
                                }
                            })
                            response = requests.request("POST", url, headers=headers, data=payload)
                    elif template_button_types.lower() == 'image':
                        video_file_path = ''
                        template_infoDetails = template_info_details.objects.filter(client_id=clientId, id=t_ID)
                        for t_i in template_infoDetails:
                            video_file_path = t_i.template_file_path
                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "image",
                                "image": {
                                    "link": f'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/{video_file_path}',

                                }
                            })
                            response = requests.request("POST", url, headers=headers, data=payload)
                    elif template_button_types.lower() == 'stop':
                        print("process is going on")
                    elif template_button_types.lower() == 'form':
                        print("s form")
                        flow_ID = 0
                        template_ID = 0
                        template_infoDetails = template_info_details.objects.filter(client_id=clientId, id=t_ID)
                        for t_i in template_infoDetails:
                            template_ID = t_i.id
                            flow_ID = t_i.template_additional_info
                        print(flow_ID)
                        formInfoObj = Form.objects.filter(client_id=clientId,id=flow_ID)
                        print(formInfoObj)
                        for f_i in formInfoObj:
                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "to": toUser,
                                "recipient_type": "individual",
                                "type": "interactive",
                                "interactive": {
                                    "type": "flow",
                                    "header": {
                                        "type": "text",
                                        "text": f_i.form_header_text
                                    },
                                    "body": {
                                        "text": f_i.form_body_text
                                    },
                                    "footer": {
                                        "text": f_i.form_body_footer
                                    },
                                    "action": {
                                        "name": "flow",
                                        "parameters": {
                                            "flow_message_version": "3",
                                            "flow_action": "navigate",
                                            "flow_token": f'campaign/{f_i.id}/{template_ID}',
                                            "flow_id": f_i.flow_id,
                                            "flow_cta": f_i.form_open_button_name,
                                            "flow_action_payload": {
                                                "screen": f_i.screen_name,
                                                "data": {
                                                    "id": "0",
                                                    "title": "Yes"
                                                }
                                            }
                                        }
                                    }
                                }
                            })
                            response = requests.request("POST", url, headers=headers, data=payload)
                    elif template_button_types.lower() == 'inflow':
                        inflow_details_obj = Inflow_Setup_Details.objects.filter(client_id=clientId, Parent_ID="0")
                        print(inflow_details_obj)
                        for n_i in inflow_details_obj:
                            parentInfoDetails = Inflow_Setup_Details.objects.filter(client_id=clientId,
                                                                                    Parent_ID=n_i.id)
                            print("parent", parentInfoDetails)
                            info_id = []
                            info_description = []
                            info_button_name = []
                            for p_i in parentInfoDetails:
                                info_id.append(p_i.id)
                                info_description.append(p_i.short_description)
                                info_button_name.append(p_i.short_title)
                            print(info_button_name)
                            list_all_buttons = []
                            for h_i in range(len(info_button_name)):
                                list_all_buttons.append({
                                    "id": "I" + str(info_id[h_i]),
                                    "title": info_button_name[h_i],
                                    "description": info_description[h_i]
                                })

                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "list",
                                    "header": {
                                        "type": "text",
                                        "text": n_i.inflow_header_text
                                    },
                                    "body": {
                                        "text": n_i.inflow_body_text
                                    },
                                    "footer": {
                                        "text": n_i.inflow_footer_text
                                    },
                                    "action": {
                                        "button": n_i.open_button_name,
                                        "sections": [
                                            {
                                                "title": "Locations",
                                                "rows": list_all_buttons
                                            }

                                        ]
                                    }
                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)
                    elif template_button_types.lower() == 'campaign':
                        print("s campaign")
                        tempDetails = template_info_details.objects.filter(client_id=clientId, id=t_ID)
                        print(tempDetails)
                        campaignId = 0
                        for t_i in tempDetails:
                            campaignId = t_i.template_additional_info

                        template_infoobj = template_info.objects.filter(client_id=clientId, generic_campaign_info_id=campaignId)
                        template_Name = ''
                        header_type = ''
                        header_text = ''
                        template_image = ''
                        for t_i in template_infoobj:
                            template_Name = t_i.template_name
                            header_type = t_i.template_header_type
                            header_text = t_i.template_header_text
                            template_image = t_i.template_header_image
                            button_componets = []
                            index_counter = 8
                            index_counter1 = 0
                            details_infoobj = template_info_details.objects.filter(client_id=request.user.id,
                                                                                   template_info_id=t_i.id)
                            for d_i in details_infoobj:
                                if 'url' in d_i.template_button_type.lower() or 'phone_number' in d_i.template_button_type.lower() or 'phone number' in d_i.template_button_type.lower():
                                    url_button = {
                                        "type": "button",
                                        "sub_type": "url",
                                        "index": str(index_counter),
                                        "parameters": [
                                            {
                                                "type": "text",
                                                "text": "admin"
                                            }
                                        ]
                                    }
                                    button_componets.append(url_button)
                                    index_counter += 1
                                elif 'image' in d_i.template_button_type.lower() or 'brochure' in d_i.template_button_type.lower() or 'document' in d_i.template_button_type.lower() or 'video' in d_i.template_button_type.lower() or 'stop' in d_i.template_button_type.lower() or 'form' in d_i.template_button_type.lower() or 'inflow' in d_i.template_button_type.lower() or 'campaign' in d_i.template_button_type.lower():
                                    print(d_i.template_button_type)
                                    reply_button = {
                                        "type": "button",
                                        "sub_type": "quick_reply",
                                        "index": str(index_counter1),
                                        "parameters": [
                                            {
                                                "type": "payload",
                                                "payload": f"B{d_i.id}"
                                            }
                                        ]
                                    }
                                    button_componets.append(reply_button)
                                    index_counter1 += 1

                            if header_type == 'text' or header_type == 'TEXT':
                                url = f"https://graph.facebook.com/v15.0/{whatsAppPhoneNumberId}/messages"

                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "template",
                                    "template": {
                                        "name": template_Name,
                                        "language": {
                                            "code": "en_Us"
                                        },
                                        "components": [
                                            {
                                                "type": "header",
                                                "parameters": [

                                                ]
                                            },
                                            {
                                                "type": "body",
                                                "parameters": [

                                                ]
                                            },
                                            *button_componets
                                        ]
                                    }
                                })
                                headers = {
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {faceBookToken}'
                                }

                                response = requests.request("POST", url, headers=headers, data=payload)

                                print(response.text)


                            else:
                                url = f"https://graph.facebook.com/v15.0/{whatsAppPhoneNumberId}/messages"

                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "template",
                                    "template": {
                                        "name": template_Name,
                                        "language": {
                                            "code": "en_Us"
                                        },
                                        "components": [
                                            {
                                                "type": "header",
                                                "parameters": [
                                                    {
                                                        "type": "image",
                                                        "image": {
                                                            "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                                            (template_image)
                                                        }
                                                    }
                                                ]
                                            },
                                            {
                                                "type": "body",
                                                "parameters": [

                                                ]
                                            },
                                            *button_componets
                                        ]
                                    }
                                })
                                headers = {
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {faceBookToken}'
                                }

                                response = requests.request("POST", url, headers=headers, data=payload)

                                print(response.text)
                elif first_letter == 'C' or first_letter == 'c':
                    print('s c')
                    payload_ID = res['entry'][0]['changes'][0]['value']['messages'][0]['button']['payload']
                    print(payload_ID)
                    inflow_Id = payload_ID[1:]

                    print(inflow_Id)

                    print("s pattern doenot contains a number and you are in same loop")
                    facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                    faceBookToken = ''
                    # businessName = ''
                    clientId = 0
                    for tok in facebookObjects:
                        faceBookToken = faceBookToken + tok.fb_access_token
                        # businessName = businessName + tok.fb_name
                        clientId = clientId + tok.client_id

                    print(clientId)
                    print("s both client ids same")
                    # ____________________________________API URL and HEADERS__________________________________

                    url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
                    headers = {
                        'Authorization': 'Bearer ' + faceBookToken,
                        'Content-Type': 'application/json'
                    }
                    button_type = ''
                    detailsInfo = Inflow_Setup_Details.objects.filter(client_id=clientId, id=inflow_Id)
                    for d_i in detailsInfo:
                        button_type = d_i.open_button_type

                    if button_type.lower() == 'chain':
                        parentInfoObj = Inflow_Setup_Details.objects.filter(client_id=clientId,
                                                                            Parent_ID=inflow_Id)
                        print("s second level of interactive chain")
                        second_info_id = []
                        second_info_button_name = []
                        second_info_description = []
                        for s_i in parentInfoObj:
                            second_info_id.append(s_i.id)
                            second_info_button_name.append(s_i.short_title)
                            second_info_description.append(s_i.short_description)
                        list_second_details = []
                        for i in range(len(second_info_button_name)):
                            list_second_details.append({
                                "id": "I" + str(second_info_id[i]),
                                "title": second_info_button_name[i],
                                "description": second_info_description[i]

                            })
                        infoObjDetails = Inflow_Setup_Details.objects.filter(client_id=clientId, id=inflow_Id)
                        for n_i in infoObjDetails:
                            if n_i.inflow_header_type.lower() == 'text':
                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "interactive",
                                    "interactive": {
                                        "type": "list",
                                        "header": {
                                            "type": "text",
                                            "text": n_i.inflow_header_text
                                        },
                                        "body": {
                                            "text": n_i.inflow_body_text
                                        },
                                        # "footer": {
                                        #     "text": n_i.inflow_footer_text
                                        # },
                                        "action": {
                                            "button": n_i.open_button_name,
                                            "sections": [
                                                {
                                                    "title": "Locations",
                                                    "rows": list_second_details
                                                }

                                            ]
                                        }
                                    }
                                })

                                response = requests.request("POST", url, headers=headers, data=payload)
                            else:
                                print("image code please wait soon it came.")
                    elif button_type.lower() == 'cards':
                        print("s its cards")
                        parentInfoObj = Inflow_Setup_Details.objects.filter(client_id=clientId,
                                                                            Parent_ID=inflow_Id)
                        print("len is----->", len(parentInfoObj))
                        All_cards = []

                        for index, p_i in enumerate(parentInfoObj):
                            All_cards.append(
                                {
                                    "card_index": index,
                                    "components": [
                                        {
                                            "type": "HEADER",
                                            "parameters": [
                                                {
                                                    "type": "IMAGE",
                                                    "image": {
                                                        "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
                                                            p_i.additional_file_path)
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "type": "BODY",
                                            "parameters": [

                                                {
                                                    "type": "TEXT",
                                                    "text": p_i.inflow_body_text
                                                }

                                            ]
                                        },
                                        {
                                            "type": "BUTTON",
                                            "sub_type": "QUICK_REPLY",
                                            "index": "0",
                                            "parameters": [
                                                {
                                                    "type": "PAYLOAD",
                                                    "payload": f"{p_i.id}_{p_i.client_id}"
                                                }
                                            ]
                                        },

                                    ]
                                },
                            )
                        data = {
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "template",
                            "template": {
                                "name": f"campaign_cards_list_set_{len(parentInfoObj)}",
                                "language": {
                                    "code": "en_US"
                                },
                                "components": [
                                    {
                                        "type": "BODY",
                                        "parameters": [
                                            {
                                                "type": "TEXT",
                                                "text": "A villa plot with modern amenities"
                                            }

                                        ]
                                    },
                                    {
                                        "type": "CAROUSEL",
                                        "cards": All_cards
                                    }
                                ]
                            }
                        }

                        response = requests.post(url, json=data, headers=headers)

                        print(response.status_code)
                        print(response.json())
                        print("s carousel sent successfully")






























            else:
                print("s no quick_reply")
                messageType = res['entry'][0]['changes'][0]['value']['messages'][0]['type']
                whatsAppPhoneNumberId = res['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
                toUser = res['entry'][0]['changes'][0]['value']['messages'][0]['from']
                message = ''
                button_type = ''
                response_id = ''
                list_title = ''

                if messageType == 'text':
                    message = res['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

                if messageType == 'interactive':
                    button_type = res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['type']
                    if button_type == 'button_reply':
                        response_id = \
                        res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['button_reply'][
                            'id']
                    elif button_type == 'list_reply':
                        response_id = \
                        res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['list_reply'][
                            'id']
                        list_title = res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['list_reply'][
                            'title']

                facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                faceBookToken = ''
                # businessName = ''
                clientId = 0
                for tok in facebookObjects:
                    faceBookToken = faceBookToken + tok.fb_access_token
                    # businessName = businessName + tok.fb_name
                    clientId = clientId + tok.client_id

                print(clientId)
                # ____________________________________API URL and HEADERS__________________________________

                url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + faceBookToken,
                    'Content-Type': 'application/json'
                }

                # __________________________________________________________________________________________

                adminPermissionObjects = admin_permission.objects.filter(client_id=clientId)

                for clientIdI in adminPermissionObjects:
                    print(clientIdI.client_service_type)
                    if clientIdI.client_service_type == 'commerce':
                        pass

                    elif clientIdI.client_service_type == 'campaign':
                        print("s servey correct")
                        # process_campaign_bot_message(message, response_id, messageType, request, url, headers, toUser,
                        #                              clientId, whatsAppPhoneNumberId, faceBookToken)
                        process_default_campaign_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                                     clientId, whatsAppPhoneNumberId, faceBookToken,list_title)


                    elif clientIdI.client_service_type == 'survey':
                        print("s servey correct")
                        process_survey_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                                   clientId, whatsAppPhoneNumberId, faceBookToken, list_title)

                    elif clientIdI.client_service_type == 'ticket':
                        if clientIdI.client_permission_status == True:
                            process_ticket_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                                       clientId, whatsAppPhoneNumberId, faceBookToken)
                        else:
                            print("waiting for admin approval")

                    elif clientIdI.client_service_type == 'donation':
                        print("dddd")
                        if clientIdI.client_permission_status == True:
                            print("vvvvvv")
                            print(whatsAppPhoneNumberId)
                            process_donation_bot_message(message, response_id, messageType, request, url, headers,
                                                         toUser,
                                                         clientId, whatsAppPhoneNumberId, faceBookToken)
                    elif clientIdI.client_service_type == 'appointement' or clientIdI.client_service_type == 'Appointement':
                        process_appointement_bot_message(message, response_id, messageType, request, url, headers,
                                                         toUser,
                                                         clientId, whatsAppPhoneNumberId, faceBookToken, list_title)


    elif first_key_from_meesage == "account_id":



            pymt_reference_id = received_message['payload']["payment_link"]['entity']['reference_id']
            print(pymt_reference_id)
            first_refer_character = pymt_reference_id[0]
            print(first_refer_character)
            if first_refer_character == 'T':
                # failed_reference_id = received_message['payload']['payment']['entity']['notes']['polacy_name']
                # print(failed_reference_id)
                ticket_reference_id = pymt_reference_id[1:]
                pymt_status = received_message['payload']['payment']['entity']['status']
                print(pymt_status)

                # update_payment_status(payment_reference_id,payment_status)

                payment_cart_details = event_ticket_cart_header.objects.filter(payment_reference_id=ticket_reference_id)
                print("going to save")

                for i in payment_cart_details:
                    if pymt_status == "captured" or "paid":
                        if i.payment_reference_id == ticket_reference_id:
                            i.payment_status = 1
                            i.save()
                            print("saved")
                    # elif pymt_status == 'failed':
                    #     print("yes payment has been failed")
                    #     if i.payment_reference_id == failed_reference_id:
                    #         i.payment_status = 2
                    #         i.save()

                    # if i.payment_reference_id == pymt_reference_id:
                    #     if pymt_status == "captured":
                    #         print("k")
                    #         i.payment_status = 1
                    #         i.save()
                    #     elif pymt_status == "failed":
                    #         print('f')
                    #         i.payment_status = 2
                    #         i.save()
                    #     else:
                    #         i.payment_status = 3
                    #         i.save()
                    break

                payment_details = event_ticket_cart_header.objects.filter(payment_reference_id=ticket_reference_id)
                clientID = ''
                toUser = ''
                for p in payment_details:
                    toUser = p.customer_phone_number
                    print(toUser)
                    clientID = p.client_id
                    facebookuseObjects = facebook_details.objects.filter(client_id=clientID)
                    faceeBookToken = ""
                    fbb_phone_number_id = ""
                    for j in facebookuseObjects:
                        fbb_phone_number_id = j.fb_phone_number_id
                        faceeBookToken = j.fb_access_token

                    if p.payment_status == 1:
                        print("vailo")
                        event_payment_information = event_settings.objects.filter(client_id=clientID)
                        ticketconformationmessage = ''
                        for q in event_payment_information:
                            ticketconformationmessage = ticketconformationmessage + q.ticket_conformation_message_body
                            if q.ticket_conformation_header_image:
                                url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
                                headers = {
                                    'Authorization': 'Bearer ' + faceeBookToken,
                                    'Content-Type': 'application/json'
                                }

                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "image",
                                    "image": {
                                        "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
                                            q.ticket_conformation_header_image)

                                    }
                                })
                                response = requests.request("POST", url, headers=headers, data=payload)
                                time.sleep(1)

                                url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
                                headers = {
                                    'Authorization': 'Bearer ' + faceeBookToken,
                                    'Content-Type': 'application/json'
                                }

                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "text",
                                    "text": {
                                        "body": ticketconformationmessage if ticketconformationmessage else "."
                                    }
                                })

                                response = requests.request("POST", url, headers=headers, data=payload)
                                customer_sent(request, toUser, clientID)
                            else:

                                url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
                                headers = {
                                    'Authorization': 'Bearer ' + faceeBookToken,
                                    'Content-Type': 'application/json'
                                }

                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "text",
                                    "text": {
                                        "body": ticketconformationmessage if ticketconformationmessage else "."
                                    }
                                })

                                response = requests.request("POST", url, headers=headers, data=payload)
                                customer_sent(request, toUser, clientID)
                        ticket_qr = ticket_information.objects.filter(client_id=clientID,
                                                                      payment_reference_id=ticket_reference_id)
                        print(ticket_qr)
                        for ticket in ticket_qr:
                            ticket.customer_phone_number = str(toUser)
                            url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
                            headers = {
                                'Authorization': 'Bearer ' + faceeBookToken,
                                'Content-Type': 'application/json'
                            }

                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "image",
                                "image": {
                                    "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
                                        ticket.ticket_QR)
                                }
                            })
                            response = requests.request("POST", url, headers=headers, data=payload)
                            customer_sent(request, toUser, clientID)
                            ticket.ticket_status = 30
                            ticket.save()

                        # payment_cart = event_ticket_cart_details.objects.filter(client_id=clientID,cart_id_id=p.id)
                        # print(payment_cart)
                        # tickets = ""
                        # for c in payment_cart:
                        #     # tickets = c.number_of_tickets
                        #     # print("z")
                        #     payment_ticket_information = ticket_information.objects.filter(client_id=clientID,
                        #                                                                    event_ticket_category_id=c.category_id,
                        #                                                                    ticket_status=20,payment_reference_id=pymt_reference_id)

                        #     # payment_ticket_information.customer_phone_number = str(toUser)
                        #     print(payment_ticket_information)

                        #     for e in payment_ticket_information[:c.number_of_tickets]:
                        #         print(c.number_of_tickets)
                        #         e.customer_phone_number = str(toUser)
                        #         print("varan")
                        #         url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
                        #         headers = {
                        #             'Authorization': 'Bearer ' + faceeBookToken,
                        #             'Content-Type': 'application/json'
                        #         }

                        #         payload = json.dumps({
                        #             "messaging_product": "whatsapp",
                        #             "recipient_type": "individual",
                        #             "to": toUser,
                        #             "type": "image",
                        #             "image": {
                        #                 "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
                        #                     e.ticket_QR)

                        #             }
                        #         })
                        #         response = requests.request("POST", url, headers=headers, data=payload)
                        #         customer_sent(request, toUser, clientID)
                        #         e.ticket_status = 30
                        #         e.save()
                    else:
                        print("failure")
                        event_payment_information = event_settings.objects.filter(client_id=clientID)
                        ticketpaymentfailuremessage = ''
                        for z in event_payment_information:
                            ticketpaymentfailuremessage = ticketpaymentfailuremessage + z.ticket_failure_message_body
                            if z.ticket_payment_failure_image:
                                url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
                                headers = {
                                    'Authorization': 'Bearer ' + faceeBookToken,
                                    'Content-Type': 'application/json'
                                }

                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "image",
                                    "image": {
                                        "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
                                            z.ticket_payment_failure_image)

                                    }
                                })
                                response = requests.request("POST", url, headers=headers, data=payload)
                                time.sleep(2)

                                url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
                                headers = {
                                    'Authorization': 'Bearer ' + faceeBookToken,
                                    'Content-Type': 'application/json'
                                }

                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "text",
                                    "text": {
                                        "body": ticketpaymentfailuremessage if ticketpaymentfailuremessage else "."
                                    }
                                })

                                response = requests.request("POST", url, headers=headers, data=payload)
                                customer_sent(request, toUser, clientID)
                            else:
                                url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
                                headers = {
                                    'Authorization': 'Bearer ' + faceeBookToken,
                                    'Content-Type': 'application/json'
                                }

                                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "text",
                                    "text": {
                                        "body": ticketpaymentfailuremessage if ticketpaymentfailuremessage else "."
                                    }
                                })

                                response = requests.request("POST", url, headers=headers, data=payload)
                                customer_sent(request, toUser, clientID)

            elif first_refer_character == 'N':


                print('please wait to update your payment status in database')
                donate_refer_id = pymt_reference_id[1:]
                # pymt_status = received_message['payload']['payment']['entity']['status']
                pymt_status = received_message['payload']["payment_link"]['entity']['status']
                is_processed = donation_details.objects.filter(donation_reference_id=donate_refer_id,
                                                               payment_status=1).exists()

                if pymt_status == 'paid' and not is_processed:

                    dynamicDataObj = donation_details.objects.filter(donation_reference_id=donate_refer_id)
                    for dy_i in dynamicDataObj:
                        clientid = dy_i.client_id
                        if dy_i.donation_reference_id == donate_refer_id:
                            dy_i.payment_status = 1
                            dy_i.save()

                        detailsOrgObject = donation_settings.objects.filter(client_id=clientid)
                        for org_i in detailsOrgObject:
                            templateLoader = jinja2.FileSystemLoader(searchpath="./")
                            templateEnv = jinja2.Environment(loader=templateLoader)
                            TEMPLATE_FILE = "templates/invoice.html"
                            print("mohan")
                            template = templateEnv.get_template(TEMPLATE_FILE)
                            print(template)
                            print("kav")

                            body = {
                                "data": {
                                    "donation_name": dy_i.donation_name,
                                    "donation_date": dy_i.donation_date,
                                    "donation_amount": dy_i.donation_amount,
                                    "donar_name": dy_i.donar_name,
                                    "donar_email": dy_i.donar_email,
                                    "donar_phone": dy_i.donar_phone_number,
                                    "donation_desc": dy_i.donation_description,
                                    "donation_short_desc": dy_i.donation_short_description,
                                    "reference_id":dy_i.donation_reference_id,
                                    "ngo_logo":org_i.ngo_logo,
                                    "ngo_name":org_i.ngo_name,
                                    "ngo_pan":org_i.ngo_pan,
                                    "ngo_gstin":org_i.ngo_gstin,
                                    "ngo_header_notes": org_i.ngo_header_notes,
                                    "ngo_footer_notes": org_i.ngo_footer_notes,
                                    "ngo_signatureHeader":org_i.ngo_signature_header,
                                    "ngo_signatureImage":org_i.ngo_signature_image,
                                    "ngo_Footer":org_i.ngo_signature_footer,
                                    "invoiceFooter":org_i.invoice_footer

                                }
                            }
                            sourceHtml = template.render(json_data=body["data"])
                            print(sourceHtml)
                            outputFilename = f"receipt_{dy_i.id}.pdf"
                            pdf_content = BytesIO()
                            pisa.CreatePDF(
                                src=sourceHtml,  # the HTML to convert
                                dest=pdf_content)
                            pdf_content.seek(0)
                            dy_i.receipient_pdf.save(outputFilename, pdf_content, save=True)
                            pdf_display(request, donate_refer_id)
                            # is_processed = True
                            # pdf_content_with_metadata = BytesIO()
                            # pdf = PyPDF2.PdfReader(pdf_content)
                            # pdf_writer = PyPDF2.PdfWriter()
                            # pdf_writer.add_page(pdf.pages[0])
                            # pdf_writer.add_metadata({
                            #     '/Filename':outputFilename,
                            #     '/Title': outputFilename,
                            #     '/Author': 'Vividhity Ventures Private Limited'
                            #
                            #     # Add more properties as needed
                            # })
                            # pdf_writer.write(pdf_content_with_metadata)
                            # pdf_content_with_metadata.seek(0)


                            # pdfobj = donation_details.objects.filter(donation_reference_id=donate_refer_id)
                            # for pdf_i in pdfobj:
                            #     pdf_i.receipient_pdf.save(outputFilename, pdf_content, save=True)
                            #
                    # donationDetailsobj = donation_details.objects.filter(donation_reference_id=donate_refer_id)
                    # for ngo_i in donationDetailsobj:
                    #     print('suceess')
                    #     if ngo_i.donation_reference_id == donate_refer_id:
                    #         print("saved")
                    #         ngo_i.payment_status = 1
                    #         ngo_i.save()
                    # pdf_display(request, donate_refer_id)
                else:
                    print('iam finded error')

                # if is_processed:
                #     pdf_display(request, donate_refer_id)
            return





    





    elif first_key_from_meesage == "entity":
        print("yes direct coming here first mister mogan rao")

        failed_reference_id = received_message['payload']['payment']['entity']['notes']['polacy_name']
        print(failed_reference_id)
        first_letter = failed_reference_id[0]
        if first_letter == "T":

            tfailed_refer_id = failed_reference_id[1:]
            pymt_status = received_message['payload']['payment']['entity']['status']

            fail_payment_cart_details = event_ticket_cart_header.objects.filter(payment_reference_id=tfailed_refer_id)
            for fail_i in fail_payment_cart_details:
                if pymt_status == "failed":
                    if fail_i.payment_reference_id == tfailed_refer_id:
                        fail_i.payment_status = 2
                        fail_i.save()
            payment_details = event_ticket_cart_header.objects.filter(payment_reference_id=tfailed_refer_id)
            clientID = ''
            toUser = ''
            for p in payment_details:
                toUser = p.customer_phone_number
                print(toUser)
                clientID = p.client_id
                facebookuseObjects = facebook_details.objects.filter(client_id=clientID)
                faceeBookToken = ""
                fbb_phone_number_id = ""
                for j in facebookuseObjects:
                    fbb_phone_number_id = j.fb_phone_number_id
                    faceeBookToken = j.fb_access_token
                if p.payment_status == 2:
                    event_payment_information = event_settings.objects.filter(client_id=clientID)
                    ticketpaymentfailuremessage = ''
                    for z in event_payment_information:
                        ticketpaymentfailuremessage = ticketpaymentfailuremessage + z.ticket_failure_message_body
                        if z.ticket_payment_failure_image:
                            url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
                            headers = {
                                'Authorization': 'Bearer ' + faceeBookToken,
                                'Content-Type': 'application/json'
                            }
                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "image",
                                "image": {
                                    "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
                                        z.ticket_payment_failure_image)

                                }
                            })
                            response = requests.request("POST", url, headers=headers, data=payload)
                            time.sleep(2)

                            url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
                            headers = {
                                'Authorization': 'Bearer ' + faceeBookToken,
                                'Content-Type': 'application/json'
                            }

                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "text",
                                "text": {
                                    "body": ticketpaymentfailuremessage if ticketpaymentfailuremessage else "."
                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)
                            customer_sent(request, toUser, clientID)
                        else:
                            url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
                            headers = {
                                'Authorization': 'Bearer ' + faceeBookToken,
                                'Content-Type': 'application/json'
                            }

                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "text",
                                "text": {
                                    "body": ticketpaymentfailuremessage if ticketpaymentfailuremessage else "."
                                }
                            })

                            response = requests.request("POST", url, headers=headers, data=payload)
                            customer_sent(request, toUser, clientID)
        elif first_letter == "N":
            print("payment failed")
            ngo_refer_id = failed_reference_id[1:]
            pymt_status = received_message['payload']['payment']['entity']['status']

            failureInfo = donation_details.objects.filter(donation_reference_id=ngo_refer_id)
            for ngo_i in failureInfo:
                if pymt_status == 'failed' or 'Failed':
                    if ngo_i.donation_reference_id == ngo_refer_id:
                        ngo_i.payment_status = 2
                        ngo_i.save()
            paymentdetails = donation_details.objects.filter(donation_reference_id=ngo_refer_id)
            for p in paymentdetails:
                toUser = p.donar_phone_number
                print(toUser)
                clientID = p.client_id
                facebookuseObjects = facebook_details.objects.filter(client_id=clientID)
                faceeBookToken = ""
                fbb_phone_number_id = ""
                for j in facebookuseObjects:
                    fbb_phone_number_id = j.fb_phone_number_id
                    faceeBookToken = j.fb_access_token
                if p.payment_status == 2:
                    settingsobj = donation_settings.objects.filter(client_id=clientID)
                    for s_i in settingsobj:
                        url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
                        headers = {
                            'Authorization': 'Bearer ' + faceeBookToken,
                            'Content-Type': 'application/json'
                        }

                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "text",
                            "text": {
                                "body": s_i.donation_failure_message if s_i.donation_failure_message else "."
                            }
                        })
                        response = requests.request("POST", url, headers=headers, data=payload)
    elif first_key_from_meesage == "encrypted_flow_data":
        print("s you are in coreect mister mouli")
        try:
            # Parse the request body
            body = json.loads(request.body)
            print(body)

            # Generate a new RSA private key (for demonstration)
            # private_key = rsa.generate_private_key(
            #     public_exponent=65537,
            #     key_size=2048
            # )

            # Serialize private key to PEM format
            # private_key_pem = private_key.private_bytes(
            #     encoding=serialization.Encoding.PEM,
            #     format=serialization.PrivateFormat.TraditionalOpenSSL,
            #     encryption_algorithm=serialization.NoEncryption()
            # )

            # Read the request fields
            encrypted_flow_data_b64 = body['encrypted_flow_data']
            encrypted_aes_key_b64 = body['encrypted_aes_key']
            initial_vector_b64 = body['initial_vector']

            decrypted_data, aes_key, iv = decrypt_request_check2(
                encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
            print("kohli")
            print(decrypted_data)
            print("rohith")
            action_type = decrypted_data['action']
            print(action_type)
            if action_type == 'data_exchange':
                # Return the next screen & data to the client
                print("s in data_exchange")
                response = {
                    "version": decrypted_data['version'],
                    "screen": "COVER",
                    "data": {
                        "options": [
                            {
                                "id": "1",
                                "title": "mohan1",
                                "description": "mohan is a very good boy"
                            },
                            {
                                "id": "2",
                                "title": "John1",
                                "description": "John is a talented artist"
                            },
                            {
                                "id": "3",
                                "title": "Emma1",
                                "description": "Emma loves to travel"
                            }
                        ]

                    }
                }

                # Return the response as plaintext
                return HttpResponse(encrypt_response_check2(response, aes_key, iv), content_type='text/plain')
            elif action_type == 'ping':

                print("s you are in ping")
                response = {
                    "version": "3.0",
                    "data": {
                        "status": "active"
                    }
                }
                return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')

        except Exception as e:
            print(e)
            return JsonResponse({}, status=500)











    else:
        print("else block")
        # uname = received_message['name']
        # uemail = received_message['email']
        # uphone = received_message['phone']
        # phone_number = "91"+ uphone.strip() 
        # print(uphone)
        # id = received_message['formid']
        tid = received_message['formid']
        first_character = tid[0]
        if first_character == 'T':
            print("ij")
            reference_characters = tid[1:37]
            ticket_id = tid[37:]
            uphone = received_message['phone']
            phone_number = "91"+ uphone.strip()
            tick_info = ticket_information.objects.filter(id=ticket_id,payment_reference_id=reference_characters)
            print(tick_info)
            for ti_i in tick_info:
                ti_i.customer_phone_number = phone_number
                ti_i.save()
        elif first_character == 'N':
            print("gg")
            donar_refId = tid[2:38]
            print(donar_refId)
            responseId = tid[38:]
            dclientID = received_message['cid']
            donarName = received_message['name']
            donarEmail = received_message['email']
            donarPan = received_message['pan']
            donarAmount = received_message['amount']
            donarcomments = received_message['comments']
            donationName=''
            donationshortdesc = ''
            donationdesc = ''
            donationImage = ''
            donation_detailsobj = donation_types.objects.filter(client_id=dclientID,id=responseId)
            print(donation_detailsobj)
            for dj_i in donation_detailsobj:
                donationName = donationName + dj_i.donation_name
                donationshortdesc = donationshortdesc + dj_i.donation_short_description
                donationdesc = donationdesc + dj_i.donation_description
                donationImage = dj_i.donation_type_image
            print(donationName)

            donar_details = donation_details.objects.filter(client_id=dclientID,donation_reference_id=donar_refId)
            print("bb")
            for dd_i in donar_details:
                dd_i.donar_name = donarName
                dd_i.donar_email = donarEmail
                dd_i.donar_pan_number = donarPan
                dd_i.donation_amount = donarAmount
                dd_i.donation_name = donationName
                dd_i.donation_short_description = donationshortdesc
                dd_i.donation_description = donationdesc
                dd_i.donation_type_image = donationImage
                dd_i.donation_date = timezone.now().date()
                dd_i.donation_comments_message = donarcomments
                dd_i.save()
            N3(request, donar_refId, dclientID)

        elif first_character == 'P':
            print("P section")
            donar_refId = tid[2:38]
            dclientID = received_message['cid']
            donarName = received_message['name']
            donarEmail = received_message['email']
            donarPan = received_message['pan']
            donarAmount = received_message['amount']
            donarcomments = received_message['comments']
            donar_details = donation_details.objects.filter(client_id=dclientID, donation_reference_id=donar_refId)
            for dd_i in donar_details:
                dd_i.donar_name = donarName
                dd_i.donar_email = donarEmail
                dd_i.donar_pan_number = donarPan
                dd_i.donation_amount = donarAmount
                dd_i.donation_date = timezone.now().date()
                dd_i.donation_comments_message = donarcomments
                dd_i.save()





            
            

            
        
                

               



        # print(uname)
        # print(uemail)
        # print(uphone)  
        # print(id)
        # uid = str(id)[:12]
        # clientId = str(id)[12:]
        # customerdetails = ticket_customer_master.objects.filter(client_id=clientId,Customer_Phone_Number=uid)
        # for customer_i in customerdetails:
        #     customer_i.Customer_First_Name = uname
        #     customer_i.Customer_Email = uemail
        #     customer_i.save()



            




    return HttpResponse('ticket')

def T(request,refid,cid):
    print(refid)
    print(cid)
    # clientId = str(id)[12:]
    # print(clientId)
    facebookDetails = facebook_details.objects.filter(client_id=cid)
    clientNumber = ''
    for f_i in facebookDetails:
        clientNumber = f_i.fb_whatsapp_number

    

    return render(request,'inform.html',{'refid':refid,'clientID':cid,'clientNumber':clientNumber})
    # return render(request,'infoform1.html',{'formid':id})
    # return HttpResponse("coming Here")
def N1(request,number,dcid):

    print(number)
    print(dcid)

    response_id = number[38:]
    d_reference_id = number[2:38]
    checkObj = donation_details.objects.filter(donation_reference_id=d_reference_id)
    toUser = ''
    dnrName = ''
    for d_i in checkObj:
        dnrName = d_i.donar_name
        toUser = d_i.donar_phone_number
    if not dnrName:
        print("name is not there")
        donation_data = donation_types.objects.filter(id=response_id)
        donation_amount = 0
        donation_name = ''
        donationImage = ''
        for dn_i in donation_data:
            donation_amount = dn_i.donation_amount
            donation_name = donation_name + dn_i.donation_name
            donationImage = dn_i.donation_type_image
        return render(request, 'donation.html',
                      {'number': number, 'clientID': dcid, 'Donation': donation_amount,
                       'dname': donation_name, 'Filename': donationImage})
    else:

        print("name is already there")
        facebookuseObjects = facebook_details.objects.filter(client_id=dcid)
        faceeBookToken = ""
        fbb_phone_number_id = ""
        client_Number = ''
        for j in facebookuseObjects:
            fbb_phone_number_id = j.fb_phone_number_id
            faceeBookToken = j.fb_access_token
            client_Number = j.fb_whatsapp_number
        url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
        headers = {
            'Authorization': 'Bearer ' + faceeBookToken,
            'Content-Type': 'application/json'
        }

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "text",
            "text": {
                "body": "Form is already Submitted.Please check your details in My Donation"
            }
        })
        response = requests.request("POST", url, headers=headers, data=payload)

        welcomeobj = donation_settings.objects.filter(client_id=dcid)

        for don_i in welcomeobj:
            if don_i.donation_image:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                                (don_i.donation_image)
                            }
                        },

                        "body": {
                            "text": don_i.donation_description if don_i.donation_description else "."
                        },
                        "footer": {
                            "text": don_i.donation_footer
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D1",
                                        "title": don_i.donation_now_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D2",
                                        "title": don_i.my_donation_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D3",
                                        "title": don_i.contact_us_button_name
                                    }
                                },

                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
            else:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": don_i.donation_description if don_i.donation_description else "."
                        },
                        "footer": {
                            "text": don_i.donation_footer
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D1",
                                        "title": don_i.donation_now_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D2",
                                        "title": don_i.my_donation_button_name
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "D3",
                                        "title": don_i.contact_us_button_name
                                    }
                                },
                            ]
                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)

        # return HttpResponse("Form is already Submitted. Plesase return back to whatsapp and continue..")
        return redirect(f"https://wa.me/{client_Number}")





    # print(donationImage)
    # print(donation_name)
    # facebookDetails = facebook_details.objects.filter(client_id=dcid)
    # clientNumber = ''
    # for f_i in facebookDetails:
    #     clientNumber = f_i.fb_whatsapp_number

    # url = "https://api.razorpay.com/v1/payment_links"
    #
    # payload = json.dumps({
    #     "amount": donation_amount * 100,
    #     "currency": "INR",
    #     "accept_partial": False,
    #     "first_min_partial_amount": 0,
    #     "reference_id": "N" + str(d_reference_id),
    #     "description": "Donation",
    #     "customer": {
    #         "name": "Gaurav Kumar",
    #         "contact": "918494863493",
    #         "email": "gaurav.kumar@example.com"
    #     },
    #     "notify": {
    #         "sms": True,
    #         "email": True
    #     },
    #     "reminder_enable": True,
    #     "notes": {
    #         "polacy_name": "N" + str(d_reference_id)
    #     },
    #     "callback_url": f"https://wa.me/{clientNumber}",
    #     "callback_method": "get"
    # })
    # headers = {
    #     'Content-Type': 'application/json',
    #     'Authorization': 'Basic cnpwX2xpdmVfSU83R0Vyckkyam9RYXQ6aGt2SVhTZkpvM0x2TWhYaGx5VUpoWTBH'
    # }
    #
    # response = requests.request("POST", url, headers=headers, data=payload)
    #
    # a = response.text
    # json_str = json.dumps(a)
    # b = json.loads(json_str)
    # c = response.json()
    # print(c)
    # payment_link = c['short_url']
    # print(payment_link)
    # dynamic_link = payment_link[17:]

    # return render(request, 'donation.html',
    #               {'number':number,'clientID':dcid,'Donation':donation_amount,
    #                 'dname':donation_name,'Filename':donationImage})

    # paymentDetails = payment_settings.objects.filter(client_id=dcid)
    # paymentGateway = ''
    # paymentGatewayID = ''
    # paymentGatewayKey = ''
    # for pd_i in paymentDetails:
    #     paymentDetailsObject = payment_gateway_details.objects.filter(client_id=dcid,payment_gateway=pd_i.payment_gateway)
    #     for pj_i in paymentDetailsObject:
    #         paymentGateway = paymentGateway + pj_i.payment_gateway
    #         paymentGatewayID = paymentGatewayID + pj_i.gateway_id
    #         paymentGatewayKey = paymentGatewayKey + pj_i.gateway_key
    #
    # if paymentGateway == "paypal":
    #     # client_id = 'ARZXGxv02vGOAL5nflRoCkm0v-cB49sRiFFp5bSM14qWTL62Wyqzr72OuM4kBLD-AjQaorEPvCD4aTYw'
    #     #
    #     # client_secret = 'EPGRkm46ShkoFxfMhXQ18_yNS_i_I_092ej6WsCs9DoNlklbnRmI8v-5s_jeewYT-4w7OIDfqG_eNAtZ'
    #     client_id = paymentGatewayID
    #     client_secret = paymentGatewayKey
    #
    #
    #     credentials = f'{client_id}:{client_secret}'
    #     encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    #
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'PayPal-Request-Id': "N"+str(d_reference_id),
    #         'Authorization': f'Basic {encoded_credentials}'
    #     }
    #
    #     data = {
    #         "intent": "CAPTURE",
    #         "purchase_units": [
    #             {
    #                 "reference_id": "N"+str(d_reference_id),
    #                 "amount": {
    #                     "currency_code": "USD",
    #                     "value": "100.00"
    #                 },
    #                 "shipping": {
    #                     "address": {
    #                         "address_line_1": "1234 Shipping Street",
    #                         "address_line_2": "Apt 5",
    #                         "admin_area_2": "San Jose",
    #                         "admin_area_1": "CA",
    #                         "postal_code": "95131",
    #                         "country_code": "US"
    #                     }
    #                 }
    #             }
    #         ],
    #         "payment_source": {
    #             "paypal": {
    #                 "experience_context": {
    #                     "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
    #                     "payment_method_selected": "PAYPAL",
    #                     "brand_name": "EXAMPLE INC",
    #                     "locale": "en-US",
    #                     "landing_page": "LOGIN",
    #                     "shipping_preference": "SET_PROVIDED_ADDRESS",
    #                     "user_action": "PAY_NOW",
    #                     "return_url": "https://vailo.ai",
    #                     "cancel_url": "https://example.com/cancelUrl"
    #                 }
    #             }
    #         }
    #     }
    #
    #     response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, json=data)
    #     # print(response.text)
    #     data = json.loads(response.text)
    #     paypal_link = data['links'][1]['href']
    #     token = paypal_link.split('=')[1]
    #
    #     return render(request, 'donation.html',
    #                   {'number': number, 'clientID': dcid, 'PaymentLink': token, 'Donation': donation_amount,'PaymentGateway':'paypal'})
    # elif paymentGateway == "razorpay":
    #     client_id = paymentGatewayID
    #     client_secret = paymentGatewayKey
    #
    #     credentials = f'{client_id}:{client_secret}'
    #     encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    #
    #     url = "https://api.razorpay.com/v1/payment_links"
    #
    #     payload = json.dumps({
    #         "amount": donation_amount * 100,
    #         "currency": "INR",
    #         "accept_partial": False,
    #         "first_min_partial_amount": 0,
    #         "reference_id": "N" + str(d_reference_id),
    #         "description": "Donation",
    #         "customer": {
    #             "name": "Gaurav Kumar",
    #             "contact": "918494863493",
    #             "email": "gaurav.kumar@example.com"
    #         },
    #         "notify": {
    #             "sms": True,
    #             "email": True
    #         },
    #         "reminder_enable": True,
    #         "notes": {
    #             "polacy_name": "N" + str(d_reference_id)
    #         },
    #         "callback_url": f"https://wa.me/{clientNumber}",
    #         "callback_method": "get"
    #     })
    #
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'PayPal-Request-Id': "N" + str(d_reference_id),
    #         'Authorization': f'Basic {encoded_credentials}'
    #     }
    #     response = requests.request("POST", url, headers=headers, data=payload)
    #
    #     a = response.text
    #     json_str = json.dumps(a)
    #     b = json.loads(json_str)
    #     c = response.json()
    #     print(c)
    #     payment_link = c['short_url']
    #     print(payment_link)
    #     dynamic_link = payment_link[17:]
    #
    #     return render(request, 'donation.html',
    #                   {'number': number, 'clientID': dcid, 'PaymentLink': dynamic_link, 'Donation': donation_amount,
    #                    'PaymentGateway': 'razorpay'})


def N2(request,number,dcid):
    d_new_reference_id = number[2:38]
    detailsData = donation_details.objects.filter(donation_reference_id=d_new_reference_id)
    donation_amount = 0
    donation_name = ''
    donationImage = ''
    donar = ''
    email = ''
    pan = ''
    comments = ''
    for dn_i in detailsData:
        donation_amount = dn_i.donation_amount
        donation_name = dn_i.donation_name
        donationImage = dn_i.donation_type_image
        donar = dn_i.donar_name
        email = dn_i.donar_email
        pan = dn_i.donar_pan_number
        comments = dn_i.donation_comments_message

    facebookDetails = facebook_details.objects.filter(client_id=dcid)
    clientNumber = ''
    for f_i in facebookDetails:
        clientNumber = f_i.fb_whatsapp_number

    url = "https://api.razorpay.com/v1/payment_links"

    payload = json.dumps({
        "amount": donation_amount * 100,
        "currency": "INR",
        "accept_partial": False,
        "first_min_partial_amount": 0,
        "reference_id": "N" + str(d_new_reference_id),
        "description": "Donation",
        "customer": {
            "name": "Gaurav Kumar",
            "contact": "918494863493",
            "email": "gaurav.kumar@example.com"
        },
        "notify": {
            "sms": True,
            "email": True
        },
        "reminder_enable": True,
        "notes": {
            "polacy_name": "N" + str(d_new_reference_id)
        },
        "callback_url": f"https://wa.me/{clientNumber}",
        "callback_method": "get"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic cnpwX2xpdmVfSU83R0Vyckkyam9RYXQ6aGt2SVhTZkpvM0x2TWhYaGx5VUpoWTBH'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    a = response.text
    json_str = json.dumps(a)
    b = json.loads(json_str)
    c = response.json()
    print(c)
    payment_link = c['short_url']
    print(payment_link)
    dynamic_link = payment_link[17:]

    return render(request, 'redonation.html',
                  {'number': number, 'clientID': dcid, 'PaymentLink': dynamic_link, 'Donation': donation_amount,
                   'PaymentGateway': 'razorpay', 'dname': donation_name, 'Filename': donationImage,'Name':donar,'Email':email,'PAN':pan,"Comments":comments})

def checklink(request):
    return render(request,"checklink.html")

def submitdonationdata(request):
    print("s")
    if request.method == 'POST':
        dreferId = request.POST.get("formid")
        dclientID = request.POST.get("cid")
        donarName = request.POST.get("name")
        donarEmail = request.POST.get("email")
        donarPan = request.POST.get("phone")
        donarAmount = request.POST.get("amount")
        donarComments = request.POST.get("comments")

        donar_refId = dreferId[2:38]
        print(donar_refId)
        responseId = dreferId[38:]
        donationName = ''
        donationshortdesc = ''
        donationdesc = ''
        donationImage = ''
        market_placeId = 0
        donation_detailsobj = donation_types.objects.filter(client_id=dclientID, id=responseId)
        print(donation_detailsobj)
        for dj_i in donation_detailsobj:
            market_placeId = dj_i.marketplace_id
            donationName = donationName + dj_i.donation_name
            donationshortdesc = donationshortdesc + dj_i.donation_short_description
            donationdesc = donationdesc + dj_i.donation_description
            donationImage = dj_i.donation_type_image

        donar_details = donation_details.objects.filter(client_id=dclientID, donation_reference_id=donar_refId)
        print("bb")
        for dd_i in donar_details:
            dd_i.donar_name = donarName
            dd_i.donar_email = donarEmail
            dd_i.donar_pan_number = donarPan
            dd_i.donation_amount = donarAmount
            dd_i.donation_name = donationName
            dd_i.donation_short_description = donationshortdesc
            dd_i.donation_description = donationdesc
            dd_i.donation_type_image = donationImage
            dd_i.donation_date = timezone.now().date()
            dd_i.donation_comments_message = donarComments
            dd_i.marketplace_id = market_placeId
            dd_i.save()

        detailsObject = donation_details.objects.filter(client_id=dclientID, donation_reference_id=donar_refId)
        donationAmount = 0
        for j_i in detailsObject:
            donationAmount = j_i.donation_amount

        facebookDetails = facebook_details.objects.filter(client_id=dclientID)
        clientNumber = ''
        for f_i in facebookDetails:
            clientNumber = f_i.fb_whatsapp_number

        url = "https://api.razorpay.com/v1/payment_links"

        payload = json.dumps({
            "amount": donationAmount * 100,
            "currency": "INR",
            "accept_partial": False,
            "first_min_partial_amount": 0,
            "reference_id": "N" + str(donar_refId),
            "description": "Donation",
            "customer": {
                "name": "Gaurav Kumar",
                "contact": "918494863493",
                "email": "gaurav.kumar@example.com"
            },
            "notify": {
                "sms": True,
                "email": True
            },
            "reminder_enable": True,
            "notes": {
                "polacy_name": "N" + str(donar_refId)
            },
            "callback_url": f"https://wa.me/{clientNumber}",
            "callback_method": "get"
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic cnpwX2xpdmVfSU83R0Vyckkyam9RYXQ6aGt2SVhTZkpvM0x2TWhYaGx5VUpoWTBH'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        a = response.text
        json_str = json.dumps(a)
        b = json.loads(json_str)
        c = response.json()
        print(c)
        payment_link = c['short_url']
        print(payment_link)
        return redirect(payment_link)


@csrf_exempt
def data(request):
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        print(action_type)
        if action_type == 'data_exchange':
            # Return the next screen & data to the client
            print("s in data_exchange")
            response = {
                "version": decrypted_data['version'],
                "screen": "COVER",
                "data": {
                    "options": [
                        {
                            "id": "1",
                            "title": "mohan1",
                            "description": "mohan is a very good boy"
                        },
                        {
                            "id": "2",
                            "title": "John1",
                            "description": "John is a talented artist"
                        },
                        {
                            "id": "3",
                            "title": "Emma1",
                            "description": "Emma loves to travel"
                        }
                    ]

                }
            }

            # Return the response as plaintext
            return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
        elif action_type == 'ping':

            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                "status": "active"
                 }
            }
            return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQItTLWm6Vc654CAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECIvFEoBWEGMFBIIEyHH6IlqdS0g3
9jhMFdyd1JBYuXJZP33tp3YMDarSLi4Aj1nui9BI23w5sHS5GcNidBGC507vq2iw
M8ckVUUOoB3wDqj0H6Uec0aOaHeFQLFDa++CGWZTx0+T6dTG4HCbC/G7VBQmgE1j
rsJ6LGkfq/85NpuNNImwKPHZreAZCxGB/4X3sEFcNYrEMqWhnsz6oGssVGV3uV3M
MPTmv9S8oWUz3GzOZVhP3vwLnpXbyD5pyFf0FPEGBvRjG2UUs9sWHHUTTjF11MtH
TxEmdAVA79Vw2RSx1bLNp5+ItAidfAfFMmIZM7W+LjbZ8DWLDp4sDw+ZpLIg+egZ
PnD/VCjTej37TZIwz8FFeIOs7FcwLX/pqjD6+nPPYUO9PYqIygG4BMndoNrGQT+d
GQjWZIMdofUiwFHsjNupSOde/uQ/JDe5pKvVHaf/+zSYfnjSIjPYELj3OeOSCZaK
A8SZ0HHuwnJeNi733C/BvNh0uh6xJtwdKq3kQSR62/UQRzxxbbRTjcBMjYucf0vY
67eqLmc2aBUyRfnOpQisRTOPaUGYADFrX9i08jM9wWGxXWx5LEDi907HvGAAtZf1
+v4nVAEl7SG5EhEZpCcvOMZaUurwStn4ve+nyD5w73aJzrINdLOuqDz0P/BRsFQF
+gPy1xMtaw/G2E+xSsvyu01t9WzPDDWAqrGI9pzqXQpotpeS4nIuAdVYlM3C/0WZ
L4hQvCfYhlCMnBFiv9X9eQQfTSGAN2gFsuDwZoLk2dVLnTZoJFtwT7+kyYN3G6kJ
bgeegQ9dA2eTIf54j4Xmh4MbozMise9wSCtRkHWylN5QCOLaiMAUx2k5tW8PD7ti
QzVyZmC1mEQgX8OUFw4xz5ikKZhP0aHrd/btTpR1B5Y7+XqBGrIJwPN9+OltmPNx
RWdRkqi2JfFwB9/RmUsKWtALf43TCCanBAvjfsghsKxCQQcFGgHwvND/3c8beVK4
XlN1quweC6mKXXfE4BZdeaIHF+1NGKahfQYDmNQ23mzRmSJydg3KeYlaUCs4BA4e
k5UFeFAWxQ2NN6DIRotOydt3iDiJk4cgoPcM3798pQre+WOa59L/aX9gXxRo0JXK
AE0ups8chhwsfe/zJjCjqOnH6DF7bten2aS6/3LiTjRLu2fGcv67uETeGyJw7TPE
lUvMh/lpiamA7lgQbI69176vF9E3H2smSVt6YsYp7FL8UjaxGMOIXyNR10Rkp82b
sqHgYkcrGZuD/l8IiUMSINqxxZjOSWm83v0wkEpRZGzufdhFJxHcRBq0Y5r/nyXE
OJ3KcCykqIV3dPtV3jpY+6lSTKpquK87gWyNN2YuUjvhEWWcN6wFeZwUiUfxhI+A
S4ZIEa/g5EjLE6CddXXxUitb6ySOnefP7LS2uAxv8sav0+57PtYQwGsWrLjMuhgA
ZDqs0VbDIqpFRgCY4Tb6KADlP+66Cg3re+PkQQ0HQHYXdyYnUPfqcJxrK9FcaWwn
QPn2IfZ/R6/pg5fgd2ARg2YX0/aSkpQ5eOd6HBqG25L6fbcLBNTIVocNRSrlWWOI
LajjtATKktVRm9fNX18XX1Ea2TWS9jZeHg8fERDOe3wR61nD8VEMYLAbVKjkospI
xdKEEsEHiaFkdjuiYbuRIg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")


@csrf_exempt
def datacheck(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        print(action_type)
        if action_type == 'INIT':
            # Return the next screen & data to the client
            print("s in data_exchange")
            response = {
                "version": decrypted_data['version'],
                "screen": "DETAILS",
                "data": {

                }
            }

            # Return the response as plaintext
            return HttpResponse(encrypt_response_check(response, aes_key, iv), content_type='text/plain')
        elif action_type == 'ping':

            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                "status": "active"
                 }
            }
            return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQItTLWm6Vc654CAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECIvFEoBWEGMFBIIEyHH6IlqdS0g3
9jhMFdyd1JBYuXJZP33tp3YMDarSLi4Aj1nui9BI23w5sHS5GcNidBGC507vq2iw
M8ckVUUOoB3wDqj0H6Uec0aOaHeFQLFDa++CGWZTx0+T6dTG4HCbC/G7VBQmgE1j
rsJ6LGkfq/85NpuNNImwKPHZreAZCxGB/4X3sEFcNYrEMqWhnsz6oGssVGV3uV3M
MPTmv9S8oWUz3GzOZVhP3vwLnpXbyD5pyFf0FPEGBvRjG2UUs9sWHHUTTjF11MtH
TxEmdAVA79Vw2RSx1bLNp5+ItAidfAfFMmIZM7W+LjbZ8DWLDp4sDw+ZpLIg+egZ
PnD/VCjTej37TZIwz8FFeIOs7FcwLX/pqjD6+nPPYUO9PYqIygG4BMndoNrGQT+d
GQjWZIMdofUiwFHsjNupSOde/uQ/JDe5pKvVHaf/+zSYfnjSIjPYELj3OeOSCZaK
A8SZ0HHuwnJeNi733C/BvNh0uh6xJtwdKq3kQSR62/UQRzxxbbRTjcBMjYucf0vY
67eqLmc2aBUyRfnOpQisRTOPaUGYADFrX9i08jM9wWGxXWx5LEDi907HvGAAtZf1
+v4nVAEl7SG5EhEZpCcvOMZaUurwStn4ve+nyD5w73aJzrINdLOuqDz0P/BRsFQF
+gPy1xMtaw/G2E+xSsvyu01t9WzPDDWAqrGI9pzqXQpotpeS4nIuAdVYlM3C/0WZ
L4hQvCfYhlCMnBFiv9X9eQQfTSGAN2gFsuDwZoLk2dVLnTZoJFtwT7+kyYN3G6kJ
bgeegQ9dA2eTIf54j4Xmh4MbozMise9wSCtRkHWylN5QCOLaiMAUx2k5tW8PD7ti
QzVyZmC1mEQgX8OUFw4xz5ikKZhP0aHrd/btTpR1B5Y7+XqBGrIJwPN9+OltmPNx
RWdRkqi2JfFwB9/RmUsKWtALf43TCCanBAvjfsghsKxCQQcFGgHwvND/3c8beVK4
XlN1quweC6mKXXfE4BZdeaIHF+1NGKahfQYDmNQ23mzRmSJydg3KeYlaUCs4BA4e
k5UFeFAWxQ2NN6DIRotOydt3iDiJk4cgoPcM3798pQre+WOa59L/aX9gXxRo0JXK
AE0ups8chhwsfe/zJjCjqOnH6DF7bten2aS6/3LiTjRLu2fGcv67uETeGyJw7TPE
lUvMh/lpiamA7lgQbI69176vF9E3H2smSVt6YsYp7FL8UjaxGMOIXyNR10Rkp82b
sqHgYkcrGZuD/l8IiUMSINqxxZjOSWm83v0wkEpRZGzufdhFJxHcRBq0Y5r/nyXE
OJ3KcCykqIV3dPtV3jpY+6lSTKpquK87gWyNN2YuUjvhEWWcN6wFeZwUiUfxhI+A
S4ZIEa/g5EjLE6CddXXxUitb6ySOnefP7LS2uAxv8sav0+57PtYQwGsWrLjMuhgA
ZDqs0VbDIqpFRgCY4Tb6KADlP+66Cg3re+PkQQ0HQHYXdyYnUPfqcJxrK9FcaWwn
QPn2IfZ/R6/pg5fgd2ARg2YX0/aSkpQ5eOd6HBqG25L6fbcLBNTIVocNRSrlWWOI
LajjtATKktVRm9fNX18XX1Ea2TWS9jZeHg8fERDOe3wR61nD8VEMYLAbVKjkospI
xdKEEsEHiaFkdjuiYbuRIg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")


@csrf_exempt
def webhook(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check3(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        print(action_type)
        if action_type == 'INIT':
            # Return the next screen & data to the client
            print("s in data_exchange")
            response = {
                "version": decrypted_data['version'],
                "screen": "DETAILS",
                "data": {

                }
            }

            # Return the response as plaintext
            return HttpResponse(encrypt_response_check(response, aes_key, iv), content_type='text/plain')
        elif action_type == 'ping':

            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                "status": "active"
                 }
            }
            return HttpResponse(encrypt_response_check3(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check3(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQItTLWm6Vc654CAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECIvFEoBWEGMFBIIEyHH6IlqdS0g3
9jhMFdyd1JBYuXJZP33tp3YMDarSLi4Aj1nui9BI23w5sHS5GcNidBGC507vq2iw
M8ckVUUOoB3wDqj0H6Uec0aOaHeFQLFDa++CGWZTx0+T6dTG4HCbC/G7VBQmgE1j
rsJ6LGkfq/85NpuNNImwKPHZreAZCxGB/4X3sEFcNYrEMqWhnsz6oGssVGV3uV3M
MPTmv9S8oWUz3GzOZVhP3vwLnpXbyD5pyFf0FPEGBvRjG2UUs9sWHHUTTjF11MtH
TxEmdAVA79Vw2RSx1bLNp5+ItAidfAfFMmIZM7W+LjbZ8DWLDp4sDw+ZpLIg+egZ
PnD/VCjTej37TZIwz8FFeIOs7FcwLX/pqjD6+nPPYUO9PYqIygG4BMndoNrGQT+d
GQjWZIMdofUiwFHsjNupSOde/uQ/JDe5pKvVHaf/+zSYfnjSIjPYELj3OeOSCZaK
A8SZ0HHuwnJeNi733C/BvNh0uh6xJtwdKq3kQSR62/UQRzxxbbRTjcBMjYucf0vY
67eqLmc2aBUyRfnOpQisRTOPaUGYADFrX9i08jM9wWGxXWx5LEDi907HvGAAtZf1
+v4nVAEl7SG5EhEZpCcvOMZaUurwStn4ve+nyD5w73aJzrINdLOuqDz0P/BRsFQF
+gPy1xMtaw/G2E+xSsvyu01t9WzPDDWAqrGI9pzqXQpotpeS4nIuAdVYlM3C/0WZ
L4hQvCfYhlCMnBFiv9X9eQQfTSGAN2gFsuDwZoLk2dVLnTZoJFtwT7+kyYN3G6kJ
bgeegQ9dA2eTIf54j4Xmh4MbozMise9wSCtRkHWylN5QCOLaiMAUx2k5tW8PD7ti
QzVyZmC1mEQgX8OUFw4xz5ikKZhP0aHrd/btTpR1B5Y7+XqBGrIJwPN9+OltmPNx
RWdRkqi2JfFwB9/RmUsKWtALf43TCCanBAvjfsghsKxCQQcFGgHwvND/3c8beVK4
XlN1quweC6mKXXfE4BZdeaIHF+1NGKahfQYDmNQ23mzRmSJydg3KeYlaUCs4BA4e
k5UFeFAWxQ2NN6DIRotOydt3iDiJk4cgoPcM3798pQre+WOa59L/aX9gXxRo0JXK
AE0ups8chhwsfe/zJjCjqOnH6DF7bten2aS6/3LiTjRLu2fGcv67uETeGyJw7TPE
lUvMh/lpiamA7lgQbI69176vF9E3H2smSVt6YsYp7FL8UjaxGMOIXyNR10Rkp82b
sqHgYkcrGZuD/l8IiUMSINqxxZjOSWm83v0wkEpRZGzufdhFJxHcRBq0Y5r/nyXE
OJ3KcCykqIV3dPtV3jpY+6lSTKpquK87gWyNN2YuUjvhEWWcN6wFeZwUiUfxhI+A
S4ZIEa/g5EjLE6CddXXxUitb6ySOnefP7LS2uAxv8sav0+57PtYQwGsWrLjMuhgA
ZDqs0VbDIqpFRgCY4Tb6KADlP+66Cg3re+PkQQ0HQHYXdyYnUPfqcJxrK9FcaWwn
QPn2IfZ/R6/pg5fgd2ARg2YX0/aSkpQ5eOd6HBqG25L6fbcLBNTIVocNRSrlWWOI
LajjtATKktVRm9fNX18XX1Ea2TWS9jZeHg8fERDOe3wR61nD8VEMYLAbVKjkospI
xdKEEsEHiaFkdjuiYbuRIg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check3(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")


@csrf_exempt
def checkdata(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check6(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        print(action_type)
        if action_type == 'INIT':
            # Return the next screen & data to the client
            flow_token = decrypted_data['flow_token']
            parts = flow_token.split('/')
            donationId = parts[0]
            donation_ref_id = parts[1]
            phonenumberId = parts[2]
            facebook_objects = facebook_details.objects.filter(fb_phone_number_id=phonenumberId)
            facebook_token = ''
            client_id = 0
            for tok in facebook_objects:
                facebook_token += tok.fb_access_token
                client_id += tok.client_id
            donation_detailsobj = donation_types.objects.filter(client_id=client_id, id=donationId)
            donation_Amount = 0
            donation_Name = ''
            for f_i in donation_detailsobj:
                donation_Amount = f_i.donation_amount
                donation_Name = f_i.donation_name
            print(donation_Amount)
            if donation_Amount == 0:
                print("s in data_exchange")
                print("s zero")
                response = {
                    "version": decrypted_data['version'],
                    "screen": "CHECK_DETAILS",
                    "data": {
                        "excess": [{
                            "id": str(donationId),
                            "title": str(donation_Name)
                        }],

                    }
                }

                # Return the response as plaintext
                return HttpResponse(encrypt_response_check6(response, aes_key, iv), content_type='text/plain')
            else:
                print("no zero")

                response = {
                    "version": "3.0",
                    "screen": "DETAILS_DATA",
                    "data": {
                        "excess": [{
                            "id": str(donationId),
                            "title": str(donation_Name)
                        }],
                        "total": "₹" + str(donation_Amount) + " " + str(donation_Name)
                    }
                }
                return HttpResponse(encrypt_response_check7(response, aes_key, iv), content_type='text/plain')







        elif action_type == 'data_exchange':
            Screen_name = decrypted_data['screen']
            if Screen_name == 'DETAILS':
                pass
        elif action_type == 'ping':

            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                    "status": "active"
                }
            }
            return HttpResponse(encrypt_response_check6(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check6(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIjHolq1Z9o+QCAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECP2t36euzeDjBIIEyDLmQb8107Ra
IvZmERYJO+Lc7mxqKEtIg+1fJhU97f00JBiwbtbQNQxIhXvAyhKcHqTws3XSglJN
MMZEvXa4uZCwLzNsi56w11b5NIiUSnzjrqhGsYJxHUGAxrDQjcJ6k9z0fK7HKlv/
r3k4hes0V0GJJ3pyL2pN+aHm/eQjM4UspEn5bJLp5E5gKcj+NvMYJhI6qZT99IBj
ByPHN9RfXN5gPF3BQlUscZHhv04uXwpbf4gfg3RNow+QN3QvgFuWhKcPzjBWivad
ySatP3CxNpHdDwmxMrNxCa9+Wht27q6Ic23+kdPaJGFEoFbwgHYsKJTdglhxkpd7
9+oqaaaSEbmpH0bcAbW7+Th0n54mpNndZS9A5ww6Igs0sj7wVhHvCNJ2Jpiy8aPa
P5i5kkgpVUE5b1mD9/SONZG1E3LlBiujbMnse8x1LieSWyrc1pu3AwPfohD8TK6X
tzDVrgYJK+tOhViBO4sua9/gl6qepJRhWOdpYZDyu9ZoPvqpBDPJpwkLWk/sxo0t
CgvoFzDUlMViHgQDga9ntNejmZeX1ieLkG/zjddaSBnZcaj/bWYXfCDAqMZIvAi7
6SYKKyzPIGIPboVXreE9dLi96w+h02JnDf3DRSMeY83WjlxHD07yxQHl96r7mpQD
EzbVmNsVu3GZUvd7nN3bGyGgGm4B1yIWwmfoyEUa3Aevsg3lAyVM6nsxlAsLqyXg
RRAMAa2cTZSCiHTkEX4pm3e4zWFyWrdSfSGuZHMpklCEVHEWP7nq4FeRm31Ac4g0
gmyisc7XTgiYwASh6kr3Vu60lMCo5ydO95Jh1TdqDEzUPQA0OTh+ByvuopLEe6o5
x8eafPcf/JYEbxuMOFXlnT5xaXeDCCcuKKabSWNc9M16jqGDedZkRVffBX085kkD
1mmlCkWzglEVye9wPcVuhvXjexNofzWqpIqCRUfCZ2h6FNYo1s2skX8/qsU3FKJl
qk1vFHZbKFygMu9MaGJQtpZFWzYSE/ROjRsNBa2OT/UFwFR8YPzDFqaotNEyNxqq
FetP+iTzmdz8ySUaCiH3A4l+QwhfDssY4sIV0M4tDBo3lnozVqELnU18DfIR/awV
jB6z7hYW0dq/Fz2htcNiJ0ZnzA2FKPij6gtxPpy3DKxlmPQ55fiiNyNXtHsS8A44
MHxeiP/O18Ly75t+Ar2inJ5c6fZUMtlL1zhdi/sibw6aH4IjLSaM69AflzZIFtR7
0IzWGZ323uFd5iRvdlXPf4yNN/pPZozU/lFdDwInYAmONRT/GHncNbUyvwsqGVNa
ecH/ffaathoYWRL4uFJEslnO4l6SqGrxKYJV1p8gizMgn6goEv5YkmDuII8PoTcq
IC/WmcZCVk23kenObJ+xtFQjDzJGTGxwy/MmxzhRQFkqA9BPfN6Z34XICTVs5Uwr
UvRn6mM8S2BX3iqgH8aFeY/nrcL0bHOdN44sZjPRGHBfiNVssKq6dgBI9U7oL12+
t7tx5Em9pVqPypCyK/tcfu6vHQG1tmAm7uUEnWGcnw4qYlauBsIG2l+5EW7HRW9A
HOl1hcRyKS75ipDgaRHXUpfUYVMkqgyV8Pyjsy95buUVO4LyuBvvb2PfxTDv0ADJ
xjikQ5bWn81UMuMz8ysUpw==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check6(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")

@csrf_exempt
def testdata(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check7(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        ref_PhonenumberId = decrypted_data['flow_token']
        PhonenumberId = ref_PhonenumberId[:15]
        reference_id = ref_PhonenumberId[15:]
        print(reference_id)
        print(action_type)
        print(PhonenumberId)
        facebook_objects = facebook_details.objects.filter(fb_phone_number_id=PhonenumberId)
        facebook_token = ''
        client_id = 0
        for tok in facebook_objects:
            facebook_token += tok.fb_access_token
            client_id += tok.client_id


        if action_type == 'INIT':
            # Return the next screen & data to the client
            print("s in data_exchange")
            response = {
                "version": decrypted_data['version'],
                "screen": "DETAILS",
                "data": {

                }
            }

            # Return the response as plaintext
            return HttpResponse(encrypt_response_check7(response, aes_key, iv), content_type='text/plain')
        elif action_type == 'data_exchange':
            Screen_name = decrypted_data['screen']
            if Screen_name == 'DETAILS':
                response_data = decrypted_data['data']
                print(response_data)
                print("delhi")
                if any(key in response_data for key in ['ngo_Name', 'ngo_location', 'ngo_category', 'ngo_type']):
                    print("You are searching for NGO details. Please wait while it updates.")

                    keys_to_check = ['ngo_Name', 'ngo_location', 'ngo_category', 'ngo_type']
                    filters = {}

                    # Mapping keys to corresponding model column names
                    column_mapping = {
                        'ngo_Name': 'ngo_name',
                        'ngo_location': 'ngo_location',
                        'ngo_category': 'ngo_category',
                        'ngo_type': 'ngo_type'
                    }

                    for key in keys_to_check:
                        value = response_data.get(key)
                        if value:
                            db_column_name = column_mapping.get(key)
                            filters[f'{db_column_name}__icontains'] = value


                    #
                    # url = f"https://graph.facebook.com/v12.0/{whatsAppPhoneNumberId}/messages"
                    # headers = {
                    #     'Authorization': 'Bearer ' + facebook_token,
                    #     'Content-Type': 'application/json'
                    # }
                    #
                    # Using Q objects to dynamically construct the query
                    query = Q(client_id=client_id)
                    for key, value in filters.items():
                        query &= Q(**{key: value})

                    # Apply the constructed query to the donation_marketplace model
                    donationObj = donation_marketplace.objects.filter(query)
                    print("jodi")
                    print(donationObj)

                    Ngo_Name = []
                    Ngo_location = []
                    Ngo_id = []

                    if donationObj:
                        for l_i in donationObj:
                            Ngo_id.append(l_i.id)
                            Ngo_Name.append(l_i.ngo_name)
                            Ngo_location.append(l_i.ngo_location)

                        Ngo_list = [{"id": "A" + str(Ngo_id[i]),
                                     "title": Ngo_Name[i],
                                     "description": Ngo_location[i]}
                                    for i in range(len(Ngo_Name))]

                        donationImage = donation_marketplace_settings.objects.filter(client_id=client_id)
                        d_image = ''
                        for d in donationImage:
                            d_image = d.marketplace_welcome_image  # Assuming this is an ImageFieldFile object
                        print(d_image)

                        # Open the image file using the ImageFieldFile object
                        with d_image.open(mode='rb') as image_file:
                            image_content = image_file.read()

                        # Convert the image content to base64
                        encoded_string = base64.b64encode(image_content).decode('utf-8')

                        # 'encoded_string' now contains the base64 representation of the image
                        print(encoded_string)
                        file_path = 'C:/Vailo/18-12-2023 updated Dashboard/A_vMart/A_vMart/encoded_image.txt'

                        # Write the encoded string to a text file
                        with open(file_path, 'w') as text_file:
                            text_file.write(encoded_string)

                        print(f"Encoded string saved at: {file_path}")
                        print(d_image)


                        response = {
                            "version": "3.0",
                            "screen": "NGO_DATA",
                            "data": {
                                "details": encoded_string,
                                "options": Ngo_list
                            }
                        }
                        return HttpResponse(encrypt_response_check7(response, aes_key, iv), content_type='text/plain')
            elif Screen_name == 'NGO_DATA':
                data = decrypted_data['data']['options']
                ngo_ID = data[1:]
                donation_name = []
                donation_desc = []
                donation_id = []
                listdonation = donation_types.objects.filter(client_id=client_id,marketplace_id=ngo_ID)
                print("bulbul")
                print(listdonation)
                for list_i in listdonation:
                    print(list_i.id)
                    donation_id.append(list_i.id)
                    donation_desc.append(list_i.donation_short_description)
                    donation_name.append(list_i.donation_name)
                print(donation_name)
                donationlist = []
                for i in range(len(donation_name)):
                    donationlist.append({"id": "M" + str(donation_id[i]),
                                         "title": donation_name[i],
                                         "description": donation_desc[i]
                                         })
                donation_setting_Image = donation_settings.objects.filter(client_id=client_id)
                d_image = ''
                for d in donation_setting_Image:
                    d_image = d.donation_image  # Assuming this is an ImageFieldFile object
                print(d_image)

                # Open the image file using the ImageFieldFile object
                with d_image.open(mode='rb') as image_file:
                    image_content = image_file.read()

                # Convert the image content to base64
                encoded_string = base64.b64encode(image_content).decode('utf-8')

                # 'encoded_string' now contains the base64 representation of the image
                print(encoded_string)
                print(d_image)
                response = {
                    "version": "3.0",
                    "screen": "DONATION_TYPES",
                    "data": {
                        "details": encoded_string,
                        "options": donationlist
                    }
                }
                return HttpResponse(encrypt_response_check7(response, aes_key, iv), content_type='text/plain')
            elif Screen_name == 'DONATION_TYPES':
                data = decrypted_data['data']['options']
                donation_ID = data[1:]
                donation_dettails_obj = donation_types.objects.filter(client_id=client_id,id=donation_ID)
                donation_Amount = 0
                donation_Name = ''
                d_image = ''
                for d_i in donation_dettails_obj:
                    donation_Amount = d_i.donation_amount
                    donation_Name = d_i.donation_name
                    d_image = d_i.donation_type_image

                with d_image.open(mode='rb') as image_file:
                    image_content = image_file.read()

                # Convert the image content to base64
                encoded_string = base64.b64encode(image_content).decode('utf-8')

                # 'encoded_string' now contains the base64 representation of the image
                print(encoded_string)
                print(d_image)

                if donation_Amount == 0:
                    print("zero")
                    response = {
                        "version": "3.0",
                        "screen": "DONATION_DETAILS",
                        "data":{
                            "details": encoded_string,
                            "excess": [{
                                "id": str(donation_ID),
                                "title": str(donation_Name)
                            }],
                        }
                    }
                    return HttpResponse(encrypt_response_check7(response, aes_key, iv), content_type='text/plain')

                else:
                    print("no zero")

                    response = {
                        "version": "3.0",
                        "screen": "SUBMIT_DETAILS_DATA",
                        "data": {
                            "details": encoded_string,
                            "excess": [{
                                "id":str(donation_ID),
                                "title":str(donation_Name)
                            }],
                             "total": "₹"+ str(donation_Amount)+" "+str(donation_Name)
                        }
                    }
                    return HttpResponse(encrypt_response_check7(response, aes_key, iv), content_type='text/plain')

        elif action_type == 'ping':
            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                    "status": "active"
                }
            }
            return HttpResponse(encrypt_response_check7(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check7(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIczQ3XnflVPACAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECB9CP6cT9tJJBIIEyL//SUFeHJbL
JcuW1cdsOCzkaTU04vVLh5QivW8BUYeHAbpz9gH8ILlZNZFl4xHmn1c15V6EcGNL
E7y7NG7N7JQIE1Wez93GX9vIh5cy6dtXA8PxwOiDQjujbuImNqz4okP5vnO/Iuha
eTmJ0/QEUCzI8Ipssn+UVVqcAw4BaY1A+eL0jlgwptTJhOg2hJt0zDegfSclyrVY
Ae8XCPOY8NN6OVPjX4MlyQYGFH5M6y9z2mS82KNTn/TiOffJpY4NGPSK7uUUIsJ0
slHza0Ss/fqWDIFaTNLjR69rKNw0aicIvdW2lFPALAYpbQdIPenzNJuyJX8X6mho
Q/Eyo4hjQkWPEAwWvlHgCCU/ebM2C49FA64VDnd81fHUqrH2kEH3Gn4ekI8uFQpF
ifo5X2T0WZV7pA8GNg3BL2KetWcnBqPyjbM+yVzn1RYCfB627s5JFYy1kwKZMQkZ
mmKcMm5UNFD0FAD7hMJG3xJHKptD8FL2L5LHSPKn1fSsPMS3fSYtVNqRRV3/xU0K
UtS/OzwJ1Ogar2ypAdhDC8A+tHIkD6+knrpHHiUuhRlcDjszyadjoQPBwvjNNz3F
CHfHmvo79vl5PvvxHIj/u+EPMKjReqyh9/3ZX/BTfBz4mPy7bVbxhNuQV1rK1Ruc
ZzxgufcekWcnjDKOJPeDa3bttCO1Is35xPuBFEtIc4vL8XxcikPQT1rmJEUL77u6
cjbE8cGo2rj+j+NAo5DHZQBtrelsIKqaGpnHT8T4KLBim3OXliuUUJwKEOKNNQhT
hvSfBemfKnMJYXrqx+pSQZnBCJOCqP56U4FbKhoQthj/5S6UwZrXLaWtR7DA/K9E
owqHwPb/ISIskvygsZPiDr9RoJ3V330dZcUe+ypeimmTcF+8QNfYWu4OhO5z8x5v
tHhwEXmamlYq5fnseU9vZh6tqn+qbx/Qqw+lby5ymYeWrNZtwrE4mxKGezQqYybW
sd+HSh5gqODx149b5e6Pl4WXCFb0mbqidf754bp+gLMWHu+V1twmnBTF+IzTPVTY
fuJgGzAGlQ1J5glXWUzfjQdUqwyU7eJjIK3sHSanMaagm/gdJqQ2lAKtR+gRawHt
/iVGyBtDhtgI1+gjm1ViVok56B6S4FCMlh6CypQvzGenqU9PVqdCYq93QKYcUdvo
YfHbmcbqTfgLCr0rxzejCUTOlC8ihQWlMQfNYUfWlTezw0FTPE9ueJk7QMhBSDDf
b3zeGw22HvDEHapq9T/ZbNv7/FhrFXG0PZeBq/BXLv5cjLs5JgB5/3t/g+eAnYGv
3s11OPX4AVB1kptujoNAvYa0yoo7RN0PHQetNaf5deL3r/bndcikB+fdcbiNymDe
RhLXAve3c6roAxhPDsBJPEhaAskBLZp3LWfVNpZEsBlQBfvP/kPwPvJbSBQbLRLf
vsrMaGZgGDcm7Tqpp/7exKDao/k23SGvrhVbKllX1EnGG9QB6A0+c3UFkKVULRnP
Rgo4HJGR84Z1PdjTdEF8MfskAT4bJ+/ywUap714JkBu2w+fP8C5j05WtwkQPpmuI
4Goei62rUpoWtinRYnsrZW4fc3ghXLqzWo8UYdlBkYrBUpSqaRiJslD0Oe0nssYd
nS/C7a9xctNeJ2kLu/wVWg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check7(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")




@csrf_exempt
def appontementdata(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check8(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        PhonenumberId = decrypted_data['flow_token']
        ref_PhonenumberId = PhonenumberId[:15]
        toUser = PhonenumberId[15:]
        # print(reference_id)
        # print(action_type)
        print(ref_PhonenumberId)
        facebook_objects = facebook_details.objects.filter(fb_phone_number_id=ref_PhonenumberId)
        facebook_token = ''
        client_id = 0
        for tok in facebook_objects:
            facebook_token += tok.fb_access_token
            client_id += tok.client_id


        if action_type == 'INIT':
            # Return the next screen & data to the client
            print("s in data_exchange")
            response = {
                "version": decrypted_data['version'],
                "screen": "DETAILS",
                "data": {

                }
            }

            # Return the response as plaintext
            return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')
        elif action_type == 'data_exchange':
            Screen_name = decrypted_data['screen']
            if Screen_name == 'DETAILS':
                response_data = decrypted_data['data']
                print(response_data)
                print("delhi")
                if any(key in response_data for key in ['group_Name', 'group_location', 'group_category', 'group_type']):
                    print("You are searching for Hospital details. Please wait while it updates.")

                    keys_to_check = ['group_Name', 'group_location', 'group_category', 'group_type']
                    filters = {}

                    # Mapping keys to corresponding model column names
                    column_mapping = {
                        'group_Name': 'group_name',
                        'group_location': 'group_location',
                        'group_category': 'group_category',
                        'group_type': 'group_type'
                    }

                    for key in keys_to_check:
                        value = response_data.get(key)
                        if value:
                            db_column_name = column_mapping.get(key)
                            filters[f'{db_column_name}__icontains'] = value

                    # facebook_objects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                    # facebook_token = ''
                    # client_id = 0
                    #
                    # for tok in facebook_objects:
                    #     facebook_token += tok.fb_access_token
                    #     client_id += tok.client_id

                    # url = f"https://graph.facebook.com/v12.0/{whatsAppPhoneNumberId}/messages"
                    # headers = {
                    #     'Authorization': 'Bearer ' + facebook_token,
                    #     'Content-Type': 'application/json'
                    # }

                    # Using Q objects to dynamically construct the query
                    query = Q(client_id=client_id)
                    for key, value in filters.items():
                        query &= Q(**{key: value})

                    # Apply the constructed query to the donation_marketplace model
                    appointementObj = appointment_marketplace.objects.filter(query)
                    print("jodi")
                    print(appointementObj)

                    Group_Name = []
                    Group_location = []
                    Group_id = []

                    if appointementObj:
                        for l_i in appointementObj:
                            Group_id.append(l_i.id)
                            Group_Name.append(l_i.group_name)
                            Group_location.append(l_i.group_location)

                        Group_list = [{"id": "A" + str(Group_id[i]),
                                     "title": Group_Name[i],
                                     "description": Group_location[i]}
                                    for i in range(len(Group_Name))]
                        apptImage = appointment_marketplace_settings.objects.filter(client_id=client_id)
                        d_image = ''
                        for d in apptImage:
                            d_image = d.marketplace_welcome_image  # Assuming this is an ImageFieldFile object
                        print(d_image)

                        # Open the image file using the ImageFieldFile object
                        with d_image.open(mode='rb') as image_file:
                            image_content = image_file.read()

                        # Convert the image content to base64
                        encoded_string = base64.b64encode(image_content).decode('utf-8')

                        # 'encoded_string' now contains the base64 representation of the image
                        print(encoded_string)
                        file_path = 'C:/Vailo/18-12-2023 updated Dashboard/A_vMart/A_vMart/encoded_image2.txt'

                        # Write the encoded string to a text file
                        with open(file_path, 'w') as text_file:
                            text_file.write(encoded_string)

                        print(f"Encoded string saved at: {file_path}")
                        print(d_image)

                        response = {
                            "version": "3.0",
                            "screen": "HOSPITAL_DATA",
                            "data": {
                                "details":encoded_string,
                                "options": Group_list
                            }
                        }
                        return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')
            elif Screen_name == 'HOSPITAL_DATA':
                data = decrypted_data['data']['options']
                appt_ID = data[1:]
                consultant_name = []
                consultant_specialization = []
                consultant_id = []
                consultantDetails = Consultant_details.objects.filter(client_id=client_id,marketplace_id=appt_ID)
                for c_i in consultantDetails:
                    consultant_id.append(c_i.id)
                    consultant_name.append(c_i.consultant_name)
                    consultant_specialization.append(c_i.consultant_specialization)
                consultantlist = []
                for i in range(len(consultant_name)):
                    consultantlist.append({"id": "N" + str(consultant_id[i]),
                                           "title": consultant_name[i],
                                           "description": consultant_specialization[i]
                                           })
                apptImage = appointment_settings.objects.filter(client_id=client_id)
                d_image = ''
                for d in apptImage:
                    d_image = d.welcome_image  # Assuming this is an ImageFieldFile object
                print(d_image)

                # Open the image file using the ImageFieldFile object
                with d_image.open(mode='rb') as image_file:
                    image_content = image_file.read()

                # Convert the image content to base64
                encoded_string = base64.b64encode(image_content).decode('utf-8')

                # 'encoded_string' now contains the base64 representation of the image
                print(encoded_string)
                file_path = 'C:/Vailo/18-12-2023 updated Dashboard/A_vMart/A_vMart/encoded_image3.txt'

                # Write the encoded string to a text file
                with open(file_path, 'w') as text_file:
                    text_file.write(encoded_string)

                print(f"Encoded string saved at: {file_path}")
                print(d_image)
                response = {
                    "version": "3.0",
                    "screen": "DOCTORS_DATA",
                    "data": {
                        "details": encoded_string,
                        "options": consultantlist
                    }
                }
                return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')
            elif Screen_name == 'DOCTORS_DATA':
                data = decrypted_data['data']['options']
                response_id_id = data[1:]
                import datetime as dt

                current_date = dt.datetime.now().date()

                current_date += dt.timedelta(days=1)

                dates = []

                for i in range(60):
                    new_date = current_date + dt.timedelta(days=i)
                    dates.append(new_date)
                print(dates)

                a = 0
                day_of_week = 0
                ex_date = []
                only_dates = []
                formateed_dates = []
                all_available_slots = []
                consultantName = ''
                consultantSpecialization = ''
                for i, date in enumerate(dates, start=ord('a')):
                    print("jinja")
                    print(date)
                    print("lalli")
                    ex_date.append(date)
                    zformatted_date = date.strftime('%d-%b %a')
                    # formatted_date = zformatted_date[:6] + zformatted_date[-5:]
                    # print(formatted_date)
                    formateed_dates.append(zformatted_date)
                    only_date = date.strftime('%d-%m-%Y')
                    only_dates.append(only_date)
                    day_of_week = int(date.strftime('%w'))
                    variable_name = chr(i)
                    print(f"{variable_name} = {zformatted_date} {day_of_week}")
                    print(formateed_dates)

                    duration = None  # Initialize to None or an appropriate default value

                    slotDuration = Consultant_details.objects.filter(client_id=client_id, id=response_id_id)
                    for s_i in slotDuration:
                        duration_str = s_i.slot_duration
                        consultantName = s_i.consultant_name
                        consultantSpecialization = s_i.consultant_specialization
                        numeric_part = int(''.join(filter(str.isdigit, duration_str)))
                        duration = numeric_part

                    hslots = []
                    not_available_slot = []
                    holidayDetails = Consultant_holiday_leaves.objects.filter(client_id=client_id, date=date)
                    for h_i in holidayDetails:
                        not_available_slots = {
                            "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
                            "end_time": h_i.end_time.strftime("%H:%M"),
                        }
                        not_available_slot.append(not_available_slots)

                    for record in not_available_slot:
                        start_time_str1 = record["start_time"]
                        end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format

                        record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
                        record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
                        current_time1 = record_start_time1
                        while current_time1 < record_end_time2:
                            slot_start = current_time1.strftime("%H:%M")
                            current_time1 += timedelta(minutes=duration)
                            slot_end = current_time1.strftime("%H:%M")
                            hslots.append((slot_start, slot_end))
                    print("aa")
                    print(hslots)
                    print("bb")

                    all_slots = []
                    availability_records = []

                    availablityObject = Consultant_availablity.objects.filter(client_id=client_id,
                                                                              Consultant_settings_id=response_id_id,
                                                                              day_of_week=day_of_week)
                    print(availablityObject)
                    for a_i in availablityObject:
                        print(a_i.id)
                        availability_record = {
                            "start_time": a_i.start_time.strftime("%H:%M"),
                            "end_time": a_i.end_time.strftime("%H:%M"),
                        }
                        # print(availability_record)
                        # print("mohan")
                        availability_records.append(availability_record)

                    for record in availability_records:
                        start_time_str = record["start_time"]
                        end_time_str = record["end_time"]

                        record_start_time = datetime.strptime(start_time_str, "%H:%M")
                        record_end_time = datetime.strptime(end_time_str, "%H:%M")
                        current_time = record_start_time

                        while current_time < record_end_time:
                            slot_start = current_time.strftime("%H:%M")
                            current_time += timedelta(minutes=duration)
                            slot_end = current_time.strftime("%H:%M")
                            all_slots.append((slot_start, slot_end))
                    final_all_slots = [slot for slot in all_slots if slot not in hslots]
                    print("channi")
                    print(final_all_slots)
                    print(len(final_all_slots))
                    print("keshav")

                    # bookingObject = Bookings.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
                    #                                         date=current_date)
                    # booked_slots = set(booking.notes1 for booking in bookingObject)
                    # available_slots = [slot for slot in final_all_slots if slot not in booked_slots]

                    existing_bookings = appointment_bookings.objects.filter(client_id=client_id,
                                                                            Consultant_settings_id=response_id_id,
                                                                            date=date)
                    print("gowda")
                    print(existing_bookings)
                    print("sekar")

                    booked_slots = set()
                    for booking in existing_bookings:
                        start_time_str = booking.start_time.strftime("%H:%M")
                        end_time_str = booking.end_time.strftime("%H:%M")
                        booked_slots.add((start_time_str, end_time_str))
                    print("vv")
                    print(booked_slots)
                    print("andhra")
                    available_slots = [slot for slot in final_all_slots if slot not in booked_slots]

                    all_available_slots.append(available_slots)
                    print("guna")
                    print(all_available_slots)
                    print("shouya")

                    # a=len(available_slots)
                    # print(a)
                    # print(available_slots)
                    # print(type(available_slots))
                    # print("done very good job")

                # first_position = len(all_available_slots[0])
                # second_position = len(all_available_slots[1])
                # third_position = len(all_available_slots[2])
                # fourth_position = len(all_available_slots[3])
                # fifth_position = len(all_available_slots[4])
                # six_position = len(all_available_slots[5])
                # seventh_position = len(all_available_slots[6])
                # print(seventh_position)

                len_all_slots = []

                for i, date in enumerate(ex_date):
                    avlslots = len(all_available_slots[i])
                    formateedDate = ''
                    if avlslots != 0 and avlslots <= 10:
                        formateedDate = date.strftime('%d %b %a')
                        len_all_slots.append((i, date, avlslots, formateedDate))
                    else:
                        print(f"No slots available for {formateedDate}")

                # Now len_all_slots contains tuples of (formatted_date, avlslots)
                print(len_all_slots)
                print("burger")

                show_avl_slots = []
                show_date = []
                total_avl_slots = 0
                for j, (i, date, avlslots, formateedDate) in enumerate(len_all_slots[:8]):
                    show_date.append(date)
                    total_avl_slots += avlslots
                    title = f"{formateedDate} ({avlslots} slots)"
                    show_avl_slots.append({"id": "K" + str(response_id_id) + "/" + str(date),
                                           "title": title

                                           })
                Consultant_Image = Consultant_details.objects.filter(client_id=client_id, id=response_id_id)
                consultant_image = ''
                for c_i in Consultant_Image:
                    consultant_image = c_i.consultant_image

                with consultant_image.open(mode='rb') as image_file:
                    image_content = image_file.read()

                # Convert the image content to base64
                encoded_string = base64.b64encode(image_content).decode('utf-8')

                # 'encoded_string' now contains the base64 representation of the image
                print(encoded_string)
                file_path = 'C:/Vailo/18-12-2023 updated Dashboard/A_vMart/A_vMart/encoded_image2.txt'

                # Write the encoded string to a text file
                with open(file_path, 'w') as text_file:
                    text_file.write(encoded_string)

                print(f"Encoded string saved at: {file_path}")
                print(consultant_image)

                print(show_avl_slots)
                first_date = show_date[0]
                last_date = show_date[-1]
                print('bomma')
                print(first_date)
                print(last_date)
                print("borusu")
                response = {
                    "version": "3.0",
                    "screen": "DATES_DATA",
                    "data": {
                        "details": encoded_string,
                        "options": show_avl_slots

                    }
                }
                return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')
            elif Screen_name == 'DATES_DATA':
                response_id = decrypted_data['data']['options']
                print("tipelinganna")
                print(response_id)
                slash_index = response_id.index('/')

                date = []
                dates = response_id[slash_index + 1:]
                print("jayamma")
                print(dates)
                print("jayanna")
                dates_new = datetime.strptime(str(dates), '%Y-%m-%d')
                date.append(dates_new)

                consult_id = response_id[1:slash_index]
                print("nagamma")
                print(consult_id)
                print("nagaraj")

                customer = appointment_visitor.objects.filter(client_id=client_id,
                                                              Visitor_Whatsapp_Number=toUser).first()
                visitor_id = 0
                if customer:
                    visitor_id = customer.id

                # import datetime as dt
                #
                # current_date = dt.datetime.now().date()
                #
                # current_date += dt.timedelta(days=1)
                #
                # dates = []
                #
                # for i in range(7):
                #     new_date = current_date + dt.timedelta(days=i)
                #     dates.append(new_date)
                # print(dates)

                a = 0
                day_of_week = 0
                only_dates = []
                sub_dates = []
                finalDates = []
                formateed_dates = []
                all_available_slots = []
                consultantName = ''
                consultantSpecialization = ''
                for i, date in enumerate(date, start=ord('a')):
                    zformatted_date = date.strftime('%d/%B/%Y %A')
                    sub_date = date.strftime('%d %b %a')
                    sub_dates.append(sub_date)
                    formatted_date = zformatted_date[:6] + zformatted_date[12:]
                    print(formatted_date)
                    formateed_dates.append(formatted_date)
                    only_date = date.strftime('%d-%m-%Y')
                    final_only_date = only_date.replace("-", "")
                    finalDates.append(final_only_date)
                    day_of_week = int(date.strftime('%w'))
                    variable_name = chr(i)
                    print(f"{variable_name} = {formatted_date} {day_of_week}")
                    print(formateed_dates)

                    duration = None  # Initialize to None or an appropriate default value
                    slotDuration = Consultant_details.objects.filter(client_id=client_id, id=consult_id)
                    for s_i in slotDuration:
                        duration_str = s_i.slot_duration
                        consultantName = s_i.consultant_name
                        consultantSpecialization = s_i.consultant_specialization
                        numeric_part = int(''.join(filter(str.isdigit, duration_str)))
                        duration = numeric_part

                    hslots = []
                    not_available_slot = []
                    holidayDetails = Consultant_holiday_leaves.objects.filter(client_id=client_id, date=date)
                    for h_i in holidayDetails:
                        not_available_slots = {
                            "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
                            "end_time": h_i.end_time.strftime("%H:%M"),
                        }
                        not_available_slot.append(not_available_slots)

                    for record in not_available_slot:
                        start_time_str1 = record["start_time"]
                        end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format

                        record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
                        record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
                        current_time1 = record_start_time1
                        while current_time1 < record_end_time2:
                            slot_start = current_time1.strftime("%H:%M")
                            current_time1 += timedelta(minutes=duration)
                            slot_end = current_time1.strftime("%H:%M")
                            hslots.append((slot_start, slot_end))
                    print("aa")
                    print(hslots)
                    print("bb")

                    all_slots = []
                    availability_records = []

                    availablityObject = Consultant_availablity.objects.filter(client_id=client_id,
                                                                              Consultant_settings_id=consult_id,
                                                                              day_of_week=day_of_week)
                    print(availablityObject)
                    for a_i in availablityObject:
                        print(a_i.id)
                        availability_record = {
                            "start_time": a_i.start_time.strftime("%H:%M"),
                            "end_time": a_i.end_time.strftime("%H:%M"),
                        }
                        print(availability_record)
                        print("mohan")
                        availability_records.append(availability_record)

                    for record in availability_records:
                        start_time_str = record["start_time"]
                        end_time_str = record["end_time"]

                        record_start_time = datetime.strptime(start_time_str, "%H:%M")
                        record_end_time = datetime.strptime(end_time_str, "%H:%M")
                        current_time = record_start_time

                        while current_time < record_end_time:
                            slot_start = current_time.strftime("%H:%M")
                            current_time += timedelta(minutes=duration)
                            slot_end = current_time.strftime("%H:%M")
                            all_slots.append((slot_start, slot_end))
                    final_all_slots = [slot for slot in all_slots if slot not in hslots]
                    print("channi")
                    print(final_all_slots)
                    print(len(final_all_slots))
                    print("keshav")

                    existing_bookings = appointment_bookings.objects.filter(client_id=client_id,
                                                                            Consultant_settings_id=consult_id,
                                                                            date=date)
                    print("gowda")
                    print(existing_bookings)
                    print("sekar")

                    booked_slots = set()
                    for booking in existing_bookings:
                        start_time_str = booking.start_time.strftime("%H:%M")
                        end_time_str = booking.end_time.strftime("%H:%M")
                        booked_slots.add((start_time_str, end_time_str))
                    print("vv")
                    print(booked_slots)
                    print("andhra")
                    available_slots = [slot for slot in final_all_slots if slot not in booked_slots]

                    all_available_slots.append(available_slots)
                print("jill")
                print(all_available_slots)
                print("jiga")
                slot_data = all_available_slots[0]
                total_time_slots = len(slot_data)

                list_all_data = []
                formatted_slots_details = []
                formatted_duration_details = []
                for slot_start, slot_end in slot_data:
                    print(slot_start)
                    print(slot_end)
                    formatted_duation_create = f"{slot_start}-{slot_end}"
                    formatted_slot_create = f"{slot_start}"
                    date_formate_slot_create = datetime.strptime(formatted_slot_create, "%H:%M")
                    formatted_start_time = date_formate_slot_create.strftime("%I:%M%p")
                    formatted_slots_details.append(formatted_start_time)
                    formatted_duration_details.append(formatted_duation_create)

                for i in range(len(formatted_slots_details)):
                    list_all_data.append({"id": "S" + str(consult_id) + "/" + str(
                        visitor_id) + "//" + str(finalDates[0]) + str(formatted_duration_details[i]) + str(i),
                                          "title": str(sub_dates[0]) + " " + str(formatted_slots_details[i])

                                          })

                print("correct")
                print(formatted_slots_details)
                response = {
                    "version": "3.0",
                    "screen": "SLOTS_DATA",
                    "data": {
                        "options": list_all_data

                    }
                }
                return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')


        elif action_type == 'ping':
            print("s in appontement")

            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                    "status": "active"
                }
            }
            return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check8(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIczQ3XnflVPACAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECB9CP6cT9tJJBIIEyL//SUFeHJbL
JcuW1cdsOCzkaTU04vVLh5QivW8BUYeHAbpz9gH8ILlZNZFl4xHmn1c15V6EcGNL
E7y7NG7N7JQIE1Wez93GX9vIh5cy6dtXA8PxwOiDQjujbuImNqz4okP5vnO/Iuha
eTmJ0/QEUCzI8Ipssn+UVVqcAw4BaY1A+eL0jlgwptTJhOg2hJt0zDegfSclyrVY
Ae8XCPOY8NN6OVPjX4MlyQYGFH5M6y9z2mS82KNTn/TiOffJpY4NGPSK7uUUIsJ0
slHza0Ss/fqWDIFaTNLjR69rKNw0aicIvdW2lFPALAYpbQdIPenzNJuyJX8X6mho
Q/Eyo4hjQkWPEAwWvlHgCCU/ebM2C49FA64VDnd81fHUqrH2kEH3Gn4ekI8uFQpF
ifo5X2T0WZV7pA8GNg3BL2KetWcnBqPyjbM+yVzn1RYCfB627s5JFYy1kwKZMQkZ
mmKcMm5UNFD0FAD7hMJG3xJHKptD8FL2L5LHSPKn1fSsPMS3fSYtVNqRRV3/xU0K
UtS/OzwJ1Ogar2ypAdhDC8A+tHIkD6+knrpHHiUuhRlcDjszyadjoQPBwvjNNz3F
CHfHmvo79vl5PvvxHIj/u+EPMKjReqyh9/3ZX/BTfBz4mPy7bVbxhNuQV1rK1Ruc
ZzxgufcekWcnjDKOJPeDa3bttCO1Is35xPuBFEtIc4vL8XxcikPQT1rmJEUL77u6
cjbE8cGo2rj+j+NAo5DHZQBtrelsIKqaGpnHT8T4KLBim3OXliuUUJwKEOKNNQhT
hvSfBemfKnMJYXrqx+pSQZnBCJOCqP56U4FbKhoQthj/5S6UwZrXLaWtR7DA/K9E
owqHwPb/ISIskvygsZPiDr9RoJ3V330dZcUe+ypeimmTcF+8QNfYWu4OhO5z8x5v
tHhwEXmamlYq5fnseU9vZh6tqn+qbx/Qqw+lby5ymYeWrNZtwrE4mxKGezQqYybW
sd+HSh5gqODx149b5e6Pl4WXCFb0mbqidf754bp+gLMWHu+V1twmnBTF+IzTPVTY
fuJgGzAGlQ1J5glXWUzfjQdUqwyU7eJjIK3sHSanMaagm/gdJqQ2lAKtR+gRawHt
/iVGyBtDhtgI1+gjm1ViVok56B6S4FCMlh6CypQvzGenqU9PVqdCYq93QKYcUdvo
YfHbmcbqTfgLCr0rxzejCUTOlC8ihQWlMQfNYUfWlTezw0FTPE9ueJk7QMhBSDDf
b3zeGw22HvDEHapq9T/ZbNv7/FhrFXG0PZeBq/BXLv5cjLs5JgB5/3t/g+eAnYGv
3s11OPX4AVB1kptujoNAvYa0yoo7RN0PHQetNaf5deL3r/bndcikB+fdcbiNymDe
RhLXAve3c6roAxhPDsBJPEhaAskBLZp3LWfVNpZEsBlQBfvP/kPwPvJbSBQbLRLf
vsrMaGZgGDcm7Tqpp/7exKDao/k23SGvrhVbKllX1EnGG9QB6A0+c3UFkKVULRnP
Rgo4HJGR84Z1PdjTdEF8MfskAT4bJ+/ywUap714JkBu2w+fP8C5j05WtwkQPpmuI
4Goei62rUpoWtinRYnsrZW4fc3ghXLqzWo8UYdlBkYrBUpSqaRiJslD0Oe0nssYd
nS/C7a9xctNeJ2kLu/wVWg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check8(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")


@csrf_exempt
def mydonationdata(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check9(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        PhonenumberId = decrypted_data['flow_token']
        ref_PhonenumberId = PhonenumberId[:15]
        toUser = PhonenumberId[15:]
        # print(reference_id)
        # print(action_type)
        print(ref_PhonenumberId)
        facebook_objects = facebook_details.objects.filter(fb_phone_number_id=ref_PhonenumberId)
        facebook_token = ''
        client_id = 0
        for tok in facebook_objects:
            facebook_token += tok.fb_access_token
            client_id += tok.client_id


        if action_type == 'INIT':
            # Return the next screen & data to the client
            print("s in INIT")
            donar_details = donation_details.objects.filter(client_id=client_id,donar_phone_number=toUser,payment_status=1)
            if donar_details:
                print(donar_details)
                donation_Id = []
                donation_Name = []
                donation_Amount = []
                for i in donar_details:
                    donation_Id.append(i.id)
                    donation_Name.append(i.donation_name)
                    donation_Amount.append(i.donation_amount)

                All_Donations = []
                for j in range(len(donation_Name)):
                    All_Donations.append({
                        "id": str(donation_Id[j]),
                        "title": donation_Name[j]
                    })

                response = {
                    "version": decrypted_data['version'],
                    "screen": "MYDONATION_DETAILS",
                    "data": {
                        "details":"Your Donations",
                        "options": All_Donations

                    }
                }

                # Return the response as plaintext
                return HttpResponse(encrypt_response_check9(response, aes_key, iv), content_type='text/plain')
            else:
                print("s no donations")
                response = {
                    "version": decrypted_data['version'],
                    "screen": "MYDONATION_DETAILS",
                    "data": {
                        "details": "You have no donations.Please donate.",
                        "options":[{
                            "id":"No records",
                            "title":"No records"
                        }]

                    }
                }

                # Return the response as plaintext
                return HttpResponse(encrypt_response_check9(response, aes_key, iv), content_type='text/plain')


        # elif action_type == 'data_exchange':
        #     Screen_name = decrypted_data['screen']
        #     if Screen_name == 'DETAILS':
        #         response_data = decrypted_data['data']
        #         print(response_data)
        #         print("delhi")
        #         if any(key in response_data for key in ['group_Name', 'group_location', 'group_category', 'group_type']):
        #             print("You are searching for Hospital details. Please wait while it updates.")
        #
        #             keys_to_check = ['group_Name', 'group_location', 'group_category', 'group_type']
        #             filters = {}
        #
        #             # Mapping keys to corresponding model column names
        #             column_mapping = {
        #                 'group_Name': 'group_name',
        #                 'group_location': 'group_location',
        #                 'group_category': 'group_category',
        #                 'group_type': 'group_type'
        #             }
        #
        #             for key in keys_to_check:
        #                 value = response_data.get(key)
        #                 if value:
        #                     db_column_name = column_mapping.get(key)
        #                     filters[f'{db_column_name}__icontains'] = value
        #
        #             # facebook_objects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
        #             # facebook_token = ''
        #             # client_id = 0
        #             #
        #             # for tok in facebook_objects:
        #             #     facebook_token += tok.fb_access_token
        #             #     client_id += tok.client_id
        #
        #             # url = f"https://graph.facebook.com/v12.0/{whatsAppPhoneNumberId}/messages"
        #             # headers = {
        #             #     'Authorization': 'Bearer ' + facebook_token,
        #             #     'Content-Type': 'application/json'
        #             # }
        #
        #             # Using Q objects to dynamically construct the query
        #             query = Q(client_id=client_id)
        #             for key, value in filters.items():
        #                 query &= Q(**{key: value})
        #
        #             # Apply the constructed query to the donation_marketplace model
        #             appointementObj = appointment_marketplace.objects.filter(query)
        #             print("jodi")
        #             print(appointementObj)
        #
        #             Group_Name = []
        #             Group_location = []
        #             Group_id = []
        #
        #             if appointementObj:
        #                 for l_i in appointementObj:
        #                     Group_id.append(l_i.id)
        #                     Group_Name.append(l_i.group_name)
        #                     Group_location.append(l_i.group_location)
        #
        #                 Group_list = [{"id": "A" + str(Group_id[i]),
        #                              "title": Group_Name[i],
        #                              "description": Group_location[i]}
        #                             for i in range(len(Group_Name))]
        #                 response = {
        #                     "version": "3.0",
        #                     "screen": "HOSPITAL_DATA",
        #                     "data": {
        #                         "options": Group_list
        #                     }
        #                 }
        #                 return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')
        #     elif Screen_name == 'HOSPITAL_DATA':
        #         data = decrypted_data['data']['options']
        #         appt_ID = data[1:]
        #         consultant_name = []
        #         consultant_specialization = []
        #         consultant_id = []
        #         consultantDetails = Consultant_details.objects.filter(client_id=client_id,marketplace_id=appt_ID)
        #         for c_i in consultantDetails:
        #             consultant_id.append(c_i.id)
        #             consultant_name.append(c_i.consultant_name)
        #             consultant_specialization.append(c_i.consultant_specialization)
        #         consultantlist = []
        #         for i in range(len(consultant_name)):
        #             consultantlist.append({"id": "N" + str(consultant_id[i]),
        #                                    "title": consultant_name[i],
        #                                    "description": consultant_specialization[i]
        #                                    })
        #         response = {
        #             "version": "3.0",
        #             "screen": "DOCTORS_DATA",
        #             "data": {
        #                 "options": consultantlist
        #             }
        #         }
        #         return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')
        #     elif Screen_name == 'DOCTORS_DATA':
        #         data = decrypted_data['data']['options']
        #         response_id_id = data[1:]
        #         import datetime as dt
        #
        #         current_date = dt.datetime.now().date()
        #
        #         current_date += dt.timedelta(days=1)
        #
        #         dates = []
        #
        #         for i in range(60):
        #             new_date = current_date + dt.timedelta(days=i)
        #             dates.append(new_date)
        #         print(dates)
        #
        #         a = 0
        #         day_of_week = 0
        #         ex_date = []
        #         only_dates = []
        #         formateed_dates = []
        #         all_available_slots = []
        #         consultantName = ''
        #         consultantSpecialization = ''
        #         for i, date in enumerate(dates, start=ord('a')):
        #             print("jinja")
        #             print(date)
        #             print("lalli")
        #             ex_date.append(date)
        #             zformatted_date = date.strftime('%d-%b %a')
        #             # formatted_date = zformatted_date[:6] + zformatted_date[-5:]
        #             # print(formatted_date)
        #             formateed_dates.append(zformatted_date)
        #             only_date = date.strftime('%d-%m-%Y')
        #             only_dates.append(only_date)
        #             day_of_week = int(date.strftime('%w'))
        #             variable_name = chr(i)
        #             print(f"{variable_name} = {zformatted_date} {day_of_week}")
        #             print(formateed_dates)
        #
        #             duration = None  # Initialize to None or an appropriate default value
        #
        #             slotDuration = Consultant_details.objects.filter(client_id=client_id, id=response_id_id)
        #             for s_i in slotDuration:
        #                 duration_str = s_i.slot_duration
        #                 consultantName = s_i.consultant_name
        #                 consultantSpecialization = s_i.consultant_specialization
        #                 numeric_part = int(''.join(filter(str.isdigit, duration_str)))
        #                 duration = numeric_part
        #
        #             hslots = []
        #             not_available_slot = []
        #             holidayDetails = Consultant_holiday_leaves.objects.filter(client_id=client_id, date=date)
        #             for h_i in holidayDetails:
        #                 not_available_slots = {
        #                     "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
        #                     "end_time": h_i.end_time.strftime("%H:%M"),
        #                 }
        #                 not_available_slot.append(not_available_slots)
        #
        #             for record in not_available_slot:
        #                 start_time_str1 = record["start_time"]
        #                 end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format
        #
        #                 record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
        #                 record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
        #                 current_time1 = record_start_time1
        #                 while current_time1 < record_end_time2:
        #                     slot_start = current_time1.strftime("%H:%M")
        #                     current_time1 += timedelta(minutes=duration)
        #                     slot_end = current_time1.strftime("%H:%M")
        #                     hslots.append((slot_start, slot_end))
        #             print("aa")
        #             print(hslots)
        #             print("bb")
        #
        #             all_slots = []
        #             availability_records = []
        #
        #             availablityObject = Consultant_availablity.objects.filter(client_id=client_id,
        #                                                                       Consultant_settings_id=response_id_id,
        #                                                                       day_of_week=day_of_week)
        #             print(availablityObject)
        #             for a_i in availablityObject:
        #                 print(a_i.id)
        #                 availability_record = {
        #                     "start_time": a_i.start_time.strftime("%H:%M"),
        #                     "end_time": a_i.end_time.strftime("%H:%M"),
        #                 }
        #                 # print(availability_record)
        #                 # print("mohan")
        #                 availability_records.append(availability_record)
        #
        #             for record in availability_records:
        #                 start_time_str = record["start_time"]
        #                 end_time_str = record["end_time"]
        #
        #                 record_start_time = datetime.strptime(start_time_str, "%H:%M")
        #                 record_end_time = datetime.strptime(end_time_str, "%H:%M")
        #                 current_time = record_start_time
        #
        #                 while current_time < record_end_time:
        #                     slot_start = current_time.strftime("%H:%M")
        #                     current_time += timedelta(minutes=duration)
        #                     slot_end = current_time.strftime("%H:%M")
        #                     all_slots.append((slot_start, slot_end))
        #             final_all_slots = [slot for slot in all_slots if slot not in hslots]
        #             print("channi")
        #             print(final_all_slots)
        #             print(len(final_all_slots))
        #             print("keshav")
        #
        #             # bookingObject = Bookings.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
        #             #                                         date=current_date)
        #             # booked_slots = set(booking.notes1 for booking in bookingObject)
        #             # available_slots = [slot for slot in final_all_slots if slot not in booked_slots]
        #
        #             existing_bookings = appointment_bookings.objects.filter(client_id=client_id,
        #                                                                     Consultant_settings_id=response_id_id,
        #                                                                     date=date)
        #             print("gowda")
        #             print(existing_bookings)
        #             print("sekar")
        #
        #             booked_slots = set()
        #             for booking in existing_bookings:
        #                 start_time_str = booking.start_time.strftime("%H:%M")
        #                 end_time_str = booking.end_time.strftime("%H:%M")
        #                 booked_slots.add((start_time_str, end_time_str))
        #             print("vv")
        #             print(booked_slots)
        #             print("andhra")
        #             available_slots = [slot for slot in final_all_slots if slot not in booked_slots]
        #
        #             all_available_slots.append(available_slots)
        #             print("guna")
        #             print(all_available_slots)
        #             print("shouya")
        #
        #             # a=len(available_slots)
        #             # print(a)
        #             # print(available_slots)
        #             # print(type(available_slots))
        #             # print("done very good job")
        #
        #         # first_position = len(all_available_slots[0])
        #         # second_position = len(all_available_slots[1])
        #         # third_position = len(all_available_slots[2])
        #         # fourth_position = len(all_available_slots[3])
        #         # fifth_position = len(all_available_slots[4])
        #         # six_position = len(all_available_slots[5])
        #         # seventh_position = len(all_available_slots[6])
        #         # print(seventh_position)
        #
        #         len_all_slots = []
        #
        #         for i, date in enumerate(ex_date):
        #             avlslots = len(all_available_slots[i])
        #             formateedDate = ''
        #             if avlslots != 0 and avlslots <= 10:
        #                 formateedDate = date.strftime('%d %b %a')
        #                 len_all_slots.append((i, date, avlslots, formateedDate))
        #             else:
        #                 print(f"No slots available for {formateedDate}")
        #
        #         # Now len_all_slots contains tuples of (formatted_date, avlslots)
        #         print(len_all_slots)
        #         print("burger")
        #
        #         show_avl_slots = []
        #         show_date = []
        #         total_avl_slots = 0
        #         for j, (i, date, avlslots, formateedDate) in enumerate(len_all_slots[:8]):
        #             show_date.append(date)
        #             total_avl_slots += avlslots
        #             title = f"{formateedDate} ({avlslots} slots)"
        #             show_avl_slots.append({"id": "K" + str(response_id_id) + "/" + str(date),
        #                                    "title": title
        #
        #                                    })
        #         print(show_avl_slots)
        #         first_date = show_date[0]
        #         last_date = show_date[-1]
        #         print('bomma')
        #         print(first_date)
        #         print(last_date)
        #         print("borusu")
        #         response = {
        #             "version": "3.0",
        #             "screen": "DATES_DATA",
        #             "data": {
        #                 "options": show_avl_slots
        #
        #             }
        #         }
        #         return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')
        #     elif Screen_name == 'DATES_DATA':
        #         response_id = decrypted_data['data']['options']
        #         print("tipelinganna")
        #         print(response_id)
        #         slash_index = response_id.index('/')
        #
        #         date = []
        #         dates = response_id[slash_index + 1:]
        #         print("jayamma")
        #         print(dates)
        #         print("jayanna")
        #         dates_new = datetime.strptime(str(dates), '%Y-%m-%d')
        #         date.append(dates_new)
        #
        #         consult_id = response_id[1:slash_index]
        #         print("nagamma")
        #         print(consult_id)
        #         print("nagaraj")
        #
        #         customer = appointment_visitor.objects.filter(client_id=client_id,
        #                                                       Visitor_Whatsapp_Number=toUser).first()
        #         visitor_id = 0
        #         if customer:
        #             visitor_id = customer.id
        #
        #         # import datetime as dt
        #         #
        #         # current_date = dt.datetime.now().date()
        #         #
        #         # current_date += dt.timedelta(days=1)
        #         #
        #         # dates = []
        #         #
        #         # for i in range(7):
        #         #     new_date = current_date + dt.timedelta(days=i)
        #         #     dates.append(new_date)
        #         # print(dates)
        #
        #         a = 0
        #         day_of_week = 0
        #         only_dates = []
        #         sub_dates = []
        #         finalDates = []
        #         formateed_dates = []
        #         all_available_slots = []
        #         consultantName = ''
        #         consultantSpecialization = ''
        #         for i, date in enumerate(date, start=ord('a')):
        #             zformatted_date = date.strftime('%d/%B/%Y %A')
        #             sub_date = date.strftime('%d %b %a')
        #             sub_dates.append(sub_date)
        #             formatted_date = zformatted_date[:6] + zformatted_date[12:]
        #             print(formatted_date)
        #             formateed_dates.append(formatted_date)
        #             only_date = date.strftime('%d-%m-%Y')
        #             final_only_date = only_date.replace("-", "")
        #             finalDates.append(final_only_date)
        #             day_of_week = int(date.strftime('%w'))
        #             variable_name = chr(i)
        #             print(f"{variable_name} = {formatted_date} {day_of_week}")
        #             print(formateed_dates)
        #
        #             duration = None  # Initialize to None or an appropriate default value
        #             slotDuration = Consultant_details.objects.filter(client_id=client_id, id=consult_id)
        #             for s_i in slotDuration:
        #                 duration_str = s_i.slot_duration
        #                 consultantName = s_i.consultant_name
        #                 consultantSpecialization = s_i.consultant_specialization
        #                 numeric_part = int(''.join(filter(str.isdigit, duration_str)))
        #                 duration = numeric_part
        #
        #             hslots = []
        #             not_available_slot = []
        #             holidayDetails = Consultant_holiday_leaves.objects.filter(client_id=client_id, date=date)
        #             for h_i in holidayDetails:
        #                 not_available_slots = {
        #                     "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
        #                     "end_time": h_i.end_time.strftime("%H:%M"),
        #                 }
        #                 not_available_slot.append(not_available_slots)
        #
        #             for record in not_available_slot:
        #                 start_time_str1 = record["start_time"]
        #                 end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format
        #
        #                 record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
        #                 record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
        #                 current_time1 = record_start_time1
        #                 while current_time1 < record_end_time2:
        #                     slot_start = current_time1.strftime("%H:%M")
        #                     current_time1 += timedelta(minutes=duration)
        #                     slot_end = current_time1.strftime("%H:%M")
        #                     hslots.append((slot_start, slot_end))
        #             print("aa")
        #             print(hslots)
        #             print("bb")
        #
        #             all_slots = []
        #             availability_records = []
        #
        #             availablityObject = Consultant_availablity.objects.filter(client_id=client_id,
        #                                                                       Consultant_settings_id=consult_id,
        #                                                                       day_of_week=day_of_week)
        #             print(availablityObject)
        #             for a_i in availablityObject:
        #                 print(a_i.id)
        #                 availability_record = {
        #                     "start_time": a_i.start_time.strftime("%H:%M"),
        #                     "end_time": a_i.end_time.strftime("%H:%M"),
        #                 }
        #                 print(availability_record)
        #                 print("mohan")
        #                 availability_records.append(availability_record)
        #
        #             for record in availability_records:
        #                 start_time_str = record["start_time"]
        #                 end_time_str = record["end_time"]
        #
        #                 record_start_time = datetime.strptime(start_time_str, "%H:%M")
        #                 record_end_time = datetime.strptime(end_time_str, "%H:%M")
        #                 current_time = record_start_time
        #
        #                 while current_time < record_end_time:
        #                     slot_start = current_time.strftime("%H:%M")
        #                     current_time += timedelta(minutes=duration)
        #                     slot_end = current_time.strftime("%H:%M")
        #                     all_slots.append((slot_start, slot_end))
        #             final_all_slots = [slot for slot in all_slots if slot not in hslots]
        #             print("channi")
        #             print(final_all_slots)
        #             print(len(final_all_slots))
        #             print("keshav")
        #
        #             existing_bookings = appointment_bookings.objects.filter(client_id=client_id,
        #                                                                     Consultant_settings_id=consult_id,
        #                                                                     date=date)
        #             print("gowda")
        #             print(existing_bookings)
        #             print("sekar")
        #
        #             booked_slots = set()
        #             for booking in existing_bookings:
        #                 start_time_str = booking.start_time.strftime("%H:%M")
        #                 end_time_str = booking.end_time.strftime("%H:%M")
        #                 booked_slots.add((start_time_str, end_time_str))
        #             print("vv")
        #             print(booked_slots)
        #             print("andhra")
        #             available_slots = [slot for slot in final_all_slots if slot not in booked_slots]
        #
        #             all_available_slots.append(available_slots)
        #         print("jill")
        #         print(all_available_slots)
        #         print("jiga")
        #         slot_data = all_available_slots[0]
        #         total_time_slots = len(slot_data)
        #
        #         list_all_data = []
        #         formatted_slots_details = []
        #         formatted_duration_details = []
        #         for slot_start, slot_end in slot_data:
        #             print(slot_start)
        #             print(slot_end)
        #             formatted_duation_create = f"{slot_start}-{slot_end}"
        #             formatted_slot_create = f"{slot_start}"
        #             date_formate_slot_create = datetime.strptime(formatted_slot_create, "%H:%M")
        #             formatted_start_time = date_formate_slot_create.strftime("%I:%M%p")
        #             formatted_slots_details.append(formatted_start_time)
        #             formatted_duration_details.append(formatted_duation_create)
        #
        #         for i in range(len(formatted_slots_details)):
        #             list_all_data.append({"id": "S" + str(consult_id) + "/" + str(
        #                 visitor_id) + "//" + str(finalDates[0]) + str(formatted_duration_details[i]) + str(i),
        #                                   "title": str(sub_dates[0]) + " " + str(formatted_slots_details[i])
        #
        #                                   })
        #
        #         print("correct")
        #         print(formatted_slots_details)
        #         response = {
        #             "version": "3.0",
        #             "screen": "SLOTS_DATA",
        #             "data": {
        #                 "options": list_all_data
        #
        #             }
        #         }
        #         return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')


        elif action_type == 'ping':
            print("s in appontement")

            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                    "status": "active"
                }
            }
            return HttpResponse(encrypt_response_check9(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check9(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIczQ3XnflVPACAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECB9CP6cT9tJJBIIEyL//SUFeHJbL
JcuW1cdsOCzkaTU04vVLh5QivW8BUYeHAbpz9gH8ILlZNZFl4xHmn1c15V6EcGNL
E7y7NG7N7JQIE1Wez93GX9vIh5cy6dtXA8PxwOiDQjujbuImNqz4okP5vnO/Iuha
eTmJ0/QEUCzI8Ipssn+UVVqcAw4BaY1A+eL0jlgwptTJhOg2hJt0zDegfSclyrVY
Ae8XCPOY8NN6OVPjX4MlyQYGFH5M6y9z2mS82KNTn/TiOffJpY4NGPSK7uUUIsJ0
slHza0Ss/fqWDIFaTNLjR69rKNw0aicIvdW2lFPALAYpbQdIPenzNJuyJX8X6mho
Q/Eyo4hjQkWPEAwWvlHgCCU/ebM2C49FA64VDnd81fHUqrH2kEH3Gn4ekI8uFQpF
ifo5X2T0WZV7pA8GNg3BL2KetWcnBqPyjbM+yVzn1RYCfB627s5JFYy1kwKZMQkZ
mmKcMm5UNFD0FAD7hMJG3xJHKptD8FL2L5LHSPKn1fSsPMS3fSYtVNqRRV3/xU0K
UtS/OzwJ1Ogar2ypAdhDC8A+tHIkD6+knrpHHiUuhRlcDjszyadjoQPBwvjNNz3F
CHfHmvo79vl5PvvxHIj/u+EPMKjReqyh9/3ZX/BTfBz4mPy7bVbxhNuQV1rK1Ruc
ZzxgufcekWcnjDKOJPeDa3bttCO1Is35xPuBFEtIc4vL8XxcikPQT1rmJEUL77u6
cjbE8cGo2rj+j+NAo5DHZQBtrelsIKqaGpnHT8T4KLBim3OXliuUUJwKEOKNNQhT
hvSfBemfKnMJYXrqx+pSQZnBCJOCqP56U4FbKhoQthj/5S6UwZrXLaWtR7DA/K9E
owqHwPb/ISIskvygsZPiDr9RoJ3V330dZcUe+ypeimmTcF+8QNfYWu4OhO5z8x5v
tHhwEXmamlYq5fnseU9vZh6tqn+qbx/Qqw+lby5ymYeWrNZtwrE4mxKGezQqYybW
sd+HSh5gqODx149b5e6Pl4WXCFb0mbqidf754bp+gLMWHu+V1twmnBTF+IzTPVTY
fuJgGzAGlQ1J5glXWUzfjQdUqwyU7eJjIK3sHSanMaagm/gdJqQ2lAKtR+gRawHt
/iVGyBtDhtgI1+gjm1ViVok56B6S4FCMlh6CypQvzGenqU9PVqdCYq93QKYcUdvo
YfHbmcbqTfgLCr0rxzejCUTOlC8ihQWlMQfNYUfWlTezw0FTPE9ueJk7QMhBSDDf
b3zeGw22HvDEHapq9T/ZbNv7/FhrFXG0PZeBq/BXLv5cjLs5JgB5/3t/g+eAnYGv
3s11OPX4AVB1kptujoNAvYa0yoo7RN0PHQetNaf5deL3r/bndcikB+fdcbiNymDe
RhLXAve3c6roAxhPDsBJPEhaAskBLZp3LWfVNpZEsBlQBfvP/kPwPvJbSBQbLRLf
vsrMaGZgGDcm7Tqpp/7exKDao/k23SGvrhVbKllX1EnGG9QB6A0+c3UFkKVULRnP
Rgo4HJGR84Z1PdjTdEF8MfskAT4bJ+/ywUap714JkBu2w+fP8C5j05WtwkQPpmuI
4Goei62rUpoWtinRYnsrZW4fc3ghXLqzWo8UYdlBkYrBUpSqaRiJslD0Oe0nssYd
nS/C7a9xctNeJ2kLu/wVWg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check9(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")


@csrf_exempt
def specificdata(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check10(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        ref_PhonenumberId = decrypted_data['flow_token']
        PhonenumberId = ref_PhonenumberId[:15]
        reference_id = ref_PhonenumberId[15:51]
        Search_ngo_id = ref_PhonenumberId[51:]
        print(Search_ngo_id)
        print(reference_id)
        print(action_type)
        print(PhonenumberId)
        facebook_objects = facebook_details.objects.filter(fb_phone_number_id=PhonenumberId)
        facebook_token = ''
        client_id = 0
        for tok in facebook_objects:
            facebook_token += tok.fb_access_token
            client_id += tok.client_id


        if action_type == 'INIT':
            # Return the next screen & data to the client
            print("s in data_exchange")
            dynamicInfo = donation_marketplace.objects.filter(client_id=client_id,ngo_id=Search_ngo_id)
            d_ngo_ID = 0
            for d_i in dynamicInfo:
                d_ngo_ID = d_i.id

            donation_name = []
            donation_desc = []
            donation_id = []
            listdonation = donation_types.objects.filter(client_id=client_id, marketplace_id=d_ngo_ID)
            print("bulbul")
            print(listdonation)
            for list_i in listdonation:
                print(list_i.id)
                donation_id.append(list_i.id)
                donation_desc.append(list_i.donation_short_description)
                donation_name.append(list_i.donation_name)
            print(donation_name)
            donationlist = []
            for i in range(len(donation_name)):
                donationlist.append({"id": "M" + str(donation_id[i]),
                                     "title": donation_name[i],
                                     "description": donation_desc[i]
                                     })
            donation_setting_Image = donation_settings.objects.filter(client_id=client_id)
            d_image = ''
            for d in donation_setting_Image:
                d_image = d.donation_image  # Assuming this is an ImageFieldFile object
            print(d_image)

            # Open the image file using the ImageFieldFile object
            with d_image.open(mode='rb') as image_file:
                image_content = image_file.read()

            # Convert the image content to base64
            encoded_string = base64.b64encode(image_content).decode('utf-8')

            # 'encoded_string' now contains the base64 representation of the image
            print(encoded_string)
            print(d_image)
            response = {
                "version": "3.0",
                "screen": "DONATION_TYPES",
                "data": {
                    "details": encoded_string,
                    "options": donationlist
                }
            }

            # Return the response as plaintext
            return HttpResponse(encrypt_response_check10(response, aes_key, iv), content_type='text/plain')
        elif action_type == 'data_exchange':
            Screen_name = decrypted_data['screen']
            if Screen_name == 'DONATION_TYPES':
                data = decrypted_data['data']['options']
                donation_ID = data[1:]
                donation_dettails_obj = donation_types.objects.filter(client_id=client_id,id=donation_ID)
                donation_Amount = 0
                donation_Name = ''
                d_image = ''
                for d_i in donation_dettails_obj:
                    donation_Amount = d_i.donation_amount
                    donation_Name = d_i.donation_name
                    d_image = d_i.donation_type_image

                with d_image.open(mode='rb') as image_file:
                    image_content = image_file.read()

                # Convert the image content to base64
                encoded_string = base64.b64encode(image_content).decode('utf-8')

                # 'encoded_string' now contains the base64 representation of the image
                print(encoded_string)
                print(d_image)

                if donation_Amount == 0:
                    print("zero")
                    response = {
                        "version": "3.0",
                        "screen": "DONATION_DETAILS",
                        "data":{
                            "details": encoded_string,
                            "excess": [{
                                "id": str(donation_ID),
                                "title": str(donation_Name)
                            }],
                        }
                    }
                    return HttpResponse(encrypt_response_check10(response, aes_key, iv), content_type='text/plain')

                else:
                    print("no zero")

                    response = {
                        "version": "3.0",
                        "screen": "SUBMIT_DETAILS_DATA",
                        "data": {
                            "details": encoded_string,
                            "excess": [{

                                "id":str(donation_ID),
                                "title":str(donation_Name)
                            }],
                             "total": "₹"+ str(donation_Amount)+" "+str(donation_Name)
                        }
                    }
                    return HttpResponse(encrypt_response_check10(response, aes_key, iv), content_type='text/plain')

        elif action_type == 'ping':

            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                    "status": "active"
                }
            }
            return HttpResponse(encrypt_response_check10(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check10(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIczQ3XnflVPACAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECB9CP6cT9tJJBIIEyL//SUFeHJbL
JcuW1cdsOCzkaTU04vVLh5QivW8BUYeHAbpz9gH8ILlZNZFl4xHmn1c15V6EcGNL
E7y7NG7N7JQIE1Wez93GX9vIh5cy6dtXA8PxwOiDQjujbuImNqz4okP5vnO/Iuha
eTmJ0/QEUCzI8Ipssn+UVVqcAw4BaY1A+eL0jlgwptTJhOg2hJt0zDegfSclyrVY
Ae8XCPOY8NN6OVPjX4MlyQYGFH5M6y9z2mS82KNTn/TiOffJpY4NGPSK7uUUIsJ0
slHza0Ss/fqWDIFaTNLjR69rKNw0aicIvdW2lFPALAYpbQdIPenzNJuyJX8X6mho
Q/Eyo4hjQkWPEAwWvlHgCCU/ebM2C49FA64VDnd81fHUqrH2kEH3Gn4ekI8uFQpF
ifo5X2T0WZV7pA8GNg3BL2KetWcnBqPyjbM+yVzn1RYCfB627s5JFYy1kwKZMQkZ
mmKcMm5UNFD0FAD7hMJG3xJHKptD8FL2L5LHSPKn1fSsPMS3fSYtVNqRRV3/xU0K
UtS/OzwJ1Ogar2ypAdhDC8A+tHIkD6+knrpHHiUuhRlcDjszyadjoQPBwvjNNz3F
CHfHmvo79vl5PvvxHIj/u+EPMKjReqyh9/3ZX/BTfBz4mPy7bVbxhNuQV1rK1Ruc
ZzxgufcekWcnjDKOJPeDa3bttCO1Is35xPuBFEtIc4vL8XxcikPQT1rmJEUL77u6
cjbE8cGo2rj+j+NAo5DHZQBtrelsIKqaGpnHT8T4KLBim3OXliuUUJwKEOKNNQhT
hvSfBemfKnMJYXrqx+pSQZnBCJOCqP56U4FbKhoQthj/5S6UwZrXLaWtR7DA/K9E
owqHwPb/ISIskvygsZPiDr9RoJ3V330dZcUe+ypeimmTcF+8QNfYWu4OhO5z8x5v
tHhwEXmamlYq5fnseU9vZh6tqn+qbx/Qqw+lby5ymYeWrNZtwrE4mxKGezQqYybW
sd+HSh5gqODx149b5e6Pl4WXCFb0mbqidf754bp+gLMWHu+V1twmnBTF+IzTPVTY
fuJgGzAGlQ1J5glXWUzfjQdUqwyU7eJjIK3sHSanMaagm/gdJqQ2lAKtR+gRawHt
/iVGyBtDhtgI1+gjm1ViVok56B6S4FCMlh6CypQvzGenqU9PVqdCYq93QKYcUdvo
YfHbmcbqTfgLCr0rxzejCUTOlC8ihQWlMQfNYUfWlTezw0FTPE9ueJk7QMhBSDDf
b3zeGw22HvDEHapq9T/ZbNv7/FhrFXG0PZeBq/BXLv5cjLs5JgB5/3t/g+eAnYGv
3s11OPX4AVB1kptujoNAvYa0yoo7RN0PHQetNaf5deL3r/bndcikB+fdcbiNymDe
RhLXAve3c6roAxhPDsBJPEhaAskBLZp3LWfVNpZEsBlQBfvP/kPwPvJbSBQbLRLf
vsrMaGZgGDcm7Tqpp/7exKDao/k23SGvrhVbKllX1EnGG9QB6A0+c3UFkKVULRnP
Rgo4HJGR84Z1PdjTdEF8MfskAT4bJ+/ywUap714JkBu2w+fP8C5j05WtwkQPpmuI
4Goei62rUpoWtinRYnsrZW4fc3ghXLqzWo8UYdlBkYrBUpSqaRiJslD0Oe0nssYd
nS/C7a9xctNeJ2kLu/wVWg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check10(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")


@csrf_exempt
def specificapptdata(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check11(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        ref_PhonenumberId = decrypted_data['flow_token']
        PhonenumberId = ref_PhonenumberId[:15]
        toUser = ref_PhonenumberId[15:27]
        Search_ngo_id = ref_PhonenumberId[27:]
        print(Search_ngo_id)
        print(action_type)
        print(PhonenumberId)
        facebook_objects = facebook_details.objects.filter(fb_phone_number_id=PhonenumberId)
        facebook_token = ''
        client_id = 0
        for tok in facebook_objects:
            facebook_token += tok.fb_access_token
            client_id += tok.client_id


        if action_type == 'INIT':
            # Return the next screen & data to the client
            print("s in data_exchange")
            dynamicInfo = appointment_marketplace.objects.filter(client_id=client_id,group_id=Search_ngo_id)
            d_ngo_ID = 0
            for d_i in dynamicInfo:
                d_ngo_ID = d_i.id

            consultant_name = []
            consultant_specialization = []
            consultant_id = []
            consultantDetails = Consultant_details.objects.filter(client_id=client_id, marketplace_id=d_ngo_ID)
            for c_i in consultantDetails:
                consultant_id.append(c_i.id)
                consultant_name.append(c_i.consultant_name)
                consultant_specialization.append(c_i.consultant_specialization)
            consultantlist = []
            for i in range(len(consultant_name)):
                consultantlist.append({"id": "N" + str(consultant_id[i]),
                                       "title": consultant_name[i],
                                       "description": consultant_specialization[i]
                                       })
            dynamicImage = appointment_marketplace.objects.filter(client_id=client_id, group_id=Search_ngo_id)
            d_image = ''
            for d_i in dynamicImage:
                settingImage = appointment_settings.objects.filter(client_id=client_id,marketplace_id=d_i.id)
                for s in settingImage:
                    d_image = s.welcome_image

            with d_image.open(mode='rb') as image_file:
                image_content = image_file.read()

            # Convert the image content to base64
            encoded_string = base64.b64encode(image_content).decode('utf-8')

            # 'encoded_string' now contains the base64 representation of the image
            print(encoded_string)
            file_path = 'C:/Vailo/18-12-2023 updated Dashboard/A_vMart/A_vMart/encoded_image12.txt'

            # Write the encoded string to a text file
            with open(file_path, 'w') as text_file:
                text_file.write(encoded_string)

            print(f"Encoded string saved at: {file_path}")
            print(d_image)

            response = {
                "version": "3.0",
                "screen": "DOCTORS_DATA",
                "data": {
                    "details": encoded_string,
                    "options": consultantlist
                }
            }


            # Return the response as plaintext
            return HttpResponse(encrypt_response_check11(response, aes_key, iv), content_type='text/plain')
        elif action_type == 'data_exchange':
            Screen_name = decrypted_data['screen']
            if Screen_name == 'DOCTORS_DATA':
                data = decrypted_data['data']['options']
                response_id_id = data[1:]
                import datetime as dt

                current_date = dt.datetime.now().date()

                current_date += dt.timedelta(days=1)

                dates = []

                for i in range(60):
                    new_date = current_date + dt.timedelta(days=i)
                    dates.append(new_date)
                print(dates)

                a = 0
                day_of_week = 0
                ex_date = []
                only_dates = []
                formateed_dates = []
                all_available_slots = []
                consultantName = ''
                consultantSpecialization = ''
                for i, date in enumerate(dates, start=ord('a')):
                    print("jinja")
                    print(date)
                    print("lalli")
                    ex_date.append(date)
                    zformatted_date = date.strftime('%d-%b %a')
                    # formatted_date = zformatted_date[:6] + zformatted_date[-5:]
                    # print(formatted_date)
                    formateed_dates.append(zformatted_date)
                    only_date = date.strftime('%d-%m-%Y')
                    only_dates.append(only_date)
                    day_of_week = int(date.strftime('%w'))
                    variable_name = chr(i)
                    print(f"{variable_name} = {zformatted_date} {day_of_week}")
                    print(formateed_dates)

                    duration = None  # Initialize to None or an appropriate default value

                    slotDuration = Consultant_details.objects.filter(client_id=client_id, id=response_id_id)
                    for s_i in slotDuration:
                        duration_str = s_i.slot_duration
                        consultantName = s_i.consultant_name
                        consultantSpecialization = s_i.consultant_specialization
                        numeric_part = int(''.join(filter(str.isdigit, duration_str)))
                        duration = numeric_part

                    hslots = []
                    not_available_slot = []
                    holidayDetails = Consultant_holiday_leaves.objects.filter(client_id=client_id, date=date)
                    for h_i in holidayDetails:
                        not_available_slots = {
                            "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
                            "end_time": h_i.end_time.strftime("%H:%M"),
                        }
                        not_available_slot.append(not_available_slots)

                    for record in not_available_slot:
                        start_time_str1 = record["start_time"]
                        end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format

                        record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
                        record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
                        current_time1 = record_start_time1
                        while current_time1 < record_end_time2:
                            slot_start = current_time1.strftime("%H:%M")
                            current_time1 += timedelta(minutes=duration)
                            slot_end = current_time1.strftime("%H:%M")
                            hslots.append((slot_start, slot_end))
                    print("aa")
                    print(hslots)
                    print("bb")

                    all_slots = []
                    availability_records = []

                    availablityObject = Consultant_availablity.objects.filter(client_id=client_id,
                                                                              Consultant_settings_id=response_id_id,
                                                                              day_of_week=day_of_week)
                    print(availablityObject)
                    for a_i in availablityObject:
                        print(a_i.id)
                        availability_record = {
                            "start_time": a_i.start_time.strftime("%H:%M"),
                            "end_time": a_i.end_time.strftime("%H:%M"),
                        }
                        # print(availability_record)
                        # print("mohan")
                        availability_records.append(availability_record)

                    for record in availability_records:
                        start_time_str = record["start_time"]
                        end_time_str = record["end_time"]

                        record_start_time = datetime.strptime(start_time_str, "%H:%M")
                        record_end_time = datetime.strptime(end_time_str, "%H:%M")
                        current_time = record_start_time

                        while current_time < record_end_time:
                            slot_start = current_time.strftime("%H:%M")
                            current_time += timedelta(minutes=duration)
                            slot_end = current_time.strftime("%H:%M")
                            all_slots.append((slot_start, slot_end))
                    final_all_slots = [slot for slot in all_slots if slot not in hslots]
                    print("channi")
                    print(final_all_slots)
                    print(len(final_all_slots))
                    print("keshav")

                    # bookingObject = Bookings.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
                    #                                         date=current_date)
                    # booked_slots = set(booking.notes1 for booking in bookingObject)
                    # available_slots = [slot for slot in final_all_slots if slot not in booked_slots]

                    existing_bookings = appointment_bookings.objects.filter(client_id=client_id,
                                                                            Consultant_settings_id=response_id_id,
                                                                            date=date)
                    print("gowda")
                    print(existing_bookings)
                    print("sekar")

                    booked_slots = set()
                    for booking in existing_bookings:
                        start_time_str = booking.start_time.strftime("%H:%M")
                        end_time_str = booking.end_time.strftime("%H:%M")
                        booked_slots.add((start_time_str, end_time_str))
                    print("vv")
                    print(booked_slots)
                    print("andhra")
                    available_slots = [slot for slot in final_all_slots if slot not in booked_slots]

                    all_available_slots.append(available_slots)
                    print("guna")
                    print(all_available_slots)
                    print("shouya")

                    # a=len(available_slots)
                    # print(a)
                    # print(available_slots)
                    # print(type(available_slots))
                    # print("done very good job")

                # first_position = len(all_available_slots[0])
                # second_position = len(all_available_slots[1])
                # third_position = len(all_available_slots[2])
                # fourth_position = len(all_available_slots[3])
                # fifth_position = len(all_available_slots[4])
                # six_position = len(all_available_slots[5])
                # seventh_position = len(all_available_slots[6])
                # print(seventh_position)

                len_all_slots = []

                for i, date in enumerate(ex_date):
                    avlslots = len(all_available_slots[i])
                    formateedDate = ''
                    if avlslots != 0 and avlslots <= 10:
                        formateedDate = date.strftime('%d %b %a')
                        len_all_slots.append((i, date, avlslots, formateedDate))
                    else:
                        print(f"No slots available for {formateedDate}")

                # Now len_all_slots contains tuples of (formatted_date, avlslots)
                print(len_all_slots)
                print("burger")

                show_avl_slots = []
                show_date = []
                total_avl_slots = 0
                for j, (i, date, avlslots, formateedDate) in enumerate(len_all_slots[:8]):
                    show_date.append(date)
                    total_avl_slots += avlslots
                    title = f"{formateedDate} ({avlslots} slots)"
                    show_avl_slots.append({"id": "K" + str(response_id_id) + "/" + str(date),
                                           "title": title

                                           })
                Consultant_Image = Consultant_details.objects.filter(client_id=client_id, id=response_id_id)
                consultant_image = ''
                for c_i in Consultant_Image:
                    consultant_image = c_i.consultant_image

                with consultant_image.open(mode='rb') as image_file:
                    image_content = image_file.read()

                # Convert the image content to base64
                encoded_string = base64.b64encode(image_content).decode('utf-8')

                # 'encoded_string' now contains the base64 representation of the image
                print(encoded_string)
                file_path = 'C:/Vailo/18-12-2023 updated Dashboard/A_vMart/A_vMart/encoded_image23.txt'

                # Write the encoded string to a text file
                with open(file_path, 'w') as text_file:
                    text_file.write(encoded_string)

                print(f"Encoded string saved at: {file_path}")
                print(consultant_image)
                print(show_avl_slots)
                first_date = show_date[0]
                last_date = show_date[-1]
                print('bomma')
                print(first_date)
                print(last_date)
                print("borusu")
                print(consultant_image)
                response = {
                    "version": "3.0",
                    "screen": "DATES_DATA",
                    "data": {
                        "details": encoded_string,
                        "options": show_avl_slots

                    }
                }
                return HttpResponse(encrypt_response_check11(response, aes_key, iv), content_type='text/plain')
            elif Screen_name == 'DATES_DATA':
                response_id = decrypted_data['data']['options']
                print("tipelinganna")
                print(response_id)
                slash_index = response_id.index('/')

                date = []
                dates = response_id[slash_index + 1:]
                print("jayamma")
                print(dates)
                print("jayanna")
                dates_new = datetime.strptime(str(dates), '%Y-%m-%d')
                date.append(dates_new)

                consult_id = response_id[1:slash_index]
                print("nagamma")
                print(consult_id)
                print("nagaraj")

                customer = appointment_visitor.objects.filter(client_id=client_id,
                                                              Visitor_Whatsapp_Number=toUser).first()
                visitor_id = 0
                if customer:
                    visitor_id = customer.id

                # import datetime as dt
                #
                # current_date = dt.datetime.now().date()
                #
                # current_date += dt.timedelta(days=1)
                #
                # dates = []
                #
                # for i in range(7):
                #     new_date = current_date + dt.timedelta(days=i)
                #     dates.append(new_date)
                # print(dates)

                a = 0
                day_of_week = 0
                only_dates = []
                sub_dates = []
                finalDates = []
                formateed_dates = []
                all_available_slots = []
                consultantName = ''
                consultantSpecialization = ''
                for i, date in enumerate(date, start=ord('a')):
                    zformatted_date = date.strftime('%d/%B/%Y %A')
                    sub_date = date.strftime('%d %b %a')
                    sub_dates.append(sub_date)
                    formatted_date = zformatted_date[:6] + zformatted_date[12:]
                    print(formatted_date)
                    formateed_dates.append(formatted_date)
                    only_date = date.strftime('%d-%m-%Y')
                    final_only_date = only_date.replace("-", "")
                    finalDates.append(final_only_date)
                    day_of_week = int(date.strftime('%w'))
                    variable_name = chr(i)
                    print(f"{variable_name} = {formatted_date} {day_of_week}")
                    print(formateed_dates)

                    duration = None  # Initialize to None or an appropriate default value
                    slotDuration = Consultant_details.objects.filter(client_id=client_id, id=consult_id)
                    for s_i in slotDuration:
                        duration_str = s_i.slot_duration
                        consultantName = s_i.consultant_name
                        consultantSpecialization = s_i.consultant_specialization
                        numeric_part = int(''.join(filter(str.isdigit, duration_str)))
                        duration = numeric_part

                    hslots = []
                    not_available_slot = []
                    holidayDetails = Consultant_holiday_leaves.objects.filter(client_id=client_id, date=date)
                    for h_i in holidayDetails:
                        not_available_slots = {
                            "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
                            "end_time": h_i.end_time.strftime("%H:%M"),
                        }
                        not_available_slot.append(not_available_slots)

                    for record in not_available_slot:
                        start_time_str1 = record["start_time"]
                        end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format

                        record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
                        record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
                        current_time1 = record_start_time1
                        while current_time1 < record_end_time2:
                            slot_start = current_time1.strftime("%H:%M")
                            current_time1 += timedelta(minutes=duration)
                            slot_end = current_time1.strftime("%H:%M")
                            hslots.append((slot_start, slot_end))
                    print("aa")
                    print(hslots)
                    print("bb")

                    all_slots = []
                    availability_records = []

                    availablityObject = Consultant_availablity.objects.filter(client_id=client_id,
                                                                              Consultant_settings_id=consult_id,
                                                                              day_of_week=day_of_week)
                    print(availablityObject)
                    for a_i in availablityObject:
                        print(a_i.id)
                        availability_record = {
                            "start_time": a_i.start_time.strftime("%H:%M"),
                            "end_time": a_i.end_time.strftime("%H:%M"),
                        }
                        print(availability_record)
                        print("mohan")
                        availability_records.append(availability_record)

                    for record in availability_records:
                        start_time_str = record["start_time"]
                        end_time_str = record["end_time"]

                        record_start_time = datetime.strptime(start_time_str, "%H:%M")
                        record_end_time = datetime.strptime(end_time_str, "%H:%M")
                        current_time = record_start_time

                        while current_time < record_end_time:
                            slot_start = current_time.strftime("%H:%M")
                            current_time += timedelta(minutes=duration)
                            slot_end = current_time.strftime("%H:%M")
                            all_slots.append((slot_start, slot_end))
                    final_all_slots = [slot for slot in all_slots if slot not in hslots]
                    print("channi")
                    print(final_all_slots)
                    print(len(final_all_slots))
                    print("keshav")

                    existing_bookings = appointment_bookings.objects.filter(client_id=client_id,
                                                                            Consultant_settings_id=consult_id,
                                                                            date=date)
                    print("gowda")
                    print(existing_bookings)
                    print("sekar")

                    booked_slots = set()
                    for booking in existing_bookings:
                        start_time_str = booking.start_time.strftime("%H:%M")
                        end_time_str = booking.end_time.strftime("%H:%M")
                        booked_slots.add((start_time_str, end_time_str))
                    print("vv")
                    print(booked_slots)
                    print("andhra")
                    available_slots = [slot for slot in final_all_slots if slot not in booked_slots]

                    all_available_slots.append(available_slots)
                print("jill")
                print(all_available_slots)
                print("jiga")
                slot_data = all_available_slots[0]
                total_time_slots = len(slot_data)

                list_all_data = []
                formatted_slots_details = []
                formatted_duration_details = []
                for slot_start, slot_end in slot_data:
                    print(slot_start)
                    print(slot_end)
                    formatted_duation_create = f"{slot_start}-{slot_end}"
                    formatted_slot_create = f"{slot_start}"
                    date_formate_slot_create = datetime.strptime(formatted_slot_create, "%H:%M")
                    formatted_start_time = date_formate_slot_create.strftime("%I:%M%p")
                    formatted_slots_details.append(formatted_start_time)
                    formatted_duration_details.append(formatted_duation_create)

                for i in range(len(formatted_slots_details)):
                    list_all_data.append({"id": "S" + str(consult_id) + "/" + str(
                        visitor_id) + "//" + str(finalDates[0]) + str(formatted_duration_details[i]) + str(i),
                                          "title": str(sub_dates[0]) + " " + str(formatted_slots_details[i])

                                          })

                print("correct")
                print(formatted_slots_details)
                response = {
                    "version": "3.0",
                    "screen": "SLOTS_DATA",
                    "data": {
                        "options": list_all_data

                    }
                }
                return HttpResponse(encrypt_response_check11(response, aes_key, iv), content_type='text/plain')



        elif action_type == 'ping':

            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                    "status": "active"
                }
            }
            return HttpResponse(encrypt_response_check11(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check11(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIczQ3XnflVPACAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECB9CP6cT9tJJBIIEyL//SUFeHJbL
JcuW1cdsOCzkaTU04vVLh5QivW8BUYeHAbpz9gH8ILlZNZFl4xHmn1c15V6EcGNL
E7y7NG7N7JQIE1Wez93GX9vIh5cy6dtXA8PxwOiDQjujbuImNqz4okP5vnO/Iuha
eTmJ0/QEUCzI8Ipssn+UVVqcAw4BaY1A+eL0jlgwptTJhOg2hJt0zDegfSclyrVY
Ae8XCPOY8NN6OVPjX4MlyQYGFH5M6y9z2mS82KNTn/TiOffJpY4NGPSK7uUUIsJ0
slHza0Ss/fqWDIFaTNLjR69rKNw0aicIvdW2lFPALAYpbQdIPenzNJuyJX8X6mho
Q/Eyo4hjQkWPEAwWvlHgCCU/ebM2C49FA64VDnd81fHUqrH2kEH3Gn4ekI8uFQpF
ifo5X2T0WZV7pA8GNg3BL2KetWcnBqPyjbM+yVzn1RYCfB627s5JFYy1kwKZMQkZ
mmKcMm5UNFD0FAD7hMJG3xJHKptD8FL2L5LHSPKn1fSsPMS3fSYtVNqRRV3/xU0K
UtS/OzwJ1Ogar2ypAdhDC8A+tHIkD6+knrpHHiUuhRlcDjszyadjoQPBwvjNNz3F
CHfHmvo79vl5PvvxHIj/u+EPMKjReqyh9/3ZX/BTfBz4mPy7bVbxhNuQV1rK1Ruc
ZzxgufcekWcnjDKOJPeDa3bttCO1Is35xPuBFEtIc4vL8XxcikPQT1rmJEUL77u6
cjbE8cGo2rj+j+NAo5DHZQBtrelsIKqaGpnHT8T4KLBim3OXliuUUJwKEOKNNQhT
hvSfBemfKnMJYXrqx+pSQZnBCJOCqP56U4FbKhoQthj/5S6UwZrXLaWtR7DA/K9E
owqHwPb/ISIskvygsZPiDr9RoJ3V330dZcUe+ypeimmTcF+8QNfYWu4OhO5z8x5v
tHhwEXmamlYq5fnseU9vZh6tqn+qbx/Qqw+lby5ymYeWrNZtwrE4mxKGezQqYybW
sd+HSh5gqODx149b5e6Pl4WXCFb0mbqidf754bp+gLMWHu+V1twmnBTF+IzTPVTY
fuJgGzAGlQ1J5glXWUzfjQdUqwyU7eJjIK3sHSanMaagm/gdJqQ2lAKtR+gRawHt
/iVGyBtDhtgI1+gjm1ViVok56B6S4FCMlh6CypQvzGenqU9PVqdCYq93QKYcUdvo
YfHbmcbqTfgLCr0rxzejCUTOlC8ihQWlMQfNYUfWlTezw0FTPE9ueJk7QMhBSDDf
b3zeGw22HvDEHapq9T/ZbNv7/FhrFXG0PZeBq/BXLv5cjLs5JgB5/3t/g+eAnYGv
3s11OPX4AVB1kptujoNAvYa0yoo7RN0PHQetNaf5deL3r/bndcikB+fdcbiNymDe
RhLXAve3c6roAxhPDsBJPEhaAskBLZp3LWfVNpZEsBlQBfvP/kPwPvJbSBQbLRLf
vsrMaGZgGDcm7Tqpp/7exKDao/k23SGvrhVbKllX1EnGG9QB6A0+c3UFkKVULRnP
Rgo4HJGR84Z1PdjTdEF8MfskAT4bJ+/ywUap714JkBu2w+fP8C5j05WtwkQPpmuI
4Goei62rUpoWtinRYnsrZW4fc3ghXLqzWo8UYdlBkYrBUpSqaRiJslD0Oe0nssYd
nS/C7a9xctNeJ2kLu/wVWg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check11(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")



@csrf_exempt
def myappointmentdata(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check12(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        PhonenumberId = decrypted_data['flow_token']
        ref_PhonenumberId = PhonenumberId[:15]
        toUser = PhonenumberId[15:]
        # print(reference_id)
        # print(action_type)
        print(ref_PhonenumberId)
        facebook_objects = facebook_details.objects.filter(fb_phone_number_id=ref_PhonenumberId)
        facebook_token = ''
        client_id = 0
        for tok in facebook_objects:
            facebook_token += tok.fb_access_token
            client_id += tok.client_id


        if action_type == 'INIT':
            # Return the next screen & data to the client
            print("s in INIT")
            appt_details = appointment_bookings.objects.filter(client_id=client_id,customer_phone_number=toUser)
            if appt_details:
                print(appt_details)
                a_date = []
                consultant_ID = []
                consultantName = []
                for a in appt_details:
                    a_date.append(a.date)
                    bookingObj = Consultant_details.objects.filter(id=a.Consultant_settings_id)
                    for d_i in bookingObj:
                        consultant_ID.append(d_i.id)
                        consultantName.append(d_i.consultant_name)
                print(consultant_ID)

                All_Appointements = []
                for i in range(len(consultantName)):
                    All_Appointements.append({
                        "id":str(consultant_ID[i]),
                        "title":consultantName[i],
                        "description":a_date[i].strftime("%Y-%m-%d")
                    })

                response = {
                    "version": decrypted_data['version'],
                    "screen": "MYAPOOINTMENT_DETAILS",
                    "data": {
                        "details":"Your Appointements",
                        "options": All_Appointements

                    }
                }

                # Return the response as plaintext
                return HttpResponse(encrypt_response_check12(response, aes_key, iv), content_type='text/plain')
            else:
                print("s no donations")
                response = {
                    "version": decrypted_data['version'],
                    "screen": "MYDONATION_DETAILS",
                    "data": {
                        "details": "You have no donations.Please donate.",
                        "options":[{
                            "id":"No records",
                            "title":"No records"
                        }]

                    }
                }

                # Return the response as plaintext
                return HttpResponse(encrypt_response_check12(response, aes_key, iv), content_type='text/plain')


        # elif action_type == 'data_exchange':
        #     Screen_name = decrypted_data['screen']
        #     if Screen_name == 'DETAILS':
        #         response_data = decrypted_data['data']
        #         print(response_data)
        #         print("delhi")
        #         if any(key in response_data for key in ['group_Name', 'group_location', 'group_category', 'group_type']):
        #             print("You are searching for Hospital details. Please wait while it updates.")
        #
        #             keys_to_check = ['group_Name', 'group_location', 'group_category', 'group_type']
        #             filters = {}
        #
        #             # Mapping keys to corresponding model column names
        #             column_mapping = {
        #                 'group_Name': 'group_name',
        #                 'group_location': 'group_location',
        #                 'group_category': 'group_category',
        #                 'group_type': 'group_type'
        #             }
        #
        #             for key in keys_to_check:
        #                 value = response_data.get(key)
        #                 if value:
        #                     db_column_name = column_mapping.get(key)
        #                     filters[f'{db_column_name}__icontains'] = value
        #
        #             # facebook_objects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
        #             # facebook_token = ''
        #             # client_id = 0
        #             #
        #             # for tok in facebook_objects:
        #             #     facebook_token += tok.fb_access_token
        #             #     client_id += tok.client_id
        #
        #             # url = f"https://graph.facebook.com/v12.0/{whatsAppPhoneNumberId}/messages"
        #             # headers = {
        #             #     'Authorization': 'Bearer ' + facebook_token,
        #             #     'Content-Type': 'application/json'
        #             # }
        #
        #             # Using Q objects to dynamically construct the query
        #             query = Q(client_id=client_id)
        #             for key, value in filters.items():
        #                 query &= Q(**{key: value})
        #
        #             # Apply the constructed query to the donation_marketplace model
        #             appointementObj = appointment_marketplace.objects.filter(query)
        #             print("jodi")
        #             print(appointementObj)
        #
        #             Group_Name = []
        #             Group_location = []
        #             Group_id = []
        #
        #             if appointementObj:
        #                 for l_i in appointementObj:
        #                     Group_id.append(l_i.id)
        #                     Group_Name.append(l_i.group_name)
        #                     Group_location.append(l_i.group_location)
        #
        #                 Group_list = [{"id": "A" + str(Group_id[i]),
        #                              "title": Group_Name[i],
        #                              "description": Group_location[i]}
        #                             for i in range(len(Group_Name))]
        #                 response = {
        #                     "version": "3.0",
        #                     "screen": "HOSPITAL_DATA",
        #                     "data": {
        #                         "options": Group_list
        #                     }
        #                 }
        #                 return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')
        #     elif Screen_name == 'HOSPITAL_DATA':
        #         data = decrypted_data['data']['options']
        #         appt_ID = data[1:]
        #         consultant_name = []
        #         consultant_specialization = []
        #         consultant_id = []
        #         consultantDetails = Consultant_details.objects.filter(client_id=client_id,marketplace_id=appt_ID)
        #         for c_i in consultantDetails:
        #             consultant_id.append(c_i.id)
        #             consultant_name.append(c_i.consultant_name)
        #             consultant_specialization.append(c_i.consultant_specialization)
        #         consultantlist = []
        #         for i in range(len(consultant_name)):
        #             consultantlist.append({"id": "N" + str(consultant_id[i]),
        #                                    "title": consultant_name[i],
        #                                    "description": consultant_specialization[i]
        #                                    })
        #         response = {
        #             "version": "3.0",
        #             "screen": "DOCTORS_DATA",
        #             "data": {
        #                 "options": consultantlist
        #             }
        #         }
        #         return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')
        #     elif Screen_name == 'DOCTORS_DATA':
        #         data = decrypted_data['data']['options']
        #         response_id_id = data[1:]
        #         import datetime as dt
        #
        #         current_date = dt.datetime.now().date()
        #
        #         current_date += dt.timedelta(days=1)
        #
        #         dates = []
        #
        #         for i in range(60):
        #             new_date = current_date + dt.timedelta(days=i)
        #             dates.append(new_date)
        #         print(dates)
        #
        #         a = 0
        #         day_of_week = 0
        #         ex_date = []
        #         only_dates = []
        #         formateed_dates = []
        #         all_available_slots = []
        #         consultantName = ''
        #         consultantSpecialization = ''
        #         for i, date in enumerate(dates, start=ord('a')):
        #             print("jinja")
        #             print(date)
        #             print("lalli")
        #             ex_date.append(date)
        #             zformatted_date = date.strftime('%d-%b %a')
        #             # formatted_date = zformatted_date[:6] + zformatted_date[-5:]
        #             # print(formatted_date)
        #             formateed_dates.append(zformatted_date)
        #             only_date = date.strftime('%d-%m-%Y')
        #             only_dates.append(only_date)
        #             day_of_week = int(date.strftime('%w'))
        #             variable_name = chr(i)
        #             print(f"{variable_name} = {zformatted_date} {day_of_week}")
        #             print(formateed_dates)
        #
        #             duration = None  # Initialize to None or an appropriate default value
        #
        #             slotDuration = Consultant_details.objects.filter(client_id=client_id, id=response_id_id)
        #             for s_i in slotDuration:
        #                 duration_str = s_i.slot_duration
        #                 consultantName = s_i.consultant_name
        #                 consultantSpecialization = s_i.consultant_specialization
        #                 numeric_part = int(''.join(filter(str.isdigit, duration_str)))
        #                 duration = numeric_part
        #
        #             hslots = []
        #             not_available_slot = []
        #             holidayDetails = Consultant_holiday_leaves.objects.filter(client_id=client_id, date=date)
        #             for h_i in holidayDetails:
        #                 not_available_slots = {
        #                     "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
        #                     "end_time": h_i.end_time.strftime("%H:%M"),
        #                 }
        #                 not_available_slot.append(not_available_slots)
        #
        #             for record in not_available_slot:
        #                 start_time_str1 = record["start_time"]
        #                 end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format
        #
        #                 record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
        #                 record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
        #                 current_time1 = record_start_time1
        #                 while current_time1 < record_end_time2:
        #                     slot_start = current_time1.strftime("%H:%M")
        #                     current_time1 += timedelta(minutes=duration)
        #                     slot_end = current_time1.strftime("%H:%M")
        #                     hslots.append((slot_start, slot_end))
        #             print("aa")
        #             print(hslots)
        #             print("bb")
        #
        #             all_slots = []
        #             availability_records = []
        #
        #             availablityObject = Consultant_availablity.objects.filter(client_id=client_id,
        #                                                                       Consultant_settings_id=response_id_id,
        #                                                                       day_of_week=day_of_week)
        #             print(availablityObject)
        #             for a_i in availablityObject:
        #                 print(a_i.id)
        #                 availability_record = {
        #                     "start_time": a_i.start_time.strftime("%H:%M"),
        #                     "end_time": a_i.end_time.strftime("%H:%M"),
        #                 }
        #                 # print(availability_record)
        #                 # print("mohan")
        #                 availability_records.append(availability_record)
        #
        #             for record in availability_records:
        #                 start_time_str = record["start_time"]
        #                 end_time_str = record["end_time"]
        #
        #                 record_start_time = datetime.strptime(start_time_str, "%H:%M")
        #                 record_end_time = datetime.strptime(end_time_str, "%H:%M")
        #                 current_time = record_start_time
        #
        #                 while current_time < record_end_time:
        #                     slot_start = current_time.strftime("%H:%M")
        #                     current_time += timedelta(minutes=duration)
        #                     slot_end = current_time.strftime("%H:%M")
        #                     all_slots.append((slot_start, slot_end))
        #             final_all_slots = [slot for slot in all_slots if slot not in hslots]
        #             print("channi")
        #             print(final_all_slots)
        #             print(len(final_all_slots))
        #             print("keshav")
        #
        #             # bookingObject = Bookings.objects.filter(client_id=clientId, Consultant_settings_id=response_id_id,
        #             #                                         date=current_date)
        #             # booked_slots = set(booking.notes1 for booking in bookingObject)
        #             # available_slots = [slot for slot in final_all_slots if slot not in booked_slots]
        #
        #             existing_bookings = appointment_bookings.objects.filter(client_id=client_id,
        #                                                                     Consultant_settings_id=response_id_id,
        #                                                                     date=date)
        #             print("gowda")
        #             print(existing_bookings)
        #             print("sekar")
        #
        #             booked_slots = set()
        #             for booking in existing_bookings:
        #                 start_time_str = booking.start_time.strftime("%H:%M")
        #                 end_time_str = booking.end_time.strftime("%H:%M")
        #                 booked_slots.add((start_time_str, end_time_str))
        #             print("vv")
        #             print(booked_slots)
        #             print("andhra")
        #             available_slots = [slot for slot in final_all_slots if slot not in booked_slots]
        #
        #             all_available_slots.append(available_slots)
        #             print("guna")
        #             print(all_available_slots)
        #             print("shouya")
        #
        #             # a=len(available_slots)
        #             # print(a)
        #             # print(available_slots)
        #             # print(type(available_slots))
        #             # print("done very good job")
        #
        #         # first_position = len(all_available_slots[0])
        #         # second_position = len(all_available_slots[1])
        #         # third_position = len(all_available_slots[2])
        #         # fourth_position = len(all_available_slots[3])
        #         # fifth_position = len(all_available_slots[4])
        #         # six_position = len(all_available_slots[5])
        #         # seventh_position = len(all_available_slots[6])
        #         # print(seventh_position)
        #
        #         len_all_slots = []
        #
        #         for i, date in enumerate(ex_date):
        #             avlslots = len(all_available_slots[i])
        #             formateedDate = ''
        #             if avlslots != 0 and avlslots <= 10:
        #                 formateedDate = date.strftime('%d %b %a')
        #                 len_all_slots.append((i, date, avlslots, formateedDate))
        #             else:
        #                 print(f"No slots available for {formateedDate}")
        #
        #         # Now len_all_slots contains tuples of (formatted_date, avlslots)
        #         print(len_all_slots)
        #         print("burger")
        #
        #         show_avl_slots = []
        #         show_date = []
        #         total_avl_slots = 0
        #         for j, (i, date, avlslots, formateedDate) in enumerate(len_all_slots[:8]):
        #             show_date.append(date)
        #             total_avl_slots += avlslots
        #             title = f"{formateedDate} ({avlslots} slots)"
        #             show_avl_slots.append({"id": "K" + str(response_id_id) + "/" + str(date),
        #                                    "title": title
        #
        #                                    })
        #         print(show_avl_slots)
        #         first_date = show_date[0]
        #         last_date = show_date[-1]
        #         print('bomma')
        #         print(first_date)
        #         print(last_date)
        #         print("borusu")
        #         response = {
        #             "version": "3.0",
        #             "screen": "DATES_DATA",
        #             "data": {
        #                 "options": show_avl_slots
        #
        #             }
        #         }
        #         return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')
        #     elif Screen_name == 'DATES_DATA':
        #         response_id = decrypted_data['data']['options']
        #         print("tipelinganna")
        #         print(response_id)
        #         slash_index = response_id.index('/')
        #
        #         date = []
        #         dates = response_id[slash_index + 1:]
        #         print("jayamma")
        #         print(dates)
        #         print("jayanna")
        #         dates_new = datetime.strptime(str(dates), '%Y-%m-%d')
        #         date.append(dates_new)
        #
        #         consult_id = response_id[1:slash_index]
        #         print("nagamma")
        #         print(consult_id)
        #         print("nagaraj")
        #
        #         customer = appointment_visitor.objects.filter(client_id=client_id,
        #                                                       Visitor_Whatsapp_Number=toUser).first()
        #         visitor_id = 0
        #         if customer:
        #             visitor_id = customer.id
        #
        #         # import datetime as dt
        #         #
        #         # current_date = dt.datetime.now().date()
        #         #
        #         # current_date += dt.timedelta(days=1)
        #         #
        #         # dates = []
        #         #
        #         # for i in range(7):
        #         #     new_date = current_date + dt.timedelta(days=i)
        #         #     dates.append(new_date)
        #         # print(dates)
        #
        #         a = 0
        #         day_of_week = 0
        #         only_dates = []
        #         sub_dates = []
        #         finalDates = []
        #         formateed_dates = []
        #         all_available_slots = []
        #         consultantName = ''
        #         consultantSpecialization = ''
        #         for i, date in enumerate(date, start=ord('a')):
        #             zformatted_date = date.strftime('%d/%B/%Y %A')
        #             sub_date = date.strftime('%d %b %a')
        #             sub_dates.append(sub_date)
        #             formatted_date = zformatted_date[:6] + zformatted_date[12:]
        #             print(formatted_date)
        #             formateed_dates.append(formatted_date)
        #             only_date = date.strftime('%d-%m-%Y')
        #             final_only_date = only_date.replace("-", "")
        #             finalDates.append(final_only_date)
        #             day_of_week = int(date.strftime('%w'))
        #             variable_name = chr(i)
        #             print(f"{variable_name} = {formatted_date} {day_of_week}")
        #             print(formateed_dates)
        #
        #             duration = None  # Initialize to None or an appropriate default value
        #             slotDuration = Consultant_details.objects.filter(client_id=client_id, id=consult_id)
        #             for s_i in slotDuration:
        #                 duration_str = s_i.slot_duration
        #                 consultantName = s_i.consultant_name
        #                 consultantSpecialization = s_i.consultant_specialization
        #                 numeric_part = int(''.join(filter(str.isdigit, duration_str)))
        #                 duration = numeric_part
        #
        #             hslots = []
        #             not_available_slot = []
        #             holidayDetails = Consultant_holiday_leaves.objects.filter(client_id=client_id, date=date)
        #             for h_i in holidayDetails:
        #                 not_available_slots = {
        #                     "start_time": h_i.start_time.strftime("%H:%M"),  # Convert to string in "HH:MM" format
        #                     "end_time": h_i.end_time.strftime("%H:%M"),
        #                 }
        #                 not_available_slot.append(not_available_slots)
        #
        #             for record in not_available_slot:
        #                 start_time_str1 = record["start_time"]
        #                 end_time_str2 = record["end_time"]  # Convert datetime to string in "HH:MM" format
        #
        #                 record_start_time1 = datetime.strptime(start_time_str1, "%H:%M")
        #                 record_end_time2 = datetime.strptime(end_time_str2, "%H:%M")
        #                 current_time1 = record_start_time1
        #                 while current_time1 < record_end_time2:
        #                     slot_start = current_time1.strftime("%H:%M")
        #                     current_time1 += timedelta(minutes=duration)
        #                     slot_end = current_time1.strftime("%H:%M")
        #                     hslots.append((slot_start, slot_end))
        #             print("aa")
        #             print(hslots)
        #             print("bb")
        #
        #             all_slots = []
        #             availability_records = []
        #
        #             availablityObject = Consultant_availablity.objects.filter(client_id=client_id,
        #                                                                       Consultant_settings_id=consult_id,
        #                                                                       day_of_week=day_of_week)
        #             print(availablityObject)
        #             for a_i in availablityObject:
        #                 print(a_i.id)
        #                 availability_record = {
        #                     "start_time": a_i.start_time.strftime("%H:%M"),
        #                     "end_time": a_i.end_time.strftime("%H:%M"),
        #                 }
        #                 print(availability_record)
        #                 print("mohan")
        #                 availability_records.append(availability_record)
        #
        #             for record in availability_records:
        #                 start_time_str = record["start_time"]
        #                 end_time_str = record["end_time"]
        #
        #                 record_start_time = datetime.strptime(start_time_str, "%H:%M")
        #                 record_end_time = datetime.strptime(end_time_str, "%H:%M")
        #                 current_time = record_start_time
        #
        #                 while current_time < record_end_time:
        #                     slot_start = current_time.strftime("%H:%M")
        #                     current_time += timedelta(minutes=duration)
        #                     slot_end = current_time.strftime("%H:%M")
        #                     all_slots.append((slot_start, slot_end))
        #             final_all_slots = [slot for slot in all_slots if slot not in hslots]
        #             print("channi")
        #             print(final_all_slots)
        #             print(len(final_all_slots))
        #             print("keshav")
        #
        #             existing_bookings = appointment_bookings.objects.filter(client_id=client_id,
        #                                                                     Consultant_settings_id=consult_id,
        #                                                                     date=date)
        #             print("gowda")
        #             print(existing_bookings)
        #             print("sekar")
        #
        #             booked_slots = set()
        #             for booking in existing_bookings:
        #                 start_time_str = booking.start_time.strftime("%H:%M")
        #                 end_time_str = booking.end_time.strftime("%H:%M")
        #                 booked_slots.add((start_time_str, end_time_str))
        #             print("vv")
        #             print(booked_slots)
        #             print("andhra")
        #             available_slots = [slot for slot in final_all_slots if slot not in booked_slots]
        #
        #             all_available_slots.append(available_slots)
        #         print("jill")
        #         print(all_available_slots)
        #         print("jiga")
        #         slot_data = all_available_slots[0]
        #         total_time_slots = len(slot_data)
        #
        #         list_all_data = []
        #         formatted_slots_details = []
        #         formatted_duration_details = []
        #         for slot_start, slot_end in slot_data:
        #             print(slot_start)
        #             print(slot_end)
        #             formatted_duation_create = f"{slot_start}-{slot_end}"
        #             formatted_slot_create = f"{slot_start}"
        #             date_formate_slot_create = datetime.strptime(formatted_slot_create, "%H:%M")
        #             formatted_start_time = date_formate_slot_create.strftime("%I:%M%p")
        #             formatted_slots_details.append(formatted_start_time)
        #             formatted_duration_details.append(formatted_duation_create)
        #
        #         for i in range(len(formatted_slots_details)):
        #             list_all_data.append({"id": "S" + str(consult_id) + "/" + str(
        #                 visitor_id) + "//" + str(finalDates[0]) + str(formatted_duration_details[i]) + str(i),
        #                                   "title": str(sub_dates[0]) + " " + str(formatted_slots_details[i])
        #
        #                                   })
        #
        #         print("correct")
        #         print(formatted_slots_details)
        #         response = {
        #             "version": "3.0",
        #             "screen": "SLOTS_DATA",
        #             "data": {
        #                 "options": list_all_data
        #
        #             }
        #         }
        #         return HttpResponse(encrypt_response_check8(response, aes_key, iv), content_type='text/plain')


        elif action_type == 'ping':
            print("s in appontement")

            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                    "status": "active"
                }
            }
            return HttpResponse(encrypt_response_check12(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check12(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIczQ3XnflVPACAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECB9CP6cT9tJJBIIEyL//SUFeHJbL
JcuW1cdsOCzkaTU04vVLh5QivW8BUYeHAbpz9gH8ILlZNZFl4xHmn1c15V6EcGNL
E7y7NG7N7JQIE1Wez93GX9vIh5cy6dtXA8PxwOiDQjujbuImNqz4okP5vnO/Iuha
eTmJ0/QEUCzI8Ipssn+UVVqcAw4BaY1A+eL0jlgwptTJhOg2hJt0zDegfSclyrVY
Ae8XCPOY8NN6OVPjX4MlyQYGFH5M6y9z2mS82KNTn/TiOffJpY4NGPSK7uUUIsJ0
slHza0Ss/fqWDIFaTNLjR69rKNw0aicIvdW2lFPALAYpbQdIPenzNJuyJX8X6mho
Q/Eyo4hjQkWPEAwWvlHgCCU/ebM2C49FA64VDnd81fHUqrH2kEH3Gn4ekI8uFQpF
ifo5X2T0WZV7pA8GNg3BL2KetWcnBqPyjbM+yVzn1RYCfB627s5JFYy1kwKZMQkZ
mmKcMm5UNFD0FAD7hMJG3xJHKptD8FL2L5LHSPKn1fSsPMS3fSYtVNqRRV3/xU0K
UtS/OzwJ1Ogar2ypAdhDC8A+tHIkD6+knrpHHiUuhRlcDjszyadjoQPBwvjNNz3F
CHfHmvo79vl5PvvxHIj/u+EPMKjReqyh9/3ZX/BTfBz4mPy7bVbxhNuQV1rK1Ruc
ZzxgufcekWcnjDKOJPeDa3bttCO1Is35xPuBFEtIc4vL8XxcikPQT1rmJEUL77u6
cjbE8cGo2rj+j+NAo5DHZQBtrelsIKqaGpnHT8T4KLBim3OXliuUUJwKEOKNNQhT
hvSfBemfKnMJYXrqx+pSQZnBCJOCqP56U4FbKhoQthj/5S6UwZrXLaWtR7DA/K9E
owqHwPb/ISIskvygsZPiDr9RoJ3V330dZcUe+ypeimmTcF+8QNfYWu4OhO5z8x5v
tHhwEXmamlYq5fnseU9vZh6tqn+qbx/Qqw+lby5ymYeWrNZtwrE4mxKGezQqYybW
sd+HSh5gqODx149b5e6Pl4WXCFb0mbqidf754bp+gLMWHu+V1twmnBTF+IzTPVTY
fuJgGzAGlQ1J5glXWUzfjQdUqwyU7eJjIK3sHSanMaagm/gdJqQ2lAKtR+gRawHt
/iVGyBtDhtgI1+gjm1ViVok56B6S4FCMlh6CypQvzGenqU9PVqdCYq93QKYcUdvo
YfHbmcbqTfgLCr0rxzejCUTOlC8ihQWlMQfNYUfWlTezw0FTPE9ueJk7QMhBSDDf
b3zeGw22HvDEHapq9T/ZbNv7/FhrFXG0PZeBq/BXLv5cjLs5JgB5/3t/g+eAnYGv
3s11OPX4AVB1kptujoNAvYa0yoo7RN0PHQetNaf5deL3r/bndcikB+fdcbiNymDe
RhLXAve3c6roAxhPDsBJPEhaAskBLZp3LWfVNpZEsBlQBfvP/kPwPvJbSBQbLRLf
vsrMaGZgGDcm7Tqpp/7exKDao/k23SGvrhVbKllX1EnGG9QB6A0+c3UFkKVULRnP
Rgo4HJGR84Z1PdjTdEF8MfskAT4bJ+/ywUap714JkBu2w+fP8C5j05WtwkQPpmuI
4Goei62rUpoWtinRYnsrZW4fc3ghXLqzWo8UYdlBkYrBUpSqaRiJslD0Oe0nssYd
nS/C7a9xctNeJ2kLu/wVWg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check12(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")

@csrf_exempt
def surveydata(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check16(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        ref_PhonenumberId = decrypted_data['flow_token']
        PhonenumberId = ref_PhonenumberId[:15]
        toUser= ref_PhonenumberId[15:]

        print(action_type)
        print(PhonenumberId)
        facebook_objects = facebook_details.objects.filter(fb_phone_number_id=PhonenumberId)
        facebook_token = ''
        client_id = 0
        for tok in facebook_objects:
            facebook_token += tok.fb_access_token
            client_id += tok.client_id


        if action_type == 'INIT':
            # Return the next screen & data to the client
            print("s in data_exchange")
            response = {
                "version": decrypted_data['version'],
                "screen": "DETAILS",
                "data": {

                }
            }

            # Return the response as plaintext
            return HttpResponse(encrypt_response_check7(response, aes_key, iv), content_type='text/plain')
        elif action_type == 'data_exchange':
            Screen_name = decrypted_data['screen']
            if Screen_name == 'DETAILS':
                response_data = decrypted_data['data']
                print(response_data)
                print("delhi")
                if any(key in response_data for key in ['s_Name', 's_location', 's_category', 's_type']):
                    print("You are searching for NGO details. Please wait while it updates.")

                    keys_to_check = ['s_Name', 's_location', 's_category', 's_type']
                    filters = {}

                    # Mapping keys to corresponding model column names
                    column_mapping = {
                        's_Name': 'survey_name',
                        's_location': 'survey_location',
                        's_category': 'survey_category',
                        's_type': 'survey_type'
                    }

                    for key in keys_to_check:
                        value = response_data.get(key)
                        if value:
                            db_column_name = column_mapping.get(key)
                            filters[f'{db_column_name}__icontains'] = value


                    #
                    # url = f"https://graph.facebook.com/v12.0/{whatsAppPhoneNumberId}/messages"
                    # headers = {
                    #     'Authorization': 'Bearer ' + facebook_token,
                    #     'Content-Type': 'application/json'
                    # }
                    #
                    # Using Q objects to dynamically construct the query
                    query = Q(client_id=client_id)
                    for key, value in filters.items():
                        query &= Q(**{key: value})

                    # Apply the constructed query to the donation_marketplace model
                    donationObj = Survey_marketplace.objects.filter(query)
                    print("jodi")
                    print(donationObj)

                    Ngo_Name = []
                    Ngo_location = []
                    Ngo_id = []

                    if donationObj:
                        for l_i in donationObj:
                            Ngo_id.append(l_i.id)
                            Ngo_Name.append(l_i.survey_name)
                            Ngo_location.append(l_i.survey_location)

                        Ngo_list = [{"id": "A" + str(Ngo_id[i]),
                                     "title": Ngo_Name[i],
                                     "description": Ngo_location[i]}
                                    for i in range(len(Ngo_Name))]

                        donationImage = Survey_marketplace_settings.objects.filter(client_id=client_id)
                        d_image = ''
                        for d in donationImage:
                            d_image = d.marketplace_welcome_image  # Assuming this is an ImageFieldFile object
                        print(d_image)

                        # Open the image file using the ImageFieldFile object
                        with d_image.open(mode='rb') as image_file:
                            image_content = image_file.read()

                        # Convert the image content to base64
                        encoded_string = base64.b64encode(image_content).decode('utf-8')

                        # # 'encoded_string' now contains the base64 representation of the image
                        # print(encoded_string)
                        # file_path = 'C:/Vailo/18-12-2023 updated Dashboard/A_vMart/A_vMart/encoded_image.txt'
                        #
                        # # Write the encoded string to a text file
                        # with open(file_path, 'w') as text_file:
                        #     text_file.write(encoded_string)
                        #
                        # print(f"Encoded string saved at: {file_path}")
                        # print(d_image)


                        response = {
                            "version": "3.0",
                            "screen": "SURVEY_INFO",
                            "data": {
                                "details": encoded_string,
                                "options": Ngo_list
                            }
                        }
                        return HttpResponse(encrypt_response_check16(response, aes_key, iv), content_type='text/plain')
            elif Screen_name == 'SURVEY_INFO':
                print("s survey_info")
                data = decrypted_data['data']['slots_data']
                ngo_ID = data[1:]
                print("bbbbbo")
                print(ngo_ID)
                donation_id = []
                listdonation = Survey_Question.objects.filter(client_id=client_id,marketplace_id=ngo_ID)
                print("bulbul")
                print(listdonation)
                question = ''
                responses = []
                for list_i in listdonation:
                    print(list_i.id)
                    donation_id.append(str(list_i.id))
                    question = list_i.question
                    responses.append(list_i.response_option1)
                    responses.append(list_i.response_option2)
                    responses.append(list_i.response_option3)
                    responses.append(list_i.response_option4)


                donationlist = []
                for i in range(len(responses)):
                    donationlist.append({"id":donation_id[0]+"R"+str(i),
                                         "title": responses[i],

                                         })
                print(donationlist)
                donation_setting_Image = Survey_list.objects.filter(client_id=client_id,marketplace_id=ngo_ID)
                d_image = ''
                for d in donation_setting_Image:
                    d_image = d.survey_image  # Assuming this is an ImageFieldFile object
                print(d_image)

                # Open the image file using the ImageFieldFile object
                with d_image.open(mode='rb') as image_file:
                    image_content = image_file.read()

                # Convert the image content to base64
                encoded_string = base64.b64encode(image_content).decode('utf-8')
                #
                # # 'encoded_string' now contains the base64 representation of the image
                # print(encoded_string)
                # print(d_image)
                response = {
                    "version": "3.0",
                    "screen": "SURVEY_DATA",
                    "data": {
                        "details_info":encoded_string,
                        "details": str(question),
                        "options": donationlist
                    }
                }
                return HttpResponse(encrypt_response_check16(response, aes_key, iv), content_type='text/plain')

        elif action_type == 'ping':
            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                    "status": "active"
                }
            }
            return HttpResponse(encrypt_response_check16(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check16(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIczQ3XnflVPACAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECB9CP6cT9tJJBIIEyL//SUFeHJbL
JcuW1cdsOCzkaTU04vVLh5QivW8BUYeHAbpz9gH8ILlZNZFl4xHmn1c15V6EcGNL
E7y7NG7N7JQIE1Wez93GX9vIh5cy6dtXA8PxwOiDQjujbuImNqz4okP5vnO/Iuha
eTmJ0/QEUCzI8Ipssn+UVVqcAw4BaY1A+eL0jlgwptTJhOg2hJt0zDegfSclyrVY
Ae8XCPOY8NN6OVPjX4MlyQYGFH5M6y9z2mS82KNTn/TiOffJpY4NGPSK7uUUIsJ0
slHza0Ss/fqWDIFaTNLjR69rKNw0aicIvdW2lFPALAYpbQdIPenzNJuyJX8X6mho
Q/Eyo4hjQkWPEAwWvlHgCCU/ebM2C49FA64VDnd81fHUqrH2kEH3Gn4ekI8uFQpF
ifo5X2T0WZV7pA8GNg3BL2KetWcnBqPyjbM+yVzn1RYCfB627s5JFYy1kwKZMQkZ
mmKcMm5UNFD0FAD7hMJG3xJHKptD8FL2L5LHSPKn1fSsPMS3fSYtVNqRRV3/xU0K
UtS/OzwJ1Ogar2ypAdhDC8A+tHIkD6+knrpHHiUuhRlcDjszyadjoQPBwvjNNz3F
CHfHmvo79vl5PvvxHIj/u+EPMKjReqyh9/3ZX/BTfBz4mPy7bVbxhNuQV1rK1Ruc
ZzxgufcekWcnjDKOJPeDa3bttCO1Is35xPuBFEtIc4vL8XxcikPQT1rmJEUL77u6
cjbE8cGo2rj+j+NAo5DHZQBtrelsIKqaGpnHT8T4KLBim3OXliuUUJwKEOKNNQhT
hvSfBemfKnMJYXrqx+pSQZnBCJOCqP56U4FbKhoQthj/5S6UwZrXLaWtR7DA/K9E
owqHwPb/ISIskvygsZPiDr9RoJ3V330dZcUe+ypeimmTcF+8QNfYWu4OhO5z8x5v
tHhwEXmamlYq5fnseU9vZh6tqn+qbx/Qqw+lby5ymYeWrNZtwrE4mxKGezQqYybW
sd+HSh5gqODx149b5e6Pl4WXCFb0mbqidf754bp+gLMWHu+V1twmnBTF+IzTPVTY
fuJgGzAGlQ1J5glXWUzfjQdUqwyU7eJjIK3sHSanMaagm/gdJqQ2lAKtR+gRawHt
/iVGyBtDhtgI1+gjm1ViVok56B6S4FCMlh6CypQvzGenqU9PVqdCYq93QKYcUdvo
YfHbmcbqTfgLCr0rxzejCUTOlC8ihQWlMQfNYUfWlTezw0FTPE9ueJk7QMhBSDDf
b3zeGw22HvDEHapq9T/ZbNv7/FhrFXG0PZeBq/BXLv5cjLs5JgB5/3t/g+eAnYGv
3s11OPX4AVB1kptujoNAvYa0yoo7RN0PHQetNaf5deL3r/bndcikB+fdcbiNymDe
RhLXAve3c6roAxhPDsBJPEhaAskBLZp3LWfVNpZEsBlQBfvP/kPwPvJbSBQbLRLf
vsrMaGZgGDcm7Tqpp/7exKDao/k23SGvrhVbKllX1EnGG9QB6A0+c3UFkKVULRnP
Rgo4HJGR84Z1PdjTdEF8MfskAT4bJ+/ywUap714JkBu2w+fP8C5j05WtwkQPpmuI
4Goei62rUpoWtinRYnsrZW4fc3ghXLqzWo8UYdlBkYrBUpSqaRiJslD0Oe0nssYd
nS/C7a9xctNeJ2kLu/wVWg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check16(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")



@csrf_exempt
def specificsurveydata(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check17(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        ref_PhonenumberId = decrypted_data['flow_token']
        PhonenumberId = ref_PhonenumberId[:15]
        toUser = ref_PhonenumberId[15:27]
        Search_ngo_id = ref_PhonenumberId[27:]
        print(Search_ngo_id)
        print(action_type)
        print(PhonenumberId)
        facebook_objects = facebook_details.objects.filter(fb_phone_number_id=PhonenumberId)
        facebook_token = ''
        client_id = 0
        for tok in facebook_objects:
            facebook_token += tok.fb_access_token
            client_id += tok.client_id


        if action_type == 'INIT':
            # Return the next screen & data to the client
            print("s in data_exchange")
            dynamicInfo = Survey_marketplace.objects.filter(client_id=client_id,survey_id=Search_ngo_id)
            d_ngo_ID = 0
            for d_i in dynamicInfo:
                d_ngo_ID = d_i.id

            listdonation = Survey_Question.objects.filter(client_id=client_id, marketplace_id=d_ngo_ID)
            print("bulbul")
            print(listdonation)
            question = ''
            donation_id = []
            responses = []
            for list_i in listdonation:
                print(list_i.id)
                donation_id.append(str(list_i.id))
                question = list_i.question
                responses.append(list_i.response_option1)
                responses.append(list_i.response_option2)
                responses.append(list_i.response_option3)
                responses.append(list_i.response_option4)

            donationlist = []
            for i in range(len(responses)):
                donationlist.append({"id": donation_id[0] + "R" + str(i),
                                     "title": responses[i],

                                     })
            print(donationlist)


            # dynamicImage = appointment_marketplace.objects.filter(client_id=client_id, group_id=Search_ngo_id)
            # d_image = ''
            # for d_i in dynamicImage:
            #     settingImage = appointment_settings.objects.filter(client_id=client_id,marketplace_id=d_i.id)
            #     for s in settingImage:
            #         d_image = s.welcome_image
            #
            # with d_image.open(mode='rb') as image_file:
            #     image_content = image_file.read()
            #
            # # Convert the image content to base64
            # encoded_string = base64.b64encode(image_content).decode('utf-8')
            #
            # # 'encoded_string' now contains the base64 representation of the image
            # print(encoded_string)
            # file_path = 'C:/Vailo/18-12-2023 updated Dashboard/A_vMart/A_vMart/encoded_image12.txt'
            #
            # # Write the encoded string to a text file
            # with open(file_path, 'w') as text_file:
            #     text_file.write(encoded_string)
            #
            # print(f"Encoded string saved at: {file_path}")
            # print(d_image)
            donation_setting_Image = Survey_list.objects.filter(client_id=client_id, marketplace_id=d_ngo_ID)
            d_image = ''
            for d in donation_setting_Image:
                d_image = d.survey_image  # Assuming this is an ImageFieldFile object
            print(d_image)

            # Open the image file using the ImageFieldFile object
            with d_image.open(mode='rb') as image_file:
                image_content = image_file.read()

            # Convert the image content to base64
            encoded_string = base64.b64encode(image_content).decode('utf-8')

            response = {
                "version": "3.0",
                "screen": "MYSPECIFIC_DETAILS",
                "data": {
                    "details_info": encoded_string,
                    "details": question,
                    "options": donationlist
                }
            }
            # Return the response as plaintext
            return HttpResponse(encrypt_response_check17(response, aes_key, iv), content_type='text/plain')





        elif action_type == 'ping':

            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                    "status": "active"
                }
            }
            return HttpResponse(encrypt_response_check17(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check17(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIczQ3XnflVPACAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECB9CP6cT9tJJBIIEyL//SUFeHJbL
JcuW1cdsOCzkaTU04vVLh5QivW8BUYeHAbpz9gH8ILlZNZFl4xHmn1c15V6EcGNL
E7y7NG7N7JQIE1Wez93GX9vIh5cy6dtXA8PxwOiDQjujbuImNqz4okP5vnO/Iuha
eTmJ0/QEUCzI8Ipssn+UVVqcAw4BaY1A+eL0jlgwptTJhOg2hJt0zDegfSclyrVY
Ae8XCPOY8NN6OVPjX4MlyQYGFH5M6y9z2mS82KNTn/TiOffJpY4NGPSK7uUUIsJ0
slHza0Ss/fqWDIFaTNLjR69rKNw0aicIvdW2lFPALAYpbQdIPenzNJuyJX8X6mho
Q/Eyo4hjQkWPEAwWvlHgCCU/ebM2C49FA64VDnd81fHUqrH2kEH3Gn4ekI8uFQpF
ifo5X2T0WZV7pA8GNg3BL2KetWcnBqPyjbM+yVzn1RYCfB627s5JFYy1kwKZMQkZ
mmKcMm5UNFD0FAD7hMJG3xJHKptD8FL2L5LHSPKn1fSsPMS3fSYtVNqRRV3/xU0K
UtS/OzwJ1Ogar2ypAdhDC8A+tHIkD6+knrpHHiUuhRlcDjszyadjoQPBwvjNNz3F
CHfHmvo79vl5PvvxHIj/u+EPMKjReqyh9/3ZX/BTfBz4mPy7bVbxhNuQV1rK1Ruc
ZzxgufcekWcnjDKOJPeDa3bttCO1Is35xPuBFEtIc4vL8XxcikPQT1rmJEUL77u6
cjbE8cGo2rj+j+NAo5DHZQBtrelsIKqaGpnHT8T4KLBim3OXliuUUJwKEOKNNQhT
hvSfBemfKnMJYXrqx+pSQZnBCJOCqP56U4FbKhoQthj/5S6UwZrXLaWtR7DA/K9E
owqHwPb/ISIskvygsZPiDr9RoJ3V330dZcUe+ypeimmTcF+8QNfYWu4OhO5z8x5v
tHhwEXmamlYq5fnseU9vZh6tqn+qbx/Qqw+lby5ymYeWrNZtwrE4mxKGezQqYybW
sd+HSh5gqODx149b5e6Pl4WXCFb0mbqidf754bp+gLMWHu+V1twmnBTF+IzTPVTY
fuJgGzAGlQ1J5glXWUzfjQdUqwyU7eJjIK3sHSanMaagm/gdJqQ2lAKtR+gRawHt
/iVGyBtDhtgI1+gjm1ViVok56B6S4FCMlh6CypQvzGenqU9PVqdCYq93QKYcUdvo
YfHbmcbqTfgLCr0rxzejCUTOlC8ihQWlMQfNYUfWlTezw0FTPE9ueJk7QMhBSDDf
b3zeGw22HvDEHapq9T/ZbNv7/FhrFXG0PZeBq/BXLv5cjLs5JgB5/3t/g+eAnYGv
3s11OPX4AVB1kptujoNAvYa0yoo7RN0PHQetNaf5deL3r/bndcikB+fdcbiNymDe
RhLXAve3c6roAxhPDsBJPEhaAskBLZp3LWfVNpZEsBlQBfvP/kPwPvJbSBQbLRLf
vsrMaGZgGDcm7Tqpp/7exKDao/k23SGvrhVbKllX1EnGG9QB6A0+c3UFkKVULRnP
Rgo4HJGR84Z1PdjTdEF8MfskAT4bJ+/ywUap714JkBu2w+fP8C5j05WtwkQPpmuI
4Goei62rUpoWtinRYnsrZW4fc3ghXLqzWo8UYdlBkYrBUpSqaRiJslD0Oe0nssYd
nS/C7a9xctNeJ2kLu/wVWg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check17(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")

@csrf_exempt
def mysurveydata(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check18(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        PhonenumberId = decrypted_data['flow_token']
        ref_PhonenumberId = PhonenumberId[:15]
        toUser = PhonenumberId[15:]
        # print(reference_id)
        # print(action_type)
        print(ref_PhonenumberId)
        facebook_objects = facebook_details.objects.filter(fb_phone_number_id=ref_PhonenumberId)
        facebook_token = ''
        client_id = 0
        for tok in facebook_objects:
            facebook_token += tok.fb_access_token
            client_id += tok.client_id


        if action_type == 'INIT':
            # Return the next screen & data to the client
            print("s in INIT")
            All_Survey = []
            question_id = []
            question_name = []
            donar_details = Survey_Customer.objects.filter(client_id=client_id,customer_whatsapp_number=toUser)
            if donar_details:
                for d_i in donar_details:
                    customer_res = Survey_Customer_Response.objects.filter(client_id=client_id,Survey_Customer_id=d_i.id)
                    for c_i in customer_res:
                        questionobj = Survey_Question.objects.filter(client_id=client_id,id=c_i.Survey_Question_id)
                        for q_i in questionobj:
                            question_id.append(str(q_i.id))
                            question_name.append(q_i.question)

                for f_i in range(len(question_name)):
                    All_Survey.append({
                        "id": question_id[f_i]+str(f_i),
                        "title": question_name[f_i]
                    })

                # All_Donations = []
                # for j in range(len(donation_Name)):
                #     All_Donations.append({
                #         "id": str(donation_Id[j]),
                #         "title": donation_Name[j]
                #     })

                response = {
                    "version": decrypted_data['version'],
                    "screen": "MYSURVEY_DETAILS",
                    "data": {
                        "details":"My Survey details",
                        "options": All_Survey
                    }
                }

                # Return the response as plaintext
                return HttpResponse(encrypt_response_check18(response, aes_key, iv), content_type='text/plain')
            else:
                print("s no donations")
                response = {
                    "version": decrypted_data['version'],
                    "screen": "MYDONATION_DETAILS",
                    "data": {
                        "details": "You have no donations.Please donate.",
                        "options":[{
                            "id":"No records",
                            "title":"No records"
                        }]

                    }
                }

                # Return the response as plaintext
                return HttpResponse(encrypt_response_check18(response, aes_key, iv), content_type='text/plain')



        elif action_type == 'ping':
            print("s in appontement")

            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                    "status": "active"
                }
            }
            return HttpResponse(encrypt_response_check18(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check18(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIczQ3XnflVPACAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECB9CP6cT9tJJBIIEyL//SUFeHJbL
JcuW1cdsOCzkaTU04vVLh5QivW8BUYeHAbpz9gH8ILlZNZFl4xHmn1c15V6EcGNL
E7y7NG7N7JQIE1Wez93GX9vIh5cy6dtXA8PxwOiDQjujbuImNqz4okP5vnO/Iuha
eTmJ0/QEUCzI8Ipssn+UVVqcAw4BaY1A+eL0jlgwptTJhOg2hJt0zDegfSclyrVY
Ae8XCPOY8NN6OVPjX4MlyQYGFH5M6y9z2mS82KNTn/TiOffJpY4NGPSK7uUUIsJ0
slHza0Ss/fqWDIFaTNLjR69rKNw0aicIvdW2lFPALAYpbQdIPenzNJuyJX8X6mho
Q/Eyo4hjQkWPEAwWvlHgCCU/ebM2C49FA64VDnd81fHUqrH2kEH3Gn4ekI8uFQpF
ifo5X2T0WZV7pA8GNg3BL2KetWcnBqPyjbM+yVzn1RYCfB627s5JFYy1kwKZMQkZ
mmKcMm5UNFD0FAD7hMJG3xJHKptD8FL2L5LHSPKn1fSsPMS3fSYtVNqRRV3/xU0K
UtS/OzwJ1Ogar2ypAdhDC8A+tHIkD6+knrpHHiUuhRlcDjszyadjoQPBwvjNNz3F
CHfHmvo79vl5PvvxHIj/u+EPMKjReqyh9/3ZX/BTfBz4mPy7bVbxhNuQV1rK1Ruc
ZzxgufcekWcnjDKOJPeDa3bttCO1Is35xPuBFEtIc4vL8XxcikPQT1rmJEUL77u6
cjbE8cGo2rj+j+NAo5DHZQBtrelsIKqaGpnHT8T4KLBim3OXliuUUJwKEOKNNQhT
hvSfBemfKnMJYXrqx+pSQZnBCJOCqP56U4FbKhoQthj/5S6UwZrXLaWtR7DA/K9E
owqHwPb/ISIskvygsZPiDr9RoJ3V330dZcUe+ypeimmTcF+8QNfYWu4OhO5z8x5v
tHhwEXmamlYq5fnseU9vZh6tqn+qbx/Qqw+lby5ymYeWrNZtwrE4mxKGezQqYybW
sd+HSh5gqODx149b5e6Pl4WXCFb0mbqidf754bp+gLMWHu+V1twmnBTF+IzTPVTY
fuJgGzAGlQ1J5glXWUzfjQdUqwyU7eJjIK3sHSanMaagm/gdJqQ2lAKtR+gRawHt
/iVGyBtDhtgI1+gjm1ViVok56B6S4FCMlh6CypQvzGenqU9PVqdCYq93QKYcUdvo
YfHbmcbqTfgLCr0rxzejCUTOlC8ihQWlMQfNYUfWlTezw0FTPE9ueJk7QMhBSDDf
b3zeGw22HvDEHapq9T/ZbNv7/FhrFXG0PZeBq/BXLv5cjLs5JgB5/3t/g+eAnYGv
3s11OPX4AVB1kptujoNAvYa0yoo7RN0PHQetNaf5deL3r/bndcikB+fdcbiNymDe
RhLXAve3c6roAxhPDsBJPEhaAskBLZp3LWfVNpZEsBlQBfvP/kPwPvJbSBQbLRLf
vsrMaGZgGDcm7Tqpp/7exKDao/k23SGvrhVbKllX1EnGG9QB6A0+c3UFkKVULRnP
Rgo4HJGR84Z1PdjTdEF8MfskAT4bJ+/ywUap714JkBu2w+fP8C5j05WtwkQPpmuI
4Goei62rUpoWtinRYnsrZW4fc3ghXLqzWo8UYdlBkYrBUpSqaRiJslD0Oe0nssYd
nS/C7a9xctNeJ2kLu/wVWg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check18(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")


@csrf_exempt
def campaigndata(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check20(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        ref_PhonenumberId = decrypted_data['flow_token']
        PhonenumberId = ref_PhonenumberId[:15]
        toUser= ref_PhonenumberId[15:]

        print(action_type)
        print(PhonenumberId)
        facebook_objects = facebook_details.objects.filter(fb_phone_number_id=PhonenumberId)
        facebook_token = ''
        client_id = 0
        for tok in facebook_objects:
            facebook_token += tok.fb_access_token
            client_id += tok.client_id


        if action_type == 'INIT':
            # Return the next screen & data to the client
            print("s in data_exchange")
            response = {
                "version": decrypted_data['version'],
                "screen": "DETAILS",
                "data": {

                }
            }

            # Return the response as plaintext
            return HttpResponse(encrypt_response_check20(response, aes_key, iv), content_type='text/plain')
        elif action_type == 'data_exchange':
            Screen_name = decrypted_data['screen']
            if Screen_name == 'DETAILS':
                response_data = decrypted_data['data']
                print(response_data)
                print("delhi")
                if any(key in response_data for key in ['c_Name', 'c_location', 'c_category', 'c_type']):
                    print("You are searching for NGO details. Please wait while it updates.")

                    keys_to_check = ['c_Name', 'c_location', 'c_category', 'c_type']
                    filters = {}

                    # Mapping keys to corresponding model column names
                    column_mapping = {
                        'c_Name': 'campaign_name',
                        'c_location': 'campaign_location',
                        'c_category': 'campaign_category',
                        'c_type': 'campaign_type'
                    }

                    for key in keys_to_check:
                        value = response_data.get(key)
                        if value:
                            db_column_name = column_mapping.get(key)
                            filters[f'{db_column_name}__icontains'] = value


                    #
                    # url = f"https://graph.facebook.com/v12.0/{whatsAppPhoneNumberId}/messages"
                    # headers = {
                    #     'Authorization': 'Bearer ' + facebook_token,
                    #     'Content-Type': 'application/json'
                    # }
                    #
                    # Using Q objects to dynamically construct the query
                    query = Q(client_id=client_id)
                    for key, value in filters.items():
                        query &= Q(**{key: value})

                    # Apply the constructed query to the donation_marketplace model
                    donationObj = campaign_marketplace.objects.filter(query)
                    print("jodi")
                    print(donationObj)

                    Ngo_Name = []
                    Ngo_location = []
                    Ngo_id = []

                    if donationObj:
                        for l_i in donationObj:
                            Ngo_id.append(l_i.id)
                            Ngo_Name.append(l_i.campaign_name)
                            Ngo_location.append(l_i.campaign_location)

                        Ngo_list = [{"id": "A" + str(Ngo_id[i]),
                                     "title": Ngo_Name[i],
                                     "description": Ngo_location[i]}
                                    for i in range(len(Ngo_Name))]

                        donationImage = campaign_marketplace_settings.objects.filter(client_id=client_id)
                        d_image = ''
                        for d in donationImage:
                            d_image = d.marketplace_welcome_image  # Assuming this is an ImageFieldFile object
                        print(d_image)

                        # Open the image file using the ImageFieldFile object
                        with d_image.open(mode='rb') as image_file:
                            image_content = image_file.read()

                        # Convert the image content to base64
                        encoded_string = base64.b64encode(image_content).decode('utf-8')

                        # # 'encoded_string' now contains the base64 representation of the image
                        # print(encoded_string)
                        # file_path = 'C:/Vailo/18-12-2023 updated Dashboard/A_vMart/A_vMart/encoded_image.txt'
                        #
                        # # Write the encoded string to a text file
                        # with open(file_path, 'w') as text_file:
                        #     text_file.write(encoded_string)
                        #
                        # print(f"Encoded string saved at: {file_path}")
                        # print(d_image)


                        response = {
                            "version": "3.0",
                            "screen": "CAMPAIGN_DATA",
                            "data": {
                                "details_info": encoded_string,
                                "details":"Available Campaigns",
                                "options": Ngo_list
                            }
                        }
                        return HttpResponse(encrypt_response_check20(response, aes_key, iv), content_type='text/plain')


        elif action_type == 'ping':
            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                    "status": "active"
                }
            }
            return HttpResponse(encrypt_response_check20(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check20(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIczQ3XnflVPACAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECB9CP6cT9tJJBIIEyL//SUFeHJbL
JcuW1cdsOCzkaTU04vVLh5QivW8BUYeHAbpz9gH8ILlZNZFl4xHmn1c15V6EcGNL
E7y7NG7N7JQIE1Wez93GX9vIh5cy6dtXA8PxwOiDQjujbuImNqz4okP5vnO/Iuha
eTmJ0/QEUCzI8Ipssn+UVVqcAw4BaY1A+eL0jlgwptTJhOg2hJt0zDegfSclyrVY
Ae8XCPOY8NN6OVPjX4MlyQYGFH5M6y9z2mS82KNTn/TiOffJpY4NGPSK7uUUIsJ0
slHza0Ss/fqWDIFaTNLjR69rKNw0aicIvdW2lFPALAYpbQdIPenzNJuyJX8X6mho
Q/Eyo4hjQkWPEAwWvlHgCCU/ebM2C49FA64VDnd81fHUqrH2kEH3Gn4ekI8uFQpF
ifo5X2T0WZV7pA8GNg3BL2KetWcnBqPyjbM+yVzn1RYCfB627s5JFYy1kwKZMQkZ
mmKcMm5UNFD0FAD7hMJG3xJHKptD8FL2L5LHSPKn1fSsPMS3fSYtVNqRRV3/xU0K
UtS/OzwJ1Ogar2ypAdhDC8A+tHIkD6+knrpHHiUuhRlcDjszyadjoQPBwvjNNz3F
CHfHmvo79vl5PvvxHIj/u+EPMKjReqyh9/3ZX/BTfBz4mPy7bVbxhNuQV1rK1Ruc
ZzxgufcekWcnjDKOJPeDa3bttCO1Is35xPuBFEtIc4vL8XxcikPQT1rmJEUL77u6
cjbE8cGo2rj+j+NAo5DHZQBtrelsIKqaGpnHT8T4KLBim3OXliuUUJwKEOKNNQhT
hvSfBemfKnMJYXrqx+pSQZnBCJOCqP56U4FbKhoQthj/5S6UwZrXLaWtR7DA/K9E
owqHwPb/ISIskvygsZPiDr9RoJ3V330dZcUe+ypeimmTcF+8QNfYWu4OhO5z8x5v
tHhwEXmamlYq5fnseU9vZh6tqn+qbx/Qqw+lby5ymYeWrNZtwrE4mxKGezQqYybW
sd+HSh5gqODx149b5e6Pl4WXCFb0mbqidf754bp+gLMWHu+V1twmnBTF+IzTPVTY
fuJgGzAGlQ1J5glXWUzfjQdUqwyU7eJjIK3sHSanMaagm/gdJqQ2lAKtR+gRawHt
/iVGyBtDhtgI1+gjm1ViVok56B6S4FCMlh6CypQvzGenqU9PVqdCYq93QKYcUdvo
YfHbmcbqTfgLCr0rxzejCUTOlC8ihQWlMQfNYUfWlTezw0FTPE9ueJk7QMhBSDDf
b3zeGw22HvDEHapq9T/ZbNv7/FhrFXG0PZeBq/BXLv5cjLs5JgB5/3t/g+eAnYGv
3s11OPX4AVB1kptujoNAvYa0yoo7RN0PHQetNaf5deL3r/bndcikB+fdcbiNymDe
RhLXAve3c6roAxhPDsBJPEhaAskBLZp3LWfVNpZEsBlQBfvP/kPwPvJbSBQbLRLf
vsrMaGZgGDcm7Tqpp/7exKDao/k23SGvrhVbKllX1EnGG9QB6A0+c3UFkKVULRnP
Rgo4HJGR84Z1PdjTdEF8MfskAT4bJ+/ywUap714JkBu2w+fP8C5j05WtwkQPpmuI
4Goei62rUpoWtinRYnsrZW4fc3ghXLqzWo8UYdlBkYrBUpSqaRiJslD0Oe0nssYd
nS/C7a9xctNeJ2kLu/wVWg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check20(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")


@csrf_exempt
def mycampaigndata(request):
    print("ssssssssssssssssssss")
    print(request)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)

        # Generate a new RSA private key (for demonstration)
        # private_key = rsa.generate_private_key(
        #     public_exponent=65537,
        #     key_size=2048
        # )

        # Serialize private key to PEM format
        # private_key_pem = private_key.private_bytes(
        #     encoding=serialization.Encoding.PEM,
        #     format=serialization.PrivateFormat.TraditionalOpenSSL,
        #     encryption_algorithm=serialization.NoEncryption()
        # )

        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check21(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print("kohli")
        print(decrypted_data)
        print("rohith")
        action_type = decrypted_data['action']
        ref_PhonenumberId = decrypted_data['flow_token']
        PhonenumberId = ref_PhonenumberId[:15]
        toUser= ref_PhonenumberId[15:]

        print(action_type)
        print(PhonenumberId)
        facebook_objects = facebook_details.objects.filter(fb_phone_number_id=PhonenumberId)
        facebook_token = ''
        client_id = 0
        for tok in facebook_objects:
            facebook_token += tok.fb_access_token
            client_id += tok.client_id


        if action_type == 'INIT':
            # Return the next screen & data to the client
            campaign_Name = []
            camp_id = []
            responseobj = campaign_customer_master.objects.filter(client_id=client_id, Customer_Whatsapp_Number=toUser)
            if responseobj:
                print("s")
                for r in responseobj:
                    customer_res_obj = generic_campaign_history.objects.filter(client_id=client_id,
                                                                               campaign_customer_master_id=r.id)
                    if customer_res_obj:
                        for j in customer_res_obj:
                            campaignObj = generic_campaign_info.objects.filter(client_id=client_id, id=j.generic_campaign_info_id)
                            for f_i in campaignObj:
                                camp_id.append(f_i.id)
                                campaign_Name.append(f_i.Campaign_Name)
            all_campaigns = []
            for g in range(len(campaign_Name)):
                all_campaigns.append({
                    "id":"C"+str(camp_id[g]),
                    "title":str(campaign_Name[g])
                })
            donationImage = campaign_marketplace_settings.objects.filter(client_id=client_id)
            d_image = ''
            for d in donationImage:
                d_image = d.marketplace_welcome_image  # Assuming this is an ImageFieldFile object
            print(d_image)

            # Open the image file using the ImageFieldFile object
            with d_image.open(mode='rb') as image_file:
                image_content = image_file.read()

            # Convert the image content to base64
            encoded_string = base64.b64encode(image_content).decode('utf-8')


            print("s in data_exchange")
            response = {
                "version": decrypted_data['version'],
                "screen": "CAMPAIGN_DATA",
                "data": {
                    "details_info": encoded_string,
                    "details": "My Campaigns",
                    "options": all_campaigns

                }
            }

            # Return the response as plaintext
            return HttpResponse(encrypt_response_check21(response, aes_key, iv), content_type='text/plain')

        elif action_type == 'ping':
            print("s you are in ping")
            response = {
                "version": "3.0",
                "data": {
                    "status": "active"
                }
            }
            return HttpResponse(encrypt_response_check21(response, aes_key, iv), content_type='text/plain')

    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check21(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("nnn")
    print(flow_data)
    print("nnvv")
    PRIVATE_KEY = '''
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIczQ3XnflVPACAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECB9CP6cT9tJJBIIEyL//SUFeHJbL
JcuW1cdsOCzkaTU04vVLh5QivW8BUYeHAbpz9gH8ILlZNZFl4xHmn1c15V6EcGNL
E7y7NG7N7JQIE1Wez93GX9vIh5cy6dtXA8PxwOiDQjujbuImNqz4okP5vnO/Iuha
eTmJ0/QEUCzI8Ipssn+UVVqcAw4BaY1A+eL0jlgwptTJhOg2hJt0zDegfSclyrVY
Ae8XCPOY8NN6OVPjX4MlyQYGFH5M6y9z2mS82KNTn/TiOffJpY4NGPSK7uUUIsJ0
slHza0Ss/fqWDIFaTNLjR69rKNw0aicIvdW2lFPALAYpbQdIPenzNJuyJX8X6mho
Q/Eyo4hjQkWPEAwWvlHgCCU/ebM2C49FA64VDnd81fHUqrH2kEH3Gn4ekI8uFQpF
ifo5X2T0WZV7pA8GNg3BL2KetWcnBqPyjbM+yVzn1RYCfB627s5JFYy1kwKZMQkZ
mmKcMm5UNFD0FAD7hMJG3xJHKptD8FL2L5LHSPKn1fSsPMS3fSYtVNqRRV3/xU0K
UtS/OzwJ1Ogar2ypAdhDC8A+tHIkD6+knrpHHiUuhRlcDjszyadjoQPBwvjNNz3F
CHfHmvo79vl5PvvxHIj/u+EPMKjReqyh9/3ZX/BTfBz4mPy7bVbxhNuQV1rK1Ruc
ZzxgufcekWcnjDKOJPeDa3bttCO1Is35xPuBFEtIc4vL8XxcikPQT1rmJEUL77u6
cjbE8cGo2rj+j+NAo5DHZQBtrelsIKqaGpnHT8T4KLBim3OXliuUUJwKEOKNNQhT
hvSfBemfKnMJYXrqx+pSQZnBCJOCqP56U4FbKhoQthj/5S6UwZrXLaWtR7DA/K9E
owqHwPb/ISIskvygsZPiDr9RoJ3V330dZcUe+ypeimmTcF+8QNfYWu4OhO5z8x5v
tHhwEXmamlYq5fnseU9vZh6tqn+qbx/Qqw+lby5ymYeWrNZtwrE4mxKGezQqYybW
sd+HSh5gqODx149b5e6Pl4WXCFb0mbqidf754bp+gLMWHu+V1twmnBTF+IzTPVTY
fuJgGzAGlQ1J5glXWUzfjQdUqwyU7eJjIK3sHSanMaagm/gdJqQ2lAKtR+gRawHt
/iVGyBtDhtgI1+gjm1ViVok56B6S4FCMlh6CypQvzGenqU9PVqdCYq93QKYcUdvo
YfHbmcbqTfgLCr0rxzejCUTOlC8ihQWlMQfNYUfWlTezw0FTPE9ueJk7QMhBSDDf
b3zeGw22HvDEHapq9T/ZbNv7/FhrFXG0PZeBq/BXLv5cjLs5JgB5/3t/g+eAnYGv
3s11OPX4AVB1kptujoNAvYa0yoo7RN0PHQetNaf5deL3r/bndcikB+fdcbiNymDe
RhLXAve3c6roAxhPDsBJPEhaAskBLZp3LWfVNpZEsBlQBfvP/kPwPvJbSBQbLRLf
vsrMaGZgGDcm7Tqpp/7exKDao/k23SGvrhVbKllX1EnGG9QB6A0+c3UFkKVULRnP
Rgo4HJGR84Z1PdjTdEF8MfskAT4bJ+/ywUap714JkBu2w+fP8C5j05WtwkQPpmuI
4Goei62rUpoWtinRYnsrZW4fc3ghXLqzWo8UYdlBkYrBUpSqaRiJslD0Oe0nssYd
nS/C7a9xctNeJ2kLu/wVWg==
-----END ENCRYPTED PRIVATE KEY-----'''

    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("jaysilan")
    aes_key = private_key.decrypt(encrypted_aes_key, OAEP(
        mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('nataaalala')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print('gangalala')
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print("vvangalaala")
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv


def encrypt_response_check21(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")

@csrf_exempt
def finalcheck(request):
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)
        print("body")
        # Read the request fields
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']

        decrypted_data, aes_key, iv = decrypt_request_check30(
            encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64)
        print(decrypted_data)

        action_type = decrypted_data['action']

        # Return the next screen & data to the client
        Ngo_list = [{"id": "A",
                     "title": "aaaaaa",
                     }
                    ]

        if action_type == 'INIT':
            # Return the next screen & data to the client
            print("s in data_exchange")
            response = {
                "version": decrypted_data['version'],
                "screen": "final_info",
                "data": {
                    "options": Ngo_list

                }
            }

            # Return the response as plaintext
            return HttpResponse(encrypt_response_check30(response, aes_key, iv), content_type='text/plain')
    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request_check30(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    print("iv",iv)
    print("flow_data",flow_data)
    with open(f'C:/Vailo/16-02-2024 new dashboard/A_vMart/A_vMart/newvailoprivate_key11.pem', 'r') as key_file:
        PRIVATE_KEY = key_file.read()
    # Decrypt the AES encryption key
    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("encrypted_aes_key",encrypted_aes_key)
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Guna@123')
    print("private_key",private_key)
    aes_key = private_key.decrypt(encrypted_aes_key, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    print('s continue')
    print(aes_key)
    # Decrypt the Flow data
    encrypted_flow_data_body = flow_data[:-16]
    print(encrypted_flow_data_body)
    encrypted_flow_data_tag = flow_data[-16:]
    print(encrypted_flow_data_tag)
    print(encrypted_flow_data_body)
    print('kkkk')
    print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data)
    return decrypted_data, aes_key, iv

def encrypt_response_check30(response, aes_key, iv):
    # Flip the initialization vector
    flipped_iv = bytearray()
    for byte in iv:
        flipped_iv.append(byte ^ 0xFF)

    # Encrypt the response data
    encryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(flipped_iv)).encryptor()
    return b64encode(
        encryptor.update(json.dumps(response).encode("utf-8")) +
        encryptor.finalize() +
        encryptor.tag
    ).decode("utf-8")

