from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from vailodb_a.models import appointment_settings, Consultant_details, Consultant_availablity, Consultant_holiday_leaves, appointment_visitor,appointment_bookings
from vailodb_n.models import donation_details, donation_settings, donation_types

from A_vMart.settings import DomainName
from vailodb.models import payment_gateway_details, payment_settings
from vailodb.models import event_master, event_slots, event_ticket_category, event_settings, \
    event_ticket_cart_details, event_ticket_cart_header, ticket_information, ticket_customer_master, \
    ticket_billing_details, ticket_billing, Subclient, SubUserPreference
from vailodb_h.models import * #Hotel_marketplace_settings,Hotel_marketplace,Hotel_settings,Hotel_services,Food,\
#      Nearby_place, Hotel_rooms, Hotel_facilities, Selfhelp, Information, Food_catalogue,Food_catalogue_items,Hotel_services_settings,\
#     Service_order, Food_order_header, Food_order_details, Guest_info, Hotel_Room_Guest_info   

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
from django.shortcuts import get_object_or_404
from django.db.models import Q

# original_tz = pytz.timezone('Asia/Kolkata')
# import pytz

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
    return render(request, 'payinfo.html')


@never_cache
@login_required
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

            # Check if the subclient is associated with the main client and subclient login is allowed
            if subclient and subclient.client == user:
                # Use subclient details and preferences
                subclient_preferences = SubUserPreference.objects.filter(client=user, subclient=subclient).first()

                # if subclient_preferences and subclient_preferences.scanner:
                #     return render(request, 'scanner.html')
                # else:
                context = {
                    'subclient': subclient,
                    'subclient_preferences': subclient_preferences,
                }
                if subclient_preferences:
                    if subclient_preferences.preference == 'donation':
                        return render(request, 'donationDash.html', context)
                    else:
                        return render(request, 'ticketDash.html', context)

        # If the user is a main client and not a valid subclient in session, display the main user dashboard
        # Fetch all associated subclients
        # subclients = Subclient.objects.filter(client=user)

        # Check if the main client has admin permission
        admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()
        if admin_permission_obj is not None and admin_permission_obj.login_allowed:
            serviceType = admin_permission_obj.client_service_type
            if serviceType == "commerce":
                return render(request, 'vmart.html')
            elif serviceType == "scanner":
                return render(request, 'scanner.html')
            elif serviceType == "ticket":

                return render(request, 'ticketDash.html')
            elif serviceType == "donation":

                return render(request, 'donationDash.html')
            elif serviceType == "Appointment":

                return render(request, 'appointmentDash.html')
            elif serviceType == "B_campaign":

                return render(request, 'Bcampaign.html')

            else:
                return HttpResponse("no sunch directory")
        else:
            return render(request, 'vmartHome.html')

    else:
        return render(request, 'vmartHome.html')


def donation_count(request, toUser, ClientID, donate_refer_id):
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

    matching_sent_records = ticket_billing_details.objects.filter(client_id=clientId, transaction_name=transaction_name,
                                                                  transaction_type=transaction_type)

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

    matching_records = ticket_billing_details.objects.filter(client_id=clientId, ticket_billing_id=ticket_billing_id,
                                                             transaction_name=transaction_name,
                                                             transaction_type=transaction_type)

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


def contact_info(request, url, headers, toUser, clientId, supportNumber):
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


def paid_info(request, toUser, url, headers, supportnum, donate_refer_id, ClientID):
    print("yes cursor coming here")
    all_donationInfo = donation_details.objects.filter(client_id=ClientID, donation_reference_id=donate_refer_id)
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


def pdf_display(request, donate_refer_id):
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
        paid_info(request, toUser, url, headers, supportnum, donate_refer_id, ClientID)
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
    dynamic_link = payment_link[17:]

    return JsonResponse({'success': True, 'PaymentLink': dynamic_link})


def process_donation_text_message(message, request, url, headers, toUser, clientId):
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


def process_donation_interactive_message(response_id, request, url, headers, toUser, clientId, whatsAppPhoneNumberId,
                                         faceBookToken):
    response_id_type = response_id[0]
    response_id_id = int(response_id[1:])
    print(response_id_type)
    print(response_id_id)

    if response_id_type == 'D':
        print('f')
        if response_id_id == 1:
            print('g')
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
                                    "title": "5Transactions"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "O2",
                                    "title": "MonthTransactions"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "K3",
                                    "title": "AllTransactions"
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
        # donation_ref_id = uuid.uuid4()
        # donation_details.objects.create(client_id=clientId,donation_reference_id=donation_ref_id,donar_phone_number=toUser)

        # detailslink = "https://vmart.ai" + "/N1/" + "N1" + str(donation_ref_id) + str(response_id_id) + '/' + str(clientId)
        donationTypeobj = donation_types.objects.filter(client_id=clientId, id=response_id_id)
        for dh_i in donationTypeobj:
            if dh_i.donation_type_image:
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
                                (dh_i.donation_type_image)
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
        print("please wait downloading")
        donation_ref_id = uuid.uuid4()
        donation_details.objects.create(client_id=clientId, donation_reference_id=donation_ref_id,
                                        donar_phone_number=toUser)
        infolinks = "N1/" + "N1" + str(donation_ref_id) + str(response_id_id) + '/' + str(clientId)
        print("completed")
        url = "https://graph.facebook.com/v15.0/" + str(whatsAppPhoneNumberId) + "/messages"
        headers = {
            'Authorization': 'Bearer ' + faceBookToken,
            'Content-Type': 'application/json'
        }
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
                                "text": infolinks
                            }
                        ]
                    }
                ]
            }
        })
        response = requests.request("POST", url, headers=headers, data=payload)
    elif response_id_type == "R":

        mydonationPdf = donation_details.objects.filter(client_id=clientId, id=response_id_id)
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
        mydonation = donation_details.objects.filter(donar_phone_number=toUser).order_by('donation_date',
                                                                                         'vailo_record_creation')[:5]
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


def process_health_interactive_message(response_id, request, url, headers, toUser, clientId, whatsAppPhoneNumberId,
                                       faceBookToken):
    response_id_type = response_id[0]
    response_id_id = int(response_id[1:])
    if response_id_type == 'H':
        if response_id_id == 1:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "header": {
                        "type": "text",
                        "text": "Seva Hospitals"
                    },

                    "body": {
                        "text": "_Choose your option by selecting the appropriate menu for knowing more about facilities / services available at the hospital._"
                    },
                    "footer": {
                        "text": "Main helpdesk: +91-1234567890"
                    },

                    "action": {
                        "button": "Select Option",
                        "sections": [
                            {
                                "title": "Select Option",
                                "rows": [
                                    {
                                        "id": "L1",
                                        "title": "Locate Services",
                                        "description": "Ambulance, Blood bank, Pharmacy etc"

                                    },
                                    {
                                        "id": "L2",
                                        "title": "Help Desk",
                                        "description": "Insurance, Billing,Wheel chair etc"

                                    },
                                    {
                                        "id": "L3",
                                        "title": "Appointments",
                                        "description": "Check availability and book yourself"

                                    },
                                    {
                                        "id": "L4",
                                        "title": "Patient Records",
                                        "description": "Lab reports for the patient"
                                    },
                                    {
                                        "id": "L5",
                                        "title": "Health Updates",
                                        "description": "Daily medicine chart, Dietary chart etc"

                                    },
                                    {
                                        "id": "L6",
                                        "title": "Insurance",
                                        "description": "Upload claim details, check status"

                                    },
                                    {
                                        "id": "L7",
                                        "title": "Billing/Payment",
                                        "description": "Your billing and payment details"

                                    },
                                    {
                                        "id": "L8",
                                        "title": "Reminders",
                                        "description": "Reminders from hospital, labs"

                                    },
                                    {
                                        "id": "L9",
                                        "title": "Others",
                                        "description": "More options that are available"

                                    },
                                    {
                                        "id": "L10",
                                        "title": "New",
                                        "description": "Newly updated facilities"

                                    }

                                ]
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 2:
            print("s coming")
            payload = json.dumps({
                "recipient_type": "individual",
                "messaging_product": "whatsapp",
                "to": "919739987142",
                "type": "interactive",
                "interactive": {
                    "type": "FLOW",
                    "header": {
                        "type": "text",
                        "text": "Flow message header"
                    },
                    "body": {
                        "text": "Flow message body"
                    },
                    "footer": {
                        "text": "Flow message footer"
                    },
                    "action": {
                        "name": "flow",
                        "parameters": {
                            "flow_message_version": "3",
                            "mode": "published",
                            "flow_token": "AQAAAAACS5FpgQ_cAAAAAD0QI3s.",
                            "flow_id": "338812185470512",
                            "flow_cta": "Book!",
                            "flow_action": "navigate",
                            "flow_action_payload": {
                                "screen": "<SCREEN_NAME>",
                                "data": {
                                    "product_name": "name",
                                    "product_description": "description",
                                    "product_price": 100
                                }
                            }
                        }
                    }
                }
            })
            response = requests.request("POST", url, headers=headers, data=payload)

    if response_id_type == 'L':
        if response_id_id == 1:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "header": {
                        "type": "text",
                        "text": " Seva Hospitals"
                    },

                    "body": {
                        "text": "_Choose from various options - Ambulance, Blood bank, Pharmacy, Cafeteria, Rest rooms, Wheel chair etc._"
                    },
                    "footer": {
                        "text": "Main helpdesk: +91-1234567890"
                    },

                    "action": {
                        "button": "Select Service",
                        "sections": [
                            {
                                "title": "Select Option",
                                "rows": [
                                    {
                                        "id": "S1",
                                        "title": "Ambulance",
                                        "description": "Ground floor near main reception"

                                    },
                                    {
                                        "id": "S2",
                                        "title": "Blood Bank",
                                        "description": "Building B1, Near car parking"

                                    },
                                    {
                                        "id": "S3",
                                        "title": "Pharmacy",
                                        "description": "Behind main reception desk"

                                    },
                                    {
                                        "id": "S4",
                                        "title": "Cafeteria",
                                        "description": "5th Floor - Buildings B3, B5"
                                    },
                                    {
                                        "id": "S5",
                                        "title": "Rest Rooms",
                                        "description": "Ground floor all buildings"

                                    },
                                    {
                                        "id": "S6",
                                        "title": "Wheel Chair",
                                        "description": "Opposite main reception desk"

                                    },
                                    {
                                        "id": "S7",
                                        "title": "Insurance Desk",
                                        "description": "1st Floor, Building B1"

                                    },
                                    {
                                        "id": "S8",
                                        "title": "Billing Desk",
                                        "description": "1st Floor, Building B1"

                                    }

                                ]
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
                    "type": "list",
                    "header": {
                        "type": "text",
                        "text": " Seva Hospitals"
                    },

                    "body": {
                        "text": "_Choose from various options - Ambulance, Blood bank, Pharmacy, Cafeteria, Rest rooms, Wheel chair etc._"
                    },
                    "footer": {
                        "text": "Main helpdesk: +91-1234567890"
                    },

                    "action": {
                        "button": "Select Service",
                        "sections": [
                            {
                                "title": "Select Option",
                                "rows": [
                                    {
                                        "id": "R1",
                                        "title": "Reception",
                                        "description": "Building B1 - main entrance"

                                    },
                                    {
                                        "id": "R2",
                                        "title": "Insurance Desk",
                                        "description": "1st Floor, Building B1"

                                    },
                                    {
                                        "id": "R3",
                                        "title": "Billing Desk",
                                        "description": "1st Floor, Building B1"

                                    }

                                ]
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 5:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/patient.png"
                        }
                    },

                    "body": {
                        "text": "_Your daily diet and treatment records are available including any updates and remarks from the duty nurse and concerned doctor_"
                    },
                    "footer": {
                        "text": "Mr. Ayush Kumar (36 years)"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "D1",
                                    "title": "Diet Chart"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "D2",
                                    "title": "Daily Chart"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 4:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/patient.png"
                        }
                    },

                    "body": {
                        "text": "_All your lab reports are here. When more reports are received they will get added to this report._"
                    },
                    "footer": {
                        "text": "Mr. Ayush Kumar (36 years)"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "P1",
                                    "title": "Lab Records"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 3:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/appointement.png"
                        }
                    },

                    "body": {
                        "text": "_You can schedule appointment with your doctor based on her/his availability. You will get a confirmation once doctor accepts your request._"
                    },
                    "footer": {
                        "text": "Confirmations will be sent within 4 hours"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "O1",
                                    "title": "Book Appointment"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "O2",
                                    "title": "My Appointments"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 6:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/newinsurance.png"
                        }
                    },

                    "body": {
                        "text": "_All insurances are accepted. Cashless processing will be done on all the working days. Paper processing usually takes 3-5 days turn around time._"
                    },
                    "footer": {
                        "text": "Mr. Ayush Kumar (36 years)"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "U1",
                                    "title": "Upload Claims"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "U2",
                                    "title": "Claim Status"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 7:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/billpay.png"
                        }
                    },

                    "body": {
                        "text": "_Payments are strictly to be in digital mode - either wallets, account transfer, UPI, credit/debit card. Your current balance to pay: Rs. 5290.00_"
                    },
                    "footer": {
                        "text": "Mr. Ayush Kumar (36 years)"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "B1",
                                    "title": "My Bills"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "B2",
                                    "title": "My Payments"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "B3",
                                    "title": "Pay Balance"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 8:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "interactive",
                "interactive": {
                    "type": "button",

                    "body": {
                        "text": f'*From*: Billing Desk \n'
                                f'*Sent on*: 01 Oct 2023 at 01:05 PM \n'
                                f'*Message*: Please clear your dues within 7 days. Due amount : Rs. 5290.00 \n'

                    },

                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "S1",
                                    "title": "Snooze"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "S2",
                                    "title": "Dismiss"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)

            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "interactive",
                "interactive": {
                    "type": "button",

                    "body": {
                        "text": f'*From*: Insurance Desk \n'
                                f'*Sent on*: 02 Oct 2023 at 02:05 PM \n'
                                f'*Message*: Your claim is on hold for additional documents. Please visit Insurance desk urgently \n'

                    },

                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "S1",
                                    "title": "Snooze"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "S2",
                                    "title": "Dismiss"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 9:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "preview_url": True,
                "recipient_type": "individual",
                "to": toUser,
                "type": "text",
                "text": {
                    "body": "Coming Soon"
                }

            })
            response = requests.request("POST", url, headers=headers, data=payload)

        elif response_id_id == 10:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "header": {
                        "type": "text",
                        "text": " Seva Hospitals"
                    },

                    "body": {
                        "text": "_Choose from various options - Nurology, Dental, Dermatology, Cardiology, Pulmanology etc._"
                    },
                    "footer": {
                        "text": "Main helpdesk: +91-1234567890"
                    },

                    "action": {
                        "button": "Select Service",
                        "sections": [
                            {
                                "title": "Select Option",
                                "rows": [
                                    {
                                        "id": "N1",
                                        "title": "Neurology",
                                        "description": "treatment of disorders of the nervous system"

                                    },
                                    {
                                        "id": "N2",
                                        "title": "Dental",
                                        "description": "treatment of lungs and respiratory system."

                                    },
                                    {
                                        "id": "N3",
                                        "title": "Dermatology",
                                        "description": "treatment of lungs and respiratory system"

                                    },
                                    {
                                        "id": "N4",
                                        "title": "Cardiology",
                                        "description": "treatment of lungs and respiratory system"
                                    },
                                    {
                                        "id": "N5",
                                        "title": "Pulmonology",
                                        "description": "treatment of lungs and respiratory system"

                                    }

                                ]
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)

    if response_id_type == 'N':
        if response_id_id == 1:
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
                            "link": "https://media.istockphoto.com/id/1390000431/photo/shot-of-a-mature-doctor-using-a-digital-tablet-in-a-modern-hospital.jpg?s=1024x1024&w=is&k=20&c=S0QE85ASQSpAKKrKhsC1NllJuJSpaDsv6rrHK0w_a40="
                        }
                    },

                    "body": {
                        "text": "A.Ramesh babu"
                    },
                    "footer": {
                        "text": "Neurologist"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Call Us"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Locate Us"
                                }
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
                    "header": {
                        "type": "image",
                        "image": {
                            "link": "https://media.istockphoto.com/id/1390000431/photo/shot-of-a-mature-doctor-using-a-digital-tablet-in-a-modern-hospital.jpg?s=1024x1024&w=is&k=20&c=S0QE85ASQSpAKKrKhsC1NllJuJSpaDsv6rrHK0w_a40="
                        }
                    },

                    "body": {
                        "text": "B. Suresh Babu"
                    },
                    "footer": {
                        "text": "Dentist"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Call Us"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Locate Us"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 3:
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
                            "link": "https://media.istockphoto.com/id/1390000431/photo/shot-of-a-mature-doctor-using-a-digital-tablet-in-a-modern-hospital.jpg?s=1024x1024&w=is&k=20&c=S0QE85ASQSpAKKrKhsC1NllJuJSpaDsv6rrHK0w_a40="
                        }
                    },

                    "body": {
                        "text": "C.Prakash babu"
                    },
                    "footer": {
                        "text": "Dermatologist"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Call Us"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Locate Us"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 4:
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
                            "link": "https://media.istockphoto.com/id/1390000431/photo/shot-of-a-mature-doctor-using-a-digital-tablet-in-a-modern-hospital.jpg?s=1024x1024&w=is&k=20&c=S0QE85ASQSpAKKrKhsC1NllJuJSpaDsv6rrHK0w_a40="
                        }
                    },

                    "body": {
                        "text": "D. Mukesh babu"
                    },
                    "footer": {
                        "text": "Cardiolagist"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Call Us"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Locate Us"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 5:
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
                            "link": "https://media.istockphoto.com/id/1390000431/photo/shot-of-a-mature-doctor-using-a-digital-tablet-in-a-modern-hospital.jpg?s=1024x1024&w=is&k=20&c=S0QE85ASQSpAKKrKhsC1NllJuJSpaDsv6rrHK0w_a40="
                        }
                    },

                    "body": {
                        "text": "E.Mahesh babu"
                    },
                    "footer": {
                        "text": "Pulmonologist"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Call Us"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Locate Us"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)

    if response_id_type == 'S':
        if response_id_id == 1:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/Ambulance.png"
                        }
                    },

                    "body": {
                        "text": "_Ambulances are available at the entrance of hospital campus. We can arrange additional ambulances using our partner network. Please reach out in case you are unable to find any._"
                    },
                    "footer": {
                        "text": "Time of availability: 24 x7"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Call Us"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Locate Us"
                                }
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
                    "header": {
                        "type": "image",
                        "image": {
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/BloodBank.png"
                        }
                    },

                    "body": {
                        "text": "_Blood bank accepts all blood groups. You can also collect blood for any group based on prescription_"
                    },
                    "footer": {
                        "text": "Working Hours: Mon-Sat 9AM to 1 PM  & 2 PM to 5 PM"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Call Us"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Locate Us"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 3:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/Pharmacy.png"
                        }
                    },

                    "body": {
                        "text": "_We provide medicines only upon prescription (other than general purpose medicine). In case of non availability, medicines will be made available using partner network._"
                    },
                    "footer": {
                        "text": "Working Hours: Mon-Sat 9AM to 1 PM  & 2 PM to 5 PM"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Call Us"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Locate Us"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 4:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/cafe.png"
                        }
                    },

                    "body": {
                        "text": "_Vegetarian and Non-vegetarian options available. Any special dietary needs prescribed by the doctor will be served at the bed._"
                    },
                    "footer": {
                        "text": "Timings: 8-10 AM, 12-2 PM, 4-6 PM, 7-10 PM"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Call Us"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Locate Us"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 5:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/newrestroom.png"
                        }
                    },

                    "body": {
                        "text": "_Toilets are available in all floors. Toilets with special needs are available in ground floor, Resting places are available in B1 Ground floor_"
                    },
                    "footer": {
                        "text": "Call +91-123567890 for any special needs"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Call Us"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Locate Us"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 6:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/wheelchair.png"
                        }
                    },

                    "body": {
                        "text": "_Wheel Chairs are provided on need basis and emergency purposes only. They are available in all floors as well as near the main reception area and near ambulance_"
                    },
                    "footer": {
                        "text": "Availability: 24x7"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Call Us"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Locate Us"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 7:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/insurancedesk.png"
                        }
                    },

                    "body": {
                        "text": "_All insurances are accepted. Cashless processing will be done on all the working days. Paper processing usually takes 3-5 days turn around time._"
                    },
                    "footer": {
                        "text": "Working Hours: Mon-Sat 9AM to 1 PM  & 2 PM to 5 PM"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Call Us"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Locate Us"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 8:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/bill.png"
                        }
                    },

                    "body": {
                        "text": "_Payments are strictly to be in digital mode - either wallets, account transfer, UPI, credit/debit card. Cash payment to be limited to minimum_"
                    },
                    "footer": {
                        "text": "Working Hours: Mon-Sat 9AM to 1 PM  & 2 PM to 5 PM"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Call Us"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Locate Us"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
    if response_id_type == 'R':
        if response_id_id == 1:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/reception.png"
                        }
                    },

                    "body": {
                        "text": "_Reach out to reception for general queries about admission, patient status, feedback, concerns etc._"
                    },
                    "footer": {
                        "text": "Working Hours: Mon-Sat 9AM to 1 PM  & 2 PM to 5 PM"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Phone Call"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Video Call"
                                }
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
                    "header": {
                        "type": "image",
                        "image": {
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/insurancedesk.png"
                        }
                    },

                    "body": {
                        "text": "_All insurances are accepted. Cashless processing will be done on all the working days. Paper processing usually takes 3-5 days turn around time._"
                    },
                    "footer": {
                        "text": "Working Hours: Mon-Sat 9AM to 1 PM  & 2 PM to 5 PM"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Phone Call"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Video Call"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 3:
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
                            "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/bill.png"
                        }
                    },

                    "body": {
                        "text": "_Payments are strictly to be in digital mode - either wallets, account transfer, UPI, credit/debit card. Cash payment to be limited to minimum_"
                    },
                    "footer": {
                        "text": "Working Hours: Mon-Sat 9AM to 1 PM  & 2 PM to 5 PM"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C1",
                                    "title": "Phone Call"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "C2",
                                    "title": "Video Call"
                                }
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
    if response_id_type == 'D':
        if response_id_id == 1:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "document",
                "document": {
                    "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/diet.pdf",
                    "filename": "Diet Chart"

                }

            })

            response = requests.request("POST", url, headers=headers, data=payload)
        elif response_id_id == 2:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "document",
                "document": {
                    "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/daily.pdf",
                    "filename": "Daily Chart"

                }

            })

            response = requests.request("POST", url, headers=headers, data=payload)
    if response_id_type == 'P':
        if response_id_id == 1:
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "document",
                "document": {
                    "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/Labrecord.pdf",
                    "filename": "Lab Records"

                }

            })

            response = requests.request("POST", url, headers=headers, data=payload)


def process_health_bot_message(message, response_id, messageType, request, url, headers, toUser,
                               clientId, whatsAppPhoneNumberId, faceBookToken):
    if messageType == 'text':
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "text",
            "text": {
                "body": "Welcome to seva hosiptals chat, For health care details you can opt the below options."
            },

        })
        response = requests.request("POST", url, headers=headers, data=payload)
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
                        "link": "https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/WelcomeHeaderImage/mainbuilding.png"
                    }
                },

                "body": {
                    "text": "_We are a leading multi speciality hospital in the city. Use this whatsapp bot for knowing and availing various services. You can send *hi* message at any point to this number and interact with the hospital any time._"
                },
                "footer": {
                    "text": "Seva Hospitals, Marenahalli, JP Nagar 2nd Phase, Bangalore"
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": "H1",
                                "title": "Explore"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "H2",
                                "title": "Register"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": "H3",
                                "title": "Preferences"
                            }
                        },

                    ]
                }
            }
        })

        response = requests.request("POST", url, headers=headers, data=payload)
    elif messageType == 'interactive':
        process_health_interactive_message(response_id, request, url, headers, toUser, clientId, whatsAppPhoneNumberId,
                                           faceBookToken)


def process_ticket_text_message(message, request, url, headers, toUser, clientId):
    if message == 'HI' or message == 'Hi' or message == 'hi' or message == 'hI':

        if not ticket_customer_master.objects.filter(client_id=clientId, Customer_Phone_Number=toUser).exists():
            new_customer = ticket_customer_master(client_id=clientId, Customer_Phone_Number=toUser)
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

        customer_receive(request, toUser, clientId)

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

        phone_number = "91" + phone_number.strip()

        ticketupdate = ticket_information.objects.filter(client_id=clientId, ticket_number=ticket_numbers)
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


from datetime import date as dat

# def slot_data_storing_object(obj, d_slot):
#     d_list = obj_dummy.d_slot
#
#     del obj_dummy.slot[int(time_slot[1:])]
#     # obj_j1=obj_j1_dummy
#     d_list = obj_j1_dummy.slot
#     if (len(d_list) != len(obj_j1_dummy.slot)):
#         d_list = list(set(obj_j1_dummy.slot) - set(d_list))
#         return d_list
#     else:
#         return d_list


# def slots(sl,length):
#     no_of_slots = 5
#
#     available_slots = []
#     for i in range(len(slot)):
#         available_slots.append(slot[i].strftime('%H:%M'))
#     # print(available_slots)
#     dummy_available_slots = available_slots
#     s = slot_selection(dummy_available_slots)
#     return s

import pytz


def process_appointement_interactive_message(response_id, request, url, headers, toUser, clientId,
                                             whatsAppPhoneNumberId,
                                             faceBookToken, list_title, project):
    consultant_name = ''
    response_id_type = response_id[0]
    resp_id_id = int(response_id[1])
    print("length of response_id", len(response_id))
    from datetime import datetime
    if project == 'Appointment':
        print('dvds')
        consultant_name = ''
        response_id_type = response_id[0]
        resp_id_id = int(response_id[1])
        print("length of response_id", len(response_id))

        # response_id_type_1=0
        # resp_id_id_1=0
        # if len(response_id) == 4:
        #     response_id_type_1 = response_id[2]
        #     resp_id_id_1 = int(response_id[3])
        #     print(response_id_type_1)
        #     print(resp_id_id_1)
        # slot_list = []

        class Count:
            count = 0

        # response_id_pos = int(response_id[-1])

        print(response_id_type)
        print(resp_id_id)

        if response_id_type == 'T':
            # General Doctor, Cardiology,eye care
            if resp_id_id == 1:
                mainobj = appointment_settings.objects.filter(client_id=clientId)
                print(len(mainobj))
                for m_i in mainobj:

                    consultant_specialization = []
                    consultant_id = []
                    consultantDetails = Consultant_details.objects.filter(client_id=clientId)
                    for c_i in consultantDetails:
                        consultant_id.append(c_i.id)
                        consultant_specialization.append(c_i.consultant_specialization)

                    # Consultants_type = ["General Care", "Cardiology", "Eye care"]

                    dummy_consultant_specialization = []
                    for i in consultant_specialization:
                        if i not in dummy_consultant_specialization:
                            dummy_consultant_specialization.append(i)

                    consultant_department_list = []
                    print(consultant_specialization)
                    for i in range(len(dummy_consultant_specialization)):
                        consultant_department_list.append({"id": "H" + str(i),
                                                           "title": dummy_consultant_specialization[i],

                                                           })
                    if len(consultant_specialization) == 1:
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
                                                "title": c_i.consultant_specialization
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
                                    "text": "Choose the Consulting department"
                                },

                                "action": {
                                    "button": "Choose Department",
                                    "sections": [
                                        {
                                            "title": "Consultants",
                                            "rows": consultant_department_list
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
                #             "text": "Select the consulting department"
                #         },
                #         "action": {
                #             "button": "Choose Department",
                #             "sections": [
                #                 {
                #                     "title": "<LIST_SECTION_1_TITLE>",
                #                     "rows": [
                #                         {
                #                             "id": "A1",
                #                             "title": Consultants_type[0],
                #
                #                         },
                #                         {
                #                             "id": "A2",
                #                             "title": Consultants_type[1],
                #
                #                         },
                #                         {
                #                             "id": "A3",
                #                             "title": Consultants_type[2],
                #                         },
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
                #         "action": {
                #             "buttons": [
                #                 {
                #                     "type": "reply",
                #                     "reply": {
                #                         "for j in range(len(Consultants_type)):"
                #                         "id": "A" + str(j)
                #
                #                     }
                #                 }
                #
                #             ]
                #         }
                #     }
                # })

                # response = requests.request("POST", url, headers=headers, data=payload)

                # mainobj = Main_settings.objects.filter(client_id=clientId)
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
                #         consultantlist.append({"id": "N" + str(consultant_id[i]),
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
                #                                 "id": "A" + str(consultant_id[0]),
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

                # else:
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
            elif resp_id_id == 3:
                Existing_Bookings = appointment_bookings.objects.filter(client_id=clientId)
                if (Existing_Bookings):
                    for i in Existing_Bookings:
                        current = datetime.today()
                        india_timezone = pytz.timezone("Asia/Kolkata")
                        current_time = datetime.now(india_timezone)
                        print(current)

                        currentdate = current.strftime("%d-%m-%Y")
                        current_time = current_time.strftime("%H:%M")
                        print(current_time, currentdate)
                        time = datetime.strptime(str(current_time), '%H:%M')
                        date_obj = datetime.strptime(currentdate, "%d-%m-%Y")
                        print(time.time())
                        print(date_obj.date())
                        # india_timezone = pytz.timezone("Asia/Kolkata")
                        #
                        # # Get the current time in the India time zone
                        # current_time = datetime.now(india_timezone)
                        #
                        # # Extract the time component as a datetime.time object
                        # time_component = current_time.time()
                        #
                        # print(time_component)
                        print(i.date, i.start_time)
                        print(date_obj.date(), time.time())
                        print(i.date >= date_obj.date())
                        print(i.start_time >= time.time())
                        print(date_obj.date(), time.time())
                        if (i.date >= date_obj.date()):
                            print("hello")
                            print("hi")
                            hours, minute, seconds = str(i.start_time).split(':')
                            start_time = hours + ':' + minute
                            hours, minute, seconds = str(i.end_time).split(':')
                            end_time = hours + ':' + minute
                            print(i.id, i.Consultant_settings_id)
                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "button",
                                    "body": {
                                        "text": f'*_Consultant Name_*: {i.Consultant_details.consultant_name}\n'
                                                f'*_Consultant specialization_*: {i.Consultant_details.consultant_specialization}\n'
                                                f'*_Date of Appointment_*: {str(i.date)}\n'
                                                f'*_Slot_*: {start_time} to {end_time}\n'
                                                f'*_Mode_*: {i.online_offline}'

                                    },
                                    "action": {
                                        "buttons": [
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "b" + str(i.id),
                                                    "title": "Cancel"
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
                        "type": "text",
                        "text": {
                            "body": "There in no appointements booked..Please book the appointements."
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)


            elif resp_id_id == 2:

                Existing_Bookings = appointment_bookings.objects.filter(client_id=clientId)
                if (Existing_Bookings):
                    for i in Existing_Bookings:
                        current = datetime.today()
                        india_timezone = pytz.timezone("Asia/Kolkata")
                        current_time = datetime.now(india_timezone)
                        print(current)

                        currentdate = current.strftime("%d-%m-%Y")
                        current_time = current_time.strftime("%H:%M")
                        print(current_time, currentdate)
                        time = datetime.strptime(str(current_time), '%H:%M')
                        date_obj = datetime.strptime(currentdate, "%d-%m-%Y")
                        print(time.time())
                        print(date_obj.date())
                        # india_timezone = pytz.timezone("Asia/Kolkata")
                        #
                        # # Get the current time in the India time zone
                        # current_time = datetime.now(india_timezone)
                        #
                        # # Extract the time component as a datetime.time object
                        # time_component = current_time.time()
                        #
                        # print(time_component)
                        print(i.date, i.start_time)
                        print(date_obj.date(), time.time())
                        print(i.date >= date_obj.date())
                        print(i.start_time >= time.time())
                        print(date_obj.date(), time.time())
                        if (i.date >= date_obj.date()):
                            print("hello")
                            print("hi")
                            hours, minute, seconds = str(i.start_time).split(':')
                            start_time = hours + ':' + minute
                            hours, minute, seconds = str(i.end_time).split(':')
                            end_time = hours + ':' + minute
                            print(i.id, i.Consultant_settings_id)
                            payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": toUser,
                                "type": "interactive",
                                "interactive": {
                                    "type": "button",
                                    "body": {
                                        "text": f'*_Consultant Name_*: {i.Consultant_details.consultant_name}\n'
                                                f'*_Consultant specialization_*: {i.Consultant_details.consultant_specialization}\n'
                                                f'*_Date of Appointment_*: {str(i.date)}\n'
                                                f'*_Slot_*: {start_time} to {end_time}\n'
                                                f'*_Mode_*: {i.online_offline}'

                                    },
                                    "action": {
                                        "buttons": [
                                            {
                                                "type": "reply",
                                                "reply": {
                                                    "id": "R" + str(i.id),
                                                    "title": "Reschedule"
                                                }
                                            },
                                        ]
                                    }
                                }

                            })
                            response = requests.request("POST", url, headers=headers, data=payload)

                        # if(i.start_time>=time.time()):

                # mainobj = Main_settings.objects.filter(client_id=clientId)
                # for f_i in mainobj:
                #     payload = json.dumps({
                #         "messaging_product": "whatsapp",
                #         "recipient_type": "individual",
                #         "to": toUser,
                #         "type": "interactive",
                #         "interactive": {
                #             "type": "button",
                #             "header": {
                #                 "type": "image",
                #                 "image": {
                #                     "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
                #                     (f_i.contactus_image)
                #                 }
                #             },
                #
                #             "body": {
                #                 "text": f_i.contactus_description
                #             },
                #
                #             "action": {
                #                 "buttons": [
                #                     {
                #                         "type": "reply",
                #                         "reply": {
                #                             "id": "Z1",
                #                             "title": "LocateUs"
                #                         }
                #                     },
                #                     {
                #                         "type": "reply",
                #                         "reply": {
                #                             "id": "Z2",
                #                             "title": "Call US"
                #                         }
                #                     }
                #
                #                 ]
                #             }
                #         }
                #     })
                #
                #     response = requests.request("POST", url, headers=headers, data=payload)

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


        elif response_id_type == 'H':
            mainobj = appointment_settings.objects.filter(client_id=clientId)
            print(len(mainobj))

            for m_i in mainobj:
                all_consultant_Name = []
                consultant_specialization = []
                consultant_id = []
                consultantDetails = Consultant_details.objects.filter(client_id=clientId)
                for c_i in consultantDetails:
                    consultant_id.append(c_i.id)
                    all_consultant_Name.append(c_i.consultant_name)
                    consultant_specialization.append(c_i.consultant_specialization)

                # Consultants_type = ["General Care", "Cardiology", "Eye care"]
                dumy_list = []
                for i in consultant_specialization:
                    if i not in dumy_list:
                        dumy_list.append(i)
                consultant_specialization = dumy_list
                # consultantDetails is either (general doctor-1,2 or cardiolgist- 1,2 or eye care-1,2)
                consultantDetails_1 = Consultant_details.objects.filter(client_id=clientId,
                                                                         consultant_specialization=
                                                                         consultant_specialization[resp_id_id])
                print("consultantDetails:", consultantDetails)
                consultantName_id = []
                for i in consultantDetails_1:
                    consultantName_id.append((i.consultant_name, i.id, i.consultant_details))
                consultantlist = []

                print(consultantName_id, consultantName_id[0][1], consultantName_id[1][1], consultantName_id[0][0],
                      consultantName_id[1][0])
                for i in range(len(consultantName_id)):
                    consultantlist.append({"id": 'I' + str(consultantName_id[i][1]),
                                           "title": consultantName_id[i][0],
                                           "description": f'exp: {consultantName_id[i][2]}'

                                           })
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "list",
                        "body": {
                            "text": "Choose the Consultant"
                        },

                        "action": {
                            "button": "Choose Specialist",
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

          
        # general doctor dates j,R
        elif response_id_type == 'I':
            response_id_id = int(response_id[1:])
            print(response_id_type, response_id_id)

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
                # print("slotDuration",slotDuration.slot_duration)
                for s_i in slotDuration:
                    duration_str = s_i.slot_duration
                    print("duration_str", duration_str)
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
                        print("all_slots", all_slots)
                final_all_slots = [slot for slot in all_slots if slot not in hslots]
                # print("final_all_slots",final_all_slots)
                print("channi")
                print("final_all_slots", final_all_slots)
                print("length of final_all_slots", len(final_all_slots))
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

               

            len_all_slots = []
            print("exdate:", ex_date)
            for i, date in enumerate(ex_date):
                avlslots = len(all_available_slots[i])
                print(avlslots)
                formateedDate = ''
                if avlslots != 0 and avlslots <= 10:
                    print("ifcondition")
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
            print("show_avl_slots", show_avl_slots)
            print("show_date", show_date)
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
                    "body": {
                        "text": "What is your preferred date to schedule the appointment?"
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
     
       # cancel appointement
        elif response_id_type == 'b':
            print('Hello')
            existing_bookings = appointment_bookings.objects.filter(id=int(response_id[1:]))
            existing_bookings.delete()
            print("successfully cancelled your Booking")
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "preview_url": True,
                "recipient_type": "individual",
                "to": toUser,
                "type": "text",
                "text": {
                    "body": 'Appointment cancelled successfully'

                }

            })
            response = requests.request("POST", url, headers=headers, data=payload)

            # for i in existing_bookings:
            #     availability=availability(
            #         consultant_name=i.Consultant_settings.consultant_name,
            #         consultant_specialization=i.Consultant_settings.consultant_specialization,
            #
            #
            #     )




        elif response_id_type == 'R':
            print('Hello')
            existing_bookings = appointment_bookings.objects.filter(id=int(response_id[1:]))
            for i in existing_bookings:
                print(i.Consultant_details.consultant_name)
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": f"Your appointment Cancelled.\nYou can reschedule your slot with *_{i.Consultant_details.consultant_name}_*"
                        },

                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "I" + str(i.Consultant_settings_id),
                                        "title": "Reschedule",
                                    },
                                },
                            ]

                        }
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
                existing_bookings.delete()
                print("Booking cancelled since they ")

            # existing_bookings.delete()

            # elif resp_id_id == 2:
            #     # slot = [time(10, 00), time(10, 30), time(11, 00), time(11, 30), time(12, 00)]
            #     # for i in range(len(General_doctors_list)):
            #     #     row = {
            #     #         "id": "I" + str(i + 1),
            #     #         "title": General_doctors_list[i],
            #     #         "description": f'{str(calculateExperience(joining_date_list[i]))} years',
            #     #     }
            #     # rows.append(row)
            #     dummmy_rows = available_dates()
            #     rows = []
            #     for i in range(len(rows)):
            #         row = {
            #             "id": "R" + str(i + 1),
            #             "title": dummmy_rows[i]
            #         }
            #         rows.append(row)
            #     payload = json.dumps({
            #         "messaging_product": "whatsapp",
            #         "recipient_type": "individual",
            #         "to": toUser,
            #         "type": "interactive",
            #         "interactive": {
            #             "type": "list",
            #
            #             "body": {
            #                 "text": "Please select the doctor you want to schedule an appointment with"
            #             },
            #             "action": {
            #                 "button": "Choose Dates",
            #                 "sections": [
            #                     {
            #                         "title": "Dates",
            #                         "rows": rows,
            #                     }
            #
            #                 ]
            #             }
            #         }
            #     })
            #
            #     response = requests.request("POST", url, headers=headers, data=payload)
        # Mode of consultation message general doctor-2

        # cardilogy dates r,h
        # elif response_id_type == 'i':
        #     if resp_id_id == 0:
        #         dummmy_rows = available_dates()
        #         rows=[]
        #         for i in range(len(dummmy_rows)):
        #             row={
        #                 "id": "r"+str(i+1),
        #                 "title": dummmy_rows[i],
        #             }
        #             rows.append(row)
        #         payload = json.dumps({
        #             "messaging_product": "whatsapp",
        #             "recipient_type": "individual",
        #             "to": toUser,
        #             "type": "interactive",
        #             "interactive": {
        #                 "type": "list",

        #                 "body": {
        #                     "text": "What is your preferred date to schedule the appointment?"
        #                 },
        #                 "action": {
        #                     "button": "Choose Dates",
        #                     "sections": [
        #                         {
        #                             "title": "Dates",
        #                             "rows": rows,
        #                         }

        #                     ]
        #                 }
        #             }
        #         })

        #         response = requests.request("POST", url, headers=headers, data=payload)
        #     elif resp_id_id == 1:
        #         dummmy_rows = available_dates()
        #         rows=[]
        #         for i in range(len(dummmy_rows)):
        #             row={
        #                 "id": "H"+str(i),
        #                 "title": dummmy_rows[i],
        #             }
        #             rows.append(row)
        #         payload = json.dumps({
        #             "messaging_product": "whatsapp",
        #             "recipient_type": "individual",
        #             "to": toUser,
        #             "type": "interactive",
        #             "interactive": {
        #                 "type": "list",

        #                 "body": {
        #                     "text": "What is your preferred date to schedule the appointment?"
        #                 },
        #                 "action": {
        #                     "button": "Choose Dates",
        #                     "sections": [
        #                         {
        #                             "title": "Dates",
        #                             "rows": rows,
        #                         }

        #                     ]
        #                 }
        #             }
        #         })

        #         response = requests.request("POST", url, headers=headers, data=payload)

        # get directions and locate us Z1,Z2
        elif response_id_type == 'e':
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
                        "text": "If you need any help in future, just type Hi or Help."
                                "We will be happy to assist you."
                    },

                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "Z1",
                                    "title": "GET DIRECTIONS",
                                },
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "Z2",
                                    "title": "CONTACT US",
                                },
                            }
                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        # confirmation messaage
        elif response_id_type == 'm':
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "text",
                "text": {
                    "body": "Your appointment is scheduled with doctor1."
                            "Thank you for consulting ------hospital."
                }

            })
            response = requests.request("POST", url, headers=headers, data=payload)










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

                availablityObject = Consultant_availablity.objects.filter(client_id=clientId,
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
                print(formatted_duation_create)
                formatted_start_slot_create = f"{slot_start}"
                formatted_end_slot_create = f"{slot_end}"
                date_formate_start_slot_create = datetime.strptime(formatted_start_slot_create, "%H:%M")
                formatted_slot_start__time = date_formate_start_slot_create.strftime("%I:%M %p")
                date_formate_end__slot_create = datetime.strptime(formatted_end_slot_create, "%H:%M")
                formatted_slot_end__time = date_formate_end__slot_create.strftime("%I:%M %p")
                formatted_slots_details.append(f'{formatted_slot_start__time} - {formatted_slot_end__time}')
                formatted_duration_details.append(formatted_duation_create)

            for i in range(len(formatted_slots_details)):
                list_all_data.append({"id": "S" + str(consult_id) + "/" + str(
                    visitor_id) + "//" + str(finalDates[0]) + str(formatted_duration_details[i]) + str(i),
                                      "title": str(formatted_slots_details[i])

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
                    "body": {
                        "text": "Choose your preferred time "
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
            # booking_ref_id = uuid.uuid4()
            Components = response_id.split("/")
            Components = str(Components[0][1:]) + str(Components[1:])
            print("componenets", Components)
            input_str = Components  # "109['110', '', '0411202306:00-07:000']"
            # Split the string by the first '[' character
            split_str = input_str.split("[")
            # Process the first part, which is '8', and then split the second part by commas
            first_part = [split_str[0].strip()]
            second_part = split_str[1].strip(" '[]").split(",")

            # Combine both parts to create the final list
            result_list = first_part + second_part
            lis = []
            a = ''
            print(result_list)
            for i, value in enumerate(result_list):

                for j in value:

                    if j == "'" or j == ' ' or j == "''" or j == "'" or j == " ":
                        value = value.replace(j, '')

                result_list[i] = value
            print(result_list)
            ConsultantId = int(result_list[0])
            print(ConsultantId)
            consultantDetails = Consultant_details.objects.filter(client_id=clientId, id=ConsultantId)

            Consultation_Mode_list = ["Video call", "In Person"]
            Consultation_Mode = []
            for j in consultantDetails:
                print(j.consultant_fee)
                for i in range(len(Consultation_Mode_list)):
                    row = {
                        "id": "a" + str(i) + str(Components),
                        "title": Consultation_Mode_list[i] + f' (Rs.{str(j.consultant_fee)})'}
                    Consultation_Mode.append(row)

            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "body": {
                        "text": "Choose your preferred Mode of Consultation "
                    },

                    "action": {
                        "button": "Mode",
                        "sections": [
                            {
                                "title": "Consultation_Mode",
                                "rows": Consultation_Mode
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
            print("end of payload in consultation mode")
            print(response)
        elif response_id_type == 'a':
            print("response_id", response_id[2:])
            if resp_id_id == 0:
                print("acoming")
                print(response_id, response_id[2:])  # 1['3', '', '0811202310:30-11:001']
                index = int(response_id[2])
                input_str = response_id[2:]  # "109['110', '', '0411202306:00-07:000']"

                # Split the string by the first '[' character
                split_str = input_str.split("[")

                # Process the first part, which is '8', and then split the second part by commas

                first_part = [split_str[0].strip()]
                second_part = split_str[1].strip(" '[]").split(",")

                # Combine both parts to create the final list
                result_list = first_part + second_part
                lis = []
                a = ''
                print(result_list)
                for i, value in enumerate(result_list):

                    for j in value:

                        if j == "'" or j == ' ' or j == "''" or j == "'" or j == " ":
                            value = value.replace(j, '')

                    result_list[i] = value
                print(result_list)

                Components = result_list
                print("Components", Components)

                ConsultantId = Components[0]
                print("ConsultantId", ConsultantId)  # Remove the leading 's'
                VisitorId = Components[1]
                # print("Components[0],Components[3],Components[6][:8]", Components[0], Components[3], Components[6][:8])
                sdate = Components[3]
                day = sdate[:2]
                month = sdate[2:4]
                year = sdate[4:8]
                fdate = f'{day}/{month}/{year}'
                print(fdate)
                date_obj = datetime.strptime(fdate, "%d/%m/%Y")
                gdate = date_obj.strftime("%Y-%m-%d")
                duration = sdate[8:19]

                print(duration.split('-'))
                # dpart = duration[11:]
                # print(dpart)
                start_time_str, end_time_str = duration.split('-')
                print("start_time_str,end_time_str,typeofend_time_str", start_time_str, end_time_str,
                      type(end_time_str))
                full_start_time = datetime.strptime(start_time_str, '%H:%M')
                start_time = full_start_time.strftime("%H:%M %p")
                print("starttime", start_time)
                full_end_time = datetime.strptime(end_time_str, '%H:%M')
                end_time = full_end_time.strftime("%H:%M %p")
                status_obj = Consultant_details.objects.filter(id=ConsultantId)
                print(" I am in mode of consultation")

                approval_mode = ''
                for a_i in status_obj:
                    approval_mode = a_i.approval_mode
                print(approval_mode)
                if approval_mode == 'Automatic' or approval_mode == 'automatic':
                    print("s automatic")

                    consultantDetails = Consultant_details.objects.filter(client_id=clientId, id=ConsultantId)

                    for i in consultantDetails:
                        print(i.consultant_name, i.consultant_specialization)
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "button",

                                "header": {
                                    "type": "text",
                                    "text": 'Please confirm your appointment'
                                },

                                "body": {
                                    "text": f'*_Name_*: {i.consultant_name}\n'
                                            f'*_Specialization_*: {i.consultant_specialization}\n'
                                            f'*_Date_*:{fdate}\n'
                                            f'*_From_*: {start_time} *_to_* {end_time}'

                                },

                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "D1" + response_id[1:],
                                                "title": "Confirm"
                                            }
                                        },
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "D2",
                                                "title": "Cancel"

                                            }
                                        },

                                    ]
                                }
                            }
                        })
                        response = requests.request("POST", url, headers=headers, data=payload)
                        # if i.id==ConsultantId:
                        #     print("hi")
                        #     consultantname=i.consultant_name
                        #     consultantspecialization=i.consultant_specialization
                        #     print(consultantname, consultantspecialization)

                        # for c_i in consultantDetails:
                        #     consultant_id.append(c_i.id)
                        #     all_consultant_Name.append(c_i.consultant_name)
                        #     consultant_specialization.append(c_i.consultant_specialization)
                    # consultantName=Consultant_settings.objects.filter(client_id=clientId,consultant_name=ConsultantId)
                    # print(consultantName)

                    # booking = Bookings(
                    #     client_id=clientId,
                    #     Visitor_id=VisitorId,
                    #     Consultant_settings_id=ConsultantId,
                    #     date=gdate,
                    #     start_time=start_time,
                    #     end_time=end_time,
                    #     status=1,
                    #     booking_reference_id=booking_ref_id,
                    #     customer_phone_number=toUser,
                    #     online_offline='offline'
                    #
                    # )
                    # booking.save()
                    print("successfully created one record in bookings")
                    # showDetails = Bookings.objects.filter(client_id=clientId, booking_reference_id=booking_ref_id)
                    # for s_i in showDetails:
                    #     duration_start = s_i.start_time
                    #     duration_end = s_i.end_time
                    #     # start_time_obj1 = datetime.strptime(str(duration_start), "%H:%M")
                    #     # end_time_obj1 = datetime.strptime(str(duration_end), "%H:%M")
                    #     formatted_start_time1 = duration_start.strftime("%I:%M%p")
                    #     formatted_end_time1 = duration_end.strftime("%I:%M%p")
                    #     date = s_i.date
                    #     date_obj = datetime.strptime(str(date), '%Y-%m-%d')
                    #     New_date = date_obj.strftime('%d-%b-%Y')
                    #     status = "Booked" if s_i.status == 1 else "blocked"
                    #     detailsObj = Consultant_settings.objects.filter(id=s_i.Consultant_settings_id)
                    #     consultantName = ''
                    #     specialization = ''
                    #     consultantImage = ''
                    #     for d_i in detailsObj:
                    #         consultantName = d_i.consultant_name
                    #         specialization = d_i.consultant_specialization
                    #         consultantImage = d_i.consultant_image
                    #
                    #     print("print")
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
            elif resp_id_id == 1:
                print("acoming")
                print(response_id, response_id[1:])  # 1['3', '', '0811202310:30-11:001']

                input_str = response_id[2:]  # "109['110', '', '0411202306:00-07:000']"

                # Split the string by the first '[' character
                split_str = input_str.split("[")

                # Process the first part, which is '8', and then split the second part by commas

                first_part = [split_str[0].strip()]
                second_part = split_str[1].strip(" '[]").split(",")

                # Combine both parts to create the final list
                result_list = first_part + second_part
                lis = []
                a = ''
                print(result_list)
                for i, value in enumerate(result_list):

                    for j in value:

                        if j == "'" or j == ' ' or j == "''" or j == "'" or j == " ":
                            value = value.replace(j, '')

                    result_list[i] = value
                print(result_list)

                Components = result_list
                ConsultantId = Components[0]
                VisitorId = Components[1]
                # print("Components[0],Components[3],Components[6][:8]", Components[0], Components[3], Components[6][:8])
                sdate = Components[3]
                day = sdate[:2]
                month = sdate[2:4]
                year = sdate[4:8]
                fdate = f'{day}/{month}/{year}'
                print(fdate)
                date_obj = datetime.strptime(fdate, "%d/%m/%Y")
                gdate = date_obj.strftime("%Y-%m-%d")
                duration = sdate[8:19]
                print(duration.split('-'))
                # dpart = duration[11:]
                # print(dpart)
                start_time_str, end_time_str = duration.split('-')
                print("start_time_str,end_time_str,typeofend_time_str", start_time_str, end_time_str,
                      type(end_time_str))
                full_start_time = datetime.strptime(start_time_str, '%H:%M')
                start_time = full_start_time.strftime("%H:%M %p")
                print("starttime", start_time)
                full_end_time = datetime.strptime(end_time_str, '%H:%M')
                end_time = full_end_time.strftime("%H:%M %p")
                status_obj = Consultant_details.objects.filter(id=ConsultantId)
                print(" I am in mode of consultation")

                approval_mode = ''
                for a_i in status_obj:
                    approval_mode = a_i.approval_mode
                print(approval_mode)
                if approval_mode == 'Automatic' or approval_mode == 'automatic':
                    print("s automatic")

                    consultantDetails = Consultant_details.objects.filter(client_id=clientId, id=ConsultantId)

                    for i in consultantDetails:
                        print(i.consultant_name, i.consultant_specialization)
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "button",

                                "header": {
                                    "type": "text",
                                    "text": 'Please confirm your appointment'
                                },

                                "body": {
                                    "text": f'*_Name_*: {i.consultant_name}\n'
                                            f'*_Specialization_*: {i.consultant_specialization}\n'
                                            f'*_Date_*:{fdate}\n'
                                            f'*_From_*: {start_time} *_to_* {end_time}'

                                },

                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "D1" + response_id[1:],
                                                "title": "Confirm"
                                            }
                                        },
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "D2",
                                                "title": "Cancel"

                                            }
                                        },

                                    ]
                                }
                            }
                        })
                        response = requests.request("POST", url, headers=headers, data=payload)
                        # if i.id==ConsultantId:
                        #     print("hi")
                        #     consultantname=i.consultant_name
                        #     consultantspecialization=i.consultant_specialization
                        #     print(consultantname, consultantspecialization)

                        # for c_i in consultantDetails:
                        #     consultant_id.append(c_i.id)
                        #     all_consultant_Name.append(c_i.consultant_name)
                        #     consultant_specialization.append(c_i.consultant_specialization)
                    # consultantName=Consultant_settings.objects.filter(client_id=clientId,consultant_name=ConsultantId)
                    # print(consultantName)

                    # booking = Bookings(
                    #     client_id=clientId,
                    #     Visitor_id=VisitorId,
                    #     Consultant_settings_id=ConsultantId,
                    #     date=gdate,
                    #     start_time=start_time,
                    #     end_time=end_time,
                    #     status=1,
                    #     booking_reference_id=booking_ref_id,
                    #     customer_phone_number=toUser,
                    #     online_offline='offline'
                    #
                    # )
                    # booking.save()
                    print("successfully created one record in bookings")
                    # showDetails = Bookings.objects.filter(client_id=clientId, booking_reference_id=booking_ref_id)
                    # for s_i in showDetails:
                    #     duration_start = s_i.start_time
                    #     duration_end = s_i.end_time
                    #     # start_time_obj1 = datetime.strptime(str(duration_start), "%H:%M")
                    #     # end_time_obj1 = datetime.strptime(str(duration_end), "%H:%M")
                    #     formatted_start_time1 = duration_start.strftime("%I:%M%p")
                    #     formatted_end_time1 = duration_end.strftime("%I:%M%p")
                    #     date = s_i.date
                    #     date_obj = datetime.strptime(str(date), '%Y-%m-%d')
                    #     New_date = date_obj.strftime('%d-%b-%Y')
                    #     status = "Booked" if s_i.status == 1 else "blocked"
                    #     detailsObj = Consultant_settings.objects.filter(id=s_i.Consultant_settings_id)
                    #     consultantName = ''
                    #     specialization = ''
                    #     consultantImage = ''
                    #     for d_i in detailsObj:
                    #         consultantName = d_i.consultant_name
                    #         specialization = d_i.consultant_specialization
                    #         consultantImage = d_i.consultant_image
                    #
                    #     print("print")




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
            consulta_id = response_id[x + 1:]
            main_available_slots = []
            next_date = datetime.strptime(str(next_date), "%Y-%m-%d").date()
            next_day = next_date + timedelta(days=1)
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
            if resp_id_id == 1:
                print(response_id[1], response_id[2])
                print(response_id, response_id[2:])  # 1['3', '', '0811202310:30-11:001']
                booking_ref_id = uuid.uuid4()
                input_str = response_id[2:]  # "109['110', '', '0411202306:00-07:000']"

                # Split the string by the first '[' character
                split_str = input_str.split("[")

                # Process the first part, which is '8', and then split the second part by commas

                first_part = [split_str[0].strip()]
                second_part = split_str[1].strip(" '[]").split(",")

                # Combine both parts to create the final list
                result_list = first_part + second_part
                lis = []
                a = ''
                print(result_list)
                for i, value in enumerate(result_list):

                    for j in value:

                        if j == "'" or j == ' ' or j == "''" or j == "'" or j == " ":
                            value = value.replace(j, '')

                    result_list[i] = value
                print(result_list)

                Components = result_list
                print("components", Components)  # ['09', '10', '', '0411202306:00-07:000'
                ConsultantId = Components[0][1:]
                Mode = Components[0][0]

                # for i, value in enumerate(str(Components[0])):  # Remove the leading 's'
                #     if Mode == str(resp_id_id):
                #         ConsultantId = int(Components[0][i:])
                #         print("consultant_id in for")
                #         print(ConsultantId)
                #         break
                #     else:
                #         Mode += value
                #         print("Mode in",Mode)
                # Mode=int(Mode)
                # print("Mode out",Mode)

                # ConsultantId = Components[0]
                print("ConsultantId", ConsultantId)  # Remove the leading 's'
                VisitorId = Components[1]
                # print("Components[0],Components[3],Components[6][:8]", Components[0], Components[3], Components[6][:8])
                sdate = Components[3]
                day = sdate[:2]
                month = sdate[2:4]
                year = sdate[4:8]
                fdate = f'{day}/{month}/{year}'
                print(fdate)

                date_obj = datetime.strptime(fdate, "%d/%m/%Y")
                gdate = date_obj.strftime("%Y-%m-%d")
                duration = sdate[8:19]
                print(duration.split('-'))
                # dpart = duration[11:]
                print("gdate:", gdate)
                # dpart = duration[11:]
                # print(dpart)
                start_time_str, end_time_str = duration.split('-')
                start_time = datetime.strptime(start_time_str.strip(), '%H:%M')
                end_time = datetime.strptime(end_time_str.strip(), '%H:%M')
                status_obj = Consultant_details.objects.filter(id=ConsultantId)
                print(" I am in mode of consultation")

                if response_id[2] == '0':
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
                        online_offline="Video call"

                    )
                    booking.save()
                elif response_id[2] == '1':
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
                        online_offline="In Person"

                    )
                    booking.save()

                    # booking = Bookings(
                    #           client_id=clientId,
                    #           Visitor_id=VisitorId,
                    #           Consultant_settings_id=ConsultantId,
                    #           date=gdate,
                    #           start_time=start_time,
                    #           end_time=end_time,
                    #           status=1,
                    #           booking_reference_id=booking_ref_id,
                    #           customer_phone_number=toUser,
                    #           online_offline=mode
                    #
                    #
                    # )
                    # booking.save()

                consultantDetails = Consultant_details.objects.filter(client_id=clientId, id=ConsultantId)

                for i in consultantDetails:
                    print(i.consultant_name, i.consultant_specialization)
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "preview_url": True,
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "text",
                        "text": {
                            "body": f"Appointment scheduled with *_{i.consultant_name}_*\n"
                                    "Thank you for consulting Seva hospital."
                        }

                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "button",
                            "body": {
                                "text": "If you need any help in future, just type Hi or Help."
                                        "We will be happy to assist you."
                            },

                            "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "Z1",
                                            "title": "Get Directions"
                                        }
                                    },
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "Z2",
                                            "title": "Contact US"
                                        }
                                    }

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)

            elif resp_id_id == 2:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "preview_url": True,
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": 'Appointment cancelled successfully'

                    }

                })
                response = requests.request("POST", url, headers=headers, data=payload)
                # mainobj = Main_settings.objects.filter(client_id=clientId)
                # for f_i in mainobj:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": "If you need any help in future, just type Hi or Help."
                                    "We will be happy to assist you."
                        },

                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "Z1",
                                        "title": "Get Directions"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "Z2",
                                        "title": "Contact US"
                                    }
                                }

                            ]
                        }
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
                bookings = appointment_bookings.objects.filter(Consultant_settings_id=consultantId, date=day)
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
                                            "id": "L" + str(m_i.Consultant_settings_id),
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
                                    "id": "G" + str(l_consult_id),
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
                            "latitude": "0",
                            "longitude": "0",
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
                        "body": "Please Call 18001800 to Contact Hospital Management...."
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)
    elif project == 'servicenow':
        if response_id_type == 'T':
            if resp_id_id == 1:
                print(response_id[2:])
                print("T1")
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        "body": {
                            "text": "Create or Post your ticket"
                        },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "navigate",
                                "flow_token": f"{response_id[2:]}",  # erwers
                                "flow_id": "232812866496469",
                                "flow_cta": "Create New Ticket",
                                "flow_action_payload": {
                                    "screen": "Create_new_ticket",
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
                print(response.status_code, response)
                if response.status_code == 200:
                    print("Request was successful")
            elif resp_id_id == 2:
                print("T2")
                print(response_id[2:])
                import base64
                import datetime

                encoded_string = response_id[2:]
                decoded_bytes = base64.b64decode(encoded_string)
                decoded_string = decoded_bytes.decode('utf-8')
                print(decoded_string)
                username, password = decoded_string.split(':')
                print(username)
                print(password)
                url = f"https://dev164889.service-now.com/api/now/table/incident?sysparm_query=caller_id.user_name%3D{username}^active=true&sysparm_fields=number%2Curgency%2Cimpact%2Csys_created_by%2Csys_updated_by%2Cpriority%2Cstate^%2Cactive%2Copened_at%2Csys_id%2Cshort_description%2Csys_created_on"
                headers = {
                    "Authorization": "Basic " + response_id[2:],
                }
                response = requests.get(url, headers=headers)

                print(response.text, response.status_code)
                response_json = response.json()
                result = response_json.get('result')
                print("length: ", len(result))
                print(result[0]['sys_created_on'], type(result[0]['sys_created_on']))
                result.sort(reverse=True, key=lambda x: x['sys_created_on'])
                print(result)

                sys_created_on_list = []
                for i, j in enumerate(result):
                    if i < 10:
                        sys_created_on_list.append(j)
                    else:
                        break

                # today = datetime.datetime.now()
                # from datetime import datetime,timedelta
                # time_to_add=timedelta(days=0,hours=5,minutes=30)
                # today_india=today+time_to_add
                # print(today,today_india)
                # from datetime import datetime
                # sys_created_on_str=result[0]['sys_created_on']
                # sys_created_on=datetime.strptime(sys_created_on_str,"%Y-%m-%d %H:%M:%S")
                # print(sys_created_on)
                # a=today_india>sys_created_on
                # print(a)
                url = "https://graph.facebook.com/v15.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + faceBookToken,
                    'Content-Type': 'application/json'
                }
                for ticket in sys_created_on_list:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "text",
                        "text": {
                            "body": f"Number:{ticket['number']}\nDescription:{ticket['short_description']}\nUrgency:{ticket['urgency']}\nsys_created_by:{ticket['sys_created_by']}\nImpact:{ticket['impact']}\nopened_at:{ticket['opened_at']}\nactive:{ticket['active']}\n"
                                    f"sys_updated_by:{ticket['sys_updated_by']}\nsys_created_on:{ticket['sys_created_on']}"
                        },
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)







            elif resp_id_id == 3:
                print(response_id[2:])
                import base64
                import datetime

                encoded_string = response_id[2:]
                decoded_bytes = base64.b64decode(encoded_string)
                decoded_string = decoded_bytes.decode('utf-8')
                print(decoded_string)
                username, password = decoded_string.split(':')
                print(username)
                print(password)
                url = f"https://dev164889.service-now.com/api/now/table/sys_user?sysparm_query=user_name={username}"
                payload = {}
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Basic {encoded_string}',
                    'Cookie': 'BIGipServerpool_dev164889=3331282698.40766.0000; JSESSIONID=6313C1AA239A358068CEDBC3290CF2E0; glide_session_store=B03880BA9762F110FB3B5C900153AFD9; glide_user_activity=U0N2M18xOnIwd2g0NnduQ0UrR1JpSWxldDZpU09jdDFxNUMzcjNuSHJvbzN6SzkrOWs9OnNBV3JZeloxSUdyL0QxcGNGYTI3K2M2QTFnYnNnRmZMUk1JV25yQ2lwbVU9; glide_user_route=glide.204f61c181048880583f00591ea5c8d1'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                response_json = response.json()
                result = response_json.get('result')
                sys_id = result[0]['sys_id']
                print(sys_id)

                url = f"https://dev164889.service-now.com/api/now/table/incident?sysparm_query=assigned_to={sys_id}^active=true&sysparm_fields=number%2Curgency%2Cimpact%2Csys_created_by%2Csys_updated_by%2Cpriority%2Cstate^%2Cactive%2Copened_at%2Csys_id%2Cshort_description%2Csys_created_on%2Cassigned_to"
                headers = {
                    "Authorization": "Basic " + response_id[2:],
                }
                response = requests.get(url, headers=headers)

                print(response.text, response.status_code)
                response_json = response.json()
                result = response_json.get('result')
                print("length: ", len(result))

                url = "https://graph.facebook.com/v15.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + faceBookToken,
                    'Content-Type': 'application/json'
                }
                if len(result) == 0:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "text",
                        "text": {
                            "body": "No Tickets are assigned to you"
                        }
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                else:
                    for ticket in result:
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "text",
                            "text": {
                                "body": f"Number:{ticket['number']}\nDescription:{ticket['short_description']}\nUrgency:{ticket['urgency']}\nsys_created_by:{ticket['sys_created_by']}\nImpact:{ticket['impact']}\nopened_at:{ticket['opened_at']}\nactive:{ticket['active']}\n"
                                        f"sys_updated_by:{ticket['sys_updated_by']}\nsys_created_on:{ticket['sys_created_on']}\nAssigned to:{ticket['assigned_to']}"
                            },
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
            elif resp_id_id == 4:
                print(response_id[2:])
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        "body": {
                            "text": "Search Tickets"
                        },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "navigate",
                                "flow_token": f"{response_id[2:]}",  # erwers
                                "flow_id": "844809780659090",
                                "flow_cta": "Search Tickets",
                                "flow_action_payload": {
                                    "screen": "Search_ticket",
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
                print(response.text, response.status_code)

    elif project == 'sports':

        if response_id_type == 'T':
            # General Doctor, Cardiology,eye care
            if resp_id_id == 1:
                mainobj = appointment_settings.objects.filter(client_id=clientId)
                print(len(mainobj))
                for m_i in mainobj:

                    consultant_specialization = []
                    consultant_id = []
                    consultantDetails = Consultant_details.objects.filter(client_id=clientId)
                    for c_i in consultantDetails:
                        consultant_id.append(c_i.id)
                        consultant_specialization.append(c_i.consultant_specialization)

                    # Consultants_type = ["General Care", "Cardiology", "Eye care"]

                    dummy_consultant_specialization = []
                    for i in consultant_specialization:
                        if i not in dummy_consultant_specialization:
                            dummy_consultant_specialization.append(i)

                    consultant_department_list = []
                    print(consultant_specialization)
                    for i in range(len(dummy_consultant_specialization)):
                        consultant_department_list.append({"id": "H" + str(i),
                                                           "title": dummy_consultant_specialization[i],

                                                           })
                    if len(consultant_specialization) == 1:
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
                                                "title": c_i.consultant_specialization
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
                                    "text": "Select a sport which you prefer to book "
                                },

                                "action": {
                                    "button": "Choose Sport",
                                    "sections": [
                                        {
                                            "title": "Consultants",
                                            "rows": consultant_department_list
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
                #             "text": "Select the consulting department"
                #         },
                #         "action": {
                #             "button": "Choose Department",
                #             "sections": [
                #                 {
                #                     "title": "<LIST_SECTION_1_TITLE>",
                #                     "rows": [
                #                         {
                #                             "id": "A1",
                #                             "title": Consultants_type[0],
                #
                #                         },
                #                         {
                #                             "id": "A2",
                #                             "title": Consultants_type[1],
                #
                #                         },
                #                         {
                #                             "id": "A3",
                #                             "title": Consultants_type[2],
                #                         },
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
                #         "action": {
                #             "buttons": [
                #                 {
                #                     "type": "reply",
                #                     "reply": {
                #                         "for j in range(len(Consultants_type)):"
                #                         "id": "A" + str(j)
                #
                #                     }
                #                 }
                #
                #             ]
                #         }
                #     }
                # })

                # response = requests.request("POST", url, headers=headers, data=payload)

                # mainobj = Main_settings.objects.filter(client_id=clientId)
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
                #         consultantlist.append({"id": "N" + str(consultant_id[i]),
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
                #                                 "id": "A" + str(consultant_id[0]),
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

                # else:
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
                                            "title": "LocateUs"
                                        }
                                    },
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "Z2",
                                            "title": "Call US"
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


        elif response_id_type == 'H':
            mainobj = appointment_settings.objects.filter(client_id=clientId)
            print(len(mainobj))

            for m_i in mainobj:
                all_consultant_Name = []
                consultant_specialization = []
                consultant_id = []
                consultantDetails = Consultant_details.objects.filter(client_id=clientId)
                for c_i in consultantDetails:
                    consultant_id.append(c_i.id)
                    all_consultant_Name.append(c_i.consultant_name)
                    consultant_specialization.append(c_i.consultant_specialization)

                # Consultants_type = ["General Care", "Cardiology", "Eye care"]
                dumy_list = []
                for i in consultant_specialization:
                    if i not in dumy_list:
                        dumy_list.append(i)
                consultant_specialization = dumy_list
                # consultantDetails is either (general doctor-1,2 or cardiolgist- 1,2 or eye care-1,2)
                consultantDetails_1 = Consultant_details.objects.filter(client_id=clientId,
                                                                         consultant_specialization=
                                                                         consultant_specialization[resp_id_id])
                print("consultantDetails:", consultantDetails)
                consultantName_id = []
                consultant_detail = ''
                text = 'Choose Ground'
                button = 'Choose Ground'
                for i in consultantDetails_1:
                    if i.consultant_details is None:
                        consultant_detail = ''
                    else:
                        consultant_detail = f'({i.consultant_details})'

                    consultantName_id.append((i.consultant_name, i.id, consultant_detail, i.consultant_fee))
                    if ((i.consultant_specialization).lower() == 'badminton'):
                        text = 'Choose Court'
                        button = 'Choose Court'
                consultantlist = []

                # exp=["exp: 13 years", "exp: 20years"]
                print(consultantName_id, consultantName_id[0][1], consultantName_id[1][1], consultantName_id[0][0],
                      consultantName_id[1][0])
                for i in range(len(consultantName_id)):
                    consultantlist.append({"id": 'I' + str(consultantName_id[i][1]),
                                           "title": consultantName_id[i][0] + consultantName_id[i][2],
                                           "description": f'fee: Rs. {consultantName_id[i][3]}',

                                           })

                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "list",
                        "body": {
                            "text": text  # "Choose the Consultant"
                        },

                        "action": {
                            "button": button,  # "Choose Specialist",
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

     

        elif response_id_type == 'I':
            response_id_id = int(response_id[1:])
            print(response_id_type, response_id_id)

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
                # print("slotDuration",slotDuration.slot_duration)
                for s_i in slotDuration:
                    duration_str = s_i.slot_duration
                    print("duration_str", duration_str)
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
                    from datetime import datetime

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
                    from datetime import datetime
                    record_start_time = datetime.strptime(start_time_str, "%H:%M")
                    record_end_time = datetime.strptime(end_time_str, "%H:%M")
                    current_time = record_start_time

                    while current_time < record_end_time:
                        slot_start = current_time.strftime("%H:%M")
                        current_time += timedelta(minutes=duration)
                        slot_end = current_time.strftime("%H:%M")
                        all_slots.append((slot_start, slot_end))
                        print("all_slots", all_slots)
                final_all_slots = [slot for slot in all_slots if slot not in hslots]
                # print("final_all_slots",final_all_slots)
                print("channi")
                print("final_all_slots", final_all_slots)
                print("length of final_all_slots", len(final_all_slots))
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

               

            len_all_slots = []
            print("exdate:", ex_date)
            for i, date in enumerate(ex_date):
                avlslots = len(all_available_slots[i])
                print("len", avlslots)
                formateedDate = ''
                if avlslots != 0 and avlslots <= 10:
                    print("ifcondition")
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
            print("show_avl_slots", show_avl_slots)
            print("show_date", show_date)
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
                    "body": {
                        "text": "What is your preferred date to schedule your booking?"
                        # "text": "What is your preferred date to schedule the appointment?"
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


        elif response_id_type == 'e':
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
                        "text": "If you need any help in future, just type Hi or Help."
                                "We will be happy to assist you."
                    },

                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "Z1",
                                    "title": "GET DIRECTIONS",
                                },
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "Z2",
                                    "title": "CONTACT US",
                                },
                            }
                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
        # confirmation messaage
        elif response_id_type == 'm':
            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "text",
                "text": {
                    "body": "Your appointment is scheduled with doctor1."
                            "Thank you for consulting ------hospital."
                }

            })
            response = requests.request("POST", url, headers=headers, data=payload)










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

                availablityObject = Consultant_availablity.objects.filter(client_id=clientId,
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

            date = []
            dates = response_id[slash_index + 1:]
            print("jayamma")
            print(dates)
            print("jayanna")
            from datetime import datetime
            dates_new = datetime.strptime(str(dates), '%Y-%m-%d')
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
                print(formatted_duation_create)
                formatted_start_slot_create = f"{slot_start}"
                formatted_end_slot_create = f"{slot_end}"
                date_formate_start_slot_create = datetime.strptime(formatted_start_slot_create, "%H:%M")
                formatted_slot_start__time = date_formate_start_slot_create.strftime("%I:%M %p")
                date_formate_end__slot_create = datetime.strptime(formatted_end_slot_create, "%H:%M")
                formatted_slot_end__time = date_formate_end__slot_create.strftime("%I:%M %p")
                formatted_slots_details.append(f'{formatted_slot_start__time} - {formatted_slot_end__time}')
                formatted_duration_details.append(formatted_duation_create)

            for i in range(len(formatted_slots_details)):
                list_all_data.append({"id": "S" + str(consult_id) + "/" + str(
                    visitor_id) + "//" + str(finalDates[0]) + str(formatted_duration_details[i]) + str(i),
                                      "title": str(formatted_slots_details[i])

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
                    "body": {
                        "text": "Choose your preferred time "
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
            # booking_ref_id = uuid.uuid4()
            from datetime import datetime
            Components = response_id.split("/")
            Components = str(Components[0][1:]) + str(Components[1:])
            print("componenets", Components)
            # ConsultantId = Components[0][1:]  # Remove the leading 's'
            # print("Components[3][:8], Components[0][1:] =",Components[3][:8],Components[0][1:],Components[3][8:])
            # VisitorId = Components[1]
            # sdate = Components[3][:8]
            # day = sdate[:2]
            # month = sdate[2:4]
            # year = sdate[4:]
            input_str = Components  # "109['110', '', '0411202306:00-07:000']"

            # Split the string by the first '[' character
            split_str = input_str.split("[")

            # Process the first part, which is '8', and then split the second part by commas

            first_part = [split_str[0].strip()]
            second_part = split_str[1].strip(" '[]").split(",")

            # Combine both parts to create the final list
            result_list = first_part + second_part
            lis = []
            a = ''
            print(result_list)
            for i, value in enumerate(result_list):

                for j in value:

                    if j == "'" or j == ' ' or j == "''" or j == "'" or j == " ":
                        value = value.replace(j, '')

                result_list[i] = value
            print(result_list)
            ConsultantId = int(result_list[0])
            print(ConsultantId)
            consultantDetails = Consultant_details.objects.filter(client_id=clientId, id=ConsultantId)

            # Consultation_Mode_list = ["Video call", "In Person"]
            Consultation_Mode_list = ["Online Payment", "Cash"]
            Consultation_Mode = []
            for j in consultantDetails:
                print(j.consultant_fee)
                for i in range(len(Consultation_Mode_list)):
                    print(i)
                    row = {
                        "id": "a" + str(i) + str(Components),
                        "title": Consultation_Mode_list[i]
                    }
                    print("row", row)
                    Consultation_Mode.append(row)
                print("Consultation_Mode1", Consultation_Mode)
            print("Consultation_Mode2", Consultation_Mode)

            payload = json.dumps({
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": toUser,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "body": {
                        "text": f"Choose your preferred Payment Mode\n"

                        # "text": "Choose your preferred Mode of Consultation"
                    },

                    "action": {
                        "button": "Mode",
                        "sections": [
                            {
                                "title": "Consultation_Mode",
                                "rows": Consultation_Mode
                            }

                        ]
                    }
                }
            })

            response = requests.request("POST", url, headers=headers, data=payload)
            print("end of payload in consultation mode")
            print(response)
        elif response_id_type == 'a':
            from datetime import datetime
            print("response_id", response_id[2:])
            if resp_id_id == 0:
                print("acoming")
                print(response_id, response_id[2:])  # 1['3', '', '0811202310:30-11:001']
                index = int(response_id[2])
                input_str = response_id[2:]  # "109['110', '', '0411202306:00-07:000']"

                # Split the string by the first '[' character
                split_str = input_str.split("[")

                # Process the first part, which is '8', and then split the second part by commas

                first_part = [split_str[0].strip()]
                second_part = split_str[1].strip(" '[]").split(",")

                # Combine both parts to create the final list
                result_list = first_part + second_part
                lis = []
                a = ''
                print(result_list)
                for i, value in enumerate(result_list):

                    for j in value:

                        if j == "'" or j == ' ' or j == "''" or j == "'" or j == " ":
                            value = value.replace(j, '')

                    result_list[i] = value
                print(result_list)

                Components = result_list
                print("Components", Components)

                ConsultantId = Components[0]
                print("ConsultantId", ConsultantId)  # Remove the leading 's'
                VisitorId = Components[1]
                # print("Components[0],Components[3],Components[6][:8]", Components[0], Components[3], Components[6][:8])
                sdate = Components[3]
                day = sdate[:2]
                month = sdate[2:4]
                year = sdate[4:8]
                fdate = f'{day}/{month}/{year}'
                print(fdate)
                date_obj = datetime.strptime(fdate, "%d/%m/%Y")
                gdate = date_obj.strftime("%Y-%m-%d")
                duration = sdate[8:19]

                print(duration.split('-'))
                # dpart = duration[11:]
                # print(dpart)
                start_time_str, end_time_str = duration.split('-')
                print("start_time_str,end_time_str,typeofend_time_str", start_time_str, end_time_str,
                      type(end_time_str))
                full_start_time = datetime.strptime(start_time_str, '%H:%M')
                start_time = full_start_time.strftime("%H:%M %p")
                print("starttime", start_time)
                full_end_time = datetime.strptime(end_time_str, '%H:%M')
                end_time = full_end_time.strftime("%H:%M %p")
                status_obj = Consultant_details.objects.filter(id=ConsultantId)
                print(" I am in mode of consultation")

                approval_mode = ''
                for a_i in status_obj:
                    approval_mode = a_i.approval_mode
                print(approval_mode)
                if approval_mode == 'Automatic' or approval_mode == 'automatic':
                    print("s automatic")

                    consultantDetails = Consultant_details.objects.filter(client_id=clientId, id=ConsultantId)

                    for i in consultantDetails:
                        print(i.consultant_name, i.consultant_specialization)
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "button",

                                "header": {
                                    "type": "text",
                                    "text": 'Please confirm your Booking'
                                    # "text": 'Please confirm your appointment'
                                },

                                "body": {
                                    "text": f'*_Name_*: {i.consultant_name}\n'
                                            f'*_Game/Sport_*: {i.consultant_specialization}\n'
                                            f'*_Date_*:{fdate}\n'
                                            f'*_From_*: {start_time} *_to_* {end_time}\n'
                                            f'*_Fee_*: Rs.{i.consultant_fee}'

                                },

                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "D1" + response_id[1:],
                                                "title": "Confirm"
                                            }
                                        },
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "D2",
                                                "title": "Cancel"

                                            }
                                        },

                                    ]
                                }
                            }
                        })
                        response = requests.request("POST", url, headers=headers, data=payload)
                        # if i.id==ConsultantId:
                        #     print("hi")
                        #     consultantname=i.consultant_name
                        #     consultantspecialization=i.consultant_specialization
                        #     print(consultantname, consultantspecialization)

                        # for c_i in consultantDetails:
                        #     consultant_id.append(c_i.id)
                        #     all_consultant_Name.append(c_i.consultant_name)
                        #     consultant_specialization.append(c_i.consultant_specialization)
                    # consultantName=Consultant_settings.objects.filter(client_id=clientId,consultant_name=ConsultantId)
                    # print(consultantName)

                    # booking = Bookings(
                    #     client_id=clientId,
                    #     Visitor_id=VisitorId,
                    #     Consultant_settings_id=ConsultantId,
                    #     date=gdate,
                    #     start_time=start_time,
                    #     end_time=end_time,
                    #     status=1,
                    #     booking_reference_id=booking_ref_id,
                    #     customer_phone_number=toUser,
                    #     online_offline='offline'
                    #
                    # )
                    # booking.save()
                    print("successfully created one record in bookings")
                    # showDetails = Bookings.objects.filter(client_id=clientId, booking_reference_id=booking_ref_id)
                    # for s_i in showDetails:
                    #     duration_start = s_i.start_time
                    #     duration_end = s_i.end_time
                    #     # start_time_obj1 = datetime.strptime(str(duration_start), "%H:%M")
                    #     # end_time_obj1 = datetime.strptime(str(duration_end), "%H:%M")
                    #     formatted_start_time1 = duration_start.strftime("%I:%M%p")
                    #     formatted_end_time1 = duration_end.strftime("%I:%M%p")
                    #     date = s_i.date
                    #     date_obj = datetime.strptime(str(date), '%Y-%m-%d')
                    #     New_date = date_obj.strftime('%d-%b-%Y')
                    #     status = "Booked" if s_i.status == 1 else "blocked"
                    #     detailsObj = Consultant_settings.objects.filter(id=s_i.Consultant_settings_id)
                    #     consultantName = ''
                    #     specialization = ''
                    #     consultantImage = ''
                    #     for d_i in detailsObj:
                    #         consultantName = d_i.consultant_name
                    #         specialization = d_i.consultant_specialization
                    #         consultantImage = d_i.consultant_image
                    #
                    #     print("print")
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
            elif resp_id_id == 1:
                print("acoming")
                print(response_id, response_id[1:])  # 1['3', '', '0811202310:30-11:001']

                input_str = response_id[2:]  # "109['110', '', '0411202306:00-07:000']"

                # Split the string by the first '[' character
                split_str = input_str.split("[")

                # Process the first part, which is '8', and then split the second part by commas

                first_part = [split_str[0].strip()]
                second_part = split_str[1].strip(" '[]").split(",")

                # Combine both parts to create the final list
                result_list = first_part + second_part
                lis = []
                a = ''
                print(result_list)
                for i, value in enumerate(result_list):

                    for j in value:

                        if j == "'" or j == ' ' or j == "''" or j == "'" or j == " ":
                            value = value.replace(j, '')

                    result_list[i] = value
                print(result_list)

                Components = result_list
                ConsultantId = Components[0]
                VisitorId = Components[1]
                # print("Components[0],Components[3],Components[6][:8]", Components[0], Components[3], Components[6][:8])
                sdate = Components[3]
                day = sdate[:2]
                month = sdate[2:4]
                year = sdate[4:8]
                fdate = f'{day}/{month}/{year}'
                print(fdate)
                date_obj = datetime.strptime(fdate, "%d/%m/%Y")
                gdate = date_obj.strftime("%Y-%m-%d")
                duration = sdate[8:19]
                print(duration.split('-'))
                # dpart = duration[11:]
                # print(dpart)
                start_time_str, end_time_str = duration.split('-')
                print("start_time_str,end_time_str,typeofend_time_str", start_time_str, end_time_str,
                      type(end_time_str))
                full_start_time = datetime.strptime(start_time_str, '%H:%M')
                start_time = full_start_time.strftime("%H:%M %p")
                print("starttime", start_time)
                full_end_time = datetime.strptime(end_time_str, '%H:%M')
                end_time = full_end_time.strftime("%H:%M %p")
                status_obj = Consultant_details.objects.filter(id=ConsultantId)
                print(" I am in mode of consultation")

                approval_mode = ''
                for a_i in status_obj:
                    approval_mode = a_i.approval_mode
                print(approval_mode)
                if approval_mode == 'Automatic' or approval_mode == 'automatic':
                    print("s automatic")

                    consultantDetails = Consultant_details.objects.filter(client_id=clientId, id=ConsultantId)

                    for i in consultantDetails:
                        print(i.consultant_name, i.consultant_specialization)
                        payload = json.dumps({
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": toUser,
                            "type": "interactive",
                            "interactive": {
                                "type": "button",

                                "header": {
                                    "type": "text",
                                    "text": 'Please confirm your appointment'
                                },

                                "body": {
                                    "text": f'*_Ground_*: {i.consultant_name}\n'
                                            f'*_Game/sport_*: {i.consultant_specialization}\n'
                                            f'*_Date_*:{fdate}\n'
                                            f'*_From_*: {start_time} *_to_* {end_time}\n'
                                            f'*_Fee_*: Rs.{i.consultant_fee}'

                                },

                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "D1" + response_id[1:],
                                                "title": "Confirm"
                                            }
                                        },
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": "D2",
                                                "title": "Cancel"

                                            }
                                        },

                                    ]
                                }
                            }
                        })
                        response = requests.request("POST", url, headers=headers, data=payload)
                        # if i.id==ConsultantId:
                        #     print("hi")
                        #     consultantname=i.consultant_name
                        #     consultantspecialization=i.consultant_specialization
                        #     print(consultantname, consultantspecialization)

                        # for c_i in consultantDetails:
                        #     consultant_id.append(c_i.id)
                        #     all_consultant_Name.append(c_i.consultant_name)
                        #     consultant_specialization.append(c_i.consultant_specialization)
                    # consultantName=Consultant_settings.objects.filter(client_id=clientId,consultant_name=ConsultantId)
                    # print(consultantName)

                    # booking = Bookings(
                    #     client_id=clientId,
                    #     Visitor_id=VisitorId,
                    #     Consultant_settings_id=ConsultantId,
                    #     date=gdate,
                    #     start_time=start_time,
                    #     end_time=end_time,
                    #     status=1,
                    #     booking_reference_id=booking_ref_id,
                    #     customer_phone_number=toUser,
                    #     online_offline='offline'
                    #
                    # )
                    # booking.save()
                    print("successfully created one record in bookings")
                    # showDetails = Bookings.objects.filter(client_id=clientId, booking_reference_id=booking_ref_id)
                    # for s_i in showDetails:
                    #     duration_start = s_i.start_time
                    #     duration_end = s_i.end_time
                    #     # start_time_obj1 = datetime.strptime(str(duration_start), "%H:%M")
                    #     # end_time_obj1 = datetime.strptime(str(duration_end), "%H:%M")
                    #     formatted_start_time1 = duration_start.strftime("%I:%M%p")
                    #     formatted_end_time1 = duration_end.strftime("%I:%M%p")
                    #     date = s_i.date
                    #     date_obj = datetime.strptime(str(date), '%Y-%m-%d')
                    #     New_date = date_obj.strftime('%d-%b-%Y')
                    #     status = "Booked" if s_i.status == 1 else "blocked"
                    #     detailsObj = Consultant_settings.objects.filter(id=s_i.Consultant_settings_id)
                    #     consultantName = ''
                    #     specialization = ''
                    #     consultantImage = ''
                    #     for d_i in detailsObj:
                    #         consultantName = d_i.consultant_name
                    #         specialization = d_i.consultant_specialization
                    #         consultantImage = d_i.consultant_image
                    #
                    #     print("print")




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
            consulta_id = response_id[x + 1:]
            main_available_slots = []
            next_date = datetime.strptime(str(next_date), "%Y-%m-%d").date()
            next_day = next_date + timedelta(days=1)
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
                        from datetime import datetime
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
            from datetime import datetime
            print("resp_id_id", resp_id_id)
            if resp_id_id == 1:
                print(response_id[1], response_id[2])
                print(response_id, response_id[2:])  # 1['3', '', '0811202310:30-11:001']
                booking_ref_id = uuid.uuid4()
                input_str = response_id[2:]  # "109['110', '', '0411202306:00-07:000']"

                # Split the string by the first '[' character
                split_str = input_str.split("[")

                # Process the first part, which is '8', and then split the second part by commas

                first_part = [split_str[0].strip()]
                second_part = split_str[1].strip(" '[]").split(",")

                # Combine both parts to create the final list
                result_list = first_part + second_part
                lis = []
                a = ''
                print(result_list)
                for i, value in enumerate(result_list):

                    for j in value:

                        if j == "'" or j == ' ' or j == "''" or j == "'" or j == " ":
                            value = value.replace(j, '')

                    result_list[i] = value
                print(result_list)

                Components = result_list
                print("components", Components)  # ['09', '10', '', '0411202306:00-07:000'
                ConsultantId = Components[0][1:]
                Mode = Components[0][0]

                # for i, value in enumerate(str(Components[0])):  # Remove the leading 's'
                #     if Mode == str(resp_id_id):
                #         ConsultantId = int(Components[0][i:])
                #         print("consultant_id in for")
                #         print(ConsultantId)
                #         break
                #     else:
                #         Mode += value
                #         print("Mode in",Mode)
                # Mode=int(Mode)
                # print("Mode out",Mode)

                # ConsultantId = Components[0]
                print("ConsultantId", ConsultantId)  # Remove the leading 's'
                VisitorId = Components[1]
                # print("Components[0],Components[3],Components[6][:8]", Components[0], Components[3], Components[6][:8])
                sdate = Components[3]
                day = sdate[:2]
                month = sdate[2:4]
                year = sdate[4:8]
                fdate = f'{day}/{month}/{year}'
                print(fdate)

                date_obj = datetime.strptime(fdate, "%d/%m/%Y")
                gdate = date_obj.strftime("%Y-%m-%d")
                duration = sdate[8:19]
                print(duration.split('-'))
                # dpart = duration[11:]
                print("gdate:", gdate)
                start_time_str, end_time_str = duration.split('-')
                start_time = datetime.strptime(start_time_str.strip(), '%H:%M')
                end_time = datetime.strptime(end_time_str.strip(), '%H:%M')
                status_obj = Consultant_details.objects.filter(id=ConsultantId)
                print(" I am in mode of consultation")

                if response_id[2] == '0':
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
                        online_offline="Online payment"
                        # online_offline="Video call"

                    )
                    booking.save()
                elif response_id[2] == '1':
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
                        online_offline="Cash"
                        # online_offline="In Person"

                    )
                    booking.save()

                print("Booking done")
                consultantDetails = Consultant_details.objects.filter(client_id=clientId, id=ConsultantId)

                for i in consultantDetails:
                    print(i.consultant_name, i.consultant_specialization)
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "preview_url": True,
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "text",
                        "text": {
                            "body": 'Thank you for booking. Your Booking is confirmed.'
                        }
                    })
                    # "body": f"Appointment scheduled with *_{i.consultant_name}_*\n"
                    #          "Thank you for consulting Seva hospital."
                    #    }

                    response = requests.request("POST", url, headers=headers, data=payload)
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "interactive",
                        "interactive": {
                            "type": "button",
                            "body": {
                                "text": "If you need any help in future, just type Hi or Help."
                                        "We will be happy to assist you."
                            },

                            "action": {
                                "buttons": [
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "Z1",
                                            "title": "Get Directions"
                                        }
                                    },
                                    {
                                        "type": "reply",
                                        "reply": {
                                            "id": "Z2",
                                            "title": "Contact US"
                                        }
                                    }

                                ]
                            }
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)

            elif resp_id_id == 2:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "preview_url": True,
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "text",
                    "text": {
                        "body": 'Booking cancelled successfully'
                        # "body": 'Appointment cancelled successfully'

                    }

                })
                response = requests.request("POST", url, headers=headers, data=payload)
                # mainobj = Main_settings.objects.filter(client_id=clientId)
                # for f_i in mainobj:
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": "If you need any help in future, just type Hi or Help."
                                    "We will be happy to assist you."
                        },

                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "Z1",
                                        "title": "Get Directions"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                        "id": "Z2",
                                        "title": "Contact US"
                                    }
                                }

                            ]
                        }
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
                bookings = appointment_bookings.objects.filter(Consultant_settings_id=consultantId, date=day)
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
                                            "id": "L" + str(m_i.Consultant_settings_id),
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
                                    "id": "G" + str(l_consult_id),
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
                            "latitude": "0",
                            "longitude": "0",
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
                        "body": "Please Call 18001800 to Contact Hospital Management...."
                    }
                })

                response = requests.request("POST", url, headers=headers, data=payload)


def process_ticket_interactive_message(response_id, request, url, headers, toUser, clientId, whatsAppPhoneNumberId,
                                       faceBookToken):
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
            transfer_ticket = ''
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
            slotcatobj1 = event_slots.objects.filter(client_id=clientId, id=response_id_id)
            for cat_ii in slotcatobj1:
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

        category_details = event_ticket_category.objects.filter(client_id=clientId, id=response_id_id_c)
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

            cart_header_detail = event_ticket_cart_header.objects.filter(client_id=clientId,
                                                                         total_tickets=response_id_id_n,
                                                                         payment_reference_id=reference_id)

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
            event_name = event_ticket_cart_details.objects.filter(client_id=clientId, id=t.id)

            for e in event_name:
                ticket_event = e.event_id
                eventinfo = event_master.objects.filter(client_id=clientId, id=ticket_event)
                for e in eventinfo:
                    ticket_event_name = e.Event_Name
                    break

        phonenumber = facebook_details.objects.filter(client_id=clientId, fb_phone_number_id=whatsAppPhoneNumberId)
        client_number = ''
        for p in phonenumber:
            client_number = p.fb_whatsapp_number

        # ---------------"blocking the tickets"----------------------
        Availbletickets = ticket_information.objects.filter(client_id=clientId,
                                                            event_ticket_category_id=response_id_id_c, ticket_status=10)
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
            "first_min_partial_amount": 0,
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
        phonenumber = facebook_details.objects.filter(client_id=clientId, fb_phone_number_id=whatsAppPhoneNumberId)
        client_number = ''
        for p in phonenumber:
            client_number = p.fb_whatsapp_number
        updateticket = ticket_information.objects.filter(client_id=clientId, id=response_id_id)
        for u_i in updateticket:
            refer_id = u_i.payment_reference_id
            # message = "Transfer ticket " + ticketnumber + " to: "
            # encoded_message = urllib.parse.quote(message)
            # print("wait")
            # url = "https://api.whatsapp.com/send?phone=84&text=hello"
            # print("bb")
            # detailslink = "https://vmart.ai"+ "/infoform/" + toUser + str(clientId) + '/'+ str(ticketnumber) + '/'
            detailslink = "https://vmart.ai" + "/T/" + str(response_id_id) + "T" + refer_id + '/' + str(clientId)

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


def process_appointement_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                     clientId, whatsAppPhoneNumberId, faceBookToken, list_title, faceBookId, project):
    print("csdf")
    print("whatsAppPhoneNumberId", whatsAppPhoneNumberId,"project: ",project)
   
    if project == 'Appointment':
        print('Appointment')
        if messageType == 'text':
            if not appointment_visitor.objects.filter(client_id=clientId, Visitor_Whatsapp_Number=toUser).exists():
                new_customer = appointment_visitor(client_id=clientId, Visitor_Whatsapp_Number=toUser)
                new_customer.save()
            else:
                print("phone number already exist")

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
                url = "https://graph.facebook.com/v18.0/129405560258915/messages"

                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer EAAFENj48uKsBO5OZBZBchbxMQfZCT0qsAuPeuodd4IwWv5ngpY1TF2SbsHk1XAtsCZCa8PZCVdvdNC9y6UwojVsZBj5NZAxUHFcdIBmLjqeJgThw9zv97Id9bMqZCVKzRKXrPusbZB93aRJVVBLD4Ri5xV18HM70No8fozQvg6IVh8fKwcYgAGUJhTK0ZB404htwwO'
                }
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        # "header": {
                        #     "type": "text",
                        #    "text": "Please Enter your details to continue."
                        # },
                        "body": {
                            "text": "Welcome to Seva Hospitals.\nPlease Enter your details to continue."
                        },
                        # "footer": {
                        #     "text": "Enter Details"
                        # },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "navigate",
                                "flow_token": "123erwers",  # erwers
                                "flow_id": "1004582320806530",
                                "flow_cta": "Enter",
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
                print(response.status_code, response)
                if response.status_code == 200:
                    print("Request was successful")






        elif messageType == 'interactive':
            process_appointement_interactive_message(response_id, request, url, headers, toUser, clientId,
                                                     whatsAppPhoneNumberId,
                                                     faceBookToken, list_title, project)
    elif project == 'servicenow':
        print("in appointement_bot servicenow")
        if messageType == 'text':
            if not appointment_visitor.objects.filter(client_id=clientId, Visitor_Whatsapp_Number=toUser).exists():
                new_customer = appointment_visitor(client_id=clientId, Visitor_Whatsapp_Number=toUser)
                new_customer.save()
            else:
                print("phone number already exist")
                print("No matching consultant settings found for phone number:", toUser)
                print("hello")
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        "body": {
                            "text": "Welcome to ServiceNow on whatsapp\nEnter your ServiceNow credentials to\nstart creating new tickets,\ncheck status of your open tickets,\nrespond/reply to tickets etc."
                        },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "navigate",
                                "flow_token": "123erwers",  # erwers
                                "flow_id": "720883519980268",
                                "flow_cta": "Sign In",
                                "flow_action_payload": {
                                    "screen": "SIGN_IN",
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
                print(response.status_code, response)

                if response.status_code == 200:
                    print("Request was successful")
                else:
                    print("sigin flow failed",response.text)

            # payload = json.dumps({
            # "messaging_product": "whatsapp",
            # "to": toUser,
            # "recipient_type": "individual",
            # "type": "interactive",
            # "interactive": {
            #     "type": "flow",
            #     "body": {
            #         "text": "Welcome to ServiceNow on whatsapp\nEnter your ServiceNow credentials to\nstart creating new tickets,\ncheck status of your open tickets,\nrespond/reply to tickets etc."
            #     },
            #     "action": {
            #         "name": "flow",
            #         "parameters": {
            #             "flow_message_version": "3",
            #             "flow_action": "navigate",
            #             "flow_token": "ed7adc18",#erwers
            #             "flow_id": "337091855606091",
            #             "flow_cta": "Sign In",
            #             "mode": "draft" , #Set the mode to 'draft'
            #             "flow_action_payload": {
            #                 "screen": "Menu",
            #                 "data": {
            #                     "id": "0",
            #                     "title": "Yes"
            #                 }
            #             }
            #         }
            #     }
            # }
            # })
            # response = requests.request("POST", url, headers=headers, data=payload)
            # print(response.status_code,response.text)

            # if response.status_code == 200:
            #     print("Request was successful")

            # payload = json.dumps({
            #     "messaging_product": "whatsapp",
            #     "to": toUser,
            #     "recipient_type": "individual",
            #     "type": "interactive",
            #     "interactive": {
            #         "type": "flow",
            #         "body": {
            #             "text": "Welcome to ServiceNow on whatsapp\nEnter your ServiceNow credentials to\nstart creating new tickets,\ncheck status of your open tickets,\nrespond/reply to tickets etc."
            #         },
            #         "action": {
            #             "name": "flow",
            #             "parameters": {
            #                 "flow_message_version": "3",
            #                 "flow_action": "navigate",
            #                 "flow_token": "123erwers",#erwers
            #                 "flow_id": "720883519980268",
            #                 "flow_cta": "Sign In",
            #                 "flow_action_payload": {
            #                     "screen": "SIGN_IN",
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
            # print(response.status_code,response)

            # if response.status_code == 200:
            #     print("Request was successful")
            # -------------------------------------------------------------------------

            # credentials = "carol.krisman:Vividhity$123"
            # encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
            # url="https://dev164889.service-now.com/api/now/table/incident"
            # data=json.dumps({
            #     "short_description": "Unable to connect to office wifi",
            #     "urgency": "2",
            #     "impact": "2",
            #     "assigned_to":{
            #             "link": "https://dev164889.service-now.com/api/now/table/sys_user/77ad8176731313005754660c4cf6a7de",
            #             "value": "77ad8176731313005754660c4cf6a7de"
            #     }
            # })
            # headers={
            #     "Authorization": f"Basic {encoded_credentials}",
            #     "Content-Type":"application/json",
            # }
            # response = requests.post(url, headers=headers, data=data)
            # print(response.text)
            # --------------------------------------------------------------------
            # print(f"Base64-encoded credentials: {encoded_credentials}")
            # url="https://dev164889.service-now.com/api/now/table/sys_user/me?"
            # header={
            #     "Authorization": f"Basic {encoded_credentials}"
            #
            # }
            # params = {
            #     "sysparm_query":"username%3dDavid.Miller",
            #     # "sysparm_fields": "name",
            #     "sysparm_limit": 1,
            #     }
            # response = requests.get(url, headers=headers, params=params)
            # print(response.text)
       

        elif messageType == 'interactive':
            process_appointement_interactive_message(response_id, request, url, headers, toUser, clientId,
                                                     whatsAppPhoneNumberId,
                                                     faceBookToken, list_title, project)
    elif project == 'sports':
        if messageType == 'text':
            if not appointment_visitor.objects.filter(client_id=clientId, Visitor_Whatsapp_Number=toUser).exists():
                new_customer = appointment_visitor(client_id=clientId, Visitor_Whatsapp_Number=toUser)
                new_customer.save()
            else:
                print("phone number already exist")

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
                url = "https://graph.facebook.com/v18.0/129405560258915/messages"

                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer EAAFENj48uKsBO5OZBZBchbxMQfZCT0qsAuPeuodd4IwWv5ngpY1TF2SbsHk1XAtsCZCa8PZCVdvdNC9y6UwojVsZBj5NZAxUHFcdIBmLjqeJgThw9zv97Id9bMqZCVKzRKXrPusbZB93aRJVVBLD4Ri5xV18HM70No8fozQvg6IVh8fKwcYgAGUJhTK0ZB404htwwO'
                }
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": toUser,
                    "recipient_type": "individual",
                    "type": "interactive",
                    "interactive": {
                        "type": "flow",
                        # "header": {
                        #     "type": "text",
                        #    "text": "Please Enter your details to continue."
                        # },
                        "body": {
                            "text": "Welcome to Sports Arena\nPlease Enter your details to continue."
                        },
                        # "footer": {
                        #     "text": "Enter Details"
                        # },
                        "action": {
                            "name": "flow",
                            "parameters": {
                                "flow_message_version": "3",
                                "flow_action": "navigate",
                                "flow_token": "123erwers",  # erwers
                                "flow_id": "1004582320806530",
                                "flow_cta": "Enter",
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
                print(response.status_code, response)

                if response.status_code == 200:
                    print("Request was successful")







        elif messageType == 'interactive':
            process_appointement_interactive_message(response_id, request, url, headers, toUser, clientId,
                                                     whatsAppPhoneNumberId,
                                                     faceBookToken, list_title, project)
def process_new_commerce_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                     clientId, whatsAppPhoneNumberId, faceBookToken, list_title, faceBookId, project):
    print('commerce')
    if messageType =='text':
        print("hi")

def process_hotel_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                                     clientId, whatsAppPhoneNumberId, faceBookToken, list_title,
                                                       faceBookId,whatsapPhoneNumber):
    facebook_object=facebook_details.objects.filter(id=faceBookId,fb_phone_number_id=whatsapPhoneNumber)
    waba_id=0
    for items in facebook_object:
        
        waba_id=items.fb_Whatsapp_business_account_id
    print('facebookId',faceBookId)
    if messageType =='text':
        if 'hotel_id' in message: 
            message_info,hotel_id=message.split('=') 
            print("clientId",clientId) 
            Hotel_marketplace_obj=Hotel_marketplace.objects.get(client_id=clientId,hotel_id=hotel_id)   
            print("Hotel_marketplace_obj",Hotel_marketplace_obj.vailo_record_creation)
            marketplace_id=Hotel_marketplace_obj.id                                           
            Hotel_settings_obj=Hotel_settings.objects.get(client_id=clientId,marketplace=Hotel_marketplace_obj)
            print("Hotel","clientId,marketplace_id,Hotel_settings_obj",clientId,marketplace_id,Hotel_settings_obj)
            datetime_utc=datetime.now()
            print("datetime_utc",datetime_utc)
            india_timezone = pytz.timezone('Asia/Kolkata')
            datetime_india = india_timezone.localize(datetime_utc)
            datetime_str=datetime.strftime(datetime_india,'%Y-%m-%d %H:%M:%S')
            print(datetime_str)
            datetime_obj=datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S')
            print(datetime_obj)
            Guest_info_obj=''
            try:
                Guest_info_obj=Guest_info.objects.get(client_id=clientId,Phone_number=toUser)
                print("Guest_info_obj",Guest_info_obj)
            except:
                print("user not checked in")
            print("Guest_info_obj",Guest_info_obj) 
            if Guest_info_obj !='':
                Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.filter(client_id=clientId,Guest_details=Guest_info_obj,Check_Out__gt=datetime_obj,Hotel_details=Hotel_settings_obj)
                print(Hotel_Room_Guest_info_obj)
                if len(Hotel_Room_Guest_info_obj)>=1:
                    Hotel_marketplace_settings_obj= Hotel_marketplace_settings.objects.get(client_id=clientId)
                    print('Hotel_marketplace_settings_obj',Hotel_marketplace_settings_obj)
                    
                        
                    
                    
                    payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "to": toUser,
                                    "recipient_type": "individual",
                                    "type": "interactive",
                                    "interactive": {
                                        "type": "flow",
                                        "body": {
                                            "text": str(Hotel_marketplace_settings_obj.marketplace_welcome_message_body)
                                        },
                                        "action": {
                                            "name": "flow",
                                            "parameters": {
                                                "flow_message_version": "3",
                                                "flow_action": "data_exchange",
                                                "flow_token": f"hotel_{clientId}_{marketplace_id}_{Hotel_settings_obj.id}_{Guest_info_obj.id}",
                                                "mode": "draft",
                                                "flow_id": f"{Hotel_marketplace_settings_obj.specific_flow_id}",

                                                "flow_cta": f"{Hotel_marketplace_settings_obj.specific_flow_cta_name}",
                                            }
                                        }
                                    }

                                })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    print("hjdhdh")
                    print(response.text)
                else:
                    print("guest is not checked in")

                    # if marketplace_id !='':
                    #     payload=json.dumps({
                    #     "messaging_product":"whatsapp",
                    #     "to":toUser,
                    #     "recipient_type":"individual",
                    #     "preview_url":False,
                    #     "type":"text",
                    #     "text":{
                    #         "body":f"https://wa.me/{whatsapPhoneNumber}?text=CheckIn={hotel_id}"
                    #     }
                    # })
                    #     response=requests.request('POST',url,headers=headers,data=payload)
            else:
                print("guest is not registered")
                
        
        elif 'CheckIn' in message:
            messageInfo,hotel_id=message.split('=')
            Hotel_marketplace_obj=Hotel_marketplace.objects.get(client_id=clientId,hotel_id=hotel_id)
            print('checkin hotel id',Hotel_marketplace_obj)
           
            # Url = f"https://graph.facebook.com/v18.0/{waba_id}/flows"

            # payload = {'name': "HotelRoomfom",
            #         'categories': '["OTHER"]'}

            # header = { 
            #     'Authorization': f'Bearer {faceBookToken}'
            # }

            # response = requests.request("POST", Url, headers=header, data=payload)
            # print(response.text)
            # response_data = json.loads(response.text)
            # id_value = response_data.get('id')
            # data={
            #         "version": "2.1",
            #         "screens": [
            #             {
            #             "id": "Hotel_room_forM",
            #             "title": "Hotel Room Application Form",
            #             "terminal": True,
            #             "data":{
            #                 "allroom_types": {
            #   "type": "array",
            #   "items": {
            #     "type": "object",
            #     "properties": {
            #       "id": {
            #         "type": "string"
            #       },
            #       "title": {
            #         "type": "string"
            #       }
                
            #     }
            #   },
            #   "__example__": [
            #     {
            #       "id": "",
            #       "title": ""
                
            #     }
            
            #   ]
            # },
            #  "room": {
            #   "type": "array",
            #   "items": {
            #     "type": "object",
            #     "properties": {
            #       "id": {
            #         "type": "string"
            #       },
            #       "title": {
            #         "type": "string"
            #       },
            #       "metadata":{
            #         "type":"string"
            #       }
            #     }
            #   },
            #   "__example__": [
            #     {
            #       "id": "",
            #       "title": "",
            #       "metadata":""
            #     }
            
            #   ]
            # },
            # "checkin": {
            #   "type": "array",
            #   "items": {
            #     "type": "object",
            #     "properties": {
            #       "id": {
            #         "type": "string"
            #       },
            #       "title": {
            #         "type": "string"
            #       }
                
            #     }
            #   },
            #   "__example__": [
            #     {
            #       "id": "",
            #       "title": ""
                
            #     }
            
            #   ]
            # },
            #  "checkout": {
            #   "type": "array",
            #   "items": {
            #     "type": "object",
            #     "properties": {
            #       "id": {
            #         "type": "string"
            #       },
            #       "title": {
            #         "type": "string"
            #       }
                
            #     }
            #   },
            #   "__example__": [
            #     {
            #       "id": "",
            #       "title": ""
                
            #     }
            
            #   ]
            # }
            #             },
            #             "layout": {
            #                 "type": "SingleColumnLayout",
            #                 "children": [
            #                 {
            #                     "type": "Form",
            #                     "name": "text_input_form",
                                
            #                     "children": [
            #                     {
            #                         "type": "TextInput",
            #                         "required": True,
            #                         "label": "Full Name",
            #                         "name": "Name"
            #                     },
            #                     {
            #                         "type": "TextInput",
            #                         "input-type":"phone",
            #                         "helper-text":"Example: 8123456709",
            #                         "required": True,
            #                         "label": "Phone Number",
            #                         "name": "PhoneNumber"
            #                     },
            #                     {
            #                         "type": "TextInput",
            #                         "required": True,
            #                         "helper-text":"Example:Aadhar,PAN",
            #                         "label": "Government Id",
            #                         "name": "GovernmentId"
            #                     },
            #                     {
            #                         "type": "TextArea",
            #                         "required": True,
            #                         "label": "Address",
            #                         "name": "Address"
            #                     },
            #                     {
            #                         "type": "RadioButtonsGroup",
            #                         "name": "Room_Type",
            #                         "label": "Room type",
            #                         "required": True,
            #                         "data-source": "${data.allroom_types}",
            #                         "on-select-action": {
            #                         "name": "data_exchange",
            #                         "payload": {
            #                             "Room_type":"${form.Room_Type}"
            #                         }
            #                         }
            #                     },
            #                     {
            #                             "type": "Dropdown",
            #                             "name": "Luxury_Type",
            #                             "label": "Luxury Type",
            #                             "required": True,
            #                             "data-source": "${data.room}",
            #                             "on-select-action": {
            #                             "name": "data_exchange",
            #                             "payload": {
            #                                 "Luxury_Type": "${form.name}"
            #                             }
            #                             }
                                    
            #                     },
            #                       {
            #                             "type": "Dropdown",
            #                             "name": "CheckIn",
            #                             "label": "Check-In",
            #                             "required": True,
            #                             "data-source": "${data.checkin}",
                                    
            #                     },
            #                     {
            #                             "type": "Dropdown",
            #                             "name": "Checkout",
            #                             "label": "Check-Out",
            #                             "required": True,
            #                             "data-source": "${data.checkout}",
                                    
            #                     },
            #                     {
            #                         "type": "Footer",
            #                         "label": "Submit",
            #                         "on-click-action": {
            #                         "name": "complete",
            #                         "payload": {
            #                             "Guest_Name":"${form.Name}",
            #                             "Guest_Ph_Number":"${form.PhoneNumber}",
            #                             "Guest_GovernmentId":"${form.GovernmentId}",
            #                             "Guest_Address":"${form.Address}",
            #                             "Room_type":"${form.Room_Type}",
            #                             "Luxury_Type":"${form.Luxury_Type}",
            #                             "CheckIn":"${form.CheckIn}",
            #                             "Checkout":"${form.Checkout}"

            #                         }
            #                         }
            #                     }
            #                     ]
            #                 }
            #                 ]
            #             }
            #             }
            #         ]
            #         } 
            # file_path = f'C:/Vailo/04-01-2023/A_vMart/A_vMart/HotelRoomFlow.json'
            # with open(file_path, 'w') as file:
            #     json.dump(data, file, indent=2)
            # print("succesfully generated the json file..")

            # Url = f" https://graph.facebook.com/v18.0/1569901800509346/assets"

            # payload = {'name': 'flow.json',
            #         'asset_type': 'FLOW_JSON'}
            
            # files = [
            # ('file',
            #     ('file', open(file_path, 'r'), 'application/json'))
            # ]
            # header = {
            # 'Authorization': f'Bearer {faceBookToken}'
            # }

            # response = requests.request("POST", Url, headers=header, data=payload, files=files)
        

            # print(response.text)
            Hotel_rooms_type_obj=Hotel_rooms_type.objects.filter(client_id=clientId, marketplace_id=Hotel_marketplace_obj.id).order_by('room_price')
            cheapest_room=Hotel_rooms_type_obj.first()
            costliest_room=Hotel_rooms_type_obj.last()

            print("Hotel_rooms_type_obj",Hotel_rooms_type_obj)
            roomdetail_cards=[]
            for index, H_d in enumerate(Hotel_rooms_type_obj):
                roomdetail_cards.append(
                     {
                        "card_index": index,
                        "components": [
                        {
                            "type": "HEADER",
                            "parameters": [
                            {
                                "type": "IMAGE",
                                "image": {
                                "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(H_d.Hotel_room_image)
                                }
                            }
                            ]
                        },
                        {
                            "type": "BODY",
                            "parameters": [
                           
                            {
                                "type": "TEXT",
                                "text": H_d.room_info
                            },
                             {
                                "type": "TEXT",
                                "text": H_d.room_price
                            },
                            {
                                "type": "TEXT",
                                "text": H_d.room_price_unit
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
                                "payload": f"{H_d.client_id}_{H_d.marketplace_id}_{H_d.id}"
                            }
                            ]
                        },
                      
                        
                        
                        ]
                    },
                )

            payload=json.dumps(
            {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toUser,
            "type": "template",
            "template": {
                "name": "hotel_room_card_"+str(len(Hotel_rooms_type_obj)),
                "language": {
                "code": "en_US"
                },
                "components": [
                {
                    "type": "BODY",
                    "parameters": [
                    {
                        "type": "TEXT",
                        "text": cheapest_room.room_price
                    },
                    {
                        "type": "TEXT",
                        "text":costliest_room.room_price
                    },
                    {
                        "type": "TEXT",
                        "text": costliest_room.room_price_unit
                    }
                    ]
                },
                {
                    "type": "CAROUSEL",
                    "cards": roomdetail_cards
                  
                }
                ]
            }
            })
            response=requests.post(url,headers=headers,data=payload)
            print(response.text, response.status_code)
                        
          
        elif 'CheckOut' in message:
            message_info,hotel_id=message.split('=')
            Hotel_marketplace_obj=Hotel_marketplace.objects.get(client_id=clientId,hotel_id=hotel_id)
            Hotel_settings_obj=Hotel_settings.objects.get(client_id=clientId,marketplace_id=Hotel_marketplace_obj.id)
            guest_obj=Guest_info.objects.get(client_id=clientId,Phone_number=toUser)
            payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "to": toUser,
                                    "recipient_type": "individual",
                                    "type": "interactive",
                                    "interactive": {
                                        "type": "flow",
                                        "body": {
                                            "text": f"Welcome to {Hotel_marketplace_obj.hotel_name}.\nThank you choosing whatsapp for booking room(s).\nYou can fill and submit the form to book room(s) in our Hotel by tapping on the below button."
                                        },
                                        "action": {
                                            "name": "flow",
                                            "parameters": {
                                                "flow_message_version": "3",
                                                "flow_action": "data_exchange",
                                                "flow_token": f"Checkout_{clientId}_{Hotel_marketplace_obj.id}_{Hotel_settings_obj.id}_{guest_obj.id}",
                                                "mode": "draft",
                                                "flow_id": "416671310870642",

                                                "flow_cta": "Room Booking Form",
                                                
                                            }
                                        }
                                    }

                                })
            response = requests.request("POST", url, headers=headers, data=payload)
            print("hjdhdh")
            print(response.text)
            # Checkout_questions_obj=Checkout_questions.objects.filter(client_id=clientId,marketplace_id=Hotel_marketplace_obj.id).values('Question')
            
            # for i in Checkout_questions_obj
        else:
            
            print(whatsAppPhoneNumberId,clientId,toUser)
            #Hotelmarketplace_obj=Hotel_marketplace.objects.filter(client_id=clientId,hotel_id=1)
            datetime_now=datetime.now()
            print("datetime_now",datetime_now)
            utc_timezone = pytz.timezone('UTC')
            localized_datetime = utc_timezone.localize(datetime_now)
            print("localized_datetime",localized_datetime)
            # india_timezone = pytz.timezone('Asia/Kolkata')
            # datetime_india = india_timezone.localize(datetime_utc)
            # datetime_str=datetime.strftime(datetime_india,'%Y-%m-%d %H:%M:%S')
            # print(datetime_str)
            # datetime_obj=datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S')
            # print(datetime_obj)            
            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.filter(client_id=clientId,Guest_details__Phone_number=toUser,Check_Out__gte=localized_datetime)
            if Hotel_Room_Guest_info_obj.exists():
                print("In else block\nhotel_id")
                payload= json.dumps({
                        "messaging_product": "whatsapp",
                        "to": toUser,
                        "text": {
                            "preview_url": False,
                            "body": f"https://wa.me/{whatsapPhoneNumber}?text=hotel_id=1"
                        }
                    })

                response = requests.request('POST',url,headers=headers,data=payload)
            else:
                print("user not checked in or they are checked out")
    elif messageType == 'button':
        print(response_id)
        client_id,marketplace_id,room_type_id=response_id.split('_')
        Hotel_settings_obj=''
        if marketplace_id:
            Hotel_settings_obj=Hotel_settings.objects.get(client_id=clientId,marketplace_id=int(marketplace_id))
        else:
            Hotel_settings_obj=Hotel_settings.objects.get(client_id=clientId,marketplace_id=marketplace_id)
        Guest_info_obj=''
        room_exist=''
        guest=''
        
        try:
            Guest_info_obj=Guest_info.objects.get(client_id=clientId,Phone_number=toUser)
            print("Guest_info_obj",Guest_info_obj)
            room_exist='Exists'
            print("room_exist",room_exist)
            guest=Guest_info_obj.id
        except Exception as e:
            print(e)
        payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "to": toUser,
                                "recipient_type": "individual",
                                "type": "interactive",
                                "interactive": {
                                    "type": "flow",
                                    "body": {
                                        "text": f"Welcome to {Hotel_settings_obj.hotel_name}.\nThank you choosing whatsapp for booking room(s).\nYou can fill and submit the form to book room(s) in our Hotel by tapping on the below button."
                                    },
                                    "action": {
                                        "name": "flow",
                                        "parameters": {
                                            "flow_message_version": "3",
                                            "flow_action": "data_exchange",
                                            "flow_token": f"Room{room_exist}_{clientId}_{marketplace_id}_{Hotel_settings_obj.id}_{guest}_{room_type_id}",
                                            "mode": "draft",
                                            "flow_id": "1569901800509346",
                                            "flow_cta": "Room Booking Form",
                                            
                                        }
                                    }
                                }

                            })
        response = requests.request("POST", url, headers=headers, data=payload)
        print("hjdhdh")
        print(response.text)
        
    elif messageType == 'interactive':
        response_type,Hotel_Room_Guest_info_id,service_food_complaint_id,service_type= response_id.split('_')
        print("service_food_complaint_id",service_food_complaint_id)
        Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.get(id=Hotel_Room_Guest_info_id)
    
        if response_type == 'ACKNOWLEDGED':
            print("service_food_complaint_id",service_food_complaint_id)
            if service_type=='service':
                Service_order_obj=Service_order.objects.get(client_id=clientId,id=int(service_food_complaint_id))
                Service_order_obj.service_status=response_type
                Service_order_obj.save()
                
                payload=json.dumps({
                            "messaging_product":"whatsapp",
                            "recipient_type":"individual",
                            "to":Hotel_Room_Guest_info_obj.Guest_details.Phone_number,
                            "type":"text",
                            "text":{
                                "body":f"Hello *{Hotel_Room_Guest_info_obj.Guest_details.Guest_name}*,\nYour request for {Service_order_obj.hotel_service.service_name} is Acknowledged by our team. the service will be provided within few hours."
                            }
                        })
                response=requests.request('POST',url,headers=headers,data=payload)
                print(response.text)
            elif service_type == 'complaint':
                Complaint_info_obj= Complaint_info.objects.get(id=int(service_food_complaint_id))
                Complaint_info_obj.Complaint_status='ACKNOWLEDGED'
                Complaint_info_obj.save()
                payload=json.dumps({
                            "messaging_product":"whatsapp",
                            "recipient_type":"individual",
                            "to":Hotel_Room_Guest_info_obj.Guest_details.Phone_number,
                            "type":"text",
                            "text":{
                                "body":f"Hello *{Hotel_Room_Guest_info_obj.Guest_details.Guest_name}*,\nThe complaint raised by you - {Complaint_info_obj.Complaint_category.Complaint_category} is Acknowleded by our team. It may get resolved in few hours."
                            }
                        })
                response=requests.request('POST',url,headers=headers,data=payload)
                print(response.text)
        elif response_type == 'COMPLETED':
            if service_type=='service':
                Service_order_obj=Service_order.objects.get(client_id=clientId,id=int(service_food_complaint_id))
                Service_order_obj.service_status=response_type
                Service_order_obj.save()
                payload=json.dumps({
                            "messaging_product":"whatsapp",
                            "recipient_type":"individual",
                            "to":Hotel_Room_Guest_info_obj.Guest_details.Phone_number,
                            "type":"text",
                            "text":{
                                "body":f"Hello *{Hotel_Room_Guest_info_obj.Guest_details.Guest_name}*,\nYour request for {Service_order_obj.hotel_service.service_name} is successfully completed."
                            }
                        })
                response=requests.request('POST',url,headers=headers,data=payload)
                print(response.text)
            elif service_type == 'complaint':
                Complaint_info_obj= Complaint_info.objects.get(id=int(service_food_complaint_id))
                Complaint_info_obj.Complaint_status='COMPLETED'
                Complaint_info_obj.save()
                payload=json.dumps({
                            "messaging_product":"whatsapp",
                            "recipient_type":"individual",
                            "to":Hotel_Room_Guest_info_obj.Guest_details.Phone_number,
                            "type":"text",
                            "text":{
                                "body":f"Hello *{Hotel_Room_Guest_info_obj.Guest_details.Guest_name}*,\nThe complaint raised by you - {Complaint_info_obj.Complaint_category.Complaint_category} is resolved successfully."
                            }
                        })
                response=requests.request('POST',url,headers=headers,data=payload)
                print(response.text)
        elif response_type == 'ACCEPTED':
            Food_order_header_obj=Food_order_header.objects.get(client_id=clientId,id=int(service_food_complaint_id))
            Food_order_header_obj.order_status= response_type
            Food_order_header_obj.save()
            Food_order_details_obj=Food_order_details.objects.filter(Food_order_header_id=Food_order_header_obj.id)
            food_items_list='*Quantity    Item*\n'
            for i in Food_order_details_obj:
                food_items_list+=f"{i.Food_quantity}    {i.Food_Item.food_name}\n"

            payload=json.dumps({
                            "messaging_product":"whatsapp",
                            "recipient_type":"individual",
                            "to":Hotel_Room_Guest_info_obj.Guest_details.Phone_number,
                            "type":"text",
                            "text":{
                                "body":f"Hello *{Hotel_Room_Guest_info_obj.Guest_details.Guest_name}*,\nYour food order is received by our hotel.\n{food_items_list}You will get your food within few minutes."
                            }
                        })
            response=requests.request('POST',url,headers=headers,data=payload)
            print(response.text)
        elif response_type == 'DELIVERED':
            Food_order_header_obj=Food_order_header.objects.get(client_id=clientId,id=int(service_food_complaint_id))
            Food_order_header_obj.order_status= response_type
            Food_order_header_obj.save()
            Food_order_details_obj=Food_order_details.objects.filter(Food_order_header_id=Food_order_header_obj.id)
            food_items_list='*Quantity    Item*\n'
            for i in Food_order_details_obj:
                food_items_list+=f"{i.Food_quantity}    {i.Food_Item.food_name}\n"

            payload=json.dumps({
                            "messaging_product":"whatsapp",
                            "recipient_type":"individual",
                            "to":Hotel_Room_Guest_info_obj.Guest_details.Phone_number,
                            "type":"text",
                            "text":{
                                "body":f"Hello *{Hotel_Room_Guest_info_obj.Guest_details.Guest_name}*,\nHope food is delivered to your Room- {Hotel_Room_Guest_info_obj.Room_details.room_number} successfully.\n{food_items_list}"
                            }
                        })
            response=requests.request('POST',url,headers=headers,data=payload)
            print(response.text)

def process_donation_bot_message(message, response_id, messageType, request, url, headers, toUser, clientId,
                                 whatsAppPhoneNumberId, faceBookToken):
    if messageType == 'text':
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
    # process_donation_text_message(message, request, url, headers, toUser, clientId)
    elif messageType == 'interactive':
        process_donation_interactive_message(response_id, request, url, headers, toUser, clientId,
                                             whatsAppPhoneNumberId,
                                             faceBookToken)


def process_ticket_bot_message(message, response_id, messageType, request, url, headers, toUser, clientId,
                               whatsAppPhoneNumberId, faceBookToken):
    if messageType == 'text':
        process_ticket_text_message(message, request, url, headers, toUser, clientId)
    elif messageType == 'interactive':
        process_ticket_interactive_message(response_id, request, url, headers, toUser, clientId, whatsAppPhoneNumberId,
                                           faceBookToken)


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

        url = DomainName + 'redirectVailo/'

        # url='https://0937-116-75-94-183.ngrok.io/re/'
        # print('iiiiiiiiii',incoming_message)
        payload = json.dumps(incoming_message)
        headers = {

            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        return HttpResponse()
       

# @csrf_exempt
# def MY_bOT(request):
#     # print("*******",request.data)

#     request_data = json.loads(request.body)
#     received_message = request_data
#     print(received_message)
#     try:
#         if 'nfm_reply' in received_message['entry'][0]['changes'][0]['value']['messages'][0]['interactive']:
#             print("yes you are in flows")
#             whatsAppPhoneNumberId = received_message['entry'][0]['changes'][0]['value']['metadata'][
#                 'phone_number_id']
#             toUser = received_message['entry'][0]['changes'][0]['value']['messages'][0]['from']
#             print(whatsAppPhoneNumberId)
#             print(toUser)
#             response_json = \
#                 received_message['entry'][0]['changes'][0]['value']['messages'][0]['interactive'][
#                     'nfm_reply'][
#                     'response_json']

#             response_data = json.loads(response_json)
#             if all(key in response_data for key in ['firstName', 'lastName', 'email']):
#                 first_name = response_data.get('firstName')
#                 last_name = response_data.get('lastName')
#                 email = response_data.get('email')
#                 print(first_name)
#                 print(last_name)
#                 print(email)

#                 existing_visitor = Visitor.objects.filter(Visitor_Whatsapp_Number=toUser).first()

#                 if existing_visitor:
#                     # Update the existing record
#                     existing_visitor.Visitor_Name = f'{first_name} {last_name}'  # Combine first and last names
#                     existing_visitor.Visitor_email = email
#                     existing_visitor.save()
#                 else:
#                     # Create a new record
#                     new_visitor = Visitor(
#                         Visitor_Whatsapp_Number=toUser,
#                         Visitor_Name=f'{first_name} {last_name}',  # Combine first and last names
#                         Visitor_email=email
#                     )
#                     new_visitor.save()

#                 facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
#                 faceBookToken = ''
#                 # businessName = ''
#                 clientId = 0
#                 for tok in facebookObjects:
#                     faceBookToken = faceBookToken + tok.fb_access_token
#                     # businessName = businessName + tok.fb_name
#                     clientId = clientId + tok.client_id

#                 url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
#                 headers = {
#                     'Authorization': 'Bearer ' + faceBookToken,
#                     'Content-Type': 'application/json'
#                 }
#                 welcomeobj = Main_settings.objects.filter(client_id=clientId)

#                 for don_i in welcomeobj:
#                     if don_i.welcome_image:
#                         payload = json.dumps({
#                             "messaging_product": "whatsapp",
#                             "recipient_type": "individual",
#                             "to": toUser,
#                             "type": "interactive",
#                             "interactive": {
#                                 "type": "button",
#                                 "header": {
#                                     "type": "image",
#                                     "image": {
#                                         "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str
#                                         (don_i.welcome_image)
#                                     }
#                                 },

#                                 "body": {
#                                     "text": don_i.welcome_message if don_i.welcome_message else "."
#                                 },

#                                 "action": {
#                                     "buttons": [
#                                         {
#                                             "type": "reply",
#                                             "reply": {
#                                                 "id": "T123",
#                                                 "title": don_i.booking_button_name
#                                             }
#                                         },
#                                         {
#                                             "type": "reply",
#                                             "reply": {
#                                                 "id": "T2",
#                                                 "title": don_i.my_bookings_button_name
#                                             }
#                                         },
#                                         {
#                                             "type": "reply",
#                                             "reply": {
#                                                 "id": "T3",
#                                                 "title": don_i.contact_us_button_name
#                                             }
#                                         },

#                                     ]
#                                 }
#                             }
#                         })

#                         response = requests.request("POST", url, headers=headers, data=payload)
#             else:
#                 print("s it is coming to survey flow")
#                 poll_answer = response_data.get('radiobuttonsgroup')
#                 position = poll_answer.find("R")
#                 servey_question_id = poll_answer[:position]
#                 print(servey_question_id)
#                 poll_response_id = poll_answer[position:]
#                 print(poll_response_id)
#                 question_info = Survey_Question.objects.filter(id=servey_question_id)
#                 response_value = ''
#                 survey_id = 0
#                 for q_i in question_info:
#                     survey_id = q_i.Survey_list_id
#                     if poll_response_id == "R1":
#                         response_value = q_i.response_option1
#                     elif poll_response_id == "R2":
#                         response_value = q_i.response_option2
#                     elif poll_response_id == "R3":
#                         response_value = q_i.response_option3
#                     elif poll_response_id == "R4":
#                         response_value = q_i.response_option4
#                 print(response_value)
#                 print(survey_id)
#                 facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
#                 faceBookToken = ''
#                 # businessName = ''
#                 clientId = 0
#                 for tok in facebookObjects:
#                     faceBookToken = faceBookToken + tok.fb_access_token
#                     # businessName = businessName + tok.fb_name
#                     clientId = clientId + tok.client_id
#                 print(clientId)
#                 customer_info = Survey_Customer.objects.filter(customer_whatsapp_number=toUser)
#                 customer_id = 0
#                 for c_i in customer_info:
#                     customer_id = c_i.id
#                 print(customer_id)
#                 print("s printed all the ids please check once")
#                 survey_customer_response = Survey_Customer_Response(
#                     client_id=clientId,
#                     Survey_list_id=survey_id,
#                     Survey_Question_id=servey_question_id,
#                     Survey_Customer_id=customer_id,
#                     Survey_Response=response_value

#                 )
#                 survey_customer_response.save()
#                 print("succcesfully saved all the data")
#                 url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
#                 headers = {
#                     'Authorization': 'Bearer ' + faceBookToken,
#                     'Content-Type': 'application/json'
#                 }
#                 payload = json.dumps({
#                     "messaging_product": "whatsapp",
#                     "recipient_type": "individual",
#                     "to": toUser,
#                     "type": "text",
#                     "text": {
#                         "body": "Thank you for Voting"
#                     }
#                 })

#                 response = requests.request("POST", url, headers=headers, data=payload)


#     except KeyError as e:
#         print(f"KeyError occurred: {e}")
#     first_key_from_meesage, first_value_from_message = next(iter(received_message.items()))
#     # print(first_key_from_meesage,first_value_from_message)

#     if first_key_from_meesage == "object" and first_value_from_message == "whatsapp_business_account":

#         url_for_domain = DomainName[:-1]
#         # url_for_domain='https://0937-116-75-94-183.ngrok.io'
#         b = ''
#         for i in request:
#             b = b + str(i)[2:-1]

#         x = b.replace('true', 'True')
#         y = x.replace('false', 'False')
#         res = ast.literal_eval(y)

#         # print("+++++++++",res)
#         key_var = res['entry'][0]['changes'][0]['value'].keys()
#         condition_list = list(key_var)

#         if 'messages' in condition_list:
#             messageType = res['entry'][0]['changes'][0]['value']['messages'][0]['type']
#             whatsAppPhoneNumberId = res['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
#             toUser = res['entry'][0]['changes'][0]['value']['messages'][0]['from']
#             message = ''
#             button_type = ''
#             response_id = ''
#             list_title = ''

#             if messageType == 'text':
#                 message = res['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

#             if messageType == 'interactive':
#                 button_type = res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['type']
#                 if button_type == 'button_reply':
#                     response_id = res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['button_reply'][
#                         'id']
#                 elif button_type == 'list_reply':
#                     response_id = res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['list_reply'][
#                         'id']
#                     list_title = res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['list_reply'][
#                         'title']

#             facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
#             faceBookToken = ''
#             # businessName = ''
#             clientId = 0
#             for tok in facebookObjects:
#                 faceBookToken = faceBookToken + tok.fb_access_token
#                 # businessName = businessName + tok.fb_name
#                 clientId = clientId + tok.client_id

#             # ____________________________________API URL and HEADERS__________________________________

#             url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
#             headers = {
#                 'Authorization': 'Bearer ' + faceBookToken,
#                 'Content-Type': 'application/json'
#             }

#             # __________________________________________________________________________________________

#             adminPermissionObjects = admin_permission.objects.filter(client_id=clientId)

#             for clientIdI in adminPermissionObjects:
#                 if clientIdI.client_service_type == 'commerce':
#                     if clientIdI.client_permission_status == True:
#                         process_health_bot_message(message, response_id, messageType, request, url, headers, toUser,
#                                                    clientId, whatsAppPhoneNumberId, faceBookToken)


#                 elif clientIdI.client_service_type == 'ticket':
#                     if clientIdI.client_permission_status == True:
#                         process_ticket_bot_message(message, response_id, messageType, request, url, headers, toUser,
#                                                    clientId, whatsAppPhoneNumberId, faceBookToken)
#                     else:
#                         print("waiting for admin approval")
#                 elif clientIdI.client_service_type == 'donation':
#                     if clientIdI.client_permission_status == True:
#                         process_donation_bot_message(message, response_id, messageType, request, url, headers, toUser,
#                                                      clientId, whatsAppPhoneNumberId, faceBookToken)


#                 elif clientIdI.client_service_type == 'appointement' or 'Appointement':
#                     project='Appointment' #Appointement or Sports or Servicenow
#                     process_appointement_bot_message(message, response_id, messageType, request, url, headers, toUser,
#                                                      clientId, whatsAppPhoneNumberId, faceBookToken, list_title,project)


#     elif first_key_from_meesage == "account_id":

#         pymt_reference_id = received_message['payload']["payment_link"]['entity']['reference_id']
#         print(pymt_reference_id)
#         first_refer_character = pymt_reference_id[0]
#         print(first_refer_character)
#         if first_refer_character == 'T':
#             # failed_reference_id = received_message['payload']['payment']['entity']['notes']['polacy_name']
#             # print(failed_reference_id)
#             ticket_reference_id = pymt_reference_id[1:]
#             pymt_status = received_message['payload']['payment']['entity']['status']
#             print(pymt_status)

#             # update_payment_status(payment_reference_id,payment_status)

#             payment_cart_details = event_ticket_cart_header.objects.filter(payment_reference_id=ticket_reference_id)
#             print("going to save")

#             for i in payment_cart_details:
#                 if pymt_status == "captured" or "paid":
#                     if i.payment_reference_id == ticket_reference_id:
#                         i.payment_status = 1
#                         i.save()
#                         print("saved")
#                 # elif pymt_status == 'failed':
#                 #     print("yes payment has been failed")
#                 #     if i.payment_reference_id == failed_reference_id:
#                 #         i.payment_status = 2
#                 #         i.save()

#                 # if i.payment_reference_id == pymt_reference_id:
#                 #     if pymt_status == "captured":
#                 #         print("k")
#                 #         i.payment_status = 1
#                 #         i.save()
#                 #     elif pymt_status == "failed":
#                 #         print('f')
#                 #         i.payment_status = 2
#                 #         i.save()
#                 #     else:
#                 #         i.payment_status = 3
#                 #         i.save()
#                 break

#             payment_details = event_ticket_cart_header.objects.filter(payment_reference_id=ticket_reference_id)
#             clientID = ''
#             toUser = ''
#             for p in payment_details:
#                 toUser = p.customer_phone_number
#                 print(toUser)
#                 clientID = p.client_id
#                 facebookuseObjects = facebook_details.objects.filter(client_id=clientID)
#                 faceeBookToken = ""
#                 fbb_phone_number_id = ""
#                 for j in facebookuseObjects:
#                     fbb_phone_number_id = j.fb_phone_number_id
#                     faceeBookToken = j.fb_access_token

#                 if p.payment_status == 1:
#                     print("vailo")
#                     event_payment_information = event_settings.objects.filter(client_id=clientID)
#                     ticketconformationmessage = ''
#                     for q in event_payment_information:
#                         ticketconformationmessage = ticketconformationmessage + q.ticket_conformation_message_body
#                         if q.ticket_conformation_header_image:
#                             url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
#                             headers = {
#                                 'Authorization': 'Bearer ' + faceeBookToken,
#                                 'Content-Type': 'application/json'
#                             }

#                             payload = json.dumps({
#                                 "messaging_product": "whatsapp",
#                                 "recipient_type": "individual",
#                                 "to": toUser,
#                                 "type": "image",
#                                 "image": {
#                                     "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
#                                         q.ticket_conformation_header_image)

#                                 }
#                             })
#                             response = requests.request("POST", url, headers=headers, data=payload)
#                             time.sleep(1)

#                             url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
#                             headers = {
#                                 'Authorization': 'Bearer ' + faceeBookToken,
#                                 'Content-Type': 'application/json'
#                             }

#                             payload = json.dumps({
#                                 "messaging_product": "whatsapp",
#                                 "recipient_type": "individual",
#                                 "to": toUser,
#                                 "type": "text",
#                                 "text": {
#                                     "body": ticketconformationmessage if ticketconformationmessage else "."
#                                 }
#                             })

#                             response = requests.request("POST", url, headers=headers, data=payload)
#                             customer_sent(request, toUser, clientID)
#                         else:

#                             url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
#                             headers = {
#                                 'Authorization': 'Bearer ' + faceeBookToken,
#                                 'Content-Type': 'application/json'
#                             }

#                             payload = json.dumps({
#                                 "messaging_product": "whatsapp",
#                                 "recipient_type": "individual",
#                                 "to": toUser,
#                                 "type": "text",
#                                 "text": {
#                                     "body": ticketconformationmessage if ticketconformationmessage else "."
#                                 }
#                             })

#                             response = requests.request("POST", url, headers=headers, data=payload)
#                             customer_sent(request, toUser, clientID)
#                     ticket_qr = ticket_information.objects.filter(client_id=clientID,
#                                                                   payment_reference_id=ticket_reference_id)
#                     print(ticket_qr)
#                     for ticket in ticket_qr:
#                         ticket.customer_phone_number = str(toUser)
#                         url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
#                         headers = {
#                             'Authorization': 'Bearer ' + faceeBookToken,
#                             'Content-Type': 'application/json'
#                         }

#                         payload = json.dumps({
#                             "messaging_product": "whatsapp",
#                             "recipient_type": "individual",
#                             "to": toUser,
#                             "type": "image",
#                             "image": {
#                                 "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
#                                     ticket.ticket_QR)
#                             }
#                         })
#                         response = requests.request("POST", url, headers=headers, data=payload)
#                         customer_sent(request, toUser, clientID)
#                         ticket.ticket_status = 30
#                         ticket.save()

#                     # payment_cart = event_ticket_cart_details.objects.filter(client_id=clientID,cart_id_id=p.id)
#                     # print(payment_cart)
#                     # tickets = ""
#                     # for c in payment_cart:
#                     #     # tickets = c.number_of_tickets
#                     #     # print("z")
#                     #     payment_ticket_information = ticket_information.objects.filter(client_id=clientID,
#                     #                                                                    event_ticket_category_id=c.category_id,
#                     #                                                                    ticket_status=20,payment_reference_id=pymt_reference_id)

#                     #     # payment_ticket_information.customer_phone_number = str(toUser)
#                     #     print(payment_ticket_information)

#                     #     for e in payment_ticket_information[:c.number_of_tickets]:
#                     #         print(c.number_of_tickets)
#                     #         e.customer_phone_number = str(toUser)
#                     #         print("varan")
#                     #         url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
#                     #         headers = {
#                     #             'Authorization': 'Bearer ' + faceeBookToken,
#                     #             'Content-Type': 'application/json'
#                     #         }

#                     #         payload = json.dumps({
#                     #             "messaging_product": "whatsapp",
#                     #             "recipient_type": "individual",
#                     #             "to": toUser,
#                     #             "type": "image",
#                     #             "image": {
#                     #                 "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
#                     #                     e.ticket_QR)

#                     #             }
#                     #         })
#                     #         response = requests.request("POST", url, headers=headers, data=payload)
#                     #         customer_sent(request, toUser, clientID)
#                     #         e.ticket_status = 30
#                     #         e.save()
#                 else:
#                     print("failure")
#                     event_payment_information = event_settings.objects.filter(client_id=clientID)
#                     ticketpaymentfailuremessage = ''
#                     for z in event_payment_information:
#                         ticketpaymentfailuremessage = ticketpaymentfailuremessage + z.ticket_failure_message_body
#                         if z.ticket_payment_failure_image:
#                             url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
#                             headers = {
#                                 'Authorization': 'Bearer ' + faceeBookToken,
#                                 'Content-Type': 'application/json'
#                             }

#                             payload = json.dumps({
#                                 "messaging_product": "whatsapp",
#                                 "recipient_type": "individual",
#                                 "to": toUser,
#                                 "type": "image",
#                                 "image": {
#                                     "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
#                                         z.ticket_payment_failure_image)

#                                 }
#                             })
#                             response = requests.request("POST", url, headers=headers, data=payload)
#                             time.sleep(2)

#                             url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
#                             headers = {
#                                 'Authorization': 'Bearer ' + faceeBookToken,
#                                 'Content-Type': 'application/json'
#                             }

#                             payload = json.dumps({
#                                 "messaging_product": "whatsapp",
#                                 "recipient_type": "individual",
#                                 "to": toUser,
#                                 "type": "text",
#                                 "text": {
#                                     "body": ticketpaymentfailuremessage if ticketpaymentfailuremessage else "."
#                                 }
#                             })

#                             response = requests.request("POST", url, headers=headers, data=payload)
#                             customer_sent(request, toUser, clientID)
#                         else:
#                             url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
#                             headers = {
#                                 'Authorization': 'Bearer ' + faceeBookToken,
#                                 'Content-Type': 'application/json'
#                             }

#                             payload = json.dumps({
#                                 "messaging_product": "whatsapp",
#                                 "recipient_type": "individual",
#                                 "to": toUser,
#                                 "type": "text",
#                                 "text": {
#                                     "body": ticketpaymentfailuremessage if ticketpaymentfailuremessage else "."
#                                 }
#                             })

#                             response = requests.request("POST", url, headers=headers, data=payload)
#                             customer_sent(request, toUser, clientID)

#         elif first_refer_character == 'N':

#             print('please wait to update your payment status in database')
#             donate_refer_id = pymt_reference_id[1:]
#             # pymt_status = received_message['payload']['payment']['entity']['status']
#             pymt_status = received_message['payload']["payment_link"]['entity']['status']
#             is_processed = donation_details.objects.filter(donation_reference_id=donate_refer_id,
#                                                            payment_status=1).exists()

#             if pymt_status == 'paid' and not is_processed:

#                 dynamicDataObj = donation_details.objects.filter(donation_reference_id=donate_refer_id)
#                 for dy_i in dynamicDataObj:
#                     clientid = dy_i.client_id
#                     if dy_i.donation_reference_id == donate_refer_id:
#                         dy_i.payment_status = 1
#                         dy_i.save()

#                     detailsOrgObject = donation_settings.objects.filter(client_id=clientid)
#                     for org_i in detailsOrgObject:
#                         templateLoader = jinja2.FileSystemLoader(searchpath="./")
#                         templateEnv = jinja2.Environment(loader=templateLoader)
#                         TEMPLATE_FILE = "templates/invoice.html"
#                         print("mohan")
#                         template = templateEnv.get_template(TEMPLATE_FILE)
#                         print(template)
#                         print("kav")

#                         body = {
#                             "data": {
#                                 "donation_name": dy_i.donation_name,
#                                 "donation_date": dy_i.donation_date,
#                                 "donation_amount": dy_i.donation_amount,
#                                 "donar_name": dy_i.donar_name,
#                                 "donar_email": dy_i.donar_email,
#                                 "donar_phone": dy_i.donar_phone_number,
#                                 "donation_desc": dy_i.donation_description,
#                                 "donation_short_desc": dy_i.donation_short_description,
#                                 "reference_id": dy_i.donation_reference_id,
#                                 "ngo_logo": org_i.ngo_logo,
#                                 "ngo_name": org_i.ngo_name,
#                                 "ngo_pan": org_i.ngo_pan,
#                                 "ngo_gstin": org_i.ngo_gstin,
#                                 "ngo_header_notes": org_i.ngo_header_notes,
#                                 "ngo_footer_notes": org_i.ngo_footer_notes,
#                                 "ngo_signatureHeader": org_i.ngo_signature_header,
#                                 "ngo_signatureImage": org_i.ngo_signature_image,
#                                 "ngo_Footer": org_i.ngo_signature_footer,
#                                 "invoiceFooter": org_i.invoice_footer

#                             }
#                         }
#                         sourceHtml = template.render(json_data=body["data"])
#                         print(sourceHtml)
#                         outputFilename = f"receipt_{dy_i.id}.pdf"
#                         pdf_content = BytesIO()
#                         pisa.CreatePDF(
#                             src=sourceHtml,  # the HTML to convert
#                             dest=pdf_content)
#                         pdf_content.seek(0)
#                         dy_i.receipient_pdf.save(outputFilename, pdf_content, save=True)
#                         pdf_display(request, donate_refer_id)
#                         # is_processed = True
#                         # pdf_content_with_metadata = BytesIO()
#                         # pdf = PyPDF2.PdfReader(pdf_content)
#                         # pdf_writer = PyPDF2.PdfWriter()
#                         # pdf_writer.add_page(pdf.pages[0])
#                         # pdf_writer.add_metadata({
#                         #     '/Filename':outputFilename,
#                         #     '/Title': outputFilename,
#                         #     '/Author': 'Vividhity Ventures Private Limited'
#                         #
#                         #     # Add more properties as needed
#                         # })
#                         # pdf_writer.write(pdf_content_with_metadata)
#                         # pdf_content_with_metadata.seek(0)

#                         # pdfobj = donation_details.objects.filter(donation_reference_id=donate_refer_id)
#                         # for pdf_i in pdfobj:
#                         #     pdf_i.receipient_pdf.save(outputFilename, pdf_content, save=True)
#                         #
#                 # donationDetailsobj = donation_details.objects.filter(donation_reference_id=donate_refer_id)
#                 # for ngo_i in donationDetailsobj:
#                 #     print('suceess')
#                 #     if ngo_i.donation_reference_id == donate_refer_id:
#                 #         print("saved")
#                 #         ngo_i.payment_status = 1
#                 #         ngo_i.save()
#                 # pdf_display(request, donate_refer_id)
#             else:
#                 print('iam finded error')
#             # if is_processed:
#             #     pdf_display(request, donate_refer_id)


#     elif first_key_from_meesage == "entity":

#         failed_reference_id = received_message['payload']['payment']['entity']['notes']['polacy_name']
#         print(failed_reference_id)
#         first_letter = failed_reference_id[0]
#         if first_letter == "T":

#             tfailed_refer_id = failed_reference_id[1:]
#             pymt_status = received_message['payload']['payment']['entity']['status']

#             fail_payment_cart_details = event_ticket_cart_header.objects.filter(payment_reference_id=tfailed_refer_id)
#             for fail_i in fail_payment_cart_details:
#                 if pymt_status == "failed":
#                     if fail_i.payment_reference_id == tfailed_refer_id:
#                         fail_i.payment_status = 2
#                         fail_i.save()
#             payment_details = event_ticket_cart_header.objects.filter(payment_reference_id=tfailed_refer_id)
#             clientID = ''
#             toUser = ''
#             for p in payment_details:
#                 toUser = p.customer_phone_number
#                 print(toUser)
#                 clientID = p.client_id
#                 facebookuseObjects = facebook_details.objects.filter(client_id=clientID)
#                 faceeBookToken = ""
#                 fbb_phone_number_id = ""
#                 for j in facebookuseObjects:
#                     fbb_phone_number_id = j.fb_phone_number_id
#                     faceeBookToken = j.fb_access_token
#                 if p.payment_status == 2:
#                     event_payment_information = event_settings.objects.filter(client_id=clientID)
#                     ticketpaymentfailuremessage = ''
#                     for z in event_payment_information:
#                         ticketpaymentfailuremessage = ticketpaymentfailuremessage + z.ticket_failure_message_body
#                         if z.ticket_payment_failure_image:
#                             url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
#                             headers = {
#                                 'Authorization': 'Bearer ' + faceeBookToken,
#                                 'Content-Type': 'application/json'
#                             }
#                             payload = json.dumps({
#                                 "messaging_product": "whatsapp",
#                                 "recipient_type": "individual",
#                                 "to": toUser,
#                                 "type": "image",
#                                 "image": {
#                                     "link": 'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/' + str(
#                                         z.ticket_payment_failure_image)

#                                 }
#                             })
#                             response = requests.request("POST", url, headers=headers, data=payload)
#                             time.sleep(2)

#                             url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
#                             headers = {
#                                 'Authorization': 'Bearer ' + faceeBookToken,
#                                 'Content-Type': 'application/json'
#                             }

#                             payload = json.dumps({
#                                 "messaging_product": "whatsapp",
#                                 "recipient_type": "individual",
#                                 "to": toUser,
#                                 "type": "text",
#                                 "text": {
#                                     "body": ticketpaymentfailuremessage if ticketpaymentfailuremessage else "."
#                                 }
#                             })

#                             response = requests.request("POST", url, headers=headers, data=payload)
#                             customer_sent(request, toUser, clientID)
#                         else:
#                             url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
#                             headers = {
#                                 'Authorization': 'Bearer ' + faceeBookToken,
#                                 'Content-Type': 'application/json'
#                             }

#                             payload = json.dumps({
#                                 "messaging_product": "whatsapp",
#                                 "recipient_type": "individual",
#                                 "to": toUser,
#                                 "type": "text",
#                                 "text": {
#                                     "body": ticketpaymentfailuremessage if ticketpaymentfailuremessage else "."
#                                 }
#                             })

#                             response = requests.request("POST", url, headers=headers, data=payload)
#                             customer_sent(request, toUser, clientID)
#         elif first_letter == "N":
#             ngo_refer_id = failed_reference_id[1:]
#             pymt_status = received_message['payload']['payment']['entity']['status']

#             failureInfo = donation_details.objects.filter(donation_reference_id=ngo_refer_id)
#             for ngo_i in failureInfo:
#                 if pymt_status == 'failed' or 'Failed':
#                     if ngo_i.donation_reference_id == ngo_refer_id:
#                         ngo_i.payment_status = 2
#                         ngo_i.save()
#             paymentdetails = donation_details.objects.filter(donation_reference_id=ngo_refer_id)
#             for p in paymentdetails:
#                 toUser = p.donar_phone_number
#                 print(toUser)
#                 clientID = p.client_id
#                 facebookuseObjects = facebook_details.objects.filter(client_id=clientID)
#                 faceeBookToken = ""
#                 fbb_phone_number_id = ""
#                 for j in facebookuseObjects:
#                     fbb_phone_number_id = j.fb_phone_number_id
#                     faceeBookToken = j.fb_access_token
#                 if p.payment_status == 2:
#                     settingsobj = donation_settings.objects.filter(client_id=clientID)
#                     for s_i in settingsobj:
#                         url = "https://graph.facebook.com/v12.0/" + str(fbb_phone_number_id) + "/messages"
#                         headers = {
#                             'Authorization': 'Bearer ' + faceeBookToken,
#                             'Content-Type': 'application/json'
#                         }

#                         payload = json.dumps({
#                             "messaging_product": "whatsapp",
#                             "recipient_type": "individual",
#                             "to": toUser,
#                             "type": "text",
#                             "text": {
#                                 "body": s_i.donation_failure_message if s_i.donation_failure_message else "."
#                             }
#                         })
#                         response = requests.request("POST", url, headers=headers, data=payload)


#     else:
#         print("else block")
#         # uname = received_message['name']
#         # uemail = received_message['email']
#         # uphone = received_message['phone']
#         # phone_number = "91"+ uphone.strip() 
#         # print(uphone)
#         # id = received_message['formid']
#         tid = received_message['formid']
#         first_character = tid[0]
#         if first_character == 'T':
#             print("ij")
#             reference_characters = tid[1:37]
#             ticket_id = tid[37:]
#             uphone = received_message['phone']
#             phone_number = "91" + uphone.strip()
#             tick_info = ticket_information.objects.filter(id=ticket_id, payment_reference_id=reference_characters)
#             print(tick_info)
#             for ti_i in tick_info:
#                 ti_i.customer_phone_number = phone_number
#                 ti_i.save()
#         elif first_character == 'N':
#             print("gg")
#             donar_refId = tid[2:38]
#             print(donar_refId)
#             responseId = tid[38:]
#             dclientID = received_message['cid']
#             donarName = received_message['name']
#             donarEmail = received_message['email']
#             donarPan = received_message['pan']
#             donarAmount = received_message['amount']
#             donarcomments = received_message['comments']
#             donationName = ''
#             donationshortdesc = ''
#             donationdesc = ''
#             donationImage = ''
#             donation_detailsobj = donation_types.objects.filter(client_id=dclientID, id=responseId)
#             print(donation_detailsobj)
#             for dj_i in donation_detailsobj:
#                 donationName = donationName + dj_i.donation_name
#                 donationshortdesc = donationshortdesc + dj_i.donation_short_description
#                 donationdesc = donationdesc + dj_i.donation_description
#                 donationImage = dj_i.donation_type_image
#             print(donationName)

#             donar_details = donation_details.objects.filter(client_id=dclientID, donation_reference_id=donar_refId)
#             print("bb")
#             for dd_i in donar_details:
#                 dd_i.donar_name = donarName
#                 dd_i.donar_email = donarEmail
#                 dd_i.donar_pan_number = donarPan
#                 dd_i.donation_amount = donarAmount
#                 dd_i.donation_name = donationName
#                 dd_i.donation_short_description = donationshortdesc
#                 dd_i.donation_description = donationdesc
#                 dd_i.donation_type_image = donationImage
#                 dd_i.donation_date = timezone.now().date()
#                 dd_i.donation_comments_message = donarcomments
#                 dd_i.save()
#             N3(request, donar_refId, dclientID)

#         elif first_character == 'P':
#             print("P section")
#             donar_refId = tid[2:38]
#             dclientID = received_message['cid']
#             donarName = received_message['name']
#             donarEmail = received_message['email']
#             donarPan = received_message['pan']
#             donarAmount = received_message['amount']
#             donarcomments = received_message['comments']
#             donar_details = donation_details.objects.filter(client_id=dclientID, donation_reference_id=donar_refId)
#             for dd_i in donar_details:
#                 dd_i.donar_name = donarName
#                 dd_i.donar_email = donarEmail
#                 dd_i.donar_pan_number = donarPan
#                 dd_i.donation_amount = donarAmount
#                 dd_i.donation_date = timezone.now().date()
#                 dd_i.donation_comments_message = donarcomments
#                 dd_i.save()

#         # print(uname)
#         # print(uemail)
#         # print(uphone)  
#         # print(id)
#         # uid = str(id)[:12]
#         # clientId = str(id)[12:]
#         # customerdetails = ticket_customer_master.objects.filter(client_id=clientId,Customer_Phone_Number=uid)
#         # for customer_i in customerdetails:
#         #     customer_i.Customer_First_Name = uname
#         #     customer_i.Customer_Email = uemail
#         #     customer_i.save()

#     return HttpResponse('ticket')
@csrf_exempt
def bot(request):
    print("sssss mouli   number is 6303")
    # print("*******",request.data)

    print("MY_bot")
    request_data = json.loads(request.body)
    received_message = request_data
    # print(received_message, ": received message")

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
          
            
            print("response_data",response_data)
           
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
                    print('for')
                    if don_i.welcome_image:
                        print('if')
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
                        print("response: ",response.text,response.status_code)
    #---------------------Servicenow------------------------------------
            elif all(key in response_data for key in ['username', 'password']):
                user_name = response_data.get('username')
                password = response_data.get('password')
                # email = response_data.get('email')
                print("username:", user_name)
                print("password", password)
                import base64
                # username = "David.Miller"
                # password = "123Vivid$$"
                credentials = f"{user_name}:{password}"
                encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

                url = f"https://dev164889.service-now.com/api/now/table/sys_user?sysparm_query=user_name={user_name}"
                payload = {}
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Basic {encoded_credentials}',
                    'Cookie': 'BIGipServerpool_dev164889=3331282698.40766.0000; JSESSIONID=6313C1AA239A358068CEDBC3290CF2E0; glide_session_store=B03880BA9762F110FB3B5C900153AFD9; glide_user_activity=U0N2M18xOnIwd2g0NnduQ0UrR1JpSWxldDZpU09jdDFxNUMzcjNuSHJvbzN6SzkrOWs9OnNBV3JZeloxSUdyL0QxcGNGYTI3K2M2QTFnYnNnRmZMUk1JV25yQ2lwbVU9; glide_user_route=glide.204f61c181048880583f00591ea5c8d1'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                print("response.text: ", response.text, response.status_code)
                if response.status_code == 200:
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
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "to": toUser,
                        "recipient_type": "individual",
                        "type": "interactive",
                        "interactive": {
                            "type": "flow",
                            "body": {
                                "text": "Choose from the available menu options to proceed further-\nCreate a new ticket, Search tickets, Check your created tickets/ Assigned tickets"
                            },
                            "action": {
                                "name": "flow",
                                "parameters": {
                                    "flow_message_version": "3",
                                    "flow_action": "data_exchange",
                                    "flow_token": encoded_credentials,
                                    
                                    "flow_id": "396267926422867",
                                    

                                    "flow_cta": "Choose from Options",
                                }
                            }
                        }

                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    print("hjdhdh")
                    print(response.text)


                else:
                    print("else: ", response.status_code, response.text)
                    facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                    faceBookToken = ''
                    # businessName = ''
                    clientId = 5290.0
                    for tok in facebookObjects:
                        faceBookToken = faceBookToken + tok.fb_access_token
                        # businessName = businessName + tok.fb_name
                        clientId = clientId + tok.client_id
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
                            "body": "Credentials are wrong",
                        }
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
            elif all(key in response_data for key in ['assignment_group', 'Impact', 'Description']):
                print("log a ticket")
                Description = response_data.get('Description')
                assignment_group = response_data.get('assignment_group')

                Impact = response_data.get('Impact')

                credentials = response_data.get('flow_token')
                print(Description, assignment_group, Impact, credentials, " posting a ticket is going to done")
                url = "https://dev164889.service-now.com/api/now/table/incident"
                data = json.dumps({
                    "short_description": f"{Description}",
                    "impact": f"{Impact}",
                    "assignment_group": f"{assignment_group}",
                })
                headers = {
                    "Authorization": "Basic " + credentials,
                    "Content-Type": "application/json",
                }
                response = requests.post(url, headers=headers, data=data)
                print("posting a ticket in servicenow: ", response.text, response.status_code)
                if response.status_code == 201:
                    print("response: ")
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
                            "body": "Ticket succeessfully raised",
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)
                    facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                    faceBookToken = ''
                    # businessName = ''
                    clientId = 0
                    for tok in facebookObjects:
                        faceBookToken = faceBookToken + tok.fb_access_token
                        # businessName = businessName + tok.fb_name
                        clientId = clientId + tok.client_id
                    print("whatsapp detailes",faceBookToken,whatsAppPhoneNumberId)
                    url = "https://graph.facebook.com/v18.0/" + str(whatsAppPhoneNumberId) + "/messages"
                    headers = {
                        'Authorization': 'Bearer ' + faceBookToken,
                        'Content-Type': 'application/json'
                    }
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "to": toUser,
                        "recipient_type": "individual",
                        "type": "interactive",
                        "interactive": {
                            "type": "flow",
                            "body": {
                                "text": "Choose from the available menu options to proceed further-\nCreate a new ticket, Search tickets, Check your created tickets/ Assigned tickets"
                            },
                            "action": {
                                "name": "flow",
                                "parameters": {
                                    "flow_message_version": "3",
                                    "flow_action": "data_exchange",
                                    "flow_token": credentials,
                                    
                                    "flow_id": "396267926422867",
                                    

                                    "flow_cta": "Choose from Options",
                                }
                            }
                        }

                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    print("hjdhdh")
                    print(response.text)
                else:
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
                            "body": "please enter valid details",
                        }
                    })

                    response = requests.request("POST", url, headers=headers, data=payload)
            elif all(key in response_data for key in ['Number', 'Description', 'assigned_to_OR_Created_by', 'Status']):
                Description = response_data.get('Description')
                Number = response_data.get('Number')
                assigned_to_OR_Created_by = response_data.get('assigned_to_OR_Created_by')

                status = response_data.get('status')
                import base64
                # dic={'Description':Description,'Number':Number}
                # for key in dic:
                #     if dic[key]!='':
                #         value = globals()[key]
                #         print("value",value)
                #         if(value):
                #             url_append+=('{'+key+'}'+'='+'{'+value+'}''^')
                #             print("if",url_append)
                # else:
                #      url_append+=('{'+key+'}'+'='+'{'+value+'}''^')

                # if key in globals():
                #     print("key:",key)
                #     value = globals()[key]
                #     print("value",value)

                # else:
                #     print("if not workin")
                # print("url_append: ",url_append)           
                credentials = response_data.get('flow_token')
                decoded_bytes = base64.b64decode(credentials)
                decoded_string = decoded_bytes.decode('utf-8')
                print(decoded_string)
                username, password = decoded_string.split(':')
                print(username)
                print(password)

                option = ''
                url_append = ''

                if assigned_to_OR_Created_by == "assigned_to":
                    option = assigned_to_OR_Created_by
                elif assigned_to_OR_Created_by == "created_by":
                    option = "sys_" + assigned_to_OR_Created_by

                url = f"https://dev164889.service-now.com/api/now/table/incident?sysparm_query=number%3d{Number}"
                print(url)
                headers = {
                    "Authorization": "Basic " + credentials,
                    "Content-Type": "application/json",
                }
                data = {}

                response = requests.get(url, headers=headers, data=data)
                print("Serching a ticket: ", response.text, response.status_code)
                response_json = response.json()
                result = response_json.get('result')
                print(result, type(result), len(result))

                #    url=f"https://dev164889.service-now.com/api/now/table/incident?sysparm_query=assigned_to={sys_id}^active=true&sysparm_fields=number%2Curgency%2Cimpact%2Csys_created_by%2Csys_updated_by%2Cpriority%2Cstate^%2Cactive%2Copened_at%2Csys_id%2Cshort_description%2Csys_created_on%2Cassigned_to"
                #    headers={
                #     "Authorization": "Basic "+response_id[2:],
                #    }
                # response=requests.get(url,headers=headers)

                # print(response.text,response.status_code)
                # response_json=response.json()
                # result=response_json.get('result')
                # print("length: ",len(result))
                # ---------------------------------------------------------------------------------------------------------------------
                url = "https://graph.facebook.com/v19.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + faceBookToken,
                    'Content-Type': 'application/json'
                }
                if len(result) == 0:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "text",
                        "text": {
                            "body": "No Tickets are assigned to you"
                        }
                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                else:
                    # for ticket in result:
                    payload = json.dumps({
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": toUser,
                        "type": "text",
                        "text": {
                            "body": f"Number:{result['number']}\nDescription:{result['short_description']}\nUrgency:{result['urgency']}\nsys_created_by:{result['sys_created_by']}\nImpact:{result['impact']}\nopened_at:{result['opened_at']}\nactive:{result['active']}\n"
                                    f"sys_updated_by:{result['sys_updated_by']}\nsys_created_on:{result['sys_created_on']}\nAssigned to:{result['assigned_to']}"
                        },
                    })
           #---------Hotel Start------------------------------- 
            
            elif 'Catalog' in response_data and 'hotel' in response_data['flow_token']:
               
                CLIENT_id,MarketplaceID,idVALUE=response_data['Catalog'].split("_")
                hotelRoom,client_id,marketplace_id,hotel_settings_id,guest= response_data['flow_token'].split("_")
                global Room_listinstance, FoodServiceId, ClientID, MarketplaceId, HotelSettingsId, Guest
                ClientID, MarketplaceId, HotelSettingsId,Guest=client_id,marketplace_id,hotel_settings_id,guest
                Room_listinstance = get_object_or_404(Room_list,id=int(response_data["Room_number"]))
                FoodServiceId=response_data["service_id"]
                Catalog_obj=Food_catalogue.objects.get(client_id=CLIENT_id,marketplace_id=MarketplaceID,id=idVALUE)
                start_time_str=''
                end_time_str=''
                end_time_str = Catalog_obj.end_time.strftime("%I:%M%p") 
                start_time_str =Catalog_obj.start_time.strftime("%I:%M%p")
                Catalog_Timing=start_time_str+' to '+ end_time_str
                Url = f"https://graph.facebook.com/{Catalog_obj.catalogue_set_id}/products"

                Payload = {}
                Headers = {
                'Authorization': f'Bearer {faceBookToken}'
                }

                response = requests.request("GET", Url, headers=Headers, data=Payload)

                # print(response.text)
                response_json=response.json()
            
                data=response_json.get('data')
            
                product_items=[]
                for i in data:
                    product_items.append(
                        {
                            "product_retailer_id": str(i['retailer_id'])
                        },
                    )
                print("product",product_items)    
                payload=json.dumps({
                    
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": toUser,
                    "type": "interactive",
                    "interactive": {
                        "type": "product_list",
                        "header": {
                            "type": "text",
                            "text": Catalog_obj.catalogue_name
                        },
                        "body": {
                            "text": Catalog_obj.catalogue_discription
                        },
                        "footer": {
                            "text": Catalog_Timing
                        },
                        "action": {
                        
                            "catalog_id": "377416438299687",
                            
                            "sections": [
                                {
                                    "title":Catalog_obj.catalogue_name ,
                                    "product_items": product_items
                                },
                                
                            ]
                        }
                    }
                })
                
                response = requests.request("POST", url, headers=headers, data=payload) 
                print("response of catalog",response.text)  
                # Hotel_marketplace_obj= Hotel_marketplace_settings.objects.get(client_id=clientId,id=marketplace_id) 
                # payload = json.dumps({
                #                 "messaging_product": "whatsapp",
                #                 "to": toUser,
                #                 "recipient_type": "individual",
                #                 "type": "interactive",
                #                 "interactive": {
                #                     "type": "flow",
                #                     "body": {
                #                         "text": str(Hotel_marketplace_obj.marketplace_welcome_message_body)
                #                     },
                #                     "action": {
                #                         "name": "flow",
                #                         "parameters": {
                #                             "flow_message_version": "3",
                #                             "flow_action": "data_exchange",
                #                             "flow_token": f"hotel_{clientId}_{marketplace_id}",
                #                             "mode": "draft",
                #                             "flow_id": f"{Hotel_marketplace_obj.specific_flow_id}",

                #                             "flow_cta": f"{Hotel_marketplace_obj.specific_flow_cta_name}",
                #                         }
                #                     }
                #                 }

                #             })
                # response = requests.request("POST", url, headers=headers, data=payload)
                # print("hjdhdh")
                # print(response.text)
                # print(response.text)
            elif all(key in response_data for key in ['Service_Report', 'Service_Image', 'Service_name', 'Service_Timings','Service_About']):
                print("customer_Phonenumber",toUser,response_data['flow_token'])
                
                Hotel_services_instance = get_object_or_404(Hotel_services, id=int(response_data["id_value"]))
                global Room_listInstance
                Room_listInstance= get_object_or_404(Room_list,id=int(response_data["Room_number"]))
                hotel,client_id,marketplace_id,hotel_settings_id,guest=response_data['flow_token'].split('_')
                print("faf")
                Hotel_services_settings_obj=Hotel_services_settings.objects.get(id=response_data["service_id"])
                datetime_utc=datetime.now()
                print("datetime_utc",datetime_utc)
                india_timezone = pytz.timezone('Asia/Kolkata')
                datetime_india = india_timezone.localize(datetime_utc)
                datetime_str=datetime.strftime(datetime_india,'%Y-%m-%d %H:%M:%S')
                print(datetime_str)
                datetime_obj=datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S')
                print(datetime_obj)
                Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.get(client_id=client_id,Hotel_details_id=int(hotel_settings_id),Room_details=Room_listInstance,Guest_details_id=int(guest),Check_Out__gte=datetime_obj)
                
               
                
                Serivce_order_obj=Service_order.objects.create(
                    client_id=int(response_data["client_id"]),
                    marketplace_id=int(response_data["marketplace_id"]),
                    customer_room=Room_listInstance.room_number,
                    hotel_service=Hotel_services_instance,
                    service_comments=response_data['Service_Report'],
                    service_status="REQUESTED", 
                    customer_phone_num=toUser,
                )
                Serivce_order_obj.save()
               
                payload = json.dumps({
                    "messaging_product":"whatsapp",
                    "recipient_type":"individual",
                    "to":f"{Hotel_services_settings_obj.support_number}",
                    "type":"interactive",
                    "interactive": {
                                "type": "button",

                                "body": {
                                    "text": f"{Hotel_Room_Guest_info_obj.Guest_details.Guest_name}requested for {Hotel_services_instance.service_name}\nfor the room-{Hotel_Room_Guest_info_obj.Room_details.room_number}.Guest contact number : {Hotel_Room_Guest_info_obj.Guest_details.Phone_number}"
                                },

                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": f"ACKNOWLEDGED_{Hotel_Room_Guest_info_obj.id}_{Serivce_order_obj.id}_service",
                                                "title": "Acknowledged"
                                            }
                                        },
                                         {
                                            "type": "reply",
                                            "reply": {
                                                "id": f"COMPLETED_{Hotel_Room_Guest_info_obj.id}_{Serivce_order_obj.id}_service",
                                                "title": "Completed"
                                            }
                                        },

                                    ]
                                }
                            }
                        
                }) 
                response = requests.request("POST", url, headers=headers, data=payload)
                print("hjdhdh")
                print(response.text)
                Hotel_marketplace_settings_obj=Hotel_marketplace_settings.objects.get(client_id=response_data["client_id"],id=int(marketplace_id))
                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "text",
                                    "text": {
                                        "body": f"Order successfully placed"
                                    }
                                })
                response = requests.request("POST", url, headers=headers, data=payload)
                print("hjdhdh")
                print(response.text)
               
                payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "to": toUser,
                                "recipient_type": "individual",
                                "type": "interactive",
                                "interactive": {
                                    "type": "flow",
                                    "body": {
                                        "text": str(Hotel_marketplace_settings_obj.marketplace_welcome_message_body)
                                    },
                                    "action": {
                                        "name": "flow",
                                        "parameters": {
                                            "flow_message_version": "3",
                                            "flow_action": "data_exchange",
                                            "flow_token": f"hotel_{response_data['client_id']}_{response_data['marketplace_id']}_{hotel_settings_id}_{guest}",
                                            "mode": "draft",
                                            "flow_id": f"{Hotel_marketplace_settings_obj.specific_flow_id}",
                                            "flow_cta": f"{Hotel_marketplace_settings_obj.specific_flow_cta_name}",
                                        }
                                    }
                                }

                            })
                response = requests.request("POST", url, headers=headers, data=payload)
                print("hjdhdh")
                print(response.text)
                
                    
            elif all(key in response_data for key in ["Guest_Name","Guest_GovernmentId","Guest_Address","CheckIn","Checkout","Room_category","no_of_rooms"]):
                if 'Reception' in response_data['flow_token']:
                    print('reception','Exist')
#Reception_{client_id}_{Hotel_details.id}_{Guest_info_obj.id}_{checkin_milli}_{checkout_milli}_{no_of_rooms}_{Room_category}"
                    Room_booking_details=response_data['flow_token'].split("_")
                    print(response_data['Room_numbers'],Room_booking_details)
                    # Convert milliseconds to seconds
                    checkin_seconds = int(Room_booking_details[4])/ 1000
                    checkout_seconds = int(Room_booking_details[5]) / 1000
                    # Create a datetime object from the seconds
                    checkin_date_obj = datetime.utcfromtimestamp(checkin_seconds)
                    checkout_date_obj = datetime.utcfromtimestamp(checkout_seconds)
                    print(checkin_date_obj,checkout_date_obj)
                    # Format the datetime object as desired
                    checkin_formatted_date = checkin_date_obj.strftime('%Y-%m-%d')
                    checkout_formatted_date = checkout_date_obj.strftime('%Y-%m-%d')
                    print(checkin_formatted_date,checkout_formatted_date)  
                    try:
                        Room_numbers=''
                        Hotel_rooms_type_instance=get_object_or_404(Hotel_rooms_type,id=int(Room_booking_details[-1]))
                        Hotel_settings_instance=get_object_or_404(Hotel_settings,id=int(Room_booking_details[2]))
                        Guest_info_instance=get_object_or_404(Guest_info,id=int(int(Room_booking_details[3])))
                        number_of_rooms=len(response_data['Room_numbers'])
                        for i,j in enumerate(response_data['Room_numbers']):
                            Room_list_instance=get_object_or_404(Room_list,id=int(j)) 
                        
                            if i==len(response_data['Room_numbers'])-2:
                                Room_numbers+=Room_list_instance.room_number+' and '
                            elif i==len(response_data['Room_numbers'])-1:
                                Room_numbers+=Room_list_instance.room_number
                            else:
                                Room_numbers+=Room_list_instance.room_number+', '
                            

                            Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.create(
                                client_id=int(Room_booking_details[1]),
                                Room_details=Room_list_instance,
                                Hotel_details=Hotel_settings_instance,
                                Guest_details=Guest_info_instance,
                                Check_In=checkin_date_obj,
                                Check_Out=checkout_date_obj
                            )
                            Hotel_Room_Guest_info_obj.save()
                        payload=json.dumps({
                            "messaging_product":"whatsapp",
                            "recipient_type":"individual",
                            "to":Guest_info_instance.Phone_number,
                            "type":"text",
                            "text":{
                                "body":f"Hello *{Guest_info_instance.Guest_name}*. Your room booking is successful in *_{Hotel_settings_instance.hotel_name}_*.\n*Below you can find your Room(s) details :* \n"
                                       f"*Room(s) Category :* {Hotel_rooms_type_instance.l_room_type}.\n*Room(s) Type :* {Hotel_rooms_type_instance.room_type}.\n"
                                       f"*Number of Room (s) :* {number_of_rooms}.\n*Room Number(s) :* {Room_numbers}.\n"
                                       f"*Check In Date :* {checkin_formatted_date}\n*Check Out Date :* {checkout_formatted_date}."
                            }
                        })
                        response=requests.request('POST',url,headers=headers,data=payload)
                        print(response.text)
                    except KeyError as e:
                        print(f"{e}")

                elif 'Room' in response_data['flow_token']  or 'Exist' in response_data['flow_token']:
                    print("in Room",response_data['flow_token'])
                    Guest_details=response_data['flow_token'].split('_')
                    client_id=Guest_details[1]
                    if 'Exist' not in response_data['flow_token']:
                        Guest_info_obj=Guest_info()
                        Guest_info_obj.client_id=int(client_id)
                        Guest_info_obj.Guest_name=response_data["Guest_Name"]
                        Guest_info_obj.GovernmentId=response_data["Guest_GovernmentId"]
                        Guest_info_obj.Address=response_data["Guest_Address"]
                        Guest_info_obj.Phone_number=toUser
                        Guest_info_obj.save()
                        
                        
                    no_of_rooms=response_data["no_of_rooms"]
                    Room_category=int(response_data["Room_category"])
                
                
                    checkin_milli,checkout_milli = int(response_data["CheckIn"]),int(response_data["Checkout"])

                    

                    Hotel_details=''
                    Hotel_rooms_type_obj=''
                    marketplace_id=Guest_details[2] # marketplace_id may '' or any val;ue like 1,2,3 etc
                    if len(Guest_details)>=3 and Guest_details[2]!='':
                        marketplace_id=int(Guest_details[2])
                        Hotel_details=Hotel_settings.objects.get(client_id=int(client_id),marketplace_id=marketplace_id)
                        Hotel_rooms_type_obj=Hotel_rooms_type.objects.get(client_id=int(client_id),marketplace_id=int(Guest_details[2]),id=Room_category)
                    print("Hotel_details",Hotel_details)
                    if Guest_details[4]:
                        Guest_info_obj=Guest_info.objects.get(client_id=int(client_id),id=int(Guest_details[4]))
                    else:
                        Guest_info_obj=Guest_info.objects.filter(client_id=int(client_id)).last()
                    facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
                    faceBookToken = ''
                    # businessName = ''
                    clientId = 0
                    for tok in facebookObjects:
                        faceBookToken = faceBookToken + tok.fb_access_token
                        # businessName = businessName + tok.fb_name
                        clientId = clientId + tok.client_id
                    url = "https://graph.facebook.com/v19.0/" + str(whatsAppPhoneNumberId) + "/messages"
                    headers = {
                        'Authorization': 'Bearer ' + faceBookToken,
                        'Content-Type': 'application/json'
                    }
                    
                    payload = json.dumps({
                                        "messaging_product": "whatsapp",
                                        "to": f"{Hotel_details.Reception_number}",
                                        "recipient_type": "individual",
                                        "type": "interactive",
                                        "interactive": {
                                            "type": "flow",
                                            "body": {
                                                "text": f"Room Request form."
                                            },
                                            "action": {
                                                "name": "flow",
                                                "parameters": {
                                                    "flow_message_version": "3",
                                                    "flow_action": "data_exchange",
                                                    "flow_token": f"Reception_{client_id}_{Hotel_details.id}_{Guest_info_obj.id}_{checkin_milli}_{checkout_milli}_{no_of_rooms}_{Room_category}",
                                                    "mode": "draft",#Reception_22_1_12_1708663336582_1708749741181_2_2
                                                    "flow_id": "1569901800509346",

                                                    "flow_cta": "Room Booking Form",
                                                    
                                                }
                                            }
                                        }

                                    })
                    response = requests.request("POST", url, headers=headers, data=payload)
                    print("hjdhdh")
                    print(response.text)
            elif all (key in response_data for key in ['Feedback_comment',"all_question_id","all_feedbacks","Checkout_response_header_id"]):
                Checkout_response_header_obj=Checkout_response_header.objects.get(id=response_data['Checkout_response_header_id'])
                Checkout_response_header_obj.Comment=response_data['Feedback_comment']
                Checkout_response_header_obj.save()
            elif all (key in response_data for key in ['ComplaintCategory','Comment','client_id','marketplace_id','id_value','Rooms']):
                hotel,client_id,marketplace_id,hotel_settings_id,guest=response_data['flow_token'].split('_')
                Complaint_info_obj=Complaint_info()
                Complaint_info_obj.client_id=int(client_id)
                Complaint_info_obj.Hotel_details_id=int(hotel_settings_id)
                Complaint_info_obj.Room_details_id=int(response_data['Rooms'])
                Complaint_info_obj.Guest_details_id=int(guest)
                Complaint_info_obj.Complaint_category_id=int(response_data['ComplaintCategory'])
                Complaint_info_obj.Complaint_comments=response_data['Comment']
                Complaint_info_obj.Complaint_status='REQUESTED'
                Complaint_info_obj.save()
                datetime_utc=datetime.now()
                print("datetime_utc",datetime_utc)
                india_timezone = pytz.timezone('Asia/Kolkata')
                datetime_india = india_timezone.localize(datetime_utc)
                datetime_str=datetime.strftime(datetime_india,'%Y-%m-%d %H:%M:%S')
                print(datetime_str)
                datetime_obj=datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S')
                print(datetime_obj) 
                Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.get(client_id=int(client_id),Hotel_details_id=int(hotel_settings_id),Room_details_id=int(response_data['Rooms']),Guest_details_id=int(guest),Check_Out__gte=datetime_obj)
                Hotel_services_settings_obj=Hotel_services_settings.objects.get(id=response_data["id_value"])
                payload = json.dumps({
                    "messaging_product":"whatsapp",
                    "recipient_type":"individual",
                    "to":f"{Hotel_services_settings_obj.support_number}",
                    "type":"interactive",
                    "interactive": {
                                "type": "button",

                                "body": {
                                    "text": f"{Hotel_Room_Guest_info_obj.Guest_details.Guest_name} has raised a complaint.\nComplaint category: {Complaint_info_obj.Complaint_category.Complaint_category}\nComment:{response_data['Comment']}\nRoom Number : {Hotel_Room_Guest_info_obj.Room_details.room_number}\nGuest contact number : {Hotel_Room_Guest_info_obj.Guest_details.Phone_number}"
                                },

                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": f"ACKNOWLEDGED_{Hotel_Room_Guest_info_obj.id}_{Complaint_info_obj.id}_complaint",
                                                "title": "Acknowledged"
                                            }
                                        },
                                         {
                                            "type": "reply",
                                            "reply": {
                                                "id": f"COMPLETED_{Hotel_Room_Guest_info_obj.id}_{Complaint_info_obj.id}_complaint",
                                                "title": "Completed"
                                            }
                                        },

                                    ]
                                }
                            }
                        
                }) 
                response = requests.request("POST", url, headers=headers, data=payload)
                print("hjdhdh")
                print(response.text)
                Hotel_marketplace_settings_obj=Hotel_marketplace_settings.objects.get(client_id=response_data["client_id"],id=int(marketplace_id))
                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "text",
                                    "text": {
                                        "body": f"Complaint raised successfully"
                                    }
                                })
                response = requests.request("POST", url, headers=headers, data=payload)
                print("hjdhdh")
                print(response.text)
               
                payload = json.dumps({
                                "messaging_product": "whatsapp",
                                "to": toUser,
                                "recipient_type": "individual",
                                "type": "interactive",
                                "interactive": {
                                    "type": "flow",
                                    "body": {
                                        "text": str(Hotel_marketplace_settings_obj.marketplace_welcome_message_body)
                                    },
                                    "action": {
                                        "name": "flow",
                                        "parameters": {
                                            "flow_message_version": "3",
                                            "flow_action": "data_exchange",
                                            "flow_token": f"hotel_{response_data['client_id']}_{response_data['marketplace_id']}_{hotel_settings_id}_{guest}",
                                            "mode": "draft",
                                            "flow_id": f"{Hotel_marketplace_settings_obj.specific_flow_id}",
                                            "flow_cta": f"{Hotel_marketplace_settings_obj.specific_flow_cta_name}",
                                        }
                                    }
                                }

                            })
                response = requests.request("POST", url, headers=headers, data=payload)
                print("hjdhdh")
                print(response.text)

                


            #elif all(key in response_data for key in ['Feedback_comment','all_question_id','all_feedbacks']):

        # else:
            #     print("s it is coming to survey flow")
            #     poll_answer = response_data.get('radiobuttonsgroup')
            #     position = poll_answer.find("R")
            #     servey_question_id = poll_answer[:position]
            #     print(servey_question_id)
            #     poll_response_id = poll_answer[position:]
            #     print(poll_response_id)
            #     question_info = Survey_Question.objects.filter(id=servey_question_id)
            #     response_value = ''
            #     survey_id = 0
            #     for q_i in question_info:
            #         survey_id = q_i.Survey_list_id
            #         if poll_response_id == "R1":
            #             response_value = q_i.response_option1
            #         elif poll_response_id == "R2":
            #             response_value = q_i.response_option2
            #         elif poll_response_id == "R3":
            #             response_value = q_i.response_option3
            #         elif poll_response_id == "R4":
            #             response_value = q_i.response_option4
            #     print(response_value)
            #     print(survey_id)
            #     facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
            #     faceBookToken = ''
            #     # businessName = ''
            #     clientId = 0
            #     for tok in facebookObjects:
            #         faceBookToken = faceBookToken + tok.fb_access_token
            #         # businessName = businessName + tok.fb_name
            #         clientId = clientId + tok.client_id
            #     print(clientId)
            #     customer_info = Survey_Customer.objects.filter(customer_whatsapp_number=toUser)
            #     customer_id = 0
            #     for c_i in customer_info:
            #         customer_id = c_i.id
            #     print(customer_id)
            #     print("s printed all the ids please check once")
            #     survey_customer_response = Survey_Customer_Response(
            #         client_id=clientId,
            #         Survey_list_id=survey_id,
            #         Survey_Question_id=servey_question_id,
            #         Survey_Customer_id=customer_id,
            #         Survey_Response=response_value

            #     )
            #     survey_customer_response.save()
            #     print("succcesfully saved all the data")
            #     url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
            #     headers = {
            #         'Authorization': 'Bearer ' + faceBookToken,
            #         'Content-Type': 'application/json'
            #     }
            #     payload = json.dumps({
            #         "messaging_product": "whatsapp",
            #         "recipient_type": "individual",
            #         "to": toUser,
            #         "type": "text",
            #         "text": {
            #             "body": "Thank you for Voting"
            #         }
            #     })

            #     response = requests.request("POST", url, headers=headers, data=payload)















    except KeyError as e:
        print(f"KeyError occurred: {e}")
        
        
    if 'entry'in received_message:
        
        toUser=received_message['entry'][0]['changes'][0]['value']['messages'][0]['from']
        whatsAppPhoneNumberId = received_message['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
        bussiness_ph_number = received_message['entry'][0]['changes'][0]['value']['metadata']['display_phone_number']
        facebook_details_instance=facebook_details.objects.get(fb_phone_number_id=whatsAppPhoneNumberId,fb_whatsapp_number=bussiness_ph_number)
        url = "https://graph.facebook.com/v17.0/" + str(whatsAppPhoneNumberId) + "/messages"
        headers = {
            'Authorization': 'Bearer ' + facebook_details_instance.fb_access_token,
            'Content-Type': 'application/json'
        }        
        try:
            if 'order' in received_message['entry'][0]['changes'][0]['value']['messages'][0]:
                items=received_message['entry'][0]['changes'][0]['value']['messages'][0]['order']['product_items']
                food_item_name=''
                total_amount=0
                
                # client_id=0
                # marketplace_id=0
                # order_details=0
                
                food_order=''
                #ClientID, MarketplaceId, HotelSettingsId,Guest
                # client_id=facebook_details_instance.client_id
                print("Room_listinstance",Room_listinstance)
                Food_order_header_obj=Food_order_header()
                Food_order_header_obj.customer_phone_num=toUser
                Food_order_header_obj.order_delivery_room= Room_listinstance.room_number
                for item in items:
                    print(item,"item")
                    # order_details=item['product_retailer_id'].split('_')
                    # client_id=order_details[-2]
                    # marketplace_id=order_details[-1]
                    total_amount+=(item['quantity']*item['item_price'])
                # print("marketplace_id",marketplace_id)
                # print("client_id",client_id)
                Food_order_header_obj.order_amount=total_amount
                Food_order_header_obj.order_status='ORDERED'
                Food_order_header_obj.client_id=int(ClientID)
                Food_order_header_obj.marketplace_id=int(MarketplaceId)
                Food_order_header_obj.save()
                
                
                Food_order_obj=Food_order_header.objects.filter(client_id=ClientID,marketplace_id=MarketplaceId).last()                        
                for item in items:
                    Food_order_details_obj=Food_order_details()                       
                    Food_order_details_obj.client_id=int(ClientID)
                    Food_order_details_obj.marketplace_id=int(MarketplaceId)
                    Food_order_details_obj.Food_order_header=Food_order_obj
                    Food_order_details_obj.Food_quantity=item['quantity']
                    Food_order_details_obj.Food_Item_Price=item['item_price']
                    order_details=item['product_retailer_id'].split('_')
                    if len(order_details[:-2]) >1:
                        Food_name='_'.join(order_details[:-2])
                        print("Food_name",Food_name)
                    else:
                        Food_name=''.join(order_details[:-2])
                        print('Food_name',Food_name)
                    food_order+=f"{item['quantity']}   {Food_name}\n"

                    Food_obj=Food.objects.get(client_id=int(ClientID),marketplace_id=int(MarketplaceId),food_name=Food_name,food_price=item['item_price'])
                    Food_order_details_obj.Food_Item= Food_obj
                    Food_order_details_obj.save()
                    # Hotel_services_instance=Hotel_services_settings.objects.get(id=int(FoodServiceId))
                    Hotel_marketplace_settings_obj=Hotel_marketplace_settings.objects.get(client_id=int(ClientID),id=int(MarketplaceId))
                    Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.get(client_id=int(ClientID),Hotel_details_id=int(HotelSettingsId),Room_details=Room_listinstance,Guest_details_id=int(Guest))
                    Hotel_services_settings_obj=Hotel_services_settings.objects.get(id=int(FoodServiceId))
                    payload = json.dumps({
                    "messaging_product":"whatsapp",
                    "recipient_type":"individual",
                    "to":f"{Hotel_services_settings_obj.support_number}",
                    "type":"interactive",
                    "interactive": {
                                "type": "button",

                                "body": {
                                    "text": f"{Hotel_Room_Guest_info_obj.Guest_details.Guest_name} ordered for\n{food_order}Room Number : {Hotel_Room_Guest_info_obj.Room_details.room_number}\nGuest contact number : {Hotel_Room_Guest_info_obj.Guest_details.Phone_number}"
                                },

                                "action": {
                                    "buttons": [
                                        {
                                            "type": "reply",
                                            "reply": {
                                                "id": f"ACCEPTED_{Hotel_Room_Guest_info_obj.id}_{Food_order_obj.id}_food",
                                                "title": "Accepted"
                                            }
                                        },
                                         {
                                            "type": "reply",
                                            "reply": {
                                                "id": f"DELIVERED_{Hotel_Room_Guest_info_obj.id}_{Food_order_obj.id}_food",
                                                "title": "Delivered"
                                            }
                                        },

                                    ]
                                }
                            }
                        
                }) 
                response = requests.request("POST", url, headers=headers, data=payload)
                print("hjdhdh")
                print(response.text)
                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "text",
                                    "text": {
                                        "body": f"Order successfully placed"
                                    }
                                })
                response = requests.request("POST", url, headers=headers, data=payload)
                print("hjdhdh")
                print(response.text) 
                # ClientID, MarketplaceId, HotelSettingsId,Guest  
                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "to": toUser,
                                    "recipient_type": "individual",
                                    "type": "interactive",
                                    "interactive": {
                                        "type": "flow",
                                        "body": {
                                            "text": str(Hotel_marketplace_settings_obj.marketplace_welcome_message_body)
                                        },
                                        "action": {
                                            "name": "flow",
                                            "parameters": {
                                                "flow_message_version": "3",
                                                "flow_action": "data_exchange",
                                                "flow_token": f"hotel_{ClientID}_{MarketplaceId}_{HotelSettingsId}_{Guest}",
                                                "mode": "draft",
                                                "flow_id": f"{Hotel_marketplace_settings_obj.specific_flow_id}",
                                                "flow_cta": f"{Hotel_marketplace_settings_obj.specific_flow_cta_name}",
                                            }
                                        }
                                    }

                                })
                response = requests.request("POST", url, headers=headers, data=payload)
                print("hjdhdh")
                print(response.text)           


                        # Food_order_header_obj.client_id=int(order_details[-2])
                        # Food_order_header_obj.marketplace_id=int(order_details[-1])
                       
                        # if len(order_details[:-2])>1:
                        #     food_item_name='_'.join(order_details[:-2])
                        # else:
                        #     food_item_name=order_details[0]
                        
        except Exception as e:
            print("error",e)
            if str(e)=="name 'Room_listinstance' is not defined":
                url = "https://graph.facebook.com/v17.0/" + str(whatsAppPhoneNumberId) + "/messages"
                headers = {
                    'Authorization': 'Bearer ' + facebook_details_instance.fb_access_token,
                    'Content-Type': 'application/json'
                }
                payload = json.dumps({
                                    "messaging_product": "whatsapp",
                                    "recipient_type": "individual",
                                    "to": toUser,
                                    "type": "text",
                                    "text": {
                                        "body": f"You Cannot order food from hear, can order food by clicking on below link\nhttps://wa.me/{bussiness_ph_number}?text=hotel_id=1"
                                    }
                                })
                response = requests.request("POST", url, headers=headers, data=payload)
                print("hjdhdh")
                print(response.text)   

    first_key_from_meesage, first_value_from_message = next(iter(received_message.items()))
    print("key,value",first_key_from_meesage, first_value_from_message)
    first_key_from_meesage, first_value_from_message = next(iter(received_message.items()))
    print(first_key_from_meesage, first_value_from_message)

    if first_key_from_meesage == "object" and first_value_from_message == "whatsapp_business_account":
        print("if condition satisfied", first_key_from_meesage)

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
                    response_id = res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['button_reply'][
                        'id']
                elif button_type == 'list_reply':
                    response_id = res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['list_reply'][
                        'id']
                    list_title = res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['list_reply'][
                        'title']
            if messageType =='button':
                response_id=res['entry'][0]['changes'][0]['value']['messages'][0]['button']['payload']


            facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
            faceBookToken = ''
            faceBookId = ''
            whatsapPhoneNumber=0
            # businessName = ''
            clientId = 0
            for tok in facebookObjects:
                faceBookToken = faceBookToken + tok.fb_access_token
                faceBookId = tok.id
                # businessName = businessName + tok.fb_name
                clientId = clientId + tok.client_id
                whatsapPhoneNumber=tok.fb_whatsapp_number

            # ____________________________________API URL and HEADERS__________________________________

            url = "https://graph.facebook.com/v17.0/" + str(whatsAppPhoneNumberId) + "/messages"
            headers = {
                'Authorization': 'Bearer ' + faceBookToken,
                'Content-Type': 'application/json'
            }

            # __________________________________________________________________________________________

            adminPermissionObjects = admin_permission.objects.filter(client_id=clientId)

            for clientIdI in adminPermissionObjects:
                if clientIdI.client_service_type == 'commerce':
                    if clientIdI.client_permission_status == True:
                        process_health_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                                   clientId, whatsAppPhoneNumberId, faceBookToken)



                elif clientIdI.client_service_type == 'ticket':
                    print(clientIdI)
                    if clientIdI.client_permission_status == True:
                        process_ticket_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                                   clientId, whatsAppPhoneNumberId, faceBookToken)
                    else:
                        print("waiting for admin approval")
                elif clientIdI.client_service_type == 'donation':
                    if clientIdI.client_permission_status == True:
                        process_donation_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                                     clientId, whatsAppPhoneNumberId, faceBookToken)


                elif clientIdI.client_service_type == 'appointement' or clientIdI.client_service_type== 'Appointement':
                    print("servicenow")
                    print("clientID",clientIdI)
                    project = 'servicenow'  # Appointment or sports or servicenow
                    if project == 'servicenow':
                        print("project: ",project)
                        process_appointement_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                                     clientId, whatsAppPhoneNumberId, faceBookToken, list_title,
                                                     faceBookId, project)
                    elif project =='democommerce':
                        process_new_commerce_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                                     clientId, whatsAppPhoneNumberId, faceBookToken, list_title,
                                                     faceBookId, project)
                elif clientIdI.client_service_type == 'hotel' or clientIdI.client_service_type== 'HOTEL' or clientIdI.client_service_type== 'HotelManagement':
                    print("before calling hotel_bot",clientIdI.client_service_type)
                    process_hotel_bot_message(message, response_id, messageType, request, url, headers, toUser,
                                                     clientId, whatsAppPhoneNumberId, faceBookToken, list_title,
                                                     faceBookId,whatsapPhoneNumber)





    elif first_key_from_meesage == "account_id":
        print("elif condition satisfied", first_key_from_meesage)

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
                                "reference_id": dy_i.donation_reference_id,
                                "ngo_logo": org_i.ngo_logo,
                                "ngo_name": org_i.ngo_name,
                                "ngo_pan": org_i.ngo_pan,
                                "ngo_gstin": org_i.ngo_gstin,
                                "ngo_header_notes": org_i.ngo_header_notes,
                                "ngo_footer_notes": org_i.ngo_footer_notes,
                                "ngo_signatureHeader": org_i.ngo_signature_header,
                                "ngo_signatureImage": org_i.ngo_signature_image,
                                "ngo_Footer": org_i.ngo_signature_footer,
                                "invoiceFooter": org_i.invoice_footer

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











    elif first_key_from_meesage == "entity":

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

    elif first_key_from_meesage == 'encrypted_flow_data':
        print("data_exchange")









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
            phone_number = "91" + uphone.strip()
            tick_info = ticket_information.objects.filter(id=ticket_id, payment_reference_id=reference_characters)
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
            donationName = ''
            donationshortdesc = ''
            donationdesc = ''
            donationImage = ''
            donation_detailsobj = donation_types.objects.filter(client_id=dclientID, id=responseId)
            print(donation_detailsobj)
            for dj_i in donation_detailsobj:
                donationName = donationName + dj_i.donation_name
                donationshortdesc = donationshortdesc + dj_i.donation_short_description
                donationdesc = donationdesc + dj_i.donation_description
                donationImage = dj_i.donation_type_image
            print(donationName)

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


# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import json
# import os
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes

# from cryptography.hazmat.primitives.serialization import load_pem_private_key
from django.http import HttpResponse, JsonResponse
# from django.http import JsonResponse
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.backends import default_backend
from django.views.decorators.csrf import csrf_exempt


# Generate RSA keys for asymmetric encryption
def hotel_genericflow(request):
    Hotel_marketplace_obj= Hotel_marketplace_settings.objects.filter(client_id=request.user.id)
    facebook_token=''
    facebook_object=facebook_details.objects.filter(client_id=request.user.id)
    for items in facebook_object:
        facebook_token=items.fb_access_token
        waid=items.fb_Whatsapp_business_account_id
    for i in Hotel_marketplace_obj:
        file_path = "C:/Vailo/04-01-2023/A_vMart/A_vMart/number.txt"

        try:
            # Try to open the file in read mode to check if it exists
            with open(file_path, 'r') as file:
                # Read the current value from the file
                current_value = int(file.read().strip())

        except FileNotFoundError:
            # If the file doesn't exist, set the initial value
            current_value = 0

        # Increment the current value
        current_value += 1

        # Write the updated value back to the file
        with open(file_path, 'w') as file:
            file.write(str(current_value))

        print(f"The value in the file '{file_path}' has been updated to {current_value}.")
       
        base_name = 'generic_flow'
        new_name = f'{base_name}{current_value}'
        url = f"https://graph.facebook.com/v18.0/{waid}/flows"

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
            for h_i in Hotel_marketplace_obj:
                h_i.generic_flow_id = id_value
                h_i.save()
        data={
        "version": "2.1",
        "data_api_version":"3.0",
        "data_channel_uri":  "https://vmart.ai/hotel_de/",
        "routing_model":{

        },

        "screens": [
            {
                "id": "WELCOME_SCREEN",
                "title": "Welcome",
                "terminal": True,
                "data": {},
                "layout": {
                    "type": "SingleColumnLayout",
                    "children": [
                        {
                            "type":"Form",
                            "name": "flow_path",
                            "children":[
                                {
                                    "type":"RadioButtonsGroup",
                                    "name":"menu",
                                    "label":"Select from the Menu",
                                    "data-source":[
                                        {
                                            "id":"Order_Food",
                                            "title": "Order Food"
                                        },
                                            {
                                            "id":"Explore_Nearby",
                                            "title": "Explore Nearby"
                                        },
                                            {
                                            "id":"Hotel_Facilities",
                                            "title": "Hotel Facilities"
                                        },
                                            {
                                            "id":"Self_Help",
                                            "title": "Self Help"
                                        },
                                        {
                                            "id":"More_Information",
                                            "title": "More Information"
                                        },
                                        {
                                            "id":"Self_help",
                                            "title": "Self help"
                                        },
                                        {
                                            "id":"Information",
                                            "title": "Information"
                                        }
                                    ],
                                    "required":True
                                }
                            ]
                        },
                        {
                            "type": "Footer",
                            "label": "Submit",
                            "on-click-action": {
                                "name": "data_exchange",
                                "payload": {
                                        "Hotel_Menu":"${form.menu}"
                                }
                            }
                        }
                    ]
                }
                
            }
        ]
        }
        file_name = f'Hotelflow.json.json'
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=2)
        print("succesfully generated the json file..")

        url = f" https://graph.facebook.com/v18.0/{id_value}/assets"

        payload = {'name': 'flow.json',
                'asset_type': 'FLOW_JSON'}
        file_path = f'C:/Vailo/04-01-2023/A_vMart/A_vMart/Hotelflow.json'
        files = [
        ('file',
            ('file', open(file_path, 'rb'), 'application/json'))
        ]
        headers = {
        'Authorization': f'Bearer {facebook_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
      

        print(response.text)
        print("s successfully updated json asset")

       


@csrf_exempt
def hotel_de(request):
    print("request",request.user.id)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']
        print("encrypted_flow_data_b64", encrypted_flow_data_b64, "length: ", len(encrypted_flow_data_b64))
        print("encrypted_aes_key_b64", encrypted_aes_key_b64, "length: ", len(encrypted_aes_key_b64))
        print("initial_vector_b64", initial_vector_b64, "length: ", len(initial_vector_b64))

        decrypted_data, aes_key, iv = decrypt_request(encrypted_flow_data_b64, encrypted_aes_key_b64,
                                                      initial_vector_b64)
        print("decrypted_data,aes_key,iv", decrypted_data, aes_key, iv)

        # --------------------------------------------------------------------
        if decrypted_data['action'] == 'ping':
            response = {

                "version": "3.0",
                "data": {
                    "status": "active"
                }

            }
            return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')

        # -----------------------------------------------------------------

        # Return the next screen & data to the client
        elif decrypted_data['action'] == 'INIT':
            response={}
            print(decrypted_data['flow_token'])
           
            if 'Room' in decrypted_data['flow_token']:
                
                Room,client_id,marketplace_id,hotel_settings_id,guest,room_type_id=decrypted_data['flow_token'].split('_')
                print("guest",guest,Room)
                
                Hotel_name_list=[]
                Hotel_rooms_category=[]
                room_type_list=[]
                if marketplace_id:
                    Hotel_rooms_category=Hotel_rooms_type.objects.filter(client_id=int(client_id),marketplace_id=int(marketplace_id),room_availability__iexact='yes',id=room_type_id)
                    Hotel_name_list=Hotel_settings.objects.get(client=int(client_id),marketplace_id=int(marketplace_id))
                else:
                    Hotel_rooms_category=Hotel_rooms_type.objects.filter(client_id=int(client_id),marketplace_id=marketplace_id,room_availability__iexact='yes',id=room_type_id)
                    Hotel_name_list=Hotel_settings.objects.get(client=int(client_id),marketplace_id=marketplace_id)

                
                print("Hotel_rooms_category",Hotel_rooms_category)
                for i in Hotel_rooms_category:
                    room_type_list.append(
                        {
                            "id":f"{i.id}",
                            "title":f"{i.l_room_type}",
                            "description":f"{i.room_type}-{i.bed}",
                            "metadata":f"{i.room_price} {i.room_price_unit}"
                        }
                    )
                print(room_type_list[0]["id"],room_type_list)

                Hotel_room_list=Room_list.objects.filter(client=int(client_id),marketplace_id=int(marketplace_id),hotel_room_type=Hotel_rooms_category[0].id)
                print("Hotel_room_list",Hotel_room_list)
                no_of_rooms=[]
                if Hotel_room_list:
                    for i in range(1,len(Hotel_room_list)+1):
                        no_of_rooms.append({"id":f"{i}","title":f"{i}"}) 
                else:
                    no_of_rooms.append({"id":str(0),"title":str(0)})
                
                check_in_date_string = str(date.today())
                check_in_date_obj = datetime.strptime(check_in_date_string, '%Y-%m-%d')

                # Get the time value of the datetime object in milliseconds
                check_in_date_milliseconds =int(check_in_date_obj.timestamp() * 1000)
                checkout_date_string = str(date.today()+timedelta(days=1))
                checkout_date_date_obj = datetime.strptime(checkout_date_string, '%Y-%m-%d')

                # Get the time value of the datetime object in milliseconds
                checkout_date_milliseconds = int(checkout_date_date_obj.timestamp() * 1000)
                print(check_in_date_milliseconds,checkout_date_milliseconds) 
                
                if 'Exist' in decrypted_data['flow_token']:
                    Guest_info_obj=Guest_info.objects.get(client_id=int(client_id),id=int(guest))
                    print("Guest_info_obj",Guest_info_obj)
                    response={
                    "version":"3.0",
                    "screen":"Hotel_room_form",
                    "data":{
                        
                        "no_of_rooms":no_of_rooms,
                        "no_of_rooms_init":no_of_rooms[0]['id'],
                        "checkin_mindate":str(check_in_date_milliseconds),
                        "checkout_mindate":str(checkout_date_milliseconds),
                        "room":room_type_list,
                        "room_init":room_type_list[0]["id"],
                        "hotel_name":Hotel_name_list.hotel_name,
                        "visible":False,
                        "required_1":False,
                        "required_2":True,
                    
                        "enabled":False,
                        "enabled_1":True,
                        "required_r_no":False,
                        "name":Guest_info_obj.Guest_name,
                        "GovernmentId":Guest_info_obj.GovernmentId,
                        "Phone_number_init":Guest_info_obj.Phone_number,
                        "Address":Guest_info_obj.Address,
                        "minrooms":0,
                        "Room_numbers":[
                            {
                            "id":"-",
                            "title":" "
                        }
                        ]
                    }
                }
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                else:    
                    response={
                            "version":"3.0",
                            "screen":"Hotel_room_form",
                            "data":{
                                
                                "no_of_rooms":no_of_rooms,
                                "no_of_rooms_init":no_of_rooms[0]['id'],
                                "checkin_mindate":str(check_in_date_milliseconds),
                                "checkout_mindate":str(checkout_date_milliseconds),
                                "room":room_type_list,
                                "room_init":room_type_list[0]["id"],
                                "hotel_name":Hotel_name_list.hotel_name,
                                "visible":False,
                                "required_1":True,
                                "required_2":True,
                                "enabled":True,
                                "enabled_1":True,
                                "required_r_no":False,
                                "name":"",
                                "GovernmentId":"",
                                "Phone_number_init":"",
                                "Address":"",
                                "minrooms":0,
                                "Room_numbers":[
                                    {
                                    "id":"-",
                                    "title":" "
                                }
                                ]
                            }
                    }
               
            
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
            elif 'Reception' in decrypted_data['flow_token']:
                Reception,client_id,hotel_id,guest_id,checkin,checkout,Guest_req_no_rooms,Room_category=decrypted_data['flow_token'].split("_")
                Guest_details=Guest_info.objects.get(client_id=int(client_id),id=int(guest_id))
                Hotel_rooms_type_obj=Hotel_rooms_type.objects.get(client_id=client_id,id=int(Room_category))
                Room_list_obj=Room_list.objects.filter(client_id=int(client_id),hotel_room_type=Hotel_rooms_type_obj)
                Hotel_settings_obj=Hotel_settings.objects.get(client_id=int(client_id),id=int(hotel_id))
                no_of_rooms=[]
                Room_numbers=[]
                print("Guest_details.Phone_number",Guest_details.Phone_number)
                for i in range(1,int(Guest_req_no_rooms)+1):
                    no_of_rooms.append(
                        {
                            "id":f"{i}",
                            "title":f"{i}"
                        }
                    )
                for i in Room_list_obj:
                    Room_numbers.append(
                          {
                            "id":f"{i.id}",
                            "title":f"{i.room_number}"
                          }
                    )
                response={
                    "version":"3.0",
                    "screen":"Hotel_room_form",
                    "data":{
                        
                        "no_of_rooms":no_of_rooms,
                        "no_of_rooms_init":Guest_req_no_rooms,
                        "checkin_mindate":checkin,
                        "checkout_mindate":checkout,
                        "room":[
                            {
                                "id":str(Hotel_rooms_type_obj.id),
                                "title":f"{Hotel_rooms_type_obj.l_room_type}-{Hotel_rooms_type_obj.room_type}-{Hotel_rooms_type_obj.bed}",
                                "description":f"{Hotel_rooms_type_obj.room_type}-{Hotel_rooms_type_obj.bed}",
                                "metadata":f"{Hotel_rooms_type_obj.room_price} {Hotel_rooms_type_obj.room_price_unit}"
                            }
                        ],
                        "room_init":str(Hotel_rooms_type_obj.id),
                        "hotel_name":Hotel_settings_obj.hotel_name,
                        "visible": True,
                        "required_1":False,
                        "required_2":False,
                        "enabled":False,
                        "required_r_no":True,
                        "enabled_1":False,
                        "name":Guest_details.Guest_name,
                        "GovernmentId":Guest_details.GovernmentId,
                        "Address":Guest_details.Address,
                         "Phone_number_init":Guest_details.Phone_number,
                        "Room_numbers":Room_numbers,
                        "minrooms":int(Guest_req_no_rooms),
                        
                    }
                }

                 
                return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
            elif 'hotel' in decrypted_data['flow_token']:
                hotel,client_id,marketplace_id,hotel_settings_id,guest=decrypted_data['flow_token'].split('_')
                HotelServiceSettings_obj=Hotel_services_settings.objects.filter(client_id=int(client_id),marketplace_id=int(marketplace_id),control='Enable')
                welcome_data=[]
                service_name=''
                for Hs_i in HotelServiceSettings_obj:
                    if Hs_i.key == 'FOOD' or Hs_i.key == 'food':
                        service_name='OrderFood'
                    elif Hs_i.key == 'NEARBY' or Hs_i.key == 'nearby place':
                        service_name='ExploreNearby'
                    elif Hs_i.key == 'SELP HELP' or Hs_i.key == 'self help':
                        service_name='selfHelp'
                    
                    elif Hs_i.key == 'FACILITIES' or Hs_i.key == 'hotel facilities':
                        service_name='HotelFacilities'
                    elif Hs_i.key == 'SERVICES' or Hs_i.key == 'hotel services':
                        service_name='Hotelservices'
                    elif Hs_i.key == 'INFORMATION' or Hs_i.key == 'Information':
                        service_name='Moreinformation'
                    elif Hs_i.key == 'COMPLAINTS' or Hs_i.key == 'Complaints':
                        service_name='Complaints'
                    if service_name:
                        welcome_data.append({
                            "id":f"{service_name}_{Hs_i.client_id}_{Hs_i.marketplace_id}_{Hs_i.id}_{guest}",
                            "title":f"{Hs_i.name}",
                            "description":f"{Hs_i.description}"
                        })
                        service_name=''
                print("welcome_data",welcome_data)
                encoded_image=''
                Hotel_settings_obj= Hotel_settings.objects.get(client_id=int(client_id),marketplace_id=int(marketplace_id))
                with Hotel_settings_obj.hotel_image.open(mode='rb') as image_file:
                        image_content= image_file.read()
                        encoded_image =base64.b64encode(image_content).decode('utf-8')
                response = {
                        "version": "3.0",
                        "screen": "WELCOMESCREEN",
                        "data": {
                            "welcomeImage":encoded_image,
                            "welcome_data":welcome_data,
                        }
                         
                    }
                return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
            elif 'Checkout' in decrypted_data['flow_token']:
                checkout,client_id,marketplace_id,hotel_settings_id,guest=decrypted_data['flow_token'].split('_')
                datetime_utc=datetime.now()
                print("datetime_utc",datetime_utc)
                india_timezone = pytz.timezone('Asia/Kolkata')
                datetime_india = india_timezone.localize(datetime_utc)
                datetime_str=datetime.strftime(datetime_india,'%Y-%m-%d %H:%M:%S')
                print(datetime_str)
                datetime_obj=datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S')
                print(datetime_obj)

                Guest_info_obj=Guest_info.objects.get(client_id=int(client_id),id=int(guest))
                Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.filter(client_id=int(client_id),Hotel_details_id=int(hotel_settings_id),Guest_details=Guest_info_obj,Check_Out__gt=datetime_obj)
                print("Hotel_Room_Guest_info_obj",Hotel_Room_Guest_info_obj)
                hotel_marketplace_obj=Hotel_marketplace.objects.get(client_id=int(client_id),id=int(marketplace_id))
                room_numbers=[]
                for i in Hotel_Room_Guest_info_obj:
                    checkin_date=(i.Check_In).date()
                    print("checkin_date",checkin_date)
                    checkin_time=datetime.strftime(i.Check_In,'%H:%M%p')
                    print("checkin_time",checkin_time)
                    room_obj=(i.Room_details)
                    print("room_obj",room_obj,room_obj.id)
                    id_value=room_obj.id
                    print("id_value",id_value)
                    room_numbers.append(
                        {
                        "id":str(id_value),
                        "title":i.Room_details.room_number,
                        "description":f"{checkin_date} - {checkin_time}"
                        }
                    )
                response={
                    "version":"3.0",
                    "screen":"Checkout_room",
                    "data":{
                        "room_numbers":room_numbers,
                        "guest_id":Guest_info_obj.id,
                        "phonenumber":Guest_info_obj.Phone_number,
                        "name":Guest_info_obj.Guest_name,
                        "address":Guest_info_obj.Address,
                        "governmentid":Guest_info_obj.GovernmentId,
                        "hotel_name":hotel_marketplace_obj.hotel_name
                        
                    }
                }
                
                return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
        elif decrypted_data['action'] == 'data_exchange':
            print("data_exchange")
            # print("data", decrypted_data['data'])
            print("flow_token",decrypted_data['flow_token'])           
            Room_hotel,client_id,marketplace_id,hotel_settings_id,guest=decrypted_data['flow_token'].split('_')
            
            if 'Hotel_Menu' in decrypted_data['data']:
                print("decrypted_data['data']['Hotel_Menu']",decrypted_data['data']['Hotel_Menu'])
                try:
                    value,clientId,market_place_id,id_value,guest=decrypted_data['data']['Hotel_Menu'].split('_')
                    print(value,clientId,market_place_id,id_value)
                except Exception as e:
                    print(e)
                    value=decrypted_data['data']['Hotel_Menu']
                    clientId=decrypted_data['data']['client_id']
                    market_place_id=decrypted_data['data']['marketplace_id']
                    id_value=decrypted_data['data']['id_value']
                if 'ExploreNearby' in decrypted_data['data']['Hotel_Menu']:
                    print('explore_nearby')
                    
                    Nearby_obj = Nearby_place.objects.filter(client_id=int(clientId),marketplace_id=market_place_id)
                    data_source=[]
                    print('Nearby_obj',Nearby_obj)
                    for i in Nearby_obj:
                        print("Marketplace",i.marketplace)
                        data_source.append(
                            {
                                "id":str(i.id),
                                "title":str(i.place_name),
                                "description":str(i.place_type)
                            }
                        )
                    print("data_source",data_source)

                    response={
                        "version":"3.0",
                        "screen":"ExploreNearby",
                        "data":{"list":data_source,"service_id":int(id_value)}
                    }
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                elif 'selfHelp' in decrypted_data['data']['Hotel_Menu']:
                    
                    selfhelp_obj = Selfhelp.objects.filter(client_id=int(clientId),marketplace_id=market_place_id)
                    data_source=[]
                    print('selfhelp_obj',selfhelp_obj)
                    for i in selfhelp_obj:
                        print("Marketplace",i.marketplace)
                        data_source.append(
                            {
                                "id":str(i.id),
                                "title":str(i.selfhelp_name),
                                
                            }
                        )
                    print("data_source",data_source)
                    response={
                        "version":"3.0",
                        "screen":"selfHelp",
                        "data":{
                            "list":data_source,
                            "service_id":int(id_value)
                        }
                    }
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                elif 'HotelFacilities' in decrypted_data['data']['Hotel_Menu']:
                    print('Hotel_facilities')
                    Hotel_facilities_obj = Hotel_facilities.objects.filter(client_id=int(clientId),marketplace_id=market_place_id)
                    data_source=[]
                    print('Hotel_facilities_obj',Hotel_facilities_obj,id_value)
                    for i in Hotel_facilities_obj:
                        print("Marketplace",i.marketplace)
                        data_source.append(
                            {
                                "id":str(i.id),
                                "title":str(i.facility_name),
                                
                            }
                        )
                    print("data_source",data_source)
                    response={
                         "version":"3.0",
                         "screen":"HotelFacilities",
                         "data":{ "list":data_source,"service_id":int(id_value)}
                    }
                    print("response",response)
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                elif 'Hotelservices' in decrypted_data['data']['Hotel_Menu']:
                    print('Hotel_services,id_value',id_value)
                    Hotel_services_obj = Hotel_services.objects.filter(client_id=int(clientId),marketplace_id=market_place_id)
                    data_source=[]
                    print('Hotel_services_obj',Hotel_services_obj)
                    for i in Hotel_services_obj:
                        print("Marketplace",i.marketplace)
                        data_source.append(
                            {
                                "id":str(i.id),
                                "title":str(i.service_name),
                                
                            }
                        )
                    print("data_source",data_source)
                    response={
                         "version":"3.0",
                         "screen":"Hotelservices",
                         "data":{ "list":data_source,"service_id":int(id_value)}
                    }
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                elif 'Moreinformation' in decrypted_data['data']['Hotel_Menu']:
                    print('More_information')
                    Information_obj = Information.objects.filter(client_id=int(clientId),marketplace_id=market_place_id)
                    data_source=[]
                    print('Information_obj',Information_obj)
                    for i in Information_obj:
                        print("Marketplace",i.marketplace)
                        data_source.append(
                            {
                                "id":str(i.id),
                                "title":str(i.information_name),
                                
                            }
                        )
                    print("data_source",data_source)
                    response={
                         "version":"3.0",
                         "screen":"Moreinformation",
                         "data":{ "list":data_source,"service_id":int(id_value)}
                    }
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                
                elif 'OrderFood' in decrypted_data['data']['Hotel_Menu']:
                    print("orderfood")
                    
                    india_timezone = pytz.timezone('Asia/Kolkata')
                    current_date_time_in_india = (datetime.now(india_timezone))
                    current_time_in_india=current_date_time_in_india.time()
                    print(current_time_in_india)
                    #Food_catalogue_obj = Food_catalogue.objects.filter(client_id=int(clientId),marketplace_id=market_place_id,end_time__gte = current_time_in_india).order_by('end_time')
                    Food_catalogue_obj = Food_catalogue.objects.filter(client_id=int(clientId),marketplace_id=market_place_id)
                    print(Food_catalogue_obj)
                    data_source=[]
                    print('Food_catalogue_obj',Food_catalogue_obj)
                    present_datetime=datetime.now()
                    Guest_info_obj=Guest_info.objects.get(client_id=int(client_id),id=int(guest))
                    Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.filter(client_id=int(client_id),Guest_details=Guest_info_obj,Check_Out__gt=present_datetime).values('Room_details')
                    print(Hotel_Room_Guest_info_obj)
                    rooms=[]
                    for i in Hotel_Room_Guest_info_obj:
                        Room_list_obj=get_object_or_404(Room_list,id=i['Room_details'])
                        rooms.append({"id":str(i['Room_details']),"title":Room_list_obj.room_number})
                    print("rooms",rooms)
                    encoded_image=''
                    start_time_str=''
                    end_time_str=''
                    data_source=[]
                    response={}
                    for H_i in Food_catalogue_obj:
                        data_source.append(
                            {
                                "id":f'{H_i.client_id}_{H_i.marketplace_id}_{H_i.id}',
                                "title":H_i.catalogue_name,
                                "description":H_i.catalogue_discription
                                
                            }
                        )
                        print("data_source",data_source)
                        # end_time_str = H_i.end_time.strftime("%I:%M%p") 
                        # start_time_str = H_i.start_time.strftime("%I:%M%p")
                        # if encoded_image=='':
                        #     with H_i.catalogue_image.open(mode='rb') as image_file:
                        #         image_content= image_file.read()
                        #         encoded_image =base64.b64encode(image_content).decode('utf-8')

                        response={
                            "version":"3.0",
                            "screen":"OrderFood",
                            "data":{
                                 "list":data_source,
                                 "Rooms":rooms,
                                 "Rooms_init":rooms[0]["id"],
                                 "service_id":int(id_value)
                                #  "src":encoded_image,
                                #  "id_value":str(H_i.id),
                                # "name":H_i.catalogue_name, 
                                # "About":H_i.catalogue_discription,
                                # "Timing":f'{start_time_str} to {end_time_str}',
                                # "set_id":str(H_i.catalogue_set_id)
                                }
                        }
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                    
                elif 'Complaints' in decrypted_data['data']['Hotel_Menu']:
                    Complaint_settings_obj=Complaint_settings.objects.filter(client_id=clientId,marketplace_id=market_place_id)
                    hotel_name=''
                    if market_place_id:
                        Hotel_markeplace_obj=Hotel_marketplace.objects.get(id=int(market_place_id))
                        hotel_name=Hotel_markeplace_obj.hotel_name
                    else:
                        Hotel_setings_obj=Hotel_settings.objects.get(id=int(hotel_settings_id))
                        hotel_name=Hotel_setings_obj.hotel_name
                    utc_now = datetime.utcnow()

                    # Set the timezone to Indian Standard Time (IST)
                    ist = pytz.timezone('Asia/Kolkata')
                    present_indian_datetime = utc_now.replace(tzinfo=pytz.utc).astimezone(ist)

                    Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.filter(client_id=int(clientId),Hotel_details_id=int(hotel_settings_id),Guest_details_id=int(guest),Check_Out__gte=present_indian_datetime) 
                    rooms=[]
                    for r_i in Hotel_Room_Guest_info_obj:
                       rooms.append({
                        "id":str(r_i.Room_details.id),
                        "title":r_i.Room_details.room_number
                       }) 
                    complaints=[]
                    for i in Complaint_settings_obj:
                        complaints.append({
                            "id":f"{i.id}",
                            "title":f"{i.Complaint_category}"
                        })
                    response={
                        "version":"3.0",
                        "screen":"Complaints",
                        "data":{
                        "hotel_name":hotel_name,
                        "marketplace_id":market_place_id,
                        "client_id":clientId,
                        "complaints":complaints,
                        "Rooms":rooms,
                        "id_value":id_value
                        }
                    }
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')


            elif 'locations' in decrypted_data['data']:
                print("locations:", decrypted_data['data']['locations'])
                Nearby_obj = Nearby_place.objects.get(id=decrypted_data['data']['locations'])
                print(Nearby_obj,Nearby_obj.place_name)
                encoded_image=''
               
            
                with Nearby_obj.place_image.open(mode='rb') as image_file:
                        image_content= image_file.read()
                        encoded_image =base64.b64encode(image_content).decode('utf-8')
                # print(Nearby_obj.distance_unit)
                response={
                    "version":"3.0",
                    "screen":"locationdetails",
                    "data":{
                        "src":encoded_image,
                        "name":Nearby_obj.place_name,
                        "About":Nearby_obj.Discription,
                        "Distance":str(Nearby_obj.distance)+' '+Nearby_obj.distance_unit,
                        "id_value":str(Nearby_obj.id),
                        "marketplace_id":str(Nearby_obj.marketplace_id),
                        "client_id":str(Nearby_obj.client_id),
                        "service_id":decrypted_data['data']['service_id']
                        
                        
                    }
                }
                return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
            elif 'Self_help_list' in decrypted_data['data']:
                selfhelp_obj = Selfhelp.objects.get(id=decrypted_data['data']['Self_help_list'])
                print(selfhelp_obj)
                encoded_image=''
                
           
                with selfhelp_obj.selfhelp_image.open(mode='rb') as image_file:
                        image_content= image_file.read()
                        encoded_image =base64.b64encode(image_content).decode('utf-8')
                
                response={
                    "version":"3.0",
                    "screen":"selfhelpdetails",
                    "data":{
                        "src":encoded_image,
                        "name":selfhelp_obj.selfhelp_name,
                        "Instructions":selfhelp_obj.selfhelp_discription,
                        "id_value":str(selfhelp_obj.id),
                        "marketplace_id":str(selfhelp_obj.marketplace_id),
                        "client_id":str(selfhelp_obj.client_id),
                        "service_id":decrypted_data['data']['service_id']
                            
                        
                        
                        
                    }
                }
                return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
            elif 'facility_list' in decrypted_data['data']:
                Hotel_facilities_obj = Hotel_facilities.objects.get(id=decrypted_data['data']['facility_list'])
                print(Hotel_facilities_obj)
                encoded_image=''
               
            
                with Hotel_facilities_obj.image.open(mode='rb') as image_file:
                        image_content= image_file.read()
                        encoded_image =base64.b64encode(image_content).decode('utf-8')
                # print(Hotel_facilities_obj.facility_name,Hotel_facilities_obj.facility_location,Hotel_facilities_obj.discription,Hotel_facilities_obj.start_time,Hotel_facilities_obj.end_time)
                # print("decrypted_data['data']['service_id']",decrypted_data['data'])       
                end_time_str = Hotel_facilities_obj.end_time.strftime("%I:%M%p") 
                start_time_str = Hotel_facilities_obj.start_time.strftime("%I:%M%p")
                response={
                    "version":"3.0",
                    "screen":"Faciltydetails",
                    "data":{
                        "src":encoded_image,
                        "name":Hotel_facilities_obj.facility_name,
                        "Location":Hotel_facilities_obj.facility_location,
                        "Timing":f"{start_time_str} to {end_time_str}",
                        "About":Hotel_facilities_obj.discription,
                        "id_value":str(Hotel_facilities_obj.id),
                        "marketplace_id":str(Hotel_facilities_obj.marketplace_id),
                        "client_id":str(Hotel_facilities_obj.client_id),
                        "service_id":decrypted_data['data']['service_id']
                            }
                }
                print("response",response)
                return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
            elif 'Services_list' in decrypted_data['data']:
                Hotel_services_obj = Hotel_services.objects.filter(id=decrypted_data['data']['Services_list'])
                Guest_info_obj=Guest_info.objects.get(client_id=int(client_id),id=int(guest))
                present_dateTime=datetime.now()
                Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.filter(client_id=int(client_id),Guest_details=Guest_info_obj,Check_Out__gt=present_dateTime).values('Room_details')
                print(Hotel_services_obj,Hotel_Room_Guest_info_obj)
                rooms=[]
                for i in Hotel_Room_Guest_info_obj:
                    Room_list_obj=get_object_or_404(Room_list,id=i['Room_details'])
                    rooms.append({"id":str(i['Room_details']),"title":Room_list_obj.room_number})
                print("rooms",rooms)
                encoded_image=''
               
                for H_i in Hotel_services_obj:
                    with H_i.service_image.open(mode='rb') as image_file:
                            image_content= image_file.read()
                            encoded_image =base64.b64encode(image_content).decode('utf-8')
                    # print(encoded_image,H_i.facility_name,H_i.facility_location,H_i.discription,H_i.start_time,H_i.end_time)
                           
                    end_time_str = H_i.end_time.strftime("%I:%M%p") 
                    start_time_str = H_i.start_time.strftime("%I:%M%p")
                    print("decrypted_data['data']['service_id']",type(decrypted_data['data']['service_id']),decrypted_data['data']['service_id'])
                    response={
                        "version":"3.0",
                        "screen":"Hotelservicesdetails",
                        "data":{
                            "src":encoded_image,
                            "name":H_i.service_name, 

                            "Timing":f"{start_time_str} to {end_time_str}",
                            "About":H_i.service_discription,
                             "id_value":str(H_i.id),
                            "marketplace_id":str(H_i.marketplace_id),
                            "client_id":str(H_i.client_id),
                            "Rooms":rooms,
                            "Rooms_init":rooms[0]['id'],
                            "service_id":decrypted_data['data']['service_id'],
                            
                              }
                    }
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
            elif 'Information_details' in decrypted_data['data']:
                Information_obj = Information.objects.get(id=decrypted_data['data']['Information_details'])
                print(Information_obj)
                encoded_image=''

               
                with Information_obj.information_image.open(mode='rb') as image_file:
                    image_content= image_file.read()
                    encoded_image =base64.b64encode(image_content).decode('utf-8')
            # print(encoded_image,H_i.facility_name,H_i.facility_location,H_i.discription,H_i.start_time,H_i.end_time)
                    
                    
                response={
                    "version":"3.0",
                    "screen":"Informationdetails",
                    "data":{
                        "src":encoded_image,
                        "name":Information_obj.information_name, 
                        "About":Information_obj.information_discription,
                        "id_value":str(Information_obj.id),
                        "marketplace_id":str(Information_obj.marketplace_id),
                        "client_id":str(Information_obj.client_id),
                        "service_id":decrypted_data['data']['service_id']
                            }
                    }
                return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
        
          
            elif 'Room_category' in decrypted_data['data']:
               
                response={}
                if decrypted_data['data']['Room_category']!='':
                 
                    Hotel_rooms_category=Hotel_rooms_type.objects.get(client_id=int(client_id),marketplace_id=int(marketplace_id),id=int(decrypted_data['data']['Room_category']))
                    print(Hotel_rooms_category,"Hotel_rooms_category")
                    Room_list_obj=Room_list.objects.filter(client_id=str(client_id),marketplace_id=str(marketplace_id),hotel_room_type=Hotel_rooms_category)
                    no_of_rooms=[]
                    if Room_list_obj:
                        for i in range(1,len(Room_list_obj)+1):
                            no_of_rooms.append({"id":f"{i}","title":f"{i}"}) 
                    else:
                        no_of_rooms.append({"id":str(0),"title":str(0)})
                    response={
                        "version":"3.0",
                        "screen":"Hotel_room_form",
                        "data":{
                            "no_of_rooms":no_of_rooms,
                            "no_of_rooms_init":str(no_of_rooms[0]['id']),
                            "name":decrypted_data['data']['Name'],
                            "GovernmentId":decrypted_data['data']['GovernmentId'],
                            "Address":decrypted_data['data']['Address'],
                            "room_init":decrypted_data['data']['Room_category'],
                     }
                    }
                else:
                   
                   
                    response={
                        "version":"3.0",
                        "screen":"Hotel_room_form",
                        "data":{"no_of_rooms":[{"id":"-","title":""}]}
                    }  
                return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
            elif 'guest_id' in decrypted_data['data'] and "check_out_room_number" in decrypted_data['data']:
                checkout,client_id,marketplace_id,hotel_id,guest=decrypted_data['flow_token'].split('_')
                Checkout_questions_obj=Checkout_questions.objects.filter(client_id=int(client_id),marketplace_id=int(marketplace_id)).order_by("id")
                hotel_marketplace_obj=Hotel_marketplace.objects.get(client_id=int(client_id), id=int(marketplace_id))
                Hotel_settings_obj=Hotel_settings.objects.get(id=hotel_id)
                Guest_info_obj=Guest_info.objects.get(id=int(guest))
                datetime_utc=datetime.now()
                print("datetime_utc",datetime_utc)
                india_timezone = pytz.timezone('Asia/Kolkata')
                datetime_india = india_timezone.localize(datetime_utc)
                datetime_str=datetime.strftime(datetime_india,'%Y-%m-%d %H:%M:%S')
                print(datetime_str)
                datetime_obj=datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S')
                print(datetime_obj)                                                                                                 
                Checkout_response_header_id=0
                for j,i in enumerate(decrypted_data['data']['check_out_room_number']):
                    Room_list_obj=Room_list.objects.get(client_id=int(client_id),marketplace_id=int(marketplace_id),id=int(i))
                    Hotel_Room_Guest_info_obj=Hotel_Room_Guest_info.objects.get(client_id=int(client_id),Room_details=Room_list_obj,Guest_details=Guest_info_obj,Hotel_details_id=int(hotel_id),Check_Out__gt=datetime_india)
                    Hotel_Room_Guest_info_obj.Check_Out=datetime_obj
                    Hotel_Room_Guest_info_obj.save()
                    if j==0:
                        Checkout_response_header_obj=Checkout_response_header.objects.create(
                            client_id=int(client_id),
                            Room_details=Room_list_obj,
                            Hotel_details=Hotel_settings_obj,
                            Guest_details=Guest_info_obj
                        )
                        Checkout_response_header_obj.save()
                        Checkout_response_header_id=Checkout_response_header_obj.id
                
                response={
                    "version":"3.0",
                    "screen":"Checkout_feedback_form",
                    "data":{
                        "Checkout_response_header_id":Checkout_response_header_id,
                        "hotel_name": hotel_marketplace_obj.hotel_name,
                        "question":Checkout_questions_obj[0].Question,
                        "question_id":Checkout_questions_obj[0].id,
                        "all_question_id":f"{Checkout_questions_obj[0].id}",
                        "all_feedbacks":"",
                        
                        "Rating":[
                            {
                                "id":"5",
                                "title":"       * * * * *  Excellent"
                            },
                             {
                                "id":"4",
                                "title":"       * * * *  Very Good"
                            },
                             {
                                "id":"3",
                                "title":"       * * *  Good"
                            },
                             {
                                "id":"2",
                                "title":"       * *  Avereage"
                            },
                             {
                                "id":"1",
                                "title":"       *  Poor"
                            }
                        ]
                    }
                }
                return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
            elif  'question_id' in decrypted_data['data'] and 'rating' in decrypted_data['data']:
                checkout,client_id,marketplace_id,hotel_settings_id,guest=decrypted_data['flow_token'].split('_')
                Checkout_responses_obj=Checkout_responses.objects.create(
                    client_id=int(client_id),
                    Checkout_response_header_id=decrypted_data["data"]["Checkout_response_header_id"],
                    Checkout_question_id=decrypted_data["data"]["question_id"],
                    Checkout_response=int(decrypted_data["data"]['rating'])
                )
                Checkout_responses_obj.save()
                response={}
                Checkout_questions_obj=Checkout_questions.objects.filter(client_id=int(client_id),marketplace_id=marketplace_id,id__gt=decrypted_data['data']['question_id']).order_by("id")
                print("Checkout_questions_obj",Checkout_questions_obj,len(Checkout_questions_obj))
                
                if len(Checkout_questions_obj) >= 1:
                    response={
                    "version":"3.0",
                    "screen":"Checkout_feedback_form",
                    "data":{
                        "Checkout_response_header_id":decrypted_data["data"]["Checkout_response_header_id"],
                        "hotel_name":decrypted_data["data"]["hotel_name"],
                        "question":Checkout_questions_obj[0].Question,
                        "question_id":Checkout_questions_obj[0].id,
                        "all_question_id":decrypted_data['data']['all_question_id']+'_'+str(Checkout_questions_obj[0].id),
                        "all_feedbacks":decrypted_data['data']['all_feedbacks']+'_'+decrypted_data['data']['rating'],
                        "Rating":[
                            {
                                "id":"5",
                                "title":"* * * * * Excellent"
                            },
                            {
                                "id":"4",
                                "title":"* * * * Very Good"
                            },
                            {
                                "id":"3",
                                "title":"* * * Good"
                            },
                            {
                                "id":"2",
                                "title":"* * Avereage"
                            },
                            {
                                "id":"1",
                                "title":"* Poor"
                            }
                        ]
                    }
                }
                elif len(Checkout_questions_obj) == 0:
                    print("else")
                    response={
                            "version":"3.0",
                            "screen":"Comment",
                            "data":{
                             "Checkout_response_header_id":decrypted_data["data"]["Checkout_response_header_id"],
                            "all_question_id":decrypted_data['data']['all_question_id'],
                            "all_feedbacks":decrypted_data['data']['all_feedbacks'][1:],
                            "hotel_name":decrypted_data['data']['hotel_name']
                            }
                        }  
                return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')      
                 
                          
                        
            response = {}
            return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
       
    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)
@csrf_exempt
def dataexchange(request):
    print("request", request)

    # print(JsonResponse(data,status=200),JsonResponse(data,status=200).text)
    try:
        # Parse the request body
        body = json.loads(request.body)
        print(body)
        encrypted_flow_data_b64 = body['encrypted_flow_data']
        encrypted_aes_key_b64 = body['encrypted_aes_key']
        initial_vector_b64 = body['initial_vector']
        print("encrypted_flow_data_b64", encrypted_flow_data_b64, "length: ", len(encrypted_flow_data_b64))
        print("encrypted_aes_key_b64", encrypted_aes_key_b64, "length: ", len(encrypted_aes_key_b64))
        print("initial_vector_b64", initial_vector_b64, "length: ", len(initial_vector_b64))

        decrypted_data, aes_key, iv = decrypt_request(encrypted_flow_data_b64, encrypted_aes_key_b64,
                                                      initial_vector_b64)
        print("decrypted_data,aes_key,iv", decrypted_data, aes_key, iv)

        # --------------------------------------------------------------------
        if decrypted_data['action'] == 'ping':
            response = {

                "version": "3.0",
                "data": {
                    "status": "active"
                }

            }
            return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
        

        # -----------------------------------------------------------------

        # Return the next screen & data to the client
        elif decrypted_data['action'] == 'INIT':
            response=' '
            print(decrypted_data['flow_token'])
          
            response = {
                    "version": "3.0",
                    "screen": "Menu",
                    "data": {
                    
                    }

                }


            return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
       

        elif decrypted_data['action'] == 'data_exchange':
            print("data_exchange")
            print("data", decrypted_data['data'])
            print(decrypted_data['flow_token'])
            decoded_bytes = base64.b64decode(decrypted_data['flow_token'])
            decoded_string = decoded_bytes.decode('utf-8')
            print(decoded_string)
            username, password = decoded_string.split(':')
            print(username)
            print(password)
            print("password")
            url = f"https://dev164889.service-now.com/api/now/table/sys_user?sysparm_query=user_name={username}"
            payload = {}
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + decrypted_data['flow_token'],
                'Cookie': 'BIGipServerpool_dev164889=3331282698.40766.0000; JSESSIONID=6313C1AA239A358068CEDBC3290CF2E0; glide_session_store=B03880BA9762F110FB3B5C900153AFD9; glide_user_activity=U0N2M18xOnIwd2g0NnduQ0UrR1JpSWxldDZpU09jdDFxNUMzcjNuSHJvbzN6SzkrOWs9OnNBV3JZeloxSUdyL0QxcGNGYTI3K2M2QTFnYnNnRmZMUk1JV25yQ2lwbVU9; glide_user_route=glide.204f61c181048880583f00591ea5c8d1'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            print(response.text,"response")
            response_json = response.json()
            print(response.text,"response",response_json)
            result = response_json.get('result')
            print("result",result)
            sys_id = result[0]['sys_id']
            print("sys_id",sys_id)

            # if decrypted_data['data']['selected_ticket']:
            #     print(decrypted_data['data']['selected_ticket'][0:3])
            if 'selected_menu' in decrypted_data['data']:
                if decrypted_data['data']['selected_menu'] == 'Create_new_ticket':
                    response = {
                        "version": "3.0",
                        "screen": "Create_new_ticket",
                        "data": {}
                    }
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                elif decrypted_data['data']['selected_menu'] == 'My_Open_tickets':
                    print('My_Open_tickets')
                    url = f"https://dev164889.service-now.com/api/now/table/incident?sysparm_query=caller_id.user_name%3D{username}^active=true&sysparm_fields=number%2Curgency%2Cimpact%2Csys_created_by%2Csys_updated_by%2Cpriority%2Cstate^%2Cactive%2Copened_at%2Csys_id%2Cshort_description%2Csys_created_on"
                    headers = {
                        "Authorization": "Basic " + decrypted_data['flow_token'],
                    }
                    response = requests.get(url, headers=headers)
                    print(response.text, response.status_code)
                    response_json = response.json()
                    result = response_json.get('result')
                    print("length: ", len(result))
                    
                    print(result)
                    if len(result) > 0:
                        print(result[0]['sys_created_on'], type(result[0]['sys_created_on']))
                        result.sort(reverse=True, key=lambda x: x['sys_created_on'])
                        sys_created_on_list = []
                        for i, j in enumerate(result):
                            if i < 10:
                                sys_created_on_list.append(j)
                            else:
                                break
                        items = []
                        for i, ticket in enumerate(sys_created_on_list):
                            if ticket['short_description'] == '':
                                ticket['short_description'] = '<No Description>'
                            elif len(ticket['short_description']) > 30:
                                ticket['short_description'] = ticket['short_description'][0:30]

                            print(ticket['short_description'])
                            # f"Number:{ticket['number']}\nDescription:{ticket['short_description']}\nUrgency:{ticket['urgency']}\nsys_created_by:{ticket['sys_created_by']}\nImpact:{ticket['impact']}\nopened_at:{ticket['opened_at']}\nactive:{ticket['active']}\nsys_updated_by:{ticket['sys_updated_by']}\nsys_created_on:{ticket['sys_created_on']}"
                            detail = {
                                "id": f"{ticket['number']}",
                                "title": f"{ticket['short_description']}"
                            }

                            items.append(detail)

                        print("items", items)
                        response = {
                            "version": "3.0",
                            "screen": "My_Open_tickets",
                            "data": {"list": items}
                        }
                        return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                    else:
                       
                        details='No Incidents/Tickets Found....'
                        response = {
                        "version": "3.0",
                        "screen": "Search_result",
                        "data": {"details": details}
                    }
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')

                elif decrypted_data['data']['selected_menu'] == 'Tickets_assigned_to_me':
                    print("assigned ")
                    # url = f"https://dev164889.service-now.com/api/now/table/sys_user?sysparm_query=user_name={username}"
                    # payload = {}
                    # headers = {
                    #     'Content-Type': 'application/json',
                    #     'Authorization': 'Basic ' + decrypted_data['flow_token'],
                    #     'Cookie': 'BIGipServerpool_dev164889=3331282698.40766.0000; JSESSIONID=6313C1AA239A358068CEDBC3290CF2E0; glide_session_store=B03880BA9762F110FB3B5C900153AFD9; glide_user_activity=U0N2M18xOnIwd2g0NnduQ0UrR1JpSWxldDZpU09jdDFxNUMzcjNuSHJvbzN6SzkrOWs9OnNBV3JZeloxSUdyL0QxcGNGYTI3K2M2QTFnYnNnRmZMUk1JV25yQ2lwbVU9; glide_user_route=glide.204f61c181048880583f00591ea5c8d1'
                    # }
                    # response = requests.request("GET", url, headers=headers, data=payload)
                    # response_json = response.json()
                    # result = response_json.get('result')
                    # sys_id = result[0]['sys_id']
                    # print(sys_id)
                    url = f"https://dev164889.service-now.com/api/now/table/incident?sysparm_query=assigned_to={sys_id}^active=true&sysparm_fields=number%2Curgency%2Cimpact%2Csys_created_by%2Csys_updated_by%2Cpriority%2Cstate^%2Cactive%2Copened_at%2Csys_id%2Cshort_description%2Csys_created_on%2Cassigned_to"
                    headers = {
                        "Authorization": "Basic " + decrypted_data['flow_token'],
                    }
                    response = requests.get(url, headers=headers)

                    print(response.text, response.status_code)
                    response_json = response.json()
                    result = response_json.get('result')
                    print("length: ", len(result))
                  
                    print("result: ", result)
                    if len (result) > 0:
                        print(result[0]['sys_created_on'], type(result[0]['sys_created_on']))
                        result.sort(reverse=True, key=lambda x: x['sys_created_on'])
                        sys_created_on_list = []
                        for i, j in enumerate(result):
                            if i < 10:
                                sys_created_on_list.append(j)
                            else:
                                break
                        print("sys_created_on_list", sys_created_on_list, len(sys_created_on_list))
                        items = []
                        for i, ticket in enumerate(sys_created_on_list):
                            if ticket['short_description'] == '':
                                ticket['short_description'] = '<No Description>'
                            elif len(ticket['short_description']) > 30:
                                ticket['short_description'] = ticket['short_description'][0:30]

                            print(ticket['short_description'])
                            # f"Number:{ticket['number']}\nDescription:{ticket['short_description']}\nUrgency:{ticket['urgency']}\nsys_created_by:{ticket['sys_created_by']}\nImpact:{ticket['impact']}\nopened_at:{ticket['opened_at']}\nactive:{ticket['active']}\nsys_updated_by:{ticket['sys_updated_by']}\nsys_created_on:{ticket['sys_created_on']}"
                            detail = {
                                "id": f"{ticket['number']}",
                                "title": f"{ticket['short_description']}"
                            }

                            items.append(detail)

                        print("items", items)
                        response = {
                            "version": "3.0",
                            "screen": "Tickets_assigned_to_me",
                            "data": {"list": items}
                        }
                        return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                    else:
                        details='No Incidents/Tickets Found....'
                        print(details)
                        response = {
                        "version": "3.0",
                        "screen": "Search_result",
                        "data": {"details": details}
                    }
                        return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                elif decrypted_data['data']['selected_menu'][0:3] == 'INC':
                    print("ticket details")
                    print(decrypted_data['data']['selected_menu'])
                    url = f"https://dev164889.service-now.com/api/now/table/incident?sysparm_query=number%3D{decrypted_data['data']['selected_menu']}&sysparm_fields=number%2Curgency%2Cimpact%2Csys_created_by%2Csys_updated_by%2Cpriority%2Cstate^%2Cactive%2Copened_at%2Csys_id%2Cshort_description%2Csys_created_on%2Ccomments%2Csys_id&sysparm_display_value=true"
                    headers = {
                        "Authorization": "Basic " + decrypted_data['flow_token'],

                    }
                    response = requests.get(url, headers=headers)
                    print(response.text, response.status_code)
                    response_json = response.json()
                    result = response_json.get('result')
                    print("length: ", len(result))
                    details = f"Number:{result[0]['number']}\nDescription: {result[0]['short_description']}\n\nActive: {result[0]['active']}\nUrgency: {result[0]['urgency']}\nImpact: {result[0]['impact']}\n\nUpdated by: {result[0]['sys_updated_by']}\nCreated by: {result[0]['sys_created_by']}\nCreated on: {result[0]['sys_created_on']}\nComment: {result[0]['comments']}\nId: {result[0]['sys_id']}\n\n"
                    url=f"https://dev164889.service-now.com/api/now/table/sys_user_has_role?sysparm_query=user={sys_id}"
                    payload = {}
                    headers = {
                    'Authorization': "Basic " + decrypted_data['flow_token'],
                    }

                    response = requests.request("GET", url, headers=headers, data=payload)

                    print(response.text,response.status_code)
                    if response.status_code== 200:
                        response = {
                        "version": "3.0",
                        "screen": "Ticket",
                        "data": {
                            "details": details
                        }
                        }
                        return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                    else:
                        response = {
                            "version": "3.0",
                            "screen": "TicketTwo",
                            "data": {
                                "details": details
                            }
                        }
                        return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                elif decrypted_data['data']['selected_menu'] == 'Search_ticket':
                    print("search_ticket")
                    response = {
                        "version": "3.0",
                        "screen": "Search_ticket",
                        "data": {}
                    }
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
            elif 'assigned_to_OR_Created_by' in decrypted_data['data']:
                print("search results")
                # {'action': 'data_exchange', 'screen': 'Search_ticket', 'data': {'short_description': 'unable to connect to office wifi', 'number': '', 'assignment_group': '',

                response = decrypted_data['data']

                # ---------------------------------------------------------------------------------------------------------------------
                response_details = ''
                for i in response:
                    print(i)
                    if response[i] != '' and i != 'assigned_to_OR_Created_by' and i != 'form_name':
                        if i == 'short_description':
                            response_details += i + 'LIKE' + response[i] + '^'
                        else:
                            response_details += i + '=' + response[i] + '^'
                print(response_details)
                url = "https://dev164889.service-now.com/api/now/table/incident?sysparm_query=" + response_details + f"{decrypted_data['data']['assigned_to_OR_Created_by']}.user_name={username}"
                print(url)
                headers = {
                    "Authorization": "Basic " + decrypted_data['flow_token'],
                }
                response = requests.get(url, headers=headers)
                print(response.text, response.status_code)
                response_json = response.json()
                result = response_json.get('result')
                print("length: ", len(result))
                result.sort(reverse=True, key=lambda x: x['sys_created_on'])
                print(result)
                # ---------------------------------------------------------------------------------------------------------------------
                # if len(result)>0:
                #     for item in response_details:
                #         print("item",item)
                #         for dic in result:
                #             print("dic",dic)
                # print(item[0])
                # if len(dic[0][item[0]])>=len(response_details[item[1]]):
                #     if dic[0][item][0][0:len[response_details[item]]]==response_details[item[1]]:
                #         print("hello")
                #         print(dic[item][0])

                # ---------------------------------------------------------------------------------------------------------------------
                details = ''
                if len(result) > 0:
                    for i, j in enumerate(result):
                        if i < 10:
                            details += f"Number:{result[i]['number']}\nDescription: {result[i]['short_description']}\nUrgency: {result[i]['urgency']}\nCreated by: {result[i]['sys_created_by']}\nImpact: {result[i]['impact']}\nOpened at:{result[i]['opened_at']}\nactive: {result[i]['active']}\nUpdated by: {result[i]['sys_updated_by']}\nCreated on: {result[i]['sys_created_on']}\n \n\n"
                        else:
                            break
                else:
                    details = 'No Results found.....'

                response = {
                    "version": "3.0",
                    "screen": "Search_result",
                    "data": {"details": details}
                }
                return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
            elif 'data' in decrypted_data['data']:
                print("hello")
                print("Comments")
                print(decrypted_data['data'], type(decrypted_data['data']['comment']))
                print("comment", decrypted_data['data']['comment'])
                print(decrypted_data['data']['data'].split('\n'))
                data = decrypted_data['data']['data'].split('\n')
                print(data[0], data[-3])
                number = data[0].split(':')
                sys_id = data[-3].split(':')
                print(number[1], sys_id[1])
                url = f"https://dev164889.service-now.com/api/now/table/incident/{sys_id[1]}"
                headers = {
                    "Content-Type": "application/json",
                    "charset": "utf-8",
                    "Authorization": "Basic " + decrypted_data['flow_token']
                }
                payload = json.dumps({
                    "comments": decrypted_data['data']['comment']
                })
                response = requests.request("PATCH", url, headers=headers, data=payload)

                print(response.text, response.status_code)
                response_json = response.json()

                if response.status_code == 200:
                    response = {
                        "version": "3.0",
                        "screen": "final",
                        "data": {
                            "details": "Comment added succesfully"
                        }
                    }
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                else:
                    response = {
                        "version": "3.0",
                        "screen": "final",
                        "data": {
                            "details": "You don't have permission to add comments. Kindley contact admin"
                        }
                    }
                    return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
                    # elif 'commment' in decrypted_data['data']:
            #     print("comments", decrypted_data['data']['data'])
            #     decrypted_data['data']['comment']
            #     response={
            #         "version":"3.0",
            #         "screen":"final",
            #         "data":{}
            #     }
            #     return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')
            response = {}
            return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')

            # if decrypted_data['data']['selected_menu']=='Create_new_ticket':
            #     print("hello")
            #     response = {
            #         "version": "3.0",
            #         "screen": "Create_new_ticket",
            #         "data": {
            #             "list":[
            #                 {
            #                 "id": "software",
            #                 "title": "Software"
            #                },
            #                {
            #                 "id": "service_desk",
            #                 "title": "Service Desk "
            #                },
            #               {
            #                 "id": "hardware",
            #                "title": "Hardware"
            #                }
            #            ]   
            #          }
            #     }

            #     print("response",response)
            #     return HttpResponse(encrypt_response(response, aes_key, iv), content_type='text/plain')

        #  "id": "Create_new_ticket",

        #             "data": {
        #            "options":[
        #             {
        #             "id" : "1",
        #             "title" : "mohan1",
        #             "description" : "mohan is a very good boy"
        #             },
        #             {
        #                 "id": "2",
        #                 "title": "John1",
        #                 "description": "John is a talented artist"
        #             },
        #             {
        #                 "id": "3",
        #                 "title": "Emma1",
        #                 "description": "Emma loves to travel"
        #             }
        #         ]

        #     }
        # }

        # Return the response as plaintext

        # elif  decrypted_data['data']['selected_menu']== 'assigned_to':
        #     response={
        #         "version": decrypted_data['version'],
        #         "screen": decrypted_data['data']['selected_menu'],
        # #  "id": "Create_new_ticket",
        #         "title": "Create a ticket",
        #          "data": {},
        #         "terminal": True,
        #          "layout": {
        #               "type": "SingleColumnLayout",  
        #                "children": []
        #      }
        #     }
    except Exception as e:
        print(e)
        return JsonResponse({}, status=500)


def decrypt_request(encrypted_flow_data_b64, encrypted_aes_key_b64, initial_vector_b64):
    flow_data = b64decode(encrypted_flow_data_b64)
    iv = b64decode(initial_vector_b64)
    PRIVATE_KEY = '''-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIFHDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQINuq0Zfuv8UUCAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECGplP+NnLpqOBIIEyLPLEFux+RIS
RMM6UTBNonWht8f5BKZTAX/aGPCE5HVLshi++76+l+f935akUUzlV/0nyMbXh1Pz
gquT51gzOr2If/bGY5/TOdBKLYB4mAU3oDhurJYpZ8jDLq9xeMK4745DhaaNCqb8
M1ouY2Z4ZCvCQQ97yDTNQl6EOm+MQ26oph74RtIZLgiacErCyltFHAjPSwmrS2lR
DJcPvqOeT6gCRGAlSwLlK304vh8EBh8E+5DI6MJ8caa3QgGh3kpgbftsWQoSTYJj
LpNRLDjCmmwbrhd3Zqdd9JU57pg26+Rx+tS+/1pt5xZVs27d5hpjWvIPN+mLndhv
tI/NEINHulKjddUzJ6yuK62fWBMdJUIE28N8EA68QWeGWyRR2FE9/Sj/E3DdeAVu
VczKvz5fcC2Bh5/+jZARJrs0R/Upa6otsdSuUVJu0qmJU5n2JWlNU0MI4wjb0kgO
6Mb0w8eQiM/0UTVCJK0gwRR/KtI8u77kUDuz9c1hYquWPd8x+n431bypZS/j4TLa
DLjo1QUKSNfcYrIA2NSNbQ5QAuO8Yv0FoV0+g6Jqz/ZMjx94Zelxy1TX8XUXuL6B
RfcddkvBotpTviP2YfT95m963ixHWEgdic+TSzyU6UpNSEnGXjtdMikyQ1bnEcnY
5GXjU+oz6LBJYfXC2098+cKDEMB/HHuKmIDotPpSyHZwAD6ygul5YPDhkWAW1p36
w5fpto6olRsuHfHHA+MbQILfEoUVcgIfs48VFLfzvcIZK2hrVduEiD0af+QVC3gL
OJmT/OdGyhJy53yXVjs25Nk91fBKUkPVe5jj4oYg7MLGK3ZP3tYFaTVBLGSAWQRI
L6M/0I4UR1/CZ2riddY9DEcxwoqq5ggH1m28uf0XOi8OwvkDgLA6khdM/mw1XXxg
XnY7hsafm6TbqzYWnftsw4KFezXN/fvszuYhwds1Cl5760ANeulCDabThDpeKqaX
ut4nN5dGUS83st8b5s7iQoR5/xlp89FlPcaadFMeko1QSofKDgZOiR3C4MDwkT9Z
4Z989AvqTxY2/re8QrP4+55ZNaAJSYAmrMLCqE+MZhorpNbMh43sKHOu9z5a/ANw
9z4+aFRtdGiu6skA3SSUYc+GobPwXZ+319gTFZN+gO3q69QFeX25RalIKjSuDriq
iU0uYk0o5ePDF4MrDNnvCzIQcwJ76tWZfW5ODJB7+BXgCUwG/ezdGA9yQerH+BNs
ximU2Unjp98Xr0omZTrUIPFbeDnWffZ6oXddDQXR+ZIMR59Kebx4UWxFV0cE2eG4
WdtqK7Le5Xd9Ejy/IqYmuPLDtUm/6PbMqUr1TGAeWnwKmXpsz+/EoWxCzSurHF6p
OIG6bzwSoQOU/ECNR5Nms7b5qsGlc2Lz0w0ALRJKM9GSdPQvXADCh6bOVVDA3FFY
i0CokvyyK23y/QbaZ+s1ky3oeHicWrefmHxgdep4oQJnUpCkvaVNrwlQoA6VLUdO
MNNt2Tp5vqdXmSOdWJaxEASY0IjcT9SQxYBjGjo/ikugev1lCl1R4pEiwVe5aWcm
P24xxIS1YgLxL0Ydcmxonmhf3sOYjuBKqy52ik4diWa+hbI/vS20Lyv18MVFmCKk
NNOS204zo325c68zRONPgg==
-----END ENCRYPTED PRIVATE KEY-----'''
    print("nnn")
    # print(flow_data)
    print("nnvv")

    # Decrypt the AES encryption key
    # print("PRIVATE_KEY", PRIVATE_KEY)

    encrypted_aes_key = b64decode(encrypted_aes_key_b64)
    print("bbbbbbbbbbbb")
    # print(encrypted_aes_key)
    print("llllllllllllllllllll")
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.encode('utf-8'), password=b'Mouli@123')
    print("jaysilan", private_key)
    public_key = private_key.public_key()
    # print(public_key)
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    print("public_key_bytes: ", public_key_bytes, type(public_key_bytes), len(public_key_bytes))
    my_public_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwHa5/S76XSxooO7yYumQ\nb44qlyVLooS4oBZoiXwrM3Yf/lWzQObDWH1TylKQWE2c2Cu66dYo8XMxJYTVSEq4\n74PD5LrRiE9Q/q/Qve8RVl4OZK0pEro6HgGCDD6WtI8bohQQJGm1EMc3vi+ln77s\noo/5an+OYgJbpWXhku7TbCMm2DuzxrzcrwePIBh6git+XVmTVPoakQgQmbfhfObK\nW0axxXSU3uEOxkhz8cN3lZ2AWSXRQTk4I57ke+PdmnLRxONoeqEGTEaSvYsBwvJ1\n0lXfVigvCFea0a77Qidq7/qofIxAosimKVBtZWTqsQMVXTwjn8F2sBiresUVk44G\nEQIDAQAB\n-----END PUBLIC KEY-----'
    print("my_public_key: ", my_public_key, type(my_public_key), len(my_public_key))
    for i in range(len(my_public_key)):
        if (my_public_key[i] != public_key_bytes[i]):
            print(i, my_public_key[i], public_key_bytes[i])
            print("different")
            break

    print(public_key_bytes[-1], public_key_bytes[-2], my_public_key[-1])

    print("triggering")
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
    # print(encrypted_flow_data_tag)
    # print(encrypted_flow_data_body)
    print('kkkk')
    # print(encrypted_flow_data_tag)
    decryptor = Cipher(algorithms.AES(aes_key),
                       modes.GCM(iv, encrypted_flow_data_tag)).decryptor()
    decrypted_data_bytes = decryptor.update(
        encrypted_flow_data_body) + decryptor.finalize()
    decrypted_data = json.loads(decrypted_data_bytes.decode("utf-8"))
    print(decrypted_data,"flow_decrypted_data")
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


def T(request, refid, cid):
    print(refid)
    print(cid)
    clientId = str(id)[12:]
    # print(clientId)
    facebookDetails = facebook_details.objects.filter(client_id=cid)
    clientNumber = ''
    for f_i in facebookDetails:
        clientNumber = f_i.fb_whatsapp_number

    return render(request, 'inform.html', {'refid': refid, 'clientID': cid, 'clientNumber': clientNumber})
    # return render(request,'infoform1.html',{'formid':id})
    # return HttpResponse("coming Here")


def N1(request, number, dcid):
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


def N2(request, number, dcid):
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
                   'PaymentGateway': 'razorpay', 'dname': donation_name, 'Filename': donationImage, 'Name': donar,
                   'Email': email, 'PAN': pan, "Comments": comments})


def checklink(request):
    return render(request, "checklink.html")


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
        donation_detailsobj = donation_types.objects.filter(client_id=dclientID, id=responseId)
        print(donation_detailsobj)
        for dj_i in donation_detailsobj:
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

def catalog_existance(request):
    Hotel_marketplace_obj= Hotel_marketplace.objects.get(client_id=request.user.id,id=marketplace_id)
    if Hotel_marketplace_obj.catalog_id:
       

        url = "https://graph.facebook.com/v19.0/129405560258915/whatsapp_commerce_settings?is_catalog_visible=false"#whatsapp_phonenumber_id

        payload = {}
        headers = {
        'Authorization': 'Bearer facebooToken'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response_json=response.json()
        print(response.text)
        
        if response.status_code==200 and 'success' in response_json:
            if 'true' in response_json['success']:
                print("food is enabled successfully")
        else:
            print("Food cannot be enabled for your Hotel kindly consult admin")
    else:
        print("Food cannot be enabled for your Hotel kindly consult admin")        
        

    
   
