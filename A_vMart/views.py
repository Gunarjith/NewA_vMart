
from django.contrib.auth import authenticate, login, logout

from django import template
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from vailodb.models import admin_permission, Subclient, SubUserPreference, vailo_leads, facebook_details, \
    ticket_billing, ticket_billing_details, ticket_information,event_master, SUBCLIENT_CHOICE

from .forms import CreateUserForm, MyPasswordChangeForm
from django.db.models import Sum

from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import secrets
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView




from django.core.mail import EmailMessage
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from A_vMart import settings
from django.contrib.auth.models import User
from .forms import CreateUserForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
# import cv2
# import numpy as np
#
# from pyzbar.pyzbar import decode
# import threading
import time
import threading
import json
from datetime import datetime, date
from datetime import datetime
import pytz



format = "%Y-%m-%d %H:%M:%S"

converted_tz = pytz.timezone('Asia/Kolkata')
datetime_object = datetime.now(converted_tz)
now = datetime_object.strftime(format)



def clientList(request):
    clientList = User.objects.all()
    adminobject = ''
    for c in clientList:
        adminobject = admin_permission.objects.filter(client_id=c.id)

    return render(request, 'superAdmin/clientAdminList.html', {'clientList': clientList, 'adminobject': adminobject})
#


def edit_client(request, client_id):
    client = get_object_or_404(User, id=client_id)
    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            print("ok")
            return redirect('clientList')
    else:
        form = CreateUserForm(instance=client)
        print("error")
    return render(request, 'superAdmin/edit_client.html', {'form': form, 'client': client})
#


register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



def clientInfo(request):
    userInfo = request.user.id
    adminPbjects = admin_permission.objects.filter(client_id=request.user.id)
    cliendStatus = ''
    for i_cliendId in adminPbjects:
        cliendStatus = cliendStatus+i_cliendId.client_status
    return JsonResponse({"clientInfo": cliendStatus})


def registerpage(request):
        print('reg')


        form = CreateUserForm()
        if request.method == 'POST':
            test_username = request.POST.get('username')
            test_email = request.POST.get('email')
            user_objects = User.objects.filter(username=test_username)
            user_objects1 = User.objects.filter(email=test_email.lower())
            if len(user_objects) == 0:
                if len(user_objects1) == 0:
                    form = CreateUserForm(request.POST)
                    if form.is_valid():
                        new_user = form.save()

                        user = form.cleaned_data.get('username')
                        messages.success(
                            request, 'Account Was Created ' + user + ' ..!')
                        print("*******")
                        transaction_type = 'new client registration'
                        transaction_name = user
                        transaction_count = 1
                        ticket_billing = ticket_billing_details(
                            client_id=new_user.id,
                            transaction_type=transaction_type,
                            transaction_name=transaction_name,
                            transaction_count=transaction_count,

                        )
                        ticket_billing.save()
                        admin_permissionCreate = admin_permission()
                        admin_permissionCreate.client_auth_key = secrets.token_urlsafe(
                            16)
                        admin_permissionCreate.client_auth_secret = secrets.token_hex(
                            16)
                        admin_permissionCreate.client_billing_status = False
                        admin_permissionCreate.login_allowed = False
                        admin_permissionCreate.client_id = new_user.id
                        admin_permissionCreate.save()

                        return redirect('clientList')
                    else:
                        context = {'form': form, 'invalid': 'text-danger',
                                   'tex': "User name was already exist!"}
                        return render(request, 'accounts/signup.html', context)
                else:
                    context = {'form': form, 'invalid': 'text-danger',
                               'tex': "User name was already exist!"}
                    return render(request, 'accounts/signup.html', context)
            else:
                context = {'form': form, 'invalid': 'text-danger',
                           'tex': "Email name was already exist!"}
                return render(request, 'accounts/signup.html', context)
        else:
            context = {'form': form}
            return render(request, 'accounts/signup.html', context)


from django.contrib.auth.hashers import check_password

def subclient(request):
    subclientList = Subclient.objects.filter(client=request.user)



    return render(request, 'accounts/subClient.html', {'subclientList': subclientList})

def openSub(request):
    return render(request, 'openSubClient.html')

def openSubClient(request):
    subclientList = Subclient.objects.filter(client_id=request.user)

    if request.method == 'POST':
        subclientname = request.POST.get('subclientname')
        emailid = request.POST.get('emailid')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')

        if password != re_password:
            messages.error(request, "Passwords do not match.")
            return redirect('openSub')

        if len(password) < 8:
            messages.error(request, "Password should be at least 8 characters long.")
            return redirect('openSub')

        if Subclient.objects.filter(client=request.user, emailid=emailid).exists():
            messages.error(request, "Email address already exists.")
            return redirect('openSub')

        if User.objects.filter(email=emailid).exists():
            messages.error(request, "Email address is already registered.")
            return redirect('openSub')

        # Check if the entered password matches the hashed password
        if not check_password(password, request.user.password):
            messages.error(request, "Invalid password.")
            return redirect('openSub')

        subclient = Subclient(client=request.user, subclientname=subclientname,
                              emailid=emailid, password=request.user.password, re_password=request.user.password)
        subclient.save()

        # Redirect to a success page or any other desired page
        return redirect('subClient')

    return render(request, 'accounts/subClient.html', {'subclientList': subclientList})

def assignSubClient(request, id):
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

        # Redirect to the ticketDash page after saving preferences
        return redirect('ticketDash')

    return render(request, 'assignSubClient.html', {'subclient': subclient, 'preferences': sub_user_preference, 'SUBCLIENT_CHOICE': SUBCLIENT_CHOICE, 'client_service_type': client_service_type})


from django.db import IntegrityError

from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from django.contrib import messages



from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from django.contrib.auth.decorators import login_required

def loginPage(request):
    request.session['scanned_tickets'] = ''

    if request.user.is_superuser:
        return render(request, 'admindash.html')

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email.lower()).first()
        if user is not None:
            if user.is_superuser and user.check_password(password):
                login(request, user)
                return render(request, 'admindash.html')
            else:
                admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()
                if admin_permission_obj is not None and admin_permission_obj.login_allowed:
                    serviceType = admin_permission_obj.client_service_type
                    admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()
                    if serviceType == "commerce":
                        if user.check_password(password):  # Validate password
                            login(request, user)
                            return render(request, 'vmart.html')
                        else:
                            messages.error(request, 'Invalid credentials!')
                    elif serviceType == "scanner":
                        if user.check_password(password):  # Validate password
                            login(request, user)
                            return render(request, 'scanner.html')
                        else:
                            messages.error(request, 'Invalid credentials!')
                    elif serviceType == "donation":
                        if user.check_password(password):  # Validate password
                            login(request, user)

                            return render(request, 'donationDash.html',{'admin_permission_obj': admin_permission_obj} )
                        else:
                            messages.error(request, 'Invalid credentials!')
                    elif serviceType == "Appointment":
                        if user.check_password(password):  # Validate password
                            login(request, user)

                            return render(request, 'appointmentDash.html',{'admin_permission_obj': admin_permission_obj})

                    elif serviceType == "survey":
                        if user.check_password(password):  # Validate password
                            login(request, user)
                            return render(request, 'surveyDash.html',{'admin_permission_obj': admin_permission_obj})

                    elif serviceType == 'hotel':
                        if user.check_password(password):
                            login(request, user)
                            return render(request, 'hotelDash.html',{'admin_permission_obj':admin_permission_obj})
                        else:
                            messages.error(request, 'Invalid credentials!1.3')
                    
                    elif serviceType == "campaign":
                        if user.check_password(password):  # Validate password
                            login(request, user)
                            # return redirect('listCampaign')
                            form_5_records = Form.objects.filter(client_id=request.user.id).order_by('-id')[:5]
                            template_5_records = template_info.objects.filter(client_id=request.user.id).order_by('-id')[:5]
                            return render(request, 'B_campaign/dashbord.html',
                                          {'admin_permission_obj': admin_permission_obj,
                                           'form_5_records': form_5_records, 'template_5_records': template_5_records})
                        else:
                            messages.error(request, 'Invalid credentials!')
                    else:
                        if user.check_password(password):  # Validate password
                            login(request, user)
                            return render(request, 'ticketDash.html')
                        else:
                            messages.error(request, 'Invalid credentials!1.1')
                else:
                    messages.error(request, 'Login not allowed')
        else:
            subclient = Subclient.objects.filter(emailid=email.lower()).first()
            client = None  # Default assignment
            if subclient is not None:
                client = subclient.client
                if check_password(password, subclient.password):  # Validate password
                    admin_permission_obj = admin_permission.objects.filter(client_id=client.id).first()
                    if admin_permission_obj is not None and admin_permission_obj.login_allowed:
                        serviceType = admin_permission_obj.client_service_type
                        if serviceType == "commerce":
                            login(request, client)
                            return render(request, 'vmart.html')
                        elif serviceType == "scanner":
                            login(request, client)
                            return render(request, 'scanner.html')

                        elif serviceType == "donation":
                            subclient_preferences = SubUserPreference.objects.filter(client=client, subclient=subclient).first()
                            request.session['subclient_id'] = subclient.id
                            # admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()
                            admin_permission_obj = admin_permission.objects.filter(client_id=client.id).first()  # Ensure admin_permission_obj is fetched for subclients
                            sub_user_preference = SubUserPreference.objects.get(client=client, subclient=subclient)
                            print("admin_permission_objsca",admin_permission_obj.client_marketplace)
                            login(request, client)

                            context = {
                                    'subclient': subclient,
                                    'subclient_preferences': subclient_preferences,
                                    'admin_permission_obj':admin_permission_obj,
                                    'sub_user_preference':sub_user_preference,
                                    }

                            if subclient_preferences and subclient_preferences.preference == 'donation':
                                return render(request, 'donationDash.html', context)
                            
                            else:
                                return redirect('ticketDash')
                            print('a3c')
                        elif serviceType == "campaign":
                            print("usersss")
                            subclient_preferences = SubUserPreference.objects.filter(client=client, subclient=subclient).first()
                            print("subclient_preferences", subclient_preferences)
                            request.session['subclient_id'] = subclient.id
                            # admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()
                            admin_permission_obj = admin_permission.objects.filter(client_id=client.id).first()  # Ensure admin_permission_obj is fetched for subclients
                            sub_user_preference = SubUserPreference.objects.get(client=client, subclient=subclient)
                            print("admin_permission_objsca",admin_permission_obj.client_marketplace)
                            login(request, client)

                            context = {
                                    'subclient': subclient,
                                    'subclient_preferences': subclient_preferences,
                                    'admin_permission_obj':admin_permission_obj,
                                    'sub_user_preference':sub_user_preference,
                                    }

                            if subclient_preferences and subclient_preferences.preference == 'campaign':
                                print('with subclient_preferences preference == "campaign"')
                                return render(request, 'Bcampaign.html', context)
                            else:
                                print('escpe')
                                return render(request, 'Bcampaign.html',context)
                            print('a4d')
                        elif serviceType == "hotel":
                            print("usersss")
                            subclient_preferences = SubUserPreference.objects.filter(client=client, subclient=subclient).first()
                            print("subclient_preferences", subclient_preferences)
                            request.session['subclient_id'] = subclient.id
                            # admin_permission_obj = admin_permission.objects.filter(client_id=user.id).first()
                            admin_permission_obj = admin_permission.objects.filter(client_id=client.id).first()  # Ensure admin_permission_obj is fetched for subclients
                            sub_user_preference = SubUserPreference.objects.get(client=client, subclient=subclient)
                            print("admin_permission_objsca",admin_permission_obj.client_marketplace)
                            login(request, client)

                            context = {
                                    'subclient': subclient,
                                    'subclient_preferences': subclient_preferences,
                                    'admin_permission_obj':admin_permission_obj,
                                    'sub_user_preference':sub_user_preference,
                                    }

                            if subclient_preferences and subclient_preferences.preference == 'hotel':
                                print('with subclient_preferences preference == "hotel"')
                                return render(request, 'hotelDash.html', context)
                            else:
                                print('escpe')
                                return render(request, 'hotelDash.html',context)
                            print('a5e')
                    else:
                        messages.error(request, 'Subclient login not allowed')
                else:
                    messages.error(request, 'Invalid credentials!1')
            else:
                messages.error(request, 'Invalid credentials!2')

    return render(request, 'accounts/login.html')





def ticketDash(request):
    print("Inside ticketDash view function")
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    print("subclient_id:", subclient_id)
    if subclient_id:
        subclient = Subclient.objects.filter(id=subclient_id).first()
        subclient_preferences = SubUserPreference.objects.filter(client=request.user, subclient=subclient).first()

        context = {
            'subclient': subclient,  # Pass the subclient to the template for reference if needed
            'subclient_preferences': subclient_preferences,
        }
        return render(request, 'ticketDash.html', context)
    else:
        
        messages.error(request, 'Subclient ID not found in session')
        return redirect('subClient')

def selectSubclient(request, subclient_id):
    request.session['subclient_id'] = subclient_id  # Store the selected subclient ID in the session
    return redirect('ticketDash')



from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutUser(request):

    request.session.pop('subclient_id', None)
    logout(request)
    return redirect('login')



class user_change_password(LoginRequiredMixin, TemplateView):
    form_class = MyPasswordChangeForm

    def get(self, request, *args, **kwargs):

        form = self.form_class(self.request.user)
        return render(request, 'accounts/passwordform.html', {'form': form, })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)  # Important!
            logoutUser(request)
            return redirect('/')
        else:
            return render(request, 'accounts/passwordform.html', {'form': form, 'password_changed': False})


@csrf_exempt
def demo(request):
    if request.method == "POST":
        print(request.POST, '------')
        subject = "Website Inquiry"
        body = {
            'first_name': request.POST.get('FirstName'),
            'last_name': request.POST.get('LastName'),
            'email': request.POST.get('emailFrom'),
            'companyName': request.POST.get('CompanyName'),
            'mobileNumber': request.POST.get('mobileNumber'),
            'JobTitle': request.POST.get('JobTitle'),

        }
        message = "\n".join(body.values())
        from_1 = settings.EMAIL_HOST_USER
        try:

            #         email = EmailMessage(
            #     subject='Hello',
            #     body='Body goes here',
            #     from_email='contact@vailo.ai',
            #     to=['contact@vailo.ai'],
            #     reply_to=['contact@vailo.ai'],
            #     headers={'Content-Type': 'text/plain'},
            # )
            #         email.send()
            send_mail(subject, message, settings.EMAIL_HOST_USER, [
                      'chetan@vividhity.com', 'vailo@vividhity.com'])
            leadsObjects = vailo_leads.objects.filter(first_name=request.POST.get('FirstName'),
                                                      last_name=request.POST.get('LastName'), company_name=request.POST.get('CompanyName'),
                                                      business_email=request.POST.get('emailFrom'), business_number=request.POST.get('mobileNumber'),
                                                      job_title=request.POST.get(
                                                          'JobTitle')
                                                      )
            if len(leadsObjects) == 0:
                leadsObjects1 = vailo_leads()
                leadsObjects1.first_name = request.POST.get('FirstName')
                leadsObjects1.last_name = request.POST.get('LastName')
                leadsObjects1.company_name = request.POST.get('CompanyName')
                leadsObjects1.business_email = request.POST.get('emailFrom')
                leadsObjects1.business_number = request.POST.get(
                    'mobileNumber')
                leadsObjects1.job_title = request.POST.get('JobTitle')
                leadsObjects1.save()
            else:
                pass

        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        return HttpResponseRedirect('/')

    else:
        return render(request, 'accounts/demo.html')

    return render(request, 'accounts/demo.html')
def scannerSub(request):
    subclient_id = request.session.get('subclient_id')  # Retrieve the selected subclient ID from the session
    # print('subclient_id',subclient_id)
    subclient = Subclient.objects.filter(id=subclient_id).first()
    subclient_preferences = SubUserPreference.objects.filter(subclient=subclient).first()

    return render(request, 'scanner.html', {'subclient_preferences':subclient_preferences})

def aboutUs(request):
    return render(request, 'aboutUs.html')

def appointmrntPage(request):
    return render(request, 'appointmrntPage.html')

def dipstickPage(request):
    return render(request, 'dipstickPage.html')


def campaignPage(request):
    return render(request, 'campaignPage.html')

def donationPage(request):
    return render(request, 'donationPage.html')

def digitalPage(request):
    return render(request, 'digitalPage.html')

def ticketPage(request):
    return render(request, 'ticketPage.html')

def pricingPage(request):
    return render(request, 'pricingPage.html')

def reachBillion(request):
    return render(request, 'reachBillion.html')

def servicesPage(request):
    return render(request, 'servicesPage.html')

def serviceNow(request):
    return render(request, 'serviceNow.html')

def homeStatic(request):
    return render(request, 'vmartHome.html')

def healthwatt(request):
    return render(request, 'healthwatt.html')

def donationWebPage(request):
    return render(request, 'donationWebPage.html')

def scanToMenuWebPage(request):
    return render(request, 'scanToMenuWebPage.html')

def ticketMenuWebPage(request):
    return render(request, 'ticketMenuWebPage.html')

def directCommerceBlog(request):
    return render(request, 'directCommerceBlog.html')

def partnerPage(request):
    return render(request, 'partnerPage.html')

def productOne(request):
    return render(request, 'product.html')


def productTwo(request):
    return render(request, 'productTwo.html')


def Services(request):
    return render(request, 'services.html')

def salon(request):
    return render(request, 'salonPage.html')

def hrSystem(request):
    return render(request, 'hrSystem.html')


def help(request):
    return render(request, 'help/help.html')


def clientView(request, catalog, newStr):
    # print(newStr)
    CheckingObject = admin_permission.objects.filter(client_auth_secret=newStr)
    if len(CheckingObject) != 0:
        face_details = facebook_details.objects.filter(fb_name=catalog.lower())
        num_num = 0
        client_id = 0
        for num_i in face_details:
            num_num = num_num+num_i.fb_whatsapp_number
            client_id = client_id+num_i.client_id

        # print(client_id,'111111111111111111111')
        adminPbjects = admin_permission.objects.filter(client_id=client_id)
        imagepath = ''
        color4 = ''
        color5 = ''
        for i in adminPbjects:
            imagepath = imagepath+str(i.client_image)
            color4 = color4+i.client_color4
            color5 = color5+i.client_color5
        final_dict = {}

        for us_i in face_details:

            p_view = product_category.objects.filter(client_id=us_i.client_id)
            for us_i2 in p_view:
                product_detai = []
                # inner_dict.update({'cata_name': us_i2.product_category_name})

                p_product_object = product_info.objects.filter(
                    client_id=us_i.client_id, product_category_id=us_i2.id, product_status=True)
                # print(len(p_product_object))
                if len(p_product_object) != 0:
                    for us_i3 in p_product_object:
                        iinner = {
                            'product_id': us_i3.id,
                            'product_name': us_i3.product_name,
                            'product_price': us_i3.product_price,
                            'product_mrp': us_i3.product_mrp,
                            'product_offer': us_i3.product_offer,
                            'product_image': us_i3.product_image,
                            'product_bot_image': us_i3.product_bot_image,
                            'product_description': us_i3.product_description.capitalize()
                        }
                        product_detai.append(iinner)

                    final_dict.update(
                        {us_i2.product_category_name: product_detai})
            # print(final_dict)

        return render(request, 'clientSiteView.html', {'color4': color4, 'color5': color5, 'im': final_dict, 'cilentId': client_id, 'Product_ca': catalog, 'num_num': num_num, 'imagepath': imagepath})
    return HttpResponse('Sorry Your Link not WOrking')


def productApi(request, pk):
    product_objects = product_info.objects.filter(id=pk)
    return JsonResponse({"product": list(product_objects.values())})


@csrf_exempt
def py_addtocart(request, pk, pk1, pk2, pk3):
    a = pk3
    b = a
    try:
        b = int(a)
    except:
        print("An exception occurred")
    if str == type(b):
        # print('jjjjjjjjjjjjjjjjjjj','......')
        # request.POST.get('a1'), request.POST.get('tokki')
        # js_id=request.POST.get('a1')
        # js_key=request.POST.get('tokki')
        js_id = int(pk)
        js_key = pk1
        # print(type(js_id),js_id,'id')
        # print(type(js_id),js_key,'key')
        key_object = order_details.objects.filter(
            js_cartid=js_key, product_fk_id=js_id)

        if pk2 == 'addTwoCart' or pk2 == 'increment':
            if len(key_object) == 0:
                add2cart_object = product_info.objects.filter(id=int(js_id))
                # print(add2cart_object)
                for add2cart_i in add2cart_object:
                    create_cart = order_details()
                    create_cart.customer_number = ''
                    create_cart.order_date = now
                    create_cart.order_status = 'a2c'
                    create_cart.product_price = add2cart_i.product_price
                    create_cart.product_value = add2cart_i.product_price
                    create_cart.product_quantity = 1
                    create_cart.product_fk_id = js_id
                    create_cart.client_id = add2cart_i.client_id
                    create_cart.client_shop = 'online'
                    create_cart.tableNumber = '0'
                    create_cart.js_cartid = js_key
                    create_cart.save()
            else:
                add2cart_object = product_info.objects.filter(id=int(js_id))
                for edit_i in add2cart_object:
                    for edit_i2 in key_object:
                        edit_object = order_details.objects.get(id=edit_i2.id)
                        edit_object.product_quantity = edit_object.product_quantity + 1
                        edit_object.product_value = edit_i.product_price * edit_object.product_quantity
                        edit_object.save()

        elif pk2 == 'decrement':
            if len(key_object) != 0:

                for add2cart_i in key_object:
                    if add2cart_i.product_quantity != 1:
                        decrementObject = order_details.objects.get(
                            id=add2cart_i.id)
                        decrementObject.product_quantity = decrementObject.product_quantity - 1
                        decrementObject.product_value = decrementObject.product_price * \
                            decrementObject.product_quantity
                        decrementObject.save()
                    else:
                        deleteObject = order_details.objects.get(
                            id=add2cart_i.id)
                        deleteObject.delete()

        elif pk2 == 'delete':
            for add2cart_i in key_object:
                deleteObject = order_details.objects.get(id=add2cart_i.id)
                deleteObject.delete()

    elif int == type(b):
        # print('jjjjjjjjjjjjjjjjjjj','......')
        # request.POST.get('a1'), request.POST.get('tokki')
        # js_id=request.POST.get('a1')
        # js_key=request.POST.get('tokki')
        js_id = int(pk)
        js_key = pk1
        # print(type(js_id),js_id,'id')
        # print(type(js_id),js_key,'key')
        key_object = order_details.objects.filter(
            js_cartid=js_key, product_fk_id=js_id)

        if pk2 == 'addTwoCart' or pk2 == 'increment':
            if len(key_object) == 0:
                add2cart_object = product_info.objects.filter(id=int(js_id))
                # print(add2cart_object)
                for add2cart_i in add2cart_object:
                    create_cart = order_details()
                    create_cart.customer_number = ''
                    create_cart.order_date = now
                    create_cart.order_status = 'a2c'
                    create_cart.product_price = add2cart_i.product_price
                    create_cart.product_value = add2cart_i.product_price
                    create_cart.product_quantity = 1
                    create_cart.product_fk_id = js_id
                    create_cart.client_id = add2cart_i.client_id
                    create_cart.js_cartid = js_key
                    create_cart.tableNumber = int(pk3)
                    create_cart.client_shop = 'offline'
                    create_cart.save()
            else:
                add2cart_object = product_info.objects.filter(id=int(js_id))
                for edit_i in add2cart_object:
                    for edit_i2 in key_object:
                        edit_object = order_details.objects.get(id=edit_i2.id)
                        edit_object.product_quantity = edit_object.product_quantity + 1
                        edit_object.product_value = edit_i.product_price * edit_object.product_quantity
                        edit_object.save()

        elif pk2 == 'decrement':
            if len(key_object) != 0:

                for add2cart_i in key_object:
                    if add2cart_i.product_quantity != 1:
                        decrementObject = order_details.objects.get(
                            id=add2cart_i.id)
                        decrementObject.product_quantity = decrementObject.product_quantity - 1
                        decrementObject.product_value = decrementObject.product_price * \
                            decrementObject.product_quantity
                        decrementObject.save()
                    else:
                        deleteObject = order_details.objects.get(
                            id=add2cart_i.id)
                        deleteObject.delete()

        elif pk2 == 'delete':
            for add2cart_i in key_object:
                deleteObject = order_details.objects.get(id=add2cart_i.id)
                deleteObject.delete()

    return HttpResponse('hi')


def customer(request):
    customerdetails = customer_address.objects.filter(
        client_id=request.user.id)
    print(customerdetails)
    if len(customerdetails) == 1:
        for a in customerdetails:
            print(a.customer_name)

    return render(request, 'CustomerDetails.html', {'customerdetails': customerdetails})


def error_404(request, exception):
    return render(request, '404_error.html')


def termsConditions(request):
    return render(request, 'termsConditions.html')


def refundAndCancelation(request):
    return render(request, 'refundAndCancelation.html')


def privacyPolicy(request):
    return render(request, 'privacyPolicy.html')


def eCommerceDashboard(request):
    return render(request, 'eCommerceDashboard.html')


def update_client(request, id):
    print(id)
    update_permission = admin_permission.objects.filter(client_id=id)
    # for u in update_permission:
    #     u.login_allowed = True
    #     u.save()
    return render(request, 'updateadmin.html', {'update_permission': update_permission})
    # return render(request, 'superAdmin/clientAdminList.html', {'clientList': User.objects.all(), 'client_id': id,'a':a})


def generate_bill(request):
    clients = User.objects.all()

    for client in clients:
        permissions = admin_permission.objects.filter(
            client_id=request.user.id).first()

        if permissions:
            tickets = ticket_billing.objects.filter(client_id=request.user.id)

            for ticket in tickets:
                transactions = ticket_billing_details.objects.filter(
                    client_id=request.user.id,
                    ticket_billing_id=ticket.id
                ).values('transaction_type').annotate(total_count=Sum('transaction_count'))

                total_amount = 0.0

                for transaction in transactions:
                    transaction_type = transaction['transaction_type']
                    transaction_count = transaction['total_count']

                    if transaction_type == 'new client registration':
                        amount = transaction_count * permissions.billing_new_client_rate
                    elif transaction_type == 'new client lead':
                        amount = transaction_count * permissions.billing_new_customer_lead_rate
                    elif transaction_type == 'campaign message sent':
                        amount = transaction_count * permissions.billing_campaign_sent_rate
                    elif transaction_type == 'ticket message sent':
                        amount = transaction_count * permissions.billing_message_sent_rate
                    elif transaction_type == 'ticket message received':
                        amount = transaction_count * permissions.billing_message_received_rate
                    else:
                        amount = 0.0

                    total_amount += amount

                billing_amount1 = permissions.billing_amount1
                billing_amount2 = permissions.billing_amount2
                billing_amount3 = permissions.billing_amount3
                billing_monthly_charge = permissions.billing_monthly_charge
                total_amount += billing_amount1
                total_amount += billing_amount2
                total_amount += billing_amount3
                total_amount += billing_monthly_charge

                ticket.billed_amount = total_amount
                ticket.save()

    return redirect('clientList')


def updatepermisions(request, client_id):
    update_admin_info = admin_permission.objects.filter(client_id=client_id)

    if request.method == 'POST':
        for admin_update in update_admin_info:
            admin_update.client_service_type = request.POST.get(
                'selectservice')
            admin_update.client_marketplace = request.POST.get(
                'marketselect')
            admin_update.client_type = request.POST.get('selecttype')
            admin_update.client_permission_status = request.POST.get(
                'permissiontype')
            admin_update.login_allowed = request.POST.get('loginallowed')

            try:
                admin_update.billing_amount1 = float(
                    request.POST.get('billing_amount1'))
            except (ValueError, TypeError):
                admin_update.billing_amount1 = None

            try:
                admin_update.billing_amount2 = float(
                    request.POST.get('billing_amount2'))
            except (ValueError, TypeError):
                admin_update.billing_amount2 = None

            try:
                admin_update.billing_amount3 = float(
                    request.POST.get('billing_amount3'))
            except (ValueError, TypeError):
                admin_update.billing_amount3 = None

            try:
                admin_update.billing_campaign_sent_rate = float(
                    request.POST.get('billing_campaign_sent_rate'))
            except (ValueError, TypeError):
                admin_update.billing_campaign_sent_rate = None

            admin_update.billing_currency = request.POST.get(
                'billing_currency')

            try:
                admin_update.billing_message_received_rate = float(
                    request.POST.get('billing_message_received_rate'))
            except (ValueError, TypeError):
                admin_update.billing_message_received_rate = None

            try:
                admin_update.billing_message_sent_rate = float(
                    request.POST.get('billing_message_sent_rate'))
            except (ValueError, TypeError):
                admin_update.billing_message_sent_rate = None

            try:
                admin_update.billing_monthly_charge = float(
                    request.POST.get('billing_monthly_charge'))
            except (ValueError, TypeError):
                admin_update.billing_monthly_charge = None

            try:
                admin_update.billing_new_client_rate = float(
                    request.POST.get('billing_new_client_rate'))
            except (ValueError, TypeError):
                admin_update.billing_new_client_rate = None

            try:
                admin_update.billing_new_customer_lead_rate = float(
                    request.POST.get('billing_new_customer_lead_rate'))
            except (ValueError, TypeError):
                admin_update.billing_new_customer_lead_rate = None

            admin_update.save()

        return render(request, 'updatepermisions.html')


def scanner(request):
    print("rootmap")

    if request.method == 'POST':
        print("sssss")
        data = json.loads(request.body.decode('utf-8'))
        barcode_data = data['data']
        ticket_number = 0
        customer_phone_number = None

        if request.session['scanned_tickets'] != barcode_data:
            request.session['scanned_tickets'] = barcode_data
            print("west")

            if '_' in barcode_data:
                category_id = barcode_data[:barcode_data.index("_")]
                ticket_number = barcode_data[barcode_data.index("_") + 1:]
                print(ticket_number)
                print(category_id)
                validateinfo = ticket_information.objects.filter(client_id=request.user.id,
                                                                 event_ticket_category_id=category_id,
                                                                 ticket_number=ticket_number)
                print(validateinfo)
                message = ''
                if validateinfo:
                    print("rr")
                    for v_i in validateinfo:
                        if v_i.ticket_number == ticket_number:
                            if v_i.ticket_status == 10:

                                message = "Allowed"
                                customer_phone_number = v_i.customer_phone_number

                                def update_ticket_info():
                                    print("cdcd")
                                    v_i.ticket_status = 20
                                    v_i.save()
                                    # message = 'None Allowed'
                                    # print(message)

                                timer = threading.Timer(
                                    10.0, update_ticket_info)
                                timer.start()
                            else:
                                message = "Not Allowed"
                                customer_phone_number = v_i.customer_phone_number
                                # return render(request,'scanner.html',{'success': True, 'message': message})
                        else:
                            print("yzyz")
                            message = 'Ticket Number Does Not Exist'
                else:
                    message = "QR information Not Found"

            else:
                print("zxzx")
                message = "Invalid QR COde"
            return JsonResponse({'success': True, 'message': message, 'ticket_number': ticket_number,
                                 'customer_phone_number': customer_phone_number})
        else:
            pass
    else:
        return JsonResponse({'success': False, 'message': 'Invalid Request'})

    return HttpResponse("hi")


def clientscanner(request):
    return HttpResponse('Progress is going on')


def helps(request):
    return HttpResponse('Please contact Admin')

from datetime import datetime, timedelta
from django.shortcuts import render, redirect

from django.utils import timezone

from datetime import timedelta

from datetime import datetime, timedelta
import pytz

def update_ticket(request):
    current_time = datetime.now(pytz.timezone('UTC'))
    print(current_time,'current_time')

    two_hours_ago = current_time - timedelta(hours=2)
    print(two_hours_ago,'two_hours_ago')
    tickets_to_update = ticket_information.objects.filter(
                                                          vailo_record_last_update__lte=two_hours_ago,
                                                          ticket_status=10)
    print(tickets_to_update,'tickets_to_update')
    for ticket in tickets_to_update:
        ticket.ticket_status = 0
        print(ticket.ticket_status,'ticket.ticket_status')
        ticket.save()
        print(ticket,'ddfsef')
    return redirect('clientList')

def process_expiry(request):
    current_date = timezone.now().date()

    events_to_update = event_master.objects.filter(End_Date__lt=current_date)
    for event in events_to_update:
        tickets_to_update = ticket_information.objects.filter(event_master_id=event.id, ticket_status__in=[0, 10, 20, 30])
        for ticket in tickets_to_update:
            ticket.ticket_status = 80
            ticket.save()

    tickets_to_update_expiry = ticket_information.objects.filter(expiry_date__lt=current_date, ticket_status__in=[0, 10, 20, 30])
    for ticket in tickets_to_update_expiry:
        ticket.ticket_status = 80
        ticket.save()

    return redirect('clientList')


# commonPage
def UpdateProfileCommon(request):
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    adminPermissionObjects = admin_permission.objects.filter(client_id=request.user.id)
    if request.method=="GET":
        user_id=request.user.id
        user_object=User.objects.filter(id=user_id)
        adminPermissionObjects=admin_permission.objects.filter(client_id=request.user.id)
        admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

        return render(request, 'common/profile.html', {'us_obj': user_object,'adminP':adminPermissionObjects,'admin_permission_obj':admin_permission_obj})
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
        return render(request, 'common/profile.html', {'us_obj': user_object1,'adminP':adminPermissionObjects,'admin_permission_obj':admin_permission_obj})


def closeCommon(reqest):
    return redirect('/')


def subclientCommon(request):

    subclientList = Subclient.objects.filter(client=request.user)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()


    return render(request, 'common/subClientCommon.html', {'subclientList': subclientList, 'admin_permission_obj':admin_permission_obj})

def openSubCommon(request):
    subclientList = Subclient.objects.filter(client=request.user)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    return render(request, 'common/openSubClientCommon.html',{'subclientList': subclientList, 'admin_permission_obj':admin_permission_obj})



# from django.contrib import messages
# from django.shortcuts import render, redirect
# from django.contrib.auth.hashers import check_password
# from django.contrib.auth.models import User



# def openSubClientCommon(request):
#     subclientList = Subclient.objects.filter(client_id=request.user)
#     admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

#     if request.method == 'POST':
#         subclientname = request.POST.get('subclientname')
#         emailid = request.POST.get('emailid')
#         password = request.POST.get('password')
#         re_password = request.POST.get('re_password')

#         if password != re_password:
#             messages.error(request, "Passwords do not match.")
#         elif len(password) < 8:
#             messages.error(request, "Password should be at least 8 characters long.")
#         elif Subclient.objects.filter(client=request.user, emailid=emailid).exists():
#             messages.error(request, "Email address already exists.")
#         elif User.objects.filter(email=emailid).exists():
#             messages.error(request, "Email address is already registered.")
#         elif not check_password(password, request.user.password):
#             messages.error(request, "Invalid password.")
#         else:
#             subclient = Subclient(
#                 client=request.user,
#                 subclientname=subclientname,
#                 emailid=emailid,
#                 password=password,  
#                 re_password=re_password  
#             )
#             subclient.save()
#             return redirect('subClientCommon')

#     return render(request, 'common/openSubClientCommon.html', {'subclientList': subclientList, 'admin_permission_obj': admin_permission_obj})









def openSubClientCommon(request):
    subclientList = Subclient.objects.filter(client_id=request.user)
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()

    if request.method == 'POST':
        subclientname = request.POST.get('subclientname')
        emailid = request.POST.get('emailid')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        if password != re_password:
            messages.error(request, "Passwords do not match.")
        if len(password) < 8:
            messages.error(request, "Password should be at least 8 characters long.")

        if Subclient.objects.filter(client=request.user, emailid=emailid).exists():
            messages.error(request, "Email address already exists.")

        if User.objects.filter(email=emailid).exists():
            messages.error(request, "Email address is already registered.")

        if not check_password(password, request.user.password):
            messages.error(request, "Invalid password.")
            # redirect('subClientCommon')
    

        subclient = Subclient(client=request.user, subclientname=subclientname,
                              emailid=emailid, password=request.user.password, re_password=request.user.password)
        subclient.save()

        # Redirect to a success page or any other desired page
        return redirect('subClientCommon')

    return render(request, 'common/openSubClientCommon.html', {'subclientList': subclientList,'admin_permission_obj':admin_permission_obj})










from vailodb_n.models import donation_marketplace
from vailodb_b.models import campaign_marketplace, Form, template_info
from vailodb_h.models import Hotel_marketplace


def assignSubClientCommonMarketId(request, id):
    subclient = Subclient.objects.get(id=id)
    client = request.user

    try:
        sub_user_preference = SubUserPreference.objects.get(client=client, subclient=subclient)
    except SubUserPreference.DoesNotExist:
        sub_user_preference = None
    admin_perm_instance = admin_permission.objects.get(client=client)
    client_service_type = admin_perm_instance.client_service_type
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    addNgoMarketPlace = donation_marketplace.objects.filter(client=request.user.id)
    groupnameinfo = Hotel_marketplace.objects.filter(client=request.user.id)
    print("groupnameinfo",groupnameinfo,request.user.id)
    if request.method == 'POST':
        selected_marketPlace_ids = request.POST.getlist('preferencesmk')
        preference_str = ','.join(selected_marketPlace_ids)
        selected_history = request.POST.getlist('preferencesHistory')
        preference_History = ','.join(selected_history)

        if sub_user_preference:
            sub_user_preference.marketplace_id = preference_str
            sub_user_preference.history_preference = preference_History
            sub_user_preference.save()
        else:
            # If the record doesn't exist, create a new one
            sub_user_preference = SubUserPreference.objects.create(
                client=client,
                subclient=subclient,
                marketplace_id=preference_str,
                history_preference=preference_History,
            )

        # Redirect to the subClientCommon page after saving preferences
        return redirect('subClientCommon')

    context = {
        'subclient': subclient,
        'preferences': sub_user_preference,
        'SUBCLIENT_CHOICE': SUBCLIENT_CHOICE,
        'client_service_type': client_service_type,
        'admin_permission_obj': admin_permission_obj,
        'addNgoMarketPlace': addNgoMarketPlace,
        'groupnameinfo':groupnameinfo,
    }
    return render(request, 'common/assignSubClientCommon.html', context)



#after history
def assignSubClientCommon(request, id):
    subclient = Subclient.objects.get(id=id)
    client = request.user

    try:
        sub_user_preference = SubUserPreference.objects.get(client=client, subclient=subclient)
        print("sub_user_preference1",sub_user_preference)   
    except SubUserPreference.DoesNotExist:
        sub_user_preference = None

    admin_perm_instance = admin_permission.objects.get(client=client)
    client_service_type = admin_perm_instance.client_service_type
    admin_permission_obj = admin_permission.objects.filter(client_id=request.user.id).first()
    addNgoMarketPlace = donation_marketplace.objects.filter(client=request.user.id)
    addcmpMarketPlace = campaign_marketplace.objects.filter(client=request.user.id)
    groupnameinfo = Hotel_marketplace.objects.filter(client=request.user.id)



    # Initialize preference_History outside the if block
    preference_History = ""

    if request.method == 'POST':
        print(request.POST.getlist('preferences'),request.POST.getlist('preferencesmk'))
        selected_preferences = request.POST.getlist('preferences')
        selected_marketplace_ids = request.POST.getlist('preferencesmk')

        preference_str = ','.join(selected_preferences)
        marketplace_preference_str = ','.join(selected_marketplace_ids)

        selected_history = request.POST.getlist('preferencesHistory')
        preference_History = ','.join(selected_history)

        if sub_user_preference:
            sub_user_preference.preference = preference_str
            sub_user_preference.marketplace_id = marketplace_preference_str
            sub_user_preference.history_preference = preference_History
            sub_user_preference.save()
        else:
            sub_user_preference = SubUserPreference.objects.create(
                client=client,
                subclient=subclient,
                preference=preference_str,
                marketplace_id=marketplace_preference_str,
                history_preference=preference_History,
            )
        print('preference selected_preferences',selected_preferences)
        # Redirect to the subClientCommon page after saving preferences
        return redirect('subClientCommon')

    # Include 'preferences' in the context for the GET request
    context = {
        'subclient': subclient,
        'preferencesHistory': preference_History,
        'preferences': sub_user_preference,  # Make sure this is included
        'preferencesmk': [int(id) for id in sub_user_preference.marketplace_id.split(',') if id.strip()] if sub_user_preference and sub_user_preference.marketplace_id else [],
        'SUBCLIENT_CHOICE': SUBCLIENT_CHOICE,
        'client_service_type': client_service_type,
        'admin_permission_obj': admin_permission_obj,
        'addNgoMarketPlace': addNgoMarketPlace,
        'addcmpMarketPlace': addcmpMarketPlace,
        'groupnameinfo':groupnameinfo,
    }

    # Render the template if it's a GET request
    return render(request, 'common/assignSubClientCommon.html', context)

def blogPage(request):
    return render(request, 'blogPage.html')

def useCasePage(request):
    return render(request, 'useCasePage.html')


@csrf_exempt
def demo1(request):
    if request.method == "POST":
        print(request.POST, '------')
        subject = "Website Inquiry"
        body = {
            'name': request.POST.get('Name'),
            'email': request.POST.get('Email'),
            'phone_number': request.POST.get('Phone number')
        }
        message = "\n".join([f"{key}: {value}" for key, value in body.items()])
        from_1 = settings.EMAIL_HOST_USER
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, ['hello@brillion1.com', 'vailo@vividhity.com'])
            # Save to database
            leads_objects = vailo_leads.objects.filter(
                first_name=request.POST.get('Name'),  # Assuming first_name corresponds to Name field
                business_email=request.POST.get('Email'),
                business_number=request.POST.get('Phone number')
            )
            if not leads_objects.exists():
                leads_objects = vailo_leads(
                    first_name=request.POST.get('Name'),
                    business_email=request.POST.get('Email'),
                    business_number=request.POST.get('Phone number')
                )
                leads_objects.save()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/')
    else:
        return render(request, 'partnerPage.html')

