from django.shortcuts import render,redirect

# Create your views here.
import requests
import secrets
import random
from vailodb.models import admin_permission, facebook_details

from A_vMart.settings import DomainName

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def facebook_info(request):
    admin_permissionObject = admin_permission.objects.filter(client_id=request.user.id)
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
            # return render(request, 'D_facebook/facebookDe1.html')
            return render(request, 'common/facebookDe1.html')

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
                # return render(request, 'D_facebook/facebookDe.html',
                return render(request, 'common/facebookDe.html',
                              {'data': user_fb_details, 'CallbackUrl': CallbackUrl, 'VerifyToken': VerifyToken})
            else:
                # return render(request, 'D_facebook/facebookDe.html', {'data': user_fb_details})

                return render(request, 'common/facebookDe.html', {'data': user_fb_details})

            # if clientpermissionstatus:
            #     return render(request, 'D_facebook/facebookDe.html', {'data': user_fb_details,'CallbackUrl': CallbackUrl,'VerifyToken': VerifyToken})


            # return render(request, 'D_facebook/facebookDe.html', {'data': user_fb_details,'CallbackUrl':CallbackUrl,'VerifyToken':VerifyToken})



    if request.method=="POST":
        print(request.POST)
        ExitingUserObjects=facebook_details.objects.filter(


                                                           fb_phone_number_id=request.POST.get('fb_phone_number_id'),


                                                           )
        if len(ExitingUserObjects)==0:
            user_fb_details = facebook_details.objects.filter(client_id=request.user.id)
            print("ppppppppp",len(user_fb_details))
            random_number = random.randint(1, 1000)
            print("fffff")
            private_base_name = 'newvailoprivate_key'
            public_base_name = 'newvailopublic_key'
            private_new_name = f'{private_base_name}{random_number}'
            public_new_name = f'{public_base_name}{random_number}'
            if len(user_fb_details) == 0:
                print("s not coming")
                print('Generate private key')
                private_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048,
                    backend=default_backend()
                )

                # Get corresponding public key
                public_key = private_key.public_key()

                # Serialize private key to PEM format
                private_pem = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.BestAvailableEncryption(b'Guna@123')
                )

                # Save private key to a file
                print(private_pem)
                private_file_name = f'{private_new_name}.pem'
                with open("vgainprivate_key.pem", "wb") as private_key_file:
                    private_key_file.write(private_pem)

                # Serialize public key to PEM format
                public_pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )

                # Save public key to a file
                public_file_name = f'{public_new_name}.pem'
                with open("vgainpublic_key.pem", "wb") as public_key_file:
                    public_key_file.write(public_pem)

                print(public_pem)

                private_key_content = private_pem.decode('utf-8')
                public_key_content = public_pem.decode('utf-8')
                print(private_key_content)
                print(public_key_content)

                fb_object = facebook_details()
                # fb_object.fb_name = request.POST.get('fb_name').lower()
                # fb_object.fb_business_manager_id = request.POST.get('fb_business_manager_id')
                fb_object.fb_Whatsapp_business_account_id = request.POST.get('fb_whatsapp_business_id')
                fb_object.fb_phone_number_id = request.POST.get('fb_phone_number_id')
                fb_object.fb_whatsapp_number=request.POST.get('fb_whatsapp_number')
                fb_object.fb_access_token = request.POST.get('fb_access_token')
                # fb_object.fb_auth_token = request.POST.get('fb_auth_token')
                # fb_object.fb_app_id = request.POST.get('fb_app_id')
                # fb_object.fb_second_number= int(request.POST.get('fb_second_number'))
                # fb_object.fb_third_number= int(request.POST.get('fb_third_number'))
                # fb_object.private_key = private_key_content
                # fb_object.public_key = public_key_content
                fb_object.private_dynamic_file_name = private_file_name
                fb_object.public_dynamic_file_name = public_file_name
                fb_object.client_id = request.user.id
                fb_object.save()
                print("s successfully saved")
                user_fb_details = facebook_details.objects.filter(client_id=request.user.id)
                facbook_token = ''
                phonenumberId = 0
                public_key = ''
                for u_i in user_fb_details:
                    facbook_token = u_i.fb_access_token
                    phonenumberId = u_i.fb_phone_number_id
                    public_key = u_i.public_key
                print(public_key)
                print(facbook_token)
                print(phonenumberId)

                # url = f"https://graph.facebook.com/v18.0/{phonenumberId}/whatsapp_business_encryption"
                # payload = {
                #     'business_public_key': public_key
                # }
                # files = [
                #
                # ]
                # headers = {
                #     'Authorization': f'Bearer {facbook_token}'
                # }
                # response = requests.request("POST", url, headers=headers, data=payload, files=files)
                #
                # print(response.text)
                # print("s successfully uploaded public for the respected phone number")

                url = f"https://graph.facebook.com/v18.0/{phonenumberId}/whatsapp_business_encryption"

                # Read the content of the PEM file
                with open(f'C:/Vailo/17-01-2024 new dashboard/A_vMart/A_vMart/vgainpublic_key.pem', 'r') as f:
                    public_key_contents = f.read()

                payload = {'business_public_key': public_key_contents}

                headers = {
                    'Authorization': f'Bearer {facbook_token}',
                    'Cookie': 'ps_l=0; ps_n=0'
                }

                response = requests.post(url, headers=headers, data=payload)

                print(response.text)
                print("s successfully uploaded public for the respected phone number")

                return render(request, 'common/facebookDe.html', {'data': user_fb_details})
            elif len(user_fb_details)!=0:
                fb_object_edit = facebook_details.objects.get(client_id=request.user.id)
                print(fb_object_edit,'pppppppp')
                # fb_object_edit.fb_name = request.POST.get('fb_name').lower()
                # fb_object_edit.fb_business_manager_id = request.POST.get('fb_business_manager_id')
                fb_object_edit.fb_Whatsapp_business_account_id = request.POST.get('fb_whatsapp_business_id')
                fb_object_edit.fb_phone_number_id = request.POST.get('fb_phone_number_idRe')
                fb_object_edit.fb_whatsapp_number=request.POST.get('fb_whatsapp_numberRe')
                fb_object_edit.fb_access_token = request.POST.get('fb_access_tokenRe')
                # fb_object_edit.fb_auth_token = request.POST.get('fb_auth_token')
                # fb_object_edit.fb_app_id = request.POST.get('fb_app_id')
                # fb_object_edit.fb_second_number= int(request.POST.get('fb_second_number'))
                # fb_object_edit.fb_third_number= int(request.POST.get('fb_third_number'))
                fb_object_edit.save()
                user_fb_details = facebook_details.objects.filter(client_id=request.user.id)
                # return render(request, 'D_facebook/facebookDe.html', {'data': user_fb_details})
                return render(request, 'common/facebookDe.html', {'data': user_fb_details})

        return redirect('/')
        # return HttpsRespond



