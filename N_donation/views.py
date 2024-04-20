from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
import secrets

from django.shortcuts import redirect

import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from vailodb.models import admin_permission

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from A_vMart.forms import MyPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from A_vMart.views import logoutUser

from vailodb.models import admin_permission, facebook_details, payment_gateway_details,ticket_billing \
,Subclient, SubUserPreference,ticket_billing_details,  SUBCLIENT_CHOICE

from vailodb_n.models import donation_details, donation_settings, donation_types,donation_marketplace \
,donation_marketplace_settings
from A_vMart.settings import DomainName
from django.urls import reverse

from django.http import HttpResponse

# Create your views here.
def UpdateProfileDonation(request):
    adminPermissionObjects = admin_permission.objects.filter(client_id=request.user.id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    if request.method=="GET":
        user_id=request.user.id
        user_object=User.objects.filter(id=user_id)
        adminPermissionObjects=admin_permission.objects.filter(client_id=request.user.id)

        return render(request, 'N_donation/profile.html', {'us_obj': user_object,'adminP':adminPermissionObjects})
    elif request.method=="POST":
        print("hhhhhhhhhhh")
        user_id = request.user.id
        user_object = User.objects.get(id=user_id)
        user_object.username=request.POST.get('username')
        user_object.first_name = request.POST.get('first_name')
        user_object.last_name = request.POST.get('last_name')
        user_object.email = request.POST.get('email')
        user_object.save()
        user_id = request.user.id
        user_object1 = User.objects.filter(id=user_id)
        return render(request, 'N_donation/profile.html', {'us_obj': user_object1,'adminP':adminPermissionObjects,'admin_permission_obj':admin_permission_obj })



class N_DonationResetPass(LoginRequiredMixin, TemplateView):
    form_class = MyPasswordChangeForm

    def get(self, request, *args, **kwargs):
        print("getPass")
        form = self.form_class(self.request.user)
        return render(request, 'N_donation/resetPass.html', {'form': form, })
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        print("postPass")
        if form.is_valid(): 
            user = form.save()

            update_session_auth_hash(request, user)  # Important!
            logoutUser(request)
            return redirect('/')
        else:
            return render(request, 'N_donation/resetPass.html', {'form': form, 'password_changed': False})





def nDonationFacebook(request):
    admin_permissionObject = admin_permission.objects.filter(client_id=request.user.id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    if len(admin_permissionObject) == 0:
        admin_permissionCreate = admin_permission()
        admin_permissionCreate.client_auth_key = secrets.token_urlsafe(16)
        admin_permissionCreate.client_auth_secret = secrets.token_hex(16)
        admin_permissionCreate.client_billing_status = False
        admin_permissionCreate.client_id = request.user.id
        admin_permissionCreate.save()
    if request.method=="GET":
        user_fb_details = facebook_details.objects.filter(client_id=request.user.id)


        if len(user_fb_details) == 0:
            return render(request, 'N_donation/facebookDe1.html')

        else:
            print(user_fb_details)
            cliendId = ''
            cliendSecrat = ''
            clientType = ''
            clientpermissionstatus = ''
            admin_details_info = admin_permission.objects.filter(client_id=request.user.id)
            for info_i in admin_details_info:
                cliendId = cliendId + info_i.client_auth_key
                cliendSecrat = cliendSecrat + info_i.client_auth_secret
                clientType = clientType + info_i.client_type
                clientpermissionstatus = info_i.client_permission_status

            CallbackUrl = DomainName + 'webhook/' + cliendId
            VerifyToken = cliendSecrat
            print(CallbackUrl)
            print(VerifyToken)

            if clientpermissionstatus:
                return render(request, 'N_donation/facebookDe.html',
                              {'data': user_fb_details, 'CallbackUrl': CallbackUrl, 'VerifyToken': VerifyToken})
            else:
                return render(request, 'N_donation/facebookDe.html', {'data': user_fb_details})

            # if clientpermissionstatus:
            #     return render(request, 'N_donation/facebookDe.html', {'data': user_fb_details,'CallbackUrl': CallbackUrl,'VerifyToken': VerifyToken})


            # return render(request, 'N_donation/facebookDe.html', {'data': user_fb_details,'CallbackUrl':CallbackUrl,'VerifyToken':VerifyToken})



    if request.method=="POST":
        print(request.POST)
        ExitingUserObjects=facebook_details.objects.filter(


                                                           fb_phone_number_id=request.POST.get('fb_phone_number_id'),


                                                           )
        if len(ExitingUserObjects)==0:
            user_fb_details = facebook_details.objects.filter(client_id=request.user.id)
            print("ppppppppp",len(user_fb_details))
            if len(user_fb_details) == 0:
                fb_object = facebook_details()
                # fb_object.fb_name = request.POST.get('fb_name').lower()
                # fb_object.fb_business_manager_id = request.POST.get('fb_business_manager_id')
                # fb_object.fb_Whatsapp_business_account_id = request.POST.get('fb_Whatsapp_business_account_id')
                fb_object.fb_phone_number_id = request.POST.get('fb_phone_number_id')
                fb_object.fb_whatsapp_number=request.POST.get('fb_whatsapp_number')
                fb_object.fb_access_token = request.POST.get('fb_access_token')
                # fb_object.fb_auth_token = request.POST.get('fb_auth_token')
                # fb_object.fb_app_id = request.POST.get('fb_app_id')
                # fb_object.fb_second_number= int(request.POST.get('fb_second_number'))
                # fb_object.fb_third_number= int(request.POST.get('fb_third_number'))
                fb_object.client_id = request.user.id
                fb_object.save()
                user_fb_details = facebook_details.objects.filter(client_id=request.user.id)
                return render(request, 'N_donation/facebookDe.html', {'data': user_fb_details})
            elif len(user_fb_details)!=0:
                fb_object_edit = facebook_details.objects.get(client_id=request.user.id)
                print(fb_object_edit,'pppppppp')
                # fb_object_edit.fb_name = request.POST.get('fb_name').lower()
                # fb_object_edit.fb_business_manager_id = request.POST.get('fb_business_manager_id')
                # fb_object_edit.fb_Whatsapp_business_account_id = request.POST.get('fb_Whatsapp_business_account_id')
                fb_object_edit.fb_phone_number_id = request.POST.get('fb_phone_number_id')
                fb_object_edit.fb_whatsapp_number=request.POST.get('fb_whatsapp_number')
                fb_object_edit.fb_access_token = request.POST.get('fb_access_token')
                # fb_object_edit.fb_auth_token = request.POST.get('fb_auth_token')
                # fb_object_edit.fb_app_id = request.POST.get('fb_app_id')
                # fb_object_edit.fb_second_number= int(request.POST.get('fb_second_number'))
                # fb_object_edit.fb_third_number= int(request.POST.get('fb_third_number'))
                fb_object_edit.save()
                user_fb_details = facebook_details.objects.filter(client_id=request.user.id)
                return render(request, 'N_donation/facebookDe.html', {'data': user_fb_details, 'admin_permission_obj':admin_permission_obj})

        return redirect('/')




def nDonationPayment(request):
   
            return render(request, 'N_donation/payment_form.html')



# def payment_success(request):
#     return render(request, 'payment_status.html')
#
#
# def payment_failed(request):
#     return render(request, 'payment_failed.html')
def nDonationPayment(request):
    payment_gatewa = payment_gateway_details.objects.filter(client=request.user)

    if request.method == 'POST':
        for gateway in payment_gatewa:
            # Retrieve the corresponding form data based on the payment gateway
            gateway_id = request.POST.get(f'{gateway.payment_gateway}_gateway_id')
            gateway_key = request.POST.get(f'{gateway.payment_gateway}_gateway_key')
            currency = request.POST.get(f'{gateway.payment_gateway}_currency')

            # Update the payment details in the existing payment gateway
            gateway.gateway_id = gateway_id
            gateway.gateway_key = gateway_key
            gateway.currency = currency
            gateway.save()

        # Create new payment gateway entries for any selected methods that don't have existing entries
        selected_methods = ['rozorpay', 'cashfree', 'paypal', 'stripe']  # Modify as per your requirements
        existing_methods = [gateway.payment_gateway for gateway in payment_gatewa]

        new_methods = set(selected_methods) - set(existing_methods)
        for method in new_methods:
            gateway_id = request.POST.get(f'{method}_gateway_id')
            gateway_key = request.POST.get(f'{method}_gateway_key')
            currency = request.POST.get(f'{method}_currency')

            # Create a new payment gateway entry in the database
            payment_gateway_details.objects.create(
                client=request.user,
                payment_gateway=method,
                gateway_id=gateway_id,
                gateway_key=gateway_key,
                currency=currency
            )

        return render(request, 'N_donation/payment_form.html')  # Replace 'success_page' with your desired success page URL

    return render(request, 'N_donation/payment_form.html', {'payment_gatewa': payment_gatewa})

def billingDonation(request):
    billing = ticket_billing.objects.filter(client_id=request.user.id).order_by('-vailo_record_creation')
    billingRate = admin_permission.objects.filter(client_id = request.user.id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    return render(request, 'N_donation/billingTicket.html', {'billing': billing, 'billingRate':billingRate, 'admin_permission_obj':admin_permission_obj })


def donorDetail(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()  # Ensure admin_permission_obj is fetched for subclients
    # sub_user_preference = SubUserPreference.objects.get(client_id=request.user.id, subclient=subclient)
                         

    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    donationList = donation_details.objects.filter(client=request.user.id)
    context = {
        'donationList': donationList, 
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj':admin_permission_obj,
        # 'sub_user_preference':sub_user_preference
    }

    return render(request, 'N_donation/donorDetail.html',context )



def helpDonation(request):
    return render(request, 'N_donation/help.html')

def settingsDonation(request):
    return render(request, 'N_donation/settingsDonation.html')


def ConfigurationDonation(request):
    return render(request, 'N_donation/ConfigDonation.html')


def subUserDonation(request):
    subclientList = Subclient.objects.filter(client=request.user.id)



    return render(request, 'N_donation/subClient1.html',{'subclientList': subclientList} )

def openSubDonation(request):
    return render(request, 'N_donation/openSubClient.html')

from django.contrib import messages
from django.contrib.auth.hashers import check_password

def formsubclient1(request):
    subclientList = Subclient.objects.filter(client_id=request.user.id)
    print(request.user.id)
    if request.method == 'POST':
        subclientname = request.POST.get('subclientname')
        print('subclientname',subclientname)
        emailid = request.POST.get('emailid')
        print('emailid',emailid)
        password = request.POST.get('password')
        print('password',password)
        re_password = request.POST.get('re_password')
        print('re_password',re_password)

        # if password != re_password:
        #     messages.error(request, "Passwords do not match.")
        #     return redirect('openSub')

        # if len(password) < 8:
        #     messages.error(request, "Password should be at least 8 characters long.")
        #     return redirect('openSub')

        # if Subclient.objects.filter(client=request.user, emailid=emailid).exists():
        #     messages.error(request, "Email address already exists.")
        #     return redirect('openSub')

        # if User.objects.filter(email=emailid).exists():
        #     messages.error(request, "Email address is already registered.")
        #     return redirect('openSub')

        # # Check if the entered password matches the hashed password
        # if not check_password(password, request.user.password):
        #     messages.error(request, "Invalid password.")
        #     return redirect('openSub')

        subclient = Subclient(client_id=request.user.id, subclientname=subclientname,
                              emailid=emailid, password=password, re_password=re_password)
        print('subclient',subclient)
        subclient.save()

        # Redirect to a success page or any other desired page
        return redirect('subUserDonation')

    return render(request, 'N_donation/subClient1.html', {'subclientList': subclientList})



def assignSubClientDonation(request, id):
    subclient = Subclient.objects.get(id=id)
    client = request.user

    try:
        sub_user_preference = SubUserPreference.objects.get(client=client, subclient=subclient)
    except SubUserPreference.DoesNotExist:
        sub_user_preference = None

    # Fetch the client_service_type from the admin_permission model
    admin_perm_instance = admin_permission.objects.get(client=client)
    client_service_type = admin_perm_instance.client_service_type

    if request.method == 'POST':
        selected_preferences = request.POST.getlist('preferences')
        preference_str = ','.join(selected_preferences)

        if sub_user_preference:
            sub_user_preference.preference = preference_str
            sub_user_preference.save()
        else:
            sub_user_preference = SubUserPreference.objects.create(
                client=client,
                subclient=subclient,
                preference=preference_str,
            )

        try:
            

            return redirect('subUserDonation')
        except Exception as e:
            print("Redirection error:", e)

    return render(request, 'N_donation/assignSubClient.html', {'subclient': subclient, 'preferences': sub_user_preference, 'SUBCLIENT_CHOICE': SUBCLIENT_CHOICE, 'client_service_type': client_service_type})


# def donationInfo(request):
#     print("33")
#     if request.method == "GET":
#         donationDash = donation_settings.objects.filter(client_id=request.user.id)
#         admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

#         print()
        
#         if len(donationDash) == 0:
#             admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    
#             return render(request, 'N_donation/donatonInfo.html', {'admin_permission_obj':admin_permission_obj})
#         else:
#             return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash,'admin_permission_obj':admin_permission_obj})

# def donationInfo(request, id=None):
#     if request.method == "GET":
#         admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

#         if id:
#             # If 'id' is present, check if associated donation_settings entry exists
#             marketplace_id = id  # Replace this line with your actual logic to get marketplace_id
#             donation_setting = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id).first()
#             print('marketplace_id',marketplace_id)
#             if donation_setting:
#                 # If donation_settings entry exists, render donationInfo1.html
#                 return render(request, 'N_donation/donationInfo1.html', {'donation_setting': donation_setting, 'admin_permission_obj': admin_permission_obj})
#             else:
#                 donation_setting = get_donation_setting_somehow()
#                 # If donation_settings entry does not exist, render donationInfo.html with default data
#                 return redirect('donationInfo', id=donation_setting.marketplace_id)
#         else:
#             # If 'id' is not present, render donationInfo.html with default data
#             donationDash = donation_settings.objects.filter(client_id=request.user.id)

#             if len(donationDash) == 0:
#                 admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
#                 return render(request, 'N_donation/donatonInfo.html', {'admin_permission_obj': admin_permission_obj})
#             else:
#                 return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash, 'admin_permission_obj': admin_permission_obj})

# def donationInfo(request, id=None):
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
#     donationDash = donation_settings.objects.filter(client_id=request.user.id)
#     if id:
#         # If 'id' is present, check if associated donation_settings entry exists
#         donation_setting = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=id).first()
#         if donation_setting:
#             # If donation_settings entry exists, render donationInfo1.html
#             return render(request, 'N_donation/donationInfo1.html', {'donation_setting': donation_setting, 'admin_permission_obj': admin_permission_obj})
#         else:
          
#             return render(request, 'N_donation/donatonInfo.html')    # If 'id' is not present or donation_settings entry does not exist, render donationInfo.html with default data
    
    
#     if len(donationDash) == 0:
#         return render(request, 'N_donation/donatonInfo.html', {'admin_permission_obj': admin_permission_obj})
#     else:
#         return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash, 'admin_permission_obj': admin_permission_obj})

# from django.shortcuts import render, redirect
# from django.urls import reverse

# def donationInfo(request, id=None):
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
#     donationDash = donation_settings.objects.filter(client_id=request.user.id)

#     if id:
#         # If 'id' is present, check if associated donation_settings entry exists
#         donation_setting = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=id).first()
#         if donation_setting:
#             # If donation_settings entry exists, render donationInfo1.html with existing data
#             return render(request, 'N_donation/donationInfo1.html', {'donation_setting': donation_setting, 'admin_permission_obj': admin_permission_obj})

#         # If donation_settings entry does not exist, set the marketplace_id to be used in the form
#         marketplace_id = id
#     else:
#         # If 'id' is not present, check if any donation_settings entry exists for the client
#         existing_donation_setting = donation_settings.objects.filter(client_id=request.user.id).first()

#         if existing_donation_setting:
#             # If donation_settings entry exists, redirect to donationInfo1.html with existing data
#             if existing_donation_setting.marketplace_id is not None:
#                 # Only include the id parameter if it's not None
#                 return redirect(reverse('donationInfo', kwargs={'id': existing_donation_setting.marketplace_id}))
#             else:
#                 return redirect('donationInfo')

#         # If no existing data, render donationInfo.html with default data and null marketplace_id
#         marketplace_id = None

#     # Render donationInfo.html with default data and the determined marketplace_id
#     return render(request, 'N_donation/donatonInfo.html', {'marketplace_id': marketplace_id, 'admin_permission_obj': admin_permission_obj})

# def donationInfo(request, id=None):
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
#     donationDash = donation_settings.objects.filter(client_id=request.user.id, marketplace_id__isnull=True)
#     print('donationDash view:', donationDash)
#     print('marketplace_id in donationInfo1 view:', id)
#     marketplace_id = request.GET.get('marketplace_id')
#     if id:
#         donationDash = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=id).first()
#         print("donation_setting Id", donationDash)
#         if donationDash:
#             return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': id})
#         else:
#             return render(request, 'N_donation/donatonInfo.html', {'marketplace_id': id, 'admin_permission_obj': admin_permission_obj})
#     else:
#         if donationDash.exists():  # Check if there are any records in the queryset
#             # Assuming you want to show the first record when id is None
#             donationDash_first = donationDash.first()
#             return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash_first, 'admin_permission_obj': admin_permission_obj})
#         else:
#             return render(request, 'N_donation/donatonInfo.html', {'admin_permission_obj': admin_permission_obj})


# def donationInfo(request, id=None):
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
#     # Retrieve marketplace_id from the session
#     marketplace_id = request.session.get('marketplace_id')

#     print('Before setting marketplace_id:', request.session.get('marketplace_id'))
#     if id:
#     # Set the marketplace_id in the session
#         request.session['marketplace_id'] = id
#         request.session.save()
#         print('After setting marketplace_id:', request.session.get('marketplace_id'))
#     # Update donationDash queryset based on the presence of marketplace_id
#     donationDash = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)

#     print('donationDash view:', donationDash)
#     print('marketplace_id in donationInfo view:', marketplace_id)

#     if marketplace_id:
#         donationDash = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id).first()
#         print("donation_setting Id", donationDash)

#         if donationDash:
#             return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id})
#         else:
#             return render(request, 'N_donation/donatonInfo.html', {'marketplace_id': marketplace_id, 'admin_permission_obj': admin_permission_obj})
#     else:
#         if donationDash.exists():
#             donationDash_first = donationDash.first()
#             return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash_first, 'admin_permission_obj': admin_permission_obj})
#         else:
#             return render(request, 'N_donation/donatonInfo.html', {'admin_permission_obj': admin_permission_obj})

# def donationInfo(request, id=None):
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    
#     # Retrieve marketplace_id from the session
#     marketplace_id = request.session.get('marketplace_id')

#     print('Before setting marketplace_id:', request.session.get('marketplace_id'))
#     if id:
#         # Set the marketplace_id in the session
#         request.session['marketplace_id'] = id
#         request.session.save()
#         print('After setting marketplace_id:', request.session.get('marketplace_id'))

#     # Update donationDash queryset based on the presence of marketplace_id
#     donationDash = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)

#     print('donationDash view:', donationDash)
#     print('marketplace_id in donationInfo view:', marketplace_id)

#     if marketplace_id:
#         # Retrieve the first object in the queryset or None
#         donationDash = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id).first()
#         print("donation_setting Id", donationDash)

#         if donationDash:
#             return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id})
#         else:
#             return render(request, 'N_donation/donatonInfo.html', {'marketplace_id': marketplace_id, 'admin_permission_obj': admin_permission_obj})
#     else:
#         if donationDash.exists():
#             donationDash_first = donationDash.first()
#             return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash_first, 'admin_permission_obj': admin_permission_obj})
#         else:
#             return render(request, 'N_donation/donatonInfo.html', {'admin_permission_obj': admin_permission_obj})

# def donationInfo(request, id=None):
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    
#     # Retrieve marketplace_id from the session
#     marketplace_id = request.session.get('marketplace_id')

#     print('Before setting marketplace_id:', request.session.get('marketplace_id'))
#     if id:
#         # Set the marketplace_id in the session
#         request.session['marketplace_id'] = id
#         request.session.save()
#         print('After setting marketplace_id:', request.session.get('marketplace_id'))

#     # Update donationDash queryset based on the presence of marketplace_id
#     donationDash = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)

#     print('donationDash view:', donationDash)
#     print('marketplace_id in donationInfo view:', marketplace_id)

#     if marketplace_id:
#         # Retrieve the first object in the queryset or None
#         donationDash = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id).first()
#         print("donation_setting Id", donationDash)

#         if donationDash:
#             return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id})
#         else:
#             return render(request, 'N_donation/donatonInfo.html', {'marketplace_id': marketplace_id, 'admin_permission_obj': admin_permission_obj})
#     else:
#         if donationDash.exists():
#             donationDash_first = donationDash.first()
#             return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash_first, 'admin_permission_obj': admin_permission_obj})
#         else:
#             return render(request, 'N_donation/donatonInfo.html', {'admin_permission_obj': admin_permission_obj})

# def donationInfo(request, id=None):
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    
#     # Retrieve marketplace_id from the session
#     marketplace_id = request.session.get('marketplace_id')

#     # Get the referer URL from the request headers
#     referer = request.META.get('HTTP_REFERER', '')

#     # Check if coming from 'donationInfo' or 'addNgoMarketPlace'
#     if 'donationInfo' in referer or 'addNgoMarketPlace' in referer:
#         # Clear the marketplace_id from the session
#         request.session.pop('marketplace_id', None)
#         request.session.save()
#         print('Cleared marketplace_id from session')

#     print('Before setting marketplace_id:', request.session.get('marketplace_id'))
#     print('User ID:', request.user.id)
#     print('ID from URL:', id)

#     if id:
#         # Set the marketplace_id in the session
#         request.session['marketplace_id'] = id
#         request.session.save()
#         print('After setting marketplace_id:', request.session.get('marketplace_id'))

#     # Update donationDash queryset based on the presence of marketplace_id
#     donationDash = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)

#     print('donationDash view:', donationDash)
#     print('marketplace_id in donationInfo view:', marketplace_id)

#     if marketplace_id:
#         # Retrieve the first object in the queryset or None
#         donationDash_first = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id).first()
#         print("donation_setting Id", donationDash_first)

#         if donationDash_first:
#             return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash_first, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id})
#         else:
#             return render(request, 'N_donation/donatonInfo.html', {'marketplace_id': marketplace_id, 'admin_permission_obj': admin_permission_obj})
#     else:
#         if donationDash.exists():
#             donationDash_first = donationDash.first()
#             print("donation_setting Id", donationDash_first)
#             return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash_first, 'admin_permission_obj': admin_permission_obj})
#         else:
#             return render(request, 'N_donation/donatonInfo.html', {'admin_permission_obj': admin_permission_obj})


from django.contrib import messages
from django.shortcuts import redirect

def donationInfo(request, id=None):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
  
    # Retrieve marketplace_id from the session
    marketplace_id = request.session.get('marketplace_id')

    # Get the referer URL from the request headers
    referer = request.META.get('HTTP_REFERER', '')

    # Check if coming from 'donationInfo' or 'addNgoMarketPlace'
    if 'donationInfo' in referer or 'addNgoMarketPlace' in referer:
        # Clear the entire session
        # marketplace_id = request.session.get('marketplace_id')
        # request.session['marketplace_id'] = None
        request.session.save()
        # print('Cleared entire session')

        # Add a success message
        # messages.success(request, 'Session cleared successfully.')

        # Redirect to the current view
        # return redirect(request.path)

    print('Before setting marketplace_id:', request.session.get('marketplace_id'))
    print('User ID:', request.user.id)
    print('ID from URL:', id)

    if id:
        # Set the marketplace_id in the session
        request.session['marketplace_id'] = id
        request.session.modified = True
        request.session.save()
        print('After setting marketplace_id:', request.session.get('marketplace_id'))

    # Update donationDash queryset based on the presence of marketplace_id
    donationDash = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id)

    print('donationDash view:', donationDash)
    print('marketplace_id in donationInfo view:', marketplace_id)

    if marketplace_id:
        # Retrieve the first object in the queryset or None
        donationDash_first = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id).first()
        print("donation_setting Id", donationDash_first)

        if donationDash_first:
            return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash_first, 'admin_permission_obj': admin_permission_obj,'subclient_preferences':subclient_preferences, 'marketplace_id': marketplace_id})
        else:
            return render(request, 'N_donation/donatonInfo.html', {'marketplace_id': marketplace_id, 'admin_permission_obj': admin_permission_obj,'subclient_preferences':subclient_preferences, 'marketplace_id': marketplace_id})
    else:
        if donationDash.exists():
            donationDash_first = donationDash.first()
            print("donation_setting Id", donationDash_first)
            return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash_first, 'admin_permission_obj': admin_permission_obj,'subclient_preferences':subclient_preferences,'marketplace_id': marketplace_id})
        else:
            return render(request, 'N_donation/donatonInfo.html', {'admin_permission_obj': admin_permission_obj,'subclient_preferences':subclient_preferences,'marketplace_id': marketplace_id})


def donationInfo1(request, id=None):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    donationDash = donation_settings.objects.filter(client_id=request.user.id, marketplace_id__isnull=True)
      
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    # Retrieve marketplace_id from the session
    marketplace_id = request.session.get('marketplace_id')

    print('donationDash view:', donationDash)
    print('marketplace_id in donationInfo view:', marketplace_id)
    print('id in donationInfo view:', id)

    if id:
        # Set the marketplace_id in the session
        request.session['marketplace_id'] = id

        # Check if the session variable is set
        if marketplace_id:
            donationDash = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=marketplace_id).first()
            print("donation_setting Id from session", donationDash)
        else:
            # If session variable is not set, use the id parameter
            donationDash = donation_settings.objects.filter(client_id=request.user.id, marketplace_id=id).first()
            print("donation_setting Id from id parameter", donationDash)

        if donationDash:
            return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': id, 'subclient_preferences':subclient_preferences,})
        else:
            return render(request, 'N_donation/donatonInfo.html', {'marketplace_id': id, 'admin_permission_obj': admin_permission_obj, 'subclient_preferences':subclient_preferences,})
    else:
        if donationDash.exists():
            donationDash_first = donationDash.first()
            return render(request, 'N_donation/donationInfo1.html', {'donationDash': donationDash_first, 'admin_permission_obj': admin_permission_obj, 'subclient_preferences':subclient_preferences,'marketplace_id': id})
        else:
            return render(request, 'N_donation/donatonInfo.html', {'admin_permission_obj': admin_permission_obj,'subclient_preferences':subclient_preferences,'marketplace_id': id})


def generalDonationInfo(request):
    # marketplace_id = request.GET.get('marketplace_id')
    # print(marketplace_id,"marketplace_id")

    if request.method == "POST":
        print('POST data:', request.POST)
        marketplace_id = request.POST.get('marketplace_id')
        print('marketplace_id:', repr(marketplace_id))
        info_creation = donation_settings()
  
        if 'donationImage' in request.FILES:
            info_creation.donation_image = request.FILES['donationImage']

       

        if 'ngoLogo' in request.FILES:
            info_creation.ngo_logo = request.FILES['ngoLogo']

        if 'contactheaderimage' in request.FILES:
            info_creation.donation_contact_us_message = request.FILES['contactheaderimage']
        
        if 'contactheaderimage' in request.FILES:
            info_creation.donation_contact_us_image = request.FILES['contactheaderimage']

       
      
            
        
        info_creation.donation_description = request.POST.get('donationDescription')

        info_creation.donation_footer = request.POST.get( 'donationFooter')
       
        info_creation.donation_now_button_name = request.POST.get(
            'donationNowButtonName')
        info_creation.my_donation_button_name = request.POST.get(
            'myDonationButtonName')
        info_creation.contact_us_button_name = request.POST.get(
            'contactUsButtonName')
       
        info_creation.donation_list_header = request.POST.get(
            'donationListHeader')
        info_creation.donation_list_body = request.POST.get(
            'donationListBody')
        info_creation.donation_list_footer = request.POST.get(
            'donationListFooter')
        info_creation.donation_list_button_name = request.POST.get(
            'donationListButtonName')
       
        info_creation.donation_conform_message = request.POST.get(
            'donationConformMessage')
        
        info_creation.donation_failure_message = request.POST.get(
            'donationFailureMessage')
        
        info_creation.donation_contact_us_message = request.POST.get(
            'donationContactUsMessage')
        
        info_creation.contact_us_details_button_name  = request.POST.get(
            'ContactNowButtonName')

        info_creation.support_number = request.POST.get(
            'supportNumber')
        info_creation.ngo_name = request.POST.get(
            'ngoName')
        

        if 'ngoSignatureImage' in request.FILES:
            info_creation.ngo_signature_image = request.FILES['ngoSignatureImage']
        
        info_creation.ngo_pan = request.POST.get('ngoPan')

        info_creation.ngo_gstin = request.POST.get('ngoGstin')

        info_creation.ngo_header_notes = request.POST.get(
            'ngoHeaderNotes')
        info_creation.ngo_footer_notes = request.POST.get(
            'ngoFooterNotes')
        info_creation.ngo_signature_header = request.POST.get(
            'ngoSignatureHeader')
        info_creation.ngo_signature_footer = request.POST.get(
            'ngoSignatureFooter')
        info_creation.invoice_footer = request.POST.get(
            'invoiceFooter')
        
        info_creation.ngo_link_text = request.POST.get(
            'ngo_link_text')
        info_creation.ngo_url = request.POST.get(
            'ngo_url')
        
        info_creation.my_donation_details_button_name1  = request.POST.get(
            'donationDetailsButton1')
        info_creation.my_donation_details_button_name2  = request.POST.get(
            'donationDetailsButton2')
        info_creation.my_donation_details_button_name3  = request.POST.get(
            'donationDetailsButton3')
       
        
        info_creation.client_id = request.user.id
        info_creation.save()

        marketplace_id = request.POST.get('marketplace_id')
        if marketplace_id:
            info_creation.marketplace_id = marketplace_id
            info_creation.save()
            return redirect(reverse('donationInfo', kwargs={'id': marketplace_id}))
        else:
            return redirect('donationInfo')

from django.urls import reverse

# def editSettingsDonation(request, id=None):
#     donationsettings = donation_settings.objects.get(client_id=request.user.id, marketplace_id=id)
#     info_creations = donation_settings()
#     print("Marketplace ID:", id)

#     # for info_creations in donationsettings:
#         if request.method == "POST":
#             donationsettings = donation_settings.objects.get(client_id=request.user.id, marketplace_id=id)
#             info_creations = donation_settings()
#             # info_creation = event_settings()
from django.shortcuts import get_object_or_404

def editSettingsDonation(request, id=None):
    print("Inside editSettingsDonation view")
    # Get the existing donation_settings object or return a 404 if not found
    # donationsettings = get_object_or_404(donation_settings, client_id=request.user.id, marketplace_id=id)
    # info_creations = donation_settings()
    marketplace_id = id
    user_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    info_creations = get_object_or_404(donation_settings, client_id=user_id, marketplace_id=marketplace_id)

    print("abc")
    if request.method == "POST":
        print('POST data:', request.POST)
        marketplace_id = request.GET.get('marketplace_id')
        print('marketplace_id:', repr(marketplace_id))
        # Create a new instance for updating the data
        if 'redonationImage' in request.FILES and len(request.FILES['redonationImage']) != 0:
            info_creations.donation_image = request.FILES['redonationImage']
        else:
            info_creations.donation_image = info_creations.donation_image
            # info_creation.welcome_header_text = request.POST.get('rewelcomemessagetext')
        info_creations.donation_description = request.POST.get('redonationDescription')

        info_creations.donation_footer = request.POST.get('redonationFooter')
            # info_creation.welcome_header_type = request.POST.get('mySelect')
        if 'rengoLogo' in request.FILES and len(request.FILES['rengoLogo']) != 0:
            info_creations.ngo_logo = request.FILES['rengoLogo']
        else:
            info_creations.ngo_logo = info_creations.ngo_logo
        if 'resignature' in request.FILES and len(request.FILES['resignature']) != 0:
            info_creations.ngo_signature_image = request.FILES['resignature']
        else:
            info_creations.ngo_signature_image = info_creations.ngo_signature_image

        if 'recontactheaderimage' in request.FILES and len(request.FILES['recontactheaderimage']) != 0:
            info_creations.donation_contact_us_image  = request.FILES['recontactheaderimage']
        else:
            info_creations.donation_contact_us_image  = info_creations.donation_contact_us_image 
            
        info_creations.donation_now_button_name = request.POST.get(
                'redonationNowButtonName')
            
        info_creations.contact_us_details_button_name  = request.POST.get(
                'reContactNowButtonName')
        info_creations.my_donation_button_name = request.POST.get(
                'remyDonationButtonName')
        info_creations.donation_list_header = request.POST.get(
                'redonationListHeader')
            # info_creation.booking_header_type = request.POST.get('booktype')
        info_creations.donation_list_body = request.POST.get(
                'redonationListBody')
        info_creations.donation_list_footer = request.POST.get(
                'redonationListFooter')
        info_creations.donation_list_button_name = request.POST.get(
                'redonationListButtonName')
        info_creations.donation_conform_message = request.POST.get(
                'redonationConformMessage')
            # if 'reCancelImage' in request.FILES and len(request.FILES['reCancelImage']) != 0:
            #     info_creations.cancel_ticket_header_image = request.FILES['reCancelImage']
            # else:
            #     info_creations.cancel_ticket_header_image = info_creations.cancel_ticket_header_image
        info_creations.donation_failure_message = request.POST.get(
                'redonationFailureMessage')
            # if 'reConformationImage' in request.FILES and len(request.FILES['reConformationImage']) != 0:
            #     info_creations.ticket_conformation_header_image = request.FILES[
            #         'reConformationImage']
            # else:
            #     info_creations.ticket_conformation_header_image = info_creations.ticket_conformation_header_image
        info_creations.donation_contact_us_message = request.POST.get(
                'redonationContactUsMessage')
            # if 'refailureImage' in request.FILES and len(request.FILES['refailureImage']) != 0:
            #     info_creations.ticket_payment_failure_image = request.FILES['refailureImage']
            # else:
            #     info_creations.ticket_payment_failure_image = info_creations.ticket_payment_failure_image
        info_creations.contact_us_button_name = request.POST.get(
                'recontactUsButtonName')
            # if 'reUseImage' in request.FILES and len(request.FILES['reUseImage']) != 0:
            #     info_creations.use_header_image = request.FILES['reUseImage']
            # else:
            #     info_creations.use_header_image = info_creations.use_header_image
            # info_creations.use_message_text = request.POST.get(
            #     'reusemessagebody')
            # info_creations.use_button_name = request.POST.get(
            #     'reusebuttonname')
        info_creations.support_number = request.POST.get(
                'resupportNumber')
            # if 'renotavailableImage' in request.FILES and len(request.FILES['renotavailableImage']) != 0:
            #     info_creations.tickets_not_availble_header_image = request.FILES[
            #         'renotavailableImage']
            # else:
            #     info_creations.tickets_not_availble_header_image = info_creations.tickets_not_availble_header_image
        info_creations.ngo_name = request.POST.get(
                'rengoName')
            


            # if 'reContactImage' in request.FILES and len(request.FILES['reContactImage']) != 0:
            #     info_creations.contact_header_image = request.FILES[
            #         'reContactImage']
            # else:
            #     info_creations.contact_header_image = info_creations.contact_header_image

        info_creations.ngo_pan = request.POST.get(
                'rengoPan')
            
        info_creations.ngo_gstin = request.POST.get(
               'rengoGstin')

        info_creations.ngo_header_notes = request.POST.get(
               'rengoHeaderNotes')
            
        info_creations.ngo_footer_notes = request.POST.get(
                    'rengoFooterNotes')
            
        info_creations.ngo_signature_header = request.POST.get(
                 'rengoSignatureHeader')
            
        info_creations.ngo_signature_footer = request.POST.get(
                   'rengoSignatureFooter')
            
        info_creations.invoice_footer = request.POST.get(
                 'reinvoiceFooter')
       
        info_creations.ngo_link_text = request.POST.get(
                   'rengo_link_text')
            
        info_creations.ngo_url = request.POST.get(
                 'rengo_url')
            
            
        info_creations.my_donation_details_button_name1  = request.POST.get(
                 'redonationDetailsButton1')
            
        info_creations.my_donation_details_button_name2  = request.POST.get(
                   'redonationDetailsButton2')
            
        info_creations.my_donation_details_button_name3  = request.POST.get(
                 'redonationDetailsButton3')
            
            # info_creations.ticketcount6_desc = request.POST.get(
            #         'reticketcount6_desc')
            # info_creations.ticketcount7_desc = request.POST.get(
            #      'reticketcount7_desc')
            # info_creations.ticketcount8_desc = request.POST.get(
            #      'reticketcount8_desc')
            # info_creations.ticketcount9_desc = request.POST.get(
            #      'reticketcount9_desc')
            # info_creations.second_number = int(
            #     request.POST.get('reticketsecondnumber'))
        print("Info Creations ID:", info_creations.id)
        print("Existing Donation Description:", info_creations.donation_description)    
        info_creations.client_id = request.user.id
        info_creations.save()
        
        print("saving")
        print("Data saved successfully with marketplace id", marketplace_id)

        if marketplace_id is not None:
            return redirect(reverse('donationInfo', kwargs={'id': marketplace_id}))
        else:
            return redirect('donationInfo1')


# def donationMaster(request):
#     client_id = request.user.id
#     donationMaster = donation_types.objects.filter(client_id=client_id)
#     admin_permission_obj = admin_permission.objects.filter(client_id=client_id).first()

#     marketplace_id = request.GET.get('marketplace_id')
    
#     if marketplace_id:
#         # If marketplace ID is provided, filter by both client and marketplace IDs
#         filtered_donationMaster = donation_types.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
#     else:
#         # If no marketplace ID is provided, filter only by client ID
#         filtered_donationMaster = donation_types.objects.filter(client_id=client_id)

#     return render(request, 'N_donation/donationMaster.html', {'donationMaster': filtered_donationMaster, 'admin_permission_obj': admin_permission_obj})
# views.py

def donationMaster(request):
    client_id = request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=client_id).first()
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    # admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    addNgoMarketPlace = donation_marketplace.objects.filter(client=request.user.id)

    # Retrieve marketplace_id from the query parameters
    marketplace_id = request.GET.get('marketplace_id')

    if marketplace_id:
        # If marketplace ID is provided, filter by both client and marketplace IDs
        filtered_donationMaster = donation_types.objects.filter(client_id=client_id, marketplace_id=marketplace_id)
    else:
        # If no marketplace ID is provided, filter only by client ID
        filtered_donationMaster = donation_types.objects.filter(client_id=client_id)
    context = {
        'donationMaster': filtered_donationMaster,
        'admin_permission_obj': admin_permission_obj, 
        'marketplace_id': marketplace_id, 
        'subclient_preferences':subclient_preferences,
        'addNgoMarketPlace':addNgoMarketPlace,
        
        }
    return render(request, 'N_donation/donationMaster.html', context)


def addDonation(request):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print("addDonation mk id", marketplace_id)
    admin_permission_obj = admin_permission.objects.filter(client_id=client_id).first()
    return render(request, 'N_donation/addDonation.html', {'marketplace_id': marketplace_id, 'admin_permission_obj': admin_permission_obj})


def submitDonation(request):
    # Retrieve marketplace_id from the form action
    marketplace_id = request.GET.get('marketplace_id')
    print('submitDonation_marketplace_id', marketplace_id)

    if request.method == "POST":
        # Create a new donation_types instance
        submitDonation = donation_types()

        # Populate fields with form data
        submitDonation.donation_name = request.POST.get('donationName')
        submitDonation.donation_short_description = request.POST.get('donationShortDescription')
        submitDonation.donation_amount = request.POST.get('donationAmount')
        submitDonation.donation_description = request.POST.get('donationDescription')
        submitDonation.donation_type_image = request.FILES['donationTypeImage']
        submitDonation.client_id = request.user.id

        # Save marketplace_id before saving the object
        if marketplace_id:
            submitDonation.marketplace_id = marketplace_id

        # Save the object
        submitDonation.save()

        # Redirect based on the presence of marketplace_id
        if marketplace_id:
            return redirect(reverse('donationMaster') + f'?marketplace_id={marketplace_id}')
        else:
            return redirect('donationMaster')

    return render(request, 'N_donation/addDonation.html')


def editDontion(request, id):
    client_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    print('editDontion_marketplace_id', marketplace_id)
 
    modifyDonation = donation_types.objects.filter(client_id=client_id, id=id)

    

    return render(request, 'N_donation/editDonation.html',
                  {'modifyDonation': modifyDonation, 'eventId': id, 'marketplace_id':marketplace_id})

def updateDonation(request, id):
    originalDonation = donation_types.objects.filter(client_id=request.user.id, id=id)
    # marketplace_id = request.POST.get('marketplace_id')
    marketplace_id = request.GET.get('marketplace_id')
    print('updateDonation_marketplace_id', marketplace_id)
    
    if request.method == 'POST':
        for i in originalDonation:
            updatedDonation = donation_types.objects.filter(client_id=request.user.id, id=id)
            if request.method == 'POST':
                for j in updatedDonation:
                    updateDonationEdit = donation_types.objects.get(id=j.id)
                    updateDonationEdit.donation_name = request.POST.get('reDonationName')
                    updateDonationEdit.donation_short_description = request.POST.get('reDonationShortdesc')
                    updateDonationEdit.donation_amount = request.POST.get('redonationAmount')
                    updateDonationEdit.donation_description = request.POST.get('redonationDescription')

                    if 'reDonationTypeImage' in request.FILES and len(request.FILES['reDonationTypeImage']) != 0:
                        updateDonationEdit.donation_type_image = request.FILES['reDonationTypeImage']
                    else:
                        updateDonationEdit.donation_type_image = i.donation_type_image

                    updateDonationEdit.save()

                    print(f"Update successful for donation ID {updateDonationEdit.id}")

                    print(f"Redirecting to donationMaster with marketplace_id={marketplace_id}")
                    if marketplace_id:
                        return redirect(reverse('donationMaster') + f'?marketplace_id={marketplace_id}')
                    else:
                        return redirect('donationMaster')

    print(f"Rendering donationMaster.html with originalDonation={originalDonation}")
    return render(request, 'N_donation/donationMaster.html', {'modifyDonation': originalDonation})

def viewDetail1(request,id):
    viewDetail = ticket_billing_details.objects.filter(client_id=request.user.id,ticket_billing_id=id)

    return render(request, 'N_donation/viewDetail1.html', {'viewDetail': viewDetail, 'id':id})


def deleteDontion(request, id):
    deleteDontion = donation_types.objects.get(client_id=request.user.id, pk=id)
    deleteDontion.delete()
    return redirect('donationMaster')

from plotly.offline import plot
import plotly.graph_objs as go
import datetime
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import plotly.express as px     
# from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth

# def doantiondashboard(request):
#     data = donation_details.objects.annotate(month=TruncMonth('donation_date')).values('month').annotate(total_amount=Sum('donation_amount'))
#     data = [entry for entry in data if entry['total_amount'] > 0]
#     donation_months = [entry['month'] for entry in data]
#     monthly_data = {month: {'total_amount': 0} for month in donation_months}

#     for entry in data:
#         month = entry['month']
#         total_amount = entry['total_amount']
#         monthly_data[month]['total_amount'] = total_amount

#     if not donation_months:
#         return render(request, 'N_donation/doantiondashboard.html')
#     chart_data = {
#         'months': [month.strftime('%Y-%m') for month in donation_months],
#         'total_amounts': [monthly_data[month]['total_amount'] for month in donation_months]
#     }

#     fig = px.bar(x=chart_data['months'], y=chart_data['total_amounts'], labels={'x': 'Month', 'y': 'Total Donation Amount'})
#     chart_div = fig.to_html(full_html=False, default_height=500)

#     return render(request, 'N_donation/donationDashboard.html', {'chart_div': chart_div})

#28--8
def doantiondashboard(request):
    user_id = request.user.id
    data = donation_details.objects.filter(client_id=user_id).annotate(month=TruncMonth('donation_date')).values('month').annotate(total_amount=Sum('donation_amount'))
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    data = [entry for entry in data if entry['total_amount'] is not None and entry['total_amount'] > 0]
    
    if not data:
        return render(request, 'N_donation/donationDashboard.html')
    
    donation_months = [entry['month'] for entry in data]
    monthly_data = {month: {'total_amount': 0} for month in donation_months}

    for entry in data:
        month = entry['month']
        total_amount = entry['total_amount']
        monthly_data[month]['total_amount'] = total_amount

    if not donation_months:
        return render(request, 'N_donation/donationDashboard.html')
    chart_data = {
        'months': [month.strftime('%Y-%m') for month in donation_months],
        'total_amounts': [monthly_data[month]['total_amount'] for month in donation_months]
    }

    fig = px.bar(x=chart_data['months'], y=chart_data['total_amounts'], labels={'x': 'Month', 'y': 'Total Donation Amount'})
    chart_div = fig.to_html(full_html=False, default_height=500)

    return render(request, 'N_donation/donationDashboard.html', {'chart_div': chart_div, 'admin_permission_obj':admin_permission_obj})

    
# def addNgoMarketPlace(request):

#     subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
#     subclient = Subclient.objects.filter(id=subclient_id).first()
#     subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
#     addNgoMarketPlace = donation_marketplace.objects.filter(client=request.user.id)
    

#     context = {
#         'addNgoMarketPlace': addNgoMarketPlace, 
#         'subclient_preferences': subclient_preferences,
#         'admin_permission_obj':admin_permission_obj,
#     }

#     return render(request, 'N_donation/addNgoMarketPlace.html',context )


def addNgoMarketPlace(request):
    # Clear the 'marketplace_id' key from the session
    request.session.pop('marketplace_id', None)
    request.session.save()
    print('Cleared entire session')

    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    addNgoMarketPlace = donation_marketplace.objects.filter(client=request.user.id)
    
    context = {
        'addNgoMarketPlace': addNgoMarketPlace, 
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,
    }

    return render(request, 'N_donation/addNgoMarketPlace.html', context)

def addNgoForm(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    addNgoMarketPlace = donation_marketplace.objects.filter(client=request.user.id)
    
    context = {
        'addNgoMarketPlace': addNgoMarketPlace, 
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,
    }
    return render(request, 'N_donation/addNgoFormMarketPlace.html',context)

# def mkSetting(request):
#     subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
#     subclient = Subclient.objects.filter(id=subclient_id).first()
#     subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
#     # addNgoMarketPlace = donation_marketplace.objects.filter(client=request.user.id)
    
#     context = {
#         'addNgoMarketPlace': addNgoMarketPlace, 
#         'subclient_preferences': subclient_preferences,
#         'admin_permission_obj': admin_permission_obj,
#     }
#     return render(request, 'N_donation/mkSetting.html',context)

# def mkSetting(request):
#     subclient_id = request.session.get('subclient_id')
#     subclient = Subclient.objects.filter(id=subclient_id).first()
#     subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

#     # Load existing data (if any) to pre-fill the form
#     existing_data = donation_marketplace_settings.objects.filter(client=request.user).first()

#     if request.method == 'POST':
#         # Handle form submission
#         generic_flow_id = request.POST.get('generic_flow_id')
#         specific_flow_id = request.POST.get('specific_flow_id')
#         my_donation_flow_id = request.POST.get('my_donation_flow_id')
#         marketplace_welcome_message_body = request.POST.get('marketplace_welcome_message_body')
#         marketplace_welcome_message_footer = request.POST.get('marketplace_welcome_message_footer')
#         generic_flow_cta_name = request.POST.get('generic_flow_cta_name')
#         specific_flow_cta_name = request.POST.get('specific_flow_cta_name')
#         mydonation_flow_cta_name = request.POST.get('mydonation_flow_cta_name')
#         marketplace_welcome_image = request.POST.get('marketplace_welcome_image')
        

#         # Update or create the model instance
#         if existing_data:
#             existing_data.generic_flow_id = generic_flow_id
#             existing_data.specific_flow_id = specific_flow_id
#             existing_data.my_donation_flow_id = my_donation_flow_id
#             existing_data.marketplace_welcome_message_body = marketplace_welcome_message_body
#             existing_data.marketplace_welcome_message_footer = marketplace_welcome_message_footer
#             existing_data.generic_flow_cta_name = generic_flow_cta_name
#             existing_data.specific_flow_cta_name = specific_flow_cta_name
#             existing_data.mydonation_flow_cta_name = mydonation_flow_cta_name
#             existing_data.marketplace_welcome_image = marketplace_welcome_image
#             # existing_data.marketplace_welcome_message_body = marketplace_welcome_message_body
#             # Update other fields as needed
#             existing_data.save()
#         else:
#             new_data = donation_marketplace_settings(
#                 client=request.user,
#                 generic_flow_id=generic_flow_id,
#                 specific_flow_id=specific_flow_id,
#                 my_donation_flow_id=my_donation_flow_id,
#                 marketplace_welcome_message_body=marketplace_welcome_message_body,
#                 marketplace_welcome_message_footer=marketplace_welcome_message_footer,
#                 generic_flow_cta_name=generic_flow_cta_name,
#                 specific_flow_cta_name=specific_flow_cta_name,
#                 mydonation_flow_cta_name=mydonation_flow_cta_name,
#                 marketplace_welcome_image=marketplace_welcome_image,
#                 client_id = request.user.id

                                
#                                                 # Add other fields as needed
#             )
#             new_data.save()

#         return redirect('mkSetting')

#     context = {
#         'existing_data': existing_data,
#         'subclient_preferences': subclient_preferences,
#         'admin_permission_obj': admin_permission_obj,
#     }
#     return render(request, 'N_donation/mkSetting.html', context)

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def mkSetting(request):
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    # Load existing data (if any) to pre-fill the form
    existing_data = donation_marketplace_settings.objects.filter(client=request.user).first()

    if request.method == 'POST':
        # Handle form submission
        generic_flow_id = request.POST.get('generic_flow_id')
        specific_flow_id = request.POST.get('specific_flow_id')
        my_donation_flow_id = request.POST.get('my_donation_flow_id')
        marketplace_welcome_message_body = request.POST.get('marketplace_welcome_message_body')
        marketplace_welcome_message_footer = request.POST.get('marketplace_welcome_message_footer')
        generic_flow_cta_name = request.POST.get('generic_flow_cta_name')
        specific_flow_cta_name = request.POST.get('specific_flow_cta_name')
        mydonation_flow_cta_name = request.POST.get('mydonation_flow_cta_name')
        marketplace_welcome_image = request.FILES.get('marketplace_welcome_image')

        # Update or create the model instance
        if existing_data:
            existing_data.generic_flow_id = generic_flow_id
            existing_data.specific_flow_id = specific_flow_id
            existing_data.my_donation_flow_id = my_donation_flow_id
            existing_data.marketplace_welcome_message_body = marketplace_welcome_message_body
            existing_data.marketplace_welcome_message_footer = marketplace_welcome_message_footer
            existing_data.generic_flow_cta_name = generic_flow_cta_name
            existing_data.specific_flow_cta_name = specific_flow_cta_name
            existing_data.mydonation_flow_cta_name = mydonation_flow_cta_name

            # Check if a new image is provided
            # if marketplace_welcome_image:
            #     # Delete old image if it exists
            #     if existing_data.marketplace_welcome_image:
            #         default_storage.delete(existing_data.marketplace_welcome_image.path)
                
            #     # Save the new image and update the model field
            #     file_name = f"FlowImage/{marketplace_welcome_image.name}"
            #     file_path = default_storage.save(file_name, ContentFile(marketplace_welcome_image.read()))
            #     existing_data.marketplace_welcome_image.name = file_path

            # existing_data.save()
            if 'marketplace_welcome_image' in request.FILES and len(request.FILES['marketplace_welcome_image']) != 0:
                existing_data.marketplace_welcome_image = request.FILES['marketplace_welcome_image']
            else:
                existing_data.marketplace_welcome_image = existing_data.marketplace_welcome_image

            existing_data.save()
        else:
            new_data = donation_marketplace_settings(
                client=request.user,
                generic_flow_id=generic_flow_id,
                specific_flow_id=specific_flow_id,
                my_donation_flow_id=my_donation_flow_id,
                marketplace_welcome_message_body=marketplace_welcome_message_body,
                marketplace_welcome_message_footer=marketplace_welcome_message_footer,
                generic_flow_cta_name=generic_flow_cta_name,
                specific_flow_cta_name=specific_flow_cta_name,
                mydonation_flow_cta_name=mydonation_flow_cta_name,
                marketplace_welcome_image=marketplace_welcome_image,
                client_id=request.user.id
            )
            new_data.save()

        return redirect('mkSetting')

    context = {
        'existing_data': existing_data,
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,
    }
    return render(request, 'N_donation/mkSetting.html', context)

def submitNgo(request):
    if request.method == "POST":
        submitNgo = donation_marketplace()
        submitNgo.ngo_name = request.POST.get('ngoName')
        submitNgo.ngo_type = request.POST.get('ngoType')
        submitNgo.ngo_category = request.POST.get('ngoCategory')
        # submitDonation.Event_Message_Header = request.POST.get('eventmessageheader')
        #  submitDonation.Event_Body = request.POST.get('eventbody')
        # submitDonation.Event_Footer = request.POST.get('eventfooter')
        submitNgo.ngo_location = request.POST.get('ngoLocation')
        # submitDonation.Event_Logo = request.FILES['Eventlogo']
        # submitDonation.Event_ticket_image = request.FILES['Eventticketimg']
        submitNgo.ngo_description =request.POST.get('ngoDescription')
        submitNgo.ngo_link_text =request.POST.get('ngo_link_text')
        submitNgo.ngo_url =request.POST.get('ngo_url')
        submitNgo.ngo_id =request.POST.get('ngo_id')
        submitNgo.key =request.POST.get('key')
        submitNgo.ngo_contact_number = request.POST.get('ngoContactNumber')
        # submitDonation.Event_Message_Header_Text = request.POST.get(
        #     'eventheadertext')
        # submitDonation.Event_Message_Body_Text = request.POST.get(
        #     'eventbodytext')
        # submitDonation.Event_Message_Footer_Text = request.POST.get(
        #     'eventfootertext')
        # submitDonation.Event_slots_button_name = request.POST.get(
        #     'eventslotbuttonname')
        submitNgo.client_id = request.user.id

        # Get the selected status value from the form
        # status_value = int(request.POST.get('status', 1))
        # submitDonation.status = status_value
        submitNgo.save()
        return redirect("addNgoMarketPlace")
    return render(request, 'N_donation/addNgoFormMarketPlace.html')


def deleteNgoMarketPlace(request, id):
    deleteNgo = donation_marketplace.objects.get(client_id=request.user.id, pk=id)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    deleteNgo.delete()
    return redirect('addNgoMarketPlace')

def editNgoMarketPlace(request, id):
    client_id = request.user.id
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

 
    modifyNgo = donation_marketplace.objects.filter(client_id=client_id, id=id)

    

    return render(request, 'N_donation/editNgoMarketPlace.html',
                  {'modifyNgo': modifyNgo, 'eventId': id, 'admin_permission_obj':admin_permission_obj})


def updateNgoMarketPlace(request, id):
    updateNgo = donation_marketplace.objects.filter(client_id=request.user.id, id=id)
    if request.method == 'POST':
        for i in updateNgo:
            updateNgo = donation_marketplace.objects.filter(
                client_id=request.user.id, id=id)
            admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
           
            if request.method == 'POST':
                for i in updateNgo:
                    updateNgoEdit = donation_marketplace.objects.get(id=i.id)
                    updateNgoEdit.ngo_name = request.POST.get(
                        'reNgpnName')
                    updateNgoEdit.ngo_type = request.POST.get(
                        'reNgoType')
                    updateNgoEdit.ngo_category = request.POST.get(
                        'reNgoCategory')
                    updateNgoEdit.ngo_location = request.POST.get(
                        'reNgoLocation')
                    updateNgoEdit.ngo_description = request.POST.get(
                        'reNgodesc')
                    updateNgoEdit.ngo_link_text = request.POST.get(
                        'rengo_link_text')
                    updateNgoEdit.ngo_url = request.POST.get(
                        'rengo_url')
                    updateNgoEdit.ngo_id = request.POST.get(
                        'rengo_id')
                    updateNgoEdit.key = request.POST.get(
                        'rekey')
                    updateNgoEdit.ngo_contact_number = request.POST.get(
                        'reNgoContactNumber')
           
                    updateNgoEdit.save()
                return redirect('addNgoMarketPlace')
            return render(request, 'N_donation/addNgoMarketPlace.html', {'modifyDonation': updateNgo, "admin_permission_obj":admin_permission_obj})



# from bs4 import BeautifulSoup
# from django.shortcuts import render
# import requests

# def get_opengraph_image(url):
#     try:
#         # Fetch the HTML content of the website
#         response = requests.get(url)
#         response.raise_for_status()

#         # Parse the HTML content using BeautifulSoup
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Find the Open Graph image meta tag
#         og_image_tag = soup.find('meta', {'property': 'og:image'})

#         # Extract the content attribute from the meta tag
#         og_image_url = og_image_tag.get('content') if og_image_tag else None

#         return og_image_url

#     except Exception as e:
#         # Handle any errors gracefully
#         print(f"Error fetching Open Graph image: {e}")
#         return None



def GenerateId(request,id):

    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()


    facebookNu = facebook_details.objects.filter(client_id=request.user.id)
    idDonationplace = donation_marketplace.objects.filter(client_id=request.user.id,id=id )
    fb_whatsapp_number = facebookNu.first().fb_whatsapp_number if facebookNu.exists() else None
    ngoId = idDonationplace.first().ngo_id if idDonationplace.exists() else None
    ngoText = idDonationplace.first().ngo_link_text if idDonationplace.exists() else None
    ngoUrl = idDonationplace.first().ngo_url if idDonationplace.exists() else None
    
   
    
    context = {
        "facebook": facebookNu,
        "donationplace": idDonationplace,
        'fb_whatsapp_number':fb_whatsapp_number,
        'ngoId':ngoId,
        'ngoText':ngoText,
        'ngoUrl':ngoUrl,
        
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,

    }
    
    return render(request, 'N_donation/GenerateId.html', context)

def GenerateLink(request,id):

    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    marketplace_id = id
    user_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    donationG = donation_settings.objects.filter(client_id=user_id, marketplace_id=marketplace_id)


    facebookNu = facebook_details.objects.filter(client_id=request.user.id)
    # idDonationplace = donation_marketplace.objects.filter(client_id=request.user.id,id=id )
    fb_whatsapp_number = facebookNu.first().fb_whatsapp_number if facebookNu.exists() else None
    ngoText = donationG.first().ngo_link_text if donationG.exists() else None
    ngoUrl = donationG.first().ngo_url if donationG.exists() else None
    
   
    
    context = {
        "facebook": facebookNu,
        "donationG": donationG,
        'fb_whatsapp_number':fb_whatsapp_number,
        
        'ngoText':ngoText,
        'ngoUrl':ngoUrl,
        
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,

    }
    
    return render(request, 'N_donation/GenerateLink.html', context)

def GenerateBarLink(request,id):

    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    marketplace_id = id
    user_id = request.user.id
    marketplace_id = request.GET.get('marketplace_id')
    donationG = donation_settings.objects.filter(client_id=user_id, marketplace_id=marketplace_id)


    facebookNu = facebook_details.objects.filter(client_id=request.user.id)
    # idDonationplace = donation_marketplace.objects.filter(client_id=request.user.id,id=id )
    fb_whatsapp_number = facebookNu.first().fb_whatsapp_number if facebookNu.exists() else None
    ngoText = donationG.first().ngo_link_text if donationG.exists() else None
    ngoUrl = donationG.first().ngo_url if donationG.exists() else None
    
   
    
    context = {
        "facebook": facebookNu,
        "donationG": donationG,
        'fb_whatsapp_number':fb_whatsapp_number,
        
        'ngoText':ngoText,
        'ngoUrl':ngoUrl,
        
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,

    }
    
    return render(request, 'N_donation/generateBarLink.html', context)


def GenerateIdBar(request,id):

    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()


    facebookNu = facebook_details.objects.filter(client_id=request.user.id)
    idDonationplace = donation_marketplace.objects.filter(client_id=request.user.id,id=id )
    fb_whatsapp_number = facebookNu.first().fb_whatsapp_number if facebookNu.exists() else None
    ngoId = idDonationplace.first().ngo_id if idDonationplace.exists() else None
    ngoText = idDonationplace.first().ngo_link_text if idDonationplace.exists() else None
    ngoUrl = idDonationplace.first().ngo_url if idDonationplace.exists() else None

    context = {
        "facebook": facebookNu,
        "donationplace": idDonationplace,
        'fb_whatsapp_number':fb_whatsapp_number,
        'ngoId':ngoId,
        'ngoText':ngoText,
        'ngoUrl':ngoUrl,
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,

    }
    
    return render(request, 'N_donation/GenerateIdBar.html', context)

def Generatekey(request,id):

    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()


    facebookNu = facebook_details.objects.filter(client_id=request.user.id)
    keyDonationplace = donation_marketplace.objects.filter(client_id=request.user.id,id=id )
    fb_whatsapp_number = facebookNu.first().fb_whatsapp_number if facebookNu.exists() else None
    ngokey = keyDonationplace.first().key if keyDonationplace.exists() else None
    ngoText = keyDonationplace.first().ngo_link_text if keyDonationplace.exists() else None
    ngoUrl = keyDonationplace.first().ngo_url if keyDonationplace.exists() else None

    
    context = {
        "facebook": facebookNu,
        "keyDonationplace": keyDonationplace,
        'fb_whatsapp_number':fb_whatsapp_number,
        'ngokey':ngokey,
        'ngoText':ngoText,
        'ngoUrl':ngoUrl,
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,
        

    }
    
    return render(request, 'N_donation/generateKey.html', context)

def generateKeyBarcode(request,id):
    
    subclient_id = request.session.get('subclient_id')
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()


    
    facebookNu = facebook_details.objects.filter(client_id=request.user.id)
    keyDonationplace = donation_marketplace.objects.filter(client_id=request.user.id,id=id )
    fb_whatsapp_number = facebookNu.first().fb_whatsapp_number if facebookNu.exists() else None
    ngokey = keyDonationplace.first().key if keyDonationplace.exists() else None
    ngoText = keyDonationplace.first().ngo_link_text if keyDonationplace.exists() else None
    ngoUrl = keyDonationplace.first().ngo_url if keyDonationplace.exists() else None
    
    
    context = {
        "facebook": facebookNu,
        "keyDonationplace": keyDonationplace,
        'fb_whatsapp_number':fb_whatsapp_number,
        'ngokey':ngokey,
        'ngoText':ngoText,
        'ngoUrl':ngoUrl,
        'subclient_preferences': subclient_preferences,
        'admin_permission_obj': admin_permission_obj,

    }
    
    return render(request, 'N_donation/generateKeyBarcode.html', context)


def genericflow(request):
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
    market_settingsObj = donation_marketplace_settings.objects.filter(client_id=request.user.id)
    for m_i in market_settingsObj:
        random_number = random.randint(1, 1000)
        print("fffff")
        base_name = 'tenth_flow'
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
            donation_obj = donation_marketplace_settings.objects.filter(client_id=request.user.id)
            for d_i in donation_obj:
                d_i.generic_flow_id = id_value
                d_i.save()
                print("successfully saved the flow id")
                type_obj = donation_ngo_type.objects.filter(client_id=request.user.id)
                ngo_Type = []
                for r_i in type_obj:
                    ngo_Type.append(r_i.donation_ngo_type)
                list_ngo_type=[]
                for h_i in range(len(ngo_Type)):
                    list_ngo_type.append({"id": ngo_Type[h_i] ,
                                         "title": ngo_Type[h_i]
                                         })
                category_obj = donation_ngo_category.objects.filter(client_id=request.user.id)
                category_Type = []
                for c_i in category_obj:
                    category_Type.append(c_i.donation_ngo_category)

                list_category_type = []
                for j in range(len(category_Type)):
                    list_category_type.append({
                        "id":category_Type[j],
                        "title":category_Type[j]
                    })
                data = {
                    "version": "2.1",
                    "data_api_version":"3.0",
                    "data_channel_uri":"https://vmart.ai/testdata",
                    "routing_model": {
                        "DETAILS": [
                            "NGO_DATA"
                        ],
                        "NGO_DATA": [
                            "DONATION_TYPES"
                        ],
                        "DONATION_TYPES": [
                            "SUBMIT_DETAILS_DATA",
                            "DONATION_DETAILS"
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
                                                "label": "Name",
                                                "input-type": "text",
                                                "name": "name",
                                                "required": False
                                            },
                                            {
                                                "type": "Dropdown",
                                                "label": "Type",
                                                "required": False,
                                                "name": "ngo_type",
                                                "data-source": list_ngo_type
                                            },
                                            {
                                                "type": "Dropdown",
                                                "label": "Category",
                                                "required": False,
                                                "name": "ngo_category",
                                                "data-source": list_category_type
                                            },
                                            {
                                                "type": "TextInput",
                                                "label": "Location",
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
                                                        "ngo_Name": "${form.name}",
                                                        "ngo_type": "${form.ngo_type}",
                                                        "ngo_category": "${form.ngo_category}",
                                                        "ngo_location": "${form.location}"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "id": "NGO_DATA",
                            "title": "NGO_DATA",
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
                            "id": "DONATION_TYPES",
                            "title": "DONATION_TYPES",
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
                            "id": "SUBMIT_DETAILS_DATA",
                            "title": "SUBMIT_DETAILS_DATA",
                            "terminal": True,
                            "data": {
                                "excess": {
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
                                        {
                                            "id": "1",
                                            "title": "$250"
                                        }


                                    ]
                                },
                                "total": {
                                    "type": "string",
                                    "__example__": "$47.98 per month"
                                }
                            },
                            "layout": {
                                "type": "SingleColumnLayout",
                                "children": [
                                    {
                                        "type": "Form",
                                        "name": "form",
                                        "init-values": {
                                            "name": "",
                                            "Email":"",
                                            "comments":""
                                        },
                                        "children": [

                                            {
                                                "type": "TextInput",
                                                "label": "name",
                                                "input-type": "text",
                                                "name": "name",
                                                "required": True
                                            },
                                            {
                                                "type": "TextInput",
                                                "label": "Email",
                                                "input-type": "text",
                                                "name": "Email",
                                                "required": False
                                            },


                                            {
                                                "type": "TextHeading",
                                                "text": "${data.total}"
                                            },
                                            {
                                                "type": "TextInput",
                                                "label": "comments",
                                                "input-type": "text",
                                                "name": "comments",
                                                "required": False
                                            },

                                            {
                                                "type": "Footer",
                                                "label": "Conform",
                                                "on-click-action": {
                                                    "name": "complete",
                                                    "payload": {
                                                        "amount":"${data.total}",
                                                        "comments":"${form.comments}",
                                                        "name":"${form.name}",
                                                        "email":"${form.Email}",
                                                        "excess":"${data.excess}"

                                                    }
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                         {
                            "id": "DONATION_DETAILS",
                            "title": "donation details",
                            "terminal": True,
                            "data": {
                                "excess": {
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
                                        {
                                            "id": "1",
                                            "title": "$250"
                                        }


                                    ]
                                }

                            },
                            "layout": {
                                "type": "SingleColumnLayout",
                                "children": [
                                    {
                                        "type": "Form",
                                        "name": "details_form",
                                        "children": [
                                            {
                                                "type": "TextInput",
                                                "label": "Name",
                                                "input-type": "text",
                                                "name": "name",
                                                "required": True
                                            },
                                            {
                                                "type": "TextInput",
                                                "label": "Email",
                                                "input-type": "text",
                                                "name": "email",
                                                "required": False
                                            },
                                            {
                                                "type": "TextInput",
                                                "label": "amount",
                                                "input-type": "text",
                                                "name": "amount",
                                                "required": True
                                            },
                                            {
                                                "type": "TextInput",
                                                "label": "comments",
                                                "input-type": "text",
                                                "name": "comments",
                                                "required": False
                                            },
                                            {
                                                "type": "Footer",
                                                "label": "complete",
                                                "on-click-action": {
                                                    "name": "complete",
                                                    "payload": {
                                                        "donar_Name": "${form.name}",
                                                        "donar_Email": "${form.email}",
                                                        "donar_Amount": "${form.amount}",
                                                        "donar_Comments": "${form.comments}",
                                                        "excess_id":"${data.excess}"
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

    return HttpResponse("Please wait")


def specificflow(request):
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
    market_settingsObj = donation_marketplace_settings.objects.filter(client_id=request.user.id)
    for m_i in market_settingsObj:
        random_number = random.randint(1, 1000)
        print("fffff")
        base_name = 'tenth_flow'
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
            donation_obj = donation_marketplace_settings.objects.filter(client_id=request.user.id)
            for d_i in donation_obj:
                d_i.specific_flow_id = id_value
                d_i.save()
                print("successfully saved the flow id")
                data = {
                    "version": "2.1",
                    "data_api_version":"3.0",
                    "data_channel_uri":"https://vmart.ai/specificdata",
                    "routing_model": {
                        "DONATION_TYPES": [
                            "SUBMIT_DETAILS_DATA",
                            "DONATION_DETAILS"
                        ]


                    },
                    "screens": [
                        {
                            "id": "DONATION_TYPES",
                            "title": "DONATION_TYPES",
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
                            "id": "SUBMIT_DETAILS_DATA",
                            "title": "SUBMIT_DETAILS_DATA",
                            "terminal": True,
                            "data": {
                                "excess": {
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
                                        {
                                            "id": "1",
                                            "title": "$250"
                                        }


                                    ]
                                },
                                "total": {
                                    "type": "string",
                                    "__example__": "$47.98 per month"
                                }
                            },
                            "layout": {
                                "type": "SingleColumnLayout",
                                "children": [
                                    {
                                        "type": "Form",
                                        "name": "form",
                                        "init-values": {
                                            "name": "",
                                            "Email":"",
                                            "comments":""
                                        },
                                        "children": [

                                            {
                                                "type": "TextInput",
                                                "label": "name",
                                                "input-type": "text",
                                                "name": "name",
                                                "required": True
                                            },
                                            {
                                                "type": "TextInput",
                                                "label": "Email",
                                                "input-type": "text",
                                                "name": "Email",
                                                "required": False
                                            },


                                            {
                                                "type": "TextHeading",
                                                "text": "${data.total}"
                                            },
                                            {
                                                "type": "TextInput",
                                                "label": "comments",
                                                "input-type": "text",
                                                "name": "comments",
                                                "required": False
                                            },

                                            {
                                                "type": "Footer",
                                                "label": "Conform",
                                                "on-click-action": {
                                                    "name": "complete",
                                                    "payload": {
                                                        "amount":"${data.total}",
                                                        "comments":"${form.comments}",
                                                        "name":"${form.name}",
                                                        "email":"${form.Email}",
                                                        "excess":"${data.excess}"

                                                    }
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                         {
                            "id": "DONATION_DETAILS",
                            "title": "donation details",
                            "terminal": True,
                            "data": {
                                "excess": {
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
                                        {
                                            "id": "1",
                                            "title": "$250"
                                        }


                                    ]
                                }

                            },
                            "layout": {
                                "type": "SingleColumnLayout",
                                "children": [
                                    {
                                        "type": "Form",
                                        "name": "details_form",
                                        "children": [
                                            {
                                                "type": "TextInput",
                                                "label": "Name",
                                                "input-type": "text",
                                                "name": "name",
                                                "required": True
                                            },
                                            {
                                                "type": "TextInput",
                                                "label": "Email",
                                                "input-type": "text",
                                                "name": "email",
                                                "required": False
                                            },
                                            {
                                                "type": "TextInput",
                                                "label": "amount",
                                                "input-type": "text",
                                                "name": "amount",
                                                "required": True
                                            },
                                            {
                                                "type": "TextInput",
                                                "label": "comments",
                                                "input-type": "text",
                                                "name": "comments",
                                                "required": False
                                            },
                                            {
                                                "type": "Footer",
                                                "label": "complete",
                                                "on-click-action": {
                                                    "name": "complete",
                                                    "payload": {
                                                        "donar_Name": "${form.name}",
                                                        "donar_Email": "${form.email}",
                                                        "donar_Amount": "${form.amount}",
                                                        "donar_Comments": "${form.comments}",
                                                        "excess_id":"${data.excess}"
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


    return HttpResponse("Please wait")


def mydonationflow(request):
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
    market_settingsObj = donation_marketplace_settings.objects.filter(client_id=request.user.id)
    for m_i in market_settingsObj:
        random_number = random.randint(1, 1000)
        print("fffff")
        base_name = 'tenth_flow'
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
            donation_obj = donation_marketplace_settings.objects.filter(client_id=request.user.id)
            for d_i in donation_obj:
                d_i.my_donation_flow_id = id_value
                d_i.save()
                print("successfully saved the flow id")
                data = {
                    "version": "2.1",
                    "data_api_version":"3.0",
                    "data_channel_uri":"https://vmart.ai/mydonationdata",
                    "routing_model": {
                        "MYDONATION_DETAILS": [

                        ]



                    },
                    "screens": [
                        {
                            "id": "MYDONATION_DETAILS",
                            "title": "MYDONATION_DETAILS",
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

    return HttpResponse("Please wait")