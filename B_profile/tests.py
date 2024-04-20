# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from A_vMart.settings import DomainName
#
#
# from django.utils.decorators import method_decorator
# from django.views import generic
# import json
# import ast
# import requests
# import secrets
#
# # Create your views here.
# from A_webhook.models import order_details,order_header,customer_track_page,customer_address
# from D_facebook.models import facebook_details
# from E_product.models import product_info,product_category
# from B_profile.models import admin_permission
# from C_billing.models import client_received_messages,client_sent_messages,client_wallet_balance,client_payment_details
#
#
# from datetime import datetime,date
#
# now = datetime.now()
# from django.contrib.auth.decorators import login_required
#
#
#
# def counterReceive(request, userid):
#     count_object = client_received_messages()
#     count_object.message_date = now
#     count_object.r_day_count = 1
#     count_object.r_month_count = 0
#     count_object.r_year_count = 0
#     count_object.client_id = userid
#     count_object.save()
#     return 1000
#
#
# def count_perMessage(request, clientId):
#     client_topupObjects = client_wallet_balance.objects.filter(client_id=clientId, topup_status='available')
#     # print("_____________________________________user topcount")
#
#     if len(client_topupObjects)!=0:
#         for topup_i in client_topupObjects:
#             if not (topup_i.wallet_balance_point <= 0):
#                 client_topupObjects2 = client_wallet_balance.objects.get(id=topup_i.id)
#                 client_topupObjects2.wallet_balance_point = client_topupObjects2.wallet_balance_point - 1
#                 client_topupObjects2.save()
#             else:
#                 client_topupObjects2 = client_wallet_balance.objects.get(id=topup_i.id)
#                 client_topupObjects2.topup_status = 'unavailable'
#                 client_topupObjects2.save()
#             # # print(topup_i.topup_status)
#
#             print(topup_i.wallet_balance_point)
#     else:
#         print('go to topup client side')
#
# def counterSent(request, userid, id_date1):
#     count_perMessage(request, userid)
#     if id_date1 == '':
#         count_object = client_sent_messages()
#         count_object.message_date = now
#         count_object.s_day_count = 1
#         count_object.s_month_count = 0
#         count_object.s_year_count = 0
#         count_object.client_id = userid
#         count_object.save()
#     else:
#         print('///////', id_date1)
#         count_messages_2 = client_sent_messages.objects.get(id=int(id_date1))
#         count_messages_2.s_day_count = count_messages_2.s_day_count + 1
#         count_messages_2.save()
#     return 1000
#
#
# def vmart(request):
#     if request.user.is_authenticated:
#         return render(request,'home.html')
#     else:
#         return render(request,'vmartHome.html')
#
# def pageUpdate2(request,pageNumber,toUser,clientId,innerPageNumber,id_date1):
#     add2CartObjects=order_details.objects.filter(client_id=clientId, order_status="a2c",customer_number=toUser)
#
#     if len(add2CartObjects) != 0:
#         for add2CartObjects_i in  add2CartObjects:
#             a2cPageCreateObjects = order_details.objects.get(id=add2CartObjects_i.id)
#             a2cPageCreateObjects.bot_page_count_1 = pageNumber
#             a2cPageCreateObjects.bot_modify_page = innerPageNumber
#             a2cPageCreateObjects.save()
#
# def pageUpdate(request,pageNumber,toUser,clientId,innerPageNumber,id_date1):
#     pageUpdate2(request,pageNumber,toUser,clientId,innerPageNumber,id_date1)
#     trackPageCreateObjects = customer_track_page.objects.get(tp_customer_number=toUser, client_id=clientId)
#     trackPageCreateObjects.tp_bot_page_count_1 = pageNumber
#     trackPageCreateObjects.tp_bot_modify_page = innerPageNumber
#     trackPageCreateObjects.save()
#
# def simpleMessageDesign(request,url,headers,toUser,Dynamic_Message,id_date1,clientId):
#
#     payload = json.dumps({
#         "messaging_product": "whatsapp",
#         "recipient_type": "individual",
#         "to": toUser,
#         "type": "text",
#         "text": {
#             "body":Dynamic_Message
#         }
#     })
#
#     response = requests.request("POST", url, headers=headers, data=payload)
#     counterSent(request, clientId, id_date1)
#
#     return 'hi'
#
# def addCartDesignBtn(request,url,headers,toUser,clientId,id_date1):
#     pd1_a2c_object = order_details.objects.filter(client_id=clientId, order_status="a2c",
#                                                   customer_number=toUser, )
#     pd1_cart_d = ''
#     pd1_cart_count = 1
#     Total_amount = 0
#     for pd1_i in pd1_a2c_object:
#         pd1_pdt_object = product_info.objects.filter(id=pd1_i.product_fk_id)
#         for pd2_i in pd1_pdt_object:
#             chart_len = pd2_i.product_name.capitalize()
#             if len(chart_len) < 5:
#                 ch = chart_len.ljust(13, ' ')
#                 pd1_cart_d = pd1_cart_d + str(
#                     pd1_cart_count) + ". " + ch + '             ' + str(
#                     pd1_i.product_quantity) + '       ' + str(pd1_i.product_value) + '\n'
#                 pd1_cart_count = pd1_cart_count + 1
#                 Total_amount = Total_amount + pd1_i.product_value
#             else:
#                 ch = chart_len.ljust(11, ' ')
#
#                 pd1_cart_d = pd1_cart_d + str(
#                     pd1_cart_count) + ". " + ch + '             ' + str(
#                     pd1_i.product_quantity) + '       ' + str(pd1_i.product_value) + '\n'
#                 pd1_cart_count = pd1_cart_count + 1
#                 Total_amount = Total_amount + pd1_i.product_value
#     # print(pd1_cart_d)
#     # print(pd1_cart_count)
#
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
#                 "text": ' *Your Cart Details* :\n\n' + "  Items" + '                  ' + " Qty " + '  ' + "Price(Rs)" + '\n\n' + pd1_cart_d
#             },
#             "footer": {
#                 "text": "\t\t\tTotal Amount  : " + " *" + str(Total_amount) + '* '
#             },
#             "action": {
#                 "buttons": [
#                     {
#                         "type": "reply",
#                         "reply": {
#                             "id": "unique-id-113",
#                             "title": "Shop More"
#                         }
#                     },
#                     {
#                         "type": "reply",
#                         "reply": {
#                             "id": "unique-id-114",
#                             "title": "Modify"
#                         }
#                     },
#                     {
#                         "type": "reply",
#                         "reply": {
#                             "id": "unique-id-115",
#                             "title": "Check Out"
#                         }
#                     }
#
#                 ]
#             }
#         }
#     })
#
#     response = requests.request("POST", url, headers=headers, data=payload)
#     counterSent(request, clientId, id_date1)
#
# def addCartDesign(request,url,headers,toUser,clientId,id_date1):
#     pd1_a2c_object = order_details.objects.filter(client_id=clientId, order_status="a2c",
#                                                   customer_number=toUser, )
#     pd1_cart_d = ''
#     pd1_cart_count = 1
#     Total_amount = 0
#     for pd1_i in pd1_a2c_object:
#         pd1_pdt_object = product_info.objects.filter(id=pd1_i.product_fk_id)
#         for pd2_i in pd1_pdt_object:
#             chart_len = pd2_i.product_name.capitalize()
#             if len(chart_len) < 5:
#                 ch = chart_len.ljust(13, ' ')
#                 pd1_cart_d = pd1_cart_d + str(
#                     pd1_cart_count) + ". " + ch + '             ' + str(
#                     pd1_i.product_quantity) + '       ' + str(pd1_i.product_value) + '\n'
#                 pd1_cart_count = pd1_cart_count + 1
#                 Total_amount = Total_amount + pd1_i.product_value
#             else:
#                 ch = chart_len.ljust(11, ' ')
#
#                 pd1_cart_d = pd1_cart_d + str(
#                     pd1_cart_count) + ". " + ch + '             ' + str(
#                     pd1_i.product_quantity) + '       ' + str(pd1_i.product_value) + '\n'
#                 pd1_cart_count = pd1_cart_count + 1
#                 Total_amount = Total_amount + pd1_i.product_value
#
#     # print(pd1_cart_d)
#     # print(pd1_cart_count)
#
#     payload = json.dumps({
#         "messaging_product": "whatsapp",
#         "recipient_type": "individual",
#         "to": toUser,
#         "type": "text",
#         "text": {
#             "body": ' *Your Cart Details* :\n\n' + "  Items" + '                  ' + " Qty " + '  ' + "Price(Rs)" + '\n\n' + pd1_cart_d + "\n\n\t\t\tTotal Amount  : " + " *" + str(
#                 Total_amount) + '* '
#         }
#     })
#
#     response = requests.request("POST", url, headers=headers, data=payload)
#     counterSent(request, clientId, id_date1)
#
# def emptyCart(request,url,headers,toUser,clientId,id_date1):
#
#     payload = json.dumps({
#         "messaging_product": "whatsapp",
#         "recipient_type": "individual",
#         "to": toUser,
#         "type": "interactive",
#         "interactive": {
#             "type": "button",
#
#             "body": {
#                 "text": "Your Cart is Empty!"
#             },
#             "action": {
#                 "buttons": [
#                     {
#                         "type": "reply",
#                         "reply": {
#                             "id": "unique-id-109",
#                             "title": "Shop More"
#                         }
#                     },
#                     {
#                         "type": "reply",
#                         "reply": {
#                             "id": "unique-id-110",
#                             "title": "Modify"
#                         }
#                     },
#                     {
#                         "type": "reply",
#                         "reply": {
#                             "id": "unique-id-111",
#                             "title": "Check Out"
#                         }
#                     },
#
#                 ]
#             }
#         }
#     })
#
#     response = requests.request("POST", url, headers=headers, data=payload)
#     counterSent(request, clientId, id_date1)
#
#
#
# class BotView(generic.View):
#
#     def get(self, request, *args, **kwargs):
#         # print(request.build_absolute_uri(), '11111111111111111111111111')
#         urlThis=str(request.build_absolute_uri())
#         # print('>>>>>',urlThis,'<<<<<')
#         b = urlThis.split('?')
#         c = b[0]
#         # print(b[0])
#         # print(c[-22:])
#         vMartCilentId=c[-22:]
#         clientCallbackUrlObjects=admin_permission.objects.filter(client_auth_key=vMartCilentId)
#         vMartCilentsecretKey=''
#
#         for i in clientCallbackUrlObjects:
#             vMartCilentsecretKey=vMartCilentsecretKey+i.client_auth_secret
#         # print(vMartCilentId,'=============')
#         # print(vMartCilentsecretKey,'================')
#         if self.request.GET['hub.verify_token'] == vMartCilentsecretKey:
#             return HttpResponse(self.request.GET['hub.challenge'])
#         else:
#             return HttpResponse('Error, invalid token')
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return generic.View.dispatch(self, request, *args, **kwargs)  # Post function to handle Facebook messages
#
#     def post(self, request, *args, **kwargs):
#         # Converts the text payload into a python dictionary
#         incoming_message = json.loads(self.request.body.decode('utf-8'))
#         # print(incoming_message)
#         # url = 'https://vvvmart.herokuapp.com/re/'
#         url = DomainName+'re/'
#         payload = json.dumps(incoming_message)
#         headers = {
#
#             'Content-Type': 'application/json'
#         }
#         response = requests.request("POST", url, headers=headers, data=payload)
#
#
#
#         return HttpResponse()
#
#
#
# @csrf_exempt
# def MY_bOT(request):
#
#     url_for_domain = DomainName[:-1]
#
#     b = ''
#     for i in request:
#         b = b + str(i)[2:-1]
#
#     x = b.replace('true', 'True')
#     y = x.replace('false', 'False')
#     res = ast.literal_eval(y)
#
#
#     key_var = res['entry'][0]['changes'][0]['value'].keys()
#     condition_list = list(key_var)
#
#     if 'messages' in condition_list:
#         messageType = res['entry'][0]['changes'][0]['value']['messages'][0]['type']
#         whatsAppPhoneNumberId = res['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
#         toUser = res['entry'][0]['changes'][0]['value']['messages'][0]['from']
#
#         facebookObjects = facebook_details.objects.filter(fb_phone_number_id=whatsAppPhoneNumberId)
#         faceBookToken = ''
#         businessName = ''
#         clientId = 0
#         for tok in facebookObjects:
#             faceBookToken = faceBookToken + tok.fb_access_token
#             businessName = businessName + tok.fb_name
#             clientId = clientId + tok.client_id
#
#
#     #________________________________date()_________________________________________
#         day_date = ''
#         id_date = ''
#         #________________________________receive____________________________________
#         clientMessageObject_r = client_received_messages.objects.filter(client_id=clientId)
#         for i_k in clientMessageObject_r:
#             if str(now.date()) == str(i_k.message_date.date()):
#                 day_date = day_date + str(i_k.message_date.date())
#                 id_date = id_date + str(i_k.id)
#                 # print(i_k.message_date.date())
#         print('___________',day_date,'====',id_date)
#
#         #_________________________send___________________
#         clientMessageObject_s = client_sent_messages.objects.filter(client_id=clientId)
#         day_date1 = ''
#         id_date1 = ''
#
#         for i_kzz in clientMessageObject_s:
#             if str(now.date()) == str(i_kzz.message_date.date()):
#                 day_date1 = day_date1 + str(i_kzz.message_date.date())
#                 id_date1 = id_date1 + str(i_kzz.id)
#                 # print(i_kzz.s_date_for_now.date())
#
#         print("+++++++",day_date1,id_date1)
#
#         #_________________________________counts______________________________
#
#
#         if id_date=='':
#             counterReceive(request,clientId)
#         else:
#             count_messages_2 = client_received_messages.objects.get(id=int(id_date))
#             count_messages_2.r_day_count = count_messages_2.r_day_count + 1
#             count_messages_2.save()
#
# #________________________________________Api Details_________________________________________
#
#         print('client ID : ',clientId)
#         # print('Token : ',faceBookToken)
#         # print('Business Name : ',businessName)
#         # print('To : ',toUser)
#         # print('Phone Number Id : ',whatsAppPhoneNumberId)
#         # print('message types',messageType)
#
# # ____________________________________API URL and HEADERS__________________________________
#
#         url = "https://graph.facebook.com/v12.0/" + str(whatsAppPhoneNumberId) + "/messages"
#         headers = {
#             'Authorization': 'Bearer ' + faceBookToken,
#             'Content-Type': 'application/json'
#         }
#
# # __________________________________________________________________________________________
#         customer_tpObjects=customer_track_page.objects.filter(tp_customer_number=toUser,client_id=clientId)
#         print("__________",len(customer_tpObjects))
#         if len(customer_tpObjects)==0:
#             trackPageCreateObjects = customer_track_page()
#             trackPageCreateObjects.tp_customer_number=toUser
#             trackPageCreateObjects.tp_bot_page_count_1 = 0
#             trackPageCreateObjects.client_id=clientId
#             trackPageCreateObjects.save()
#
#         customer_AddressObjects = customer_address.objects.filter(customer_number=toUser, client_id=clientId)
#
#         if len(customer_AddressObjects) == 0:
#             trackPageCreateObjects = customer_address()
#             trackPageCreateObjects.customer_number = toUser
#             trackPageCreateObjects.bot_page_count = 8
#             trackPageCreateObjects.client_id = clientId
#             trackPageCreateObjects.save()
#         adminPermissionObjects=admin_permission.objects.filter(client_id=clientId)
#         for clientIdI in adminPermissionObjects:
#             if clientIdI.client_permission==True:
#
#                 if messageType == 'text':
#
#                     message = res['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
#
#                     # _________________________________first message_____________________________
#                     page_object = customer_track_page.objects.filter(tp_customer_number=toUser, client_id=clientId)
#                     botModifyPage = 0
#                     botPageCount1 = 0
#                     botPageCount2 = ''
#
#                     for page_object_i in page_object:
#                         botModifyPage = botModifyPage + page_object_i.tp_bot_modify_page
#                         botPageCount1 = botPageCount1 + page_object_i.tp_bot_page_count_1
#                         botPageCount2 = botPageCount2 + page_object_i.tp_bot_page_count_2
#                     print(botModifyPage, 'mp')
#                     print(botPageCount1, 'c1')
#                     print(botPageCount2, 'c2')
#
#                     if message == 'HI' or message == 'Hi' or message == 'hi' or message == 'hI':
#
#                         pageNumber = 1
#                         innerPageNumber = 0
#                         pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                         payload = json.dumps({
#
#                             "messaging_product": "whatsapp",
#                             "recipient_type": "individual",
#                             "to": toUser,
#                             "type": "interactive",
#                             "interactive": {
#                                 "type": "button",
#                                 "header": {
#                                     "type": "image",
#                                     "image": {
#                                         "link": "https://ubotnext.herokuapp.com/static/image/Alphonso.png"
#                                     }
#                                 },
#                                 "body": {
#                                     "text": "Welcome to our *" + businessName.capitalize() + '* '
#                                 },
#                                 "footer": {
#                                     "text": "Our Shop Is there in your hand...keep enjoy!"
#                                 },
#                                 "action": {
#                                     "buttons": [
#                                         {
#                                             "type": "reply",
#                                             "reply": {
#                                                 "id": "unique-id-123",
#                                                 "title": "Shop"
#                                             }
#                                         },
#                                         {
#                                             "type": "reply",
#                                             "reply": {
#                                                 "id": "unique-id-124",
#                                                 "title": "Check Status"
#                                             }
#                                         },
#                                         {
#                                             "type": "reply",
#                                             "reply": {
#                                                 "id": "unique-id-125",
#                                                 "title": "Contact Us"
#                                             }
#                                         }
#
#                                     ]
#                                 }
#                             }
#                         })
#
#                         response = requests.request("POST", url, headers=headers, data=payload)
#                         counterSent(request, clientId, id_date1)
#
#
#
#
#                     elif message[0:10] == 'Cart ID : ':
#                         print(">>>>>>Cart ID<<<<<<<<")
#                         print(message[10:])
#                         card_Id = order_details.objects.filter(js_cartid=message[10:])
#                         card_count = order_details.objects.filter(customer_number=toUser)
#                         card_count_a2c = order_details.objects.filter(customer_number=toUser, order_status='a2c')
#
#                         print(card_Id)
#
#                         if len(card_Id) != 0:
#                             for card_Id_i1 in card_Id:
#                                 addNumber = order_details.objects.get(id=card_Id_i1.id)
#                                 addNumber.customer_number = str(toUser)
#                                 addNumber.save()
#
#                             filter1 = order_details.objects.filter(customer_number=toUser, order_status='a2c')
#
#                             flit_list = []
#                             flit_list_id = []
#                             for flit_i in filter1:
#                                 print(flit_i.product_fk_id)
#                                 flit_list.append(flit_i.product_fk_id)
#                                 flit_list_id.append(flit_i.id)
#                             print("hihihi", flit_list, flit_list_id)
#                             for i_list in range(len(flit_list)):
#                                 flit_objects = order_details.objects.filter(customer_number=toUser, order_status='a2c',
#                                                                             id=flit_list_id[i_list])
#                                 for j_list in range(i_list + 1, len(flit_list)):
#                                     if flit_list[i_list] == flit_list[j_list]:
#                                         flit_objects_filter = order_details.objects.filter(id=flit_list_id[j_list])
#                                         for zz_i in flit_objects_filter:
#                                             flit_objects_get = order_details.objects.get(id=flit_list_id[i_list])
#                                             flit_objects_get.product_quantity = flit_objects_get.product_quantity + zz_i.product_quantity
#                                             flit_objects_get.product_value = flit_objects_get.product_value + zz_i.product_value
#                                             flit_objects_get.save()
#                                         flit_objects_delete = order_details.objects.get(id=flit_list_id[j_list])
#                                         flit_objects_delete.delete()
#                                     else:
#                                         pass
#
#                             pd1_a2c_object = order_details.objects.filter(client_id=clientId, order_status="a2c",
#                                                                           customer_number=toUser)
#                             pd1_cart_d = ''
#                             pd1_cart_count = 1
#                             Total_amount = 0
#                             for pd1_i in pd1_a2c_object:
#                                 pd1_pdt_object = product_info.objects.filter(id=pd1_i.product_fk_id)
#                                 for pd2_i in pd1_pdt_object:
#                                     chart_len = pd2_i.product_name.capitalize()
#                                     if len(chart_len) < 5:
#                                         ch = chart_len.ljust(13, ' ')
#                                         pd1_cart_d = pd1_cart_d + str(
#                                             pd1_cart_count) + ". " + ch + '             ' + str(
#                                             pd1_i.product_quantity) + '       ' + str(pd1_i.product_value) + '\n'
#                                         pd1_cart_count = pd1_cart_count + 1
#                                         Total_amount = Total_amount + pd1_i.product_value
#                                     else:
#                                         ch = chart_len.ljust(11, ' ')
#
#                                         pd1_cart_d = pd1_cart_d + str(
#                                             pd1_cart_count) + ". " + ch + '             ' + str(
#                                             pd1_i.product_quantity) + '       ' + str(pd1_i.product_value) + '\n'
#                                         pd1_cart_count = pd1_cart_count + 1
#                                         Total_amount = Total_amount + pd1_i.product_value
#                             print(pd1_cart_d)
#                             print(pd1_cart_count)
#
#                             payload = json.dumps({
#                                 "messaging_product": "whatsapp",
#                                 "recipient_type": "individual",
#                                 "to": toUser,
#                                 "type": "interactive",
#                                 "interactive": {
#                                     "type": "button",
#
#                                     "body": {
#                                         "text": ' *Your Cart Details* :\n\n' + "  Items" + '                  ' + " Qty " + '  ' + "Price(Rs)" + '\n\n' + pd1_cart_d
#                                     },
#                                     "footer": {
#                                         "text": "\t\t\tTotal Amount  : " + " *" + str(Total_amount) + '* '
#                                     },
#                                     "action": {
#                                         "buttons": [
#                                             {
#                                                 "type": "reply",
#                                                 "reply": {
#                                                     "id": "unique-id-113",
#                                                     "title": "Shop More"
#                                                 }
#                                             },
#                                             {
#                                                 "type": "reply",
#                                                 "reply": {
#                                                     "id": "unique-id-114",
#                                                     "title": "Modify"
#                                                 }
#                                             },
#                                             {
#                                                 "type": "reply",
#                                                 "reply": {
#                                                     "id": "unique-id-115",
#                                                     "title": "Check Out"
#                                                 }
#                                             }
#
#                                         ]
#                                     }
#                                 }
#                             })
#
#                             response = requests.request("POST", url, headers=headers, data=payload)
#                             counterSent(request, clientId, id_date1)
#
#
#
#                         else:
#                             Dynamic_Message = 'Invalid cart id!'
#
#                             payload = json.dumps({
#                                 "messaging_product": "whatsapp",
#                                 "recipient_type": "individual",
#                                 "to": toUser,
#                                 "type": "interactive",
#                                 "interactive": {
#                                     "type": "button",
#
#                                     "body": {
#                                         "text": Dynamic_Message
#                                     },
#                                     "action": {
#                                         "buttons": [
#                                             {
#                                                 "type": "reply",
#                                                 "reply": {
#                                                     "id": "unique-id-109",
#                                                     "title": "Shop More"
#                                                 }
#                                             },
#                                             {
#                                                 "type": "reply",
#                                                 "reply": {
#                                                     "id": "unique-id-110",
#                                                     "title": "Modify"
#                                                 }
#                                             },
#                                             {
#                                                 "type": "reply",
#                                                 "reply": {
#                                                     "id": "unique-id-111",
#                                                     "title": "Check Out"
#                                                 }
#                                             },
#
#                                         ]
#                                     }
#                                 }
#                             })
#
#                             response = requests.request("POST", url, headers=headers, data=payload)
#                             counterSent(request, clientId, id_date1)
#
#
#
#                     elif botPageCount1 == 7 and message == message:
#
#                         if botPageCount1 == 7 and botModifyPage == 1:
#                             print('line number')
#                             modifyCount2 = order_details.objects.filter(customer_number=toUser, client_id=clientId,
#                                                                         order_status='a2c')
#                             try:
#                                 userInput = int(message)
#                             except ValueError:
#                                 Dynamic_Message = 'Sorry,invalid reply! please give\n correct *line number*.'
#                                 simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                             else:
#                                 print(userInput)
#                                 print(type(userInput))
#                                 if len(modifyCount2) >= userInput and userInput != 0 and userInput >= 0:
#                                     varr = 1
#                                     for iii in modifyCount2:
#                                         if varr == int(message):
#                                             modify_object2 = order_details.objects.get(id=iii.id)
#                                             modify_object2.bot_page_count_2 = "T"
#                                             modify_object2.save()
#
#                                             modify_object3 = customer_track_page.objects.get(tp_customer_number=toUser,
#                                                                                              client_id=clientId)
#                                             modify_object3.tp_bot_page_count_2 = "T"
#                                             modify_object3.save()
#                                         varr = varr + 1
#
#                                     pageNumber = 7
#                                     innerPageNumber = 2
#                                     pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                                     Dynamic_Message = 'Please send how many quantity\n want or suppose you want to\n delete sent " *0* "'
#                                     simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                                 elif len(modifyCount2) < userInput or userInput == 0:
#                                     lineNUmber = len(modifyCount2)
#                                     Dynamic_Message = 'Sorry you have ' + str(
#                                         lineNUmber) + 'lines only,but you not given correct line.'
#                                     simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                                 elif len(modifyCount2) > 10:
#                                     Dynamic_Message = 'invalid reply!'
#                                     simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#                                 else:
#                                     Dynamic_Message = 'invalid reply!'
#                                     simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#
#                         elif botPageCount1 == 7 and botModifyPage == 2:
#                             print('Product Qty')
#
#                             modifyCount2 = order_details.objects.filter(customer_number=toUser, client_id=clientId,
#                                                                         order_status='a2c', bot_page_count_2='T')
#                             try:
#                                 userInput = int(message)
#                             except ValueError:
#                                 Dynamic_Message = 'Sorry,invalid reply! please give\n correct *Quantity numbers*.'
#                                 simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#
#                             else:
#                                 if int(message) == 0:
#                                     for message_i in modifyCount2:
#                                         deleteLineObject = order_details.objects.get(id=message_i.id)
#                                         deleteLineObject.delete()
#                                     pageNumber = 7
#                                     innerPageNumber = 0
#                                     pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#                                     addCartDesignBtn(request, url, headers, toUser, clientId,id_date1)
#
#                                 elif int(message) != 0 and int(message) > 0:
#                                     if int(message) <= 10:
#                                         for message_i in modifyCount2:
#                                             addQtyLineObject = order_details.objects.get(id=message_i.id)
#                                             addQtyLineObject.product_quantity = int(message)
#                                             addQtyLineObject.product_value = addQtyLineObject.product_price * addQtyLineObject.product_quantity
#                                             addQtyLineObject.bot_page_count_2 = 'F'
#                                             addQtyLineObject.save()
#                                         modify_object3 = customer_track_page.objects.get(tp_customer_number=toUser,
#                                                                                          client_id=clientId)
#                                         modify_object3.tp_bot_page_count_2 = "F"
#                                         modify_object3.save()
#
#                                         pageNumber = 7
#                                         innerPageNumber = 0
#                                         pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#                                         emtyObject = order_details.objects.filter(customer_number=toUser,
#                                                                                   client_id=clientId,
#                                                                                   order_status='a2c')
#                                         if len(emtyObject) == 0:
#                                             pass
#                                         else:
#                                             addCartDesignBtn(request, url, headers, toUser, clientId,id_date1)
#
#                                     else:
#                                         Dynamic_Message = 'This is to much of quantitys ,so we are provide only 10Qty ,if you want contact help line'
#                                         simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#
#                                 else:
#                                     Dynamic_Message = 'Invalid,Give a proper numbers'
#                                     simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                     elif botPageCount1 == 8 and message == message:
#                         if botPageCount1 == 8 and botModifyPage == 1:
#
#                             fillAddressObject = customer_address.objects.get(customer_number=toUser, client_id=clientId,
#                                                                              bot_page_count=8)
#                             fillAddressObject.customer_name = message
#                             fillAddressObject.save()
#
#                             pageNumber = 8
#                             innerPageNumber = 2
#                             pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                             Dynamic_Message = " *Your shipping address is :* \n\n\t\t\t\t\t\t\t\t  Name   *:  " + message + "*\n Address Line 1  *:  _______________*\nArea/Landmark  *:  _______________*\n\t\t\t\t\t\t\t\tPincode  *:  _______________* "
#                             simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                             Dynamic_Message = '\tPlease fill *Address Line 1* '
#                             simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                         elif botPageCount1 == 8 and botModifyPage == 2:
#                             customerName = ''
#                             fillAddressObject = customer_address.objects.get(customer_number=toUser, client_id=clientId,
#                                                                              bot_page_count=8)
#                             fillAddressObject.customer_addressline1 = message
#                             customerName = customerName + fillAddressObject.customer_name
#                             fillAddressObject.save()
#
#                             pageNumber = 8
#                             innerPageNumber = 3
#                             pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                             Dynamic_Message = " *Your shipping address is :* \n\n\t\t\t\t\t\t\t\t  Name   *:  " + customerName + "*\n Address Line 1  *:  " + message + "*\nArea/Landmark  *:  _______________*\n\t\t\t\t\t\t\t\tPincode  *:  _______________* "
#                             simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                             Dynamic_Message = '\tPlease fill *Area/Landmark* '
#                             simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                         elif botPageCount1 == 8 and botModifyPage == 3:
#                             customerName = ''
#                             customerAddressLine1 = ''
#                             fillAddressObject = customer_address.objects.get(customer_number=toUser, client_id=clientId,
#                                                                              bot_page_count=8)
#                             fillAddressObject.customer_area = message
#                             customerName = customerName + fillAddressObject.customer_name
#                             customerAddressLine1 = customerAddressLine1 + fillAddressObject.customer_addressline1
#                             fillAddressObject.save()
#
#                             pageNumber = 8
#                             innerPageNumber = 4
#                             pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                             Dynamic_Message = " *Your shipping address is :* \n\n\t\t\t\t\t\t\t\t  Name   *:  " + customerName + "*\n Address Line 1  *:  " + customerAddressLine1 + "*\nArea/Landmark  *:  " + message + "*\n\t\t\t\t\t\t\t\tPincode  *:  _______________* "
#                             simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                             Dynamic_Message = '\tPlease fill *Pincode* '
#                             simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                         elif botPageCount1 == 8 and botModifyPage == 4:
#
#                             try:
#                                 userInput = int(message)
#                             except ValueError:
#                                 Dynamic_Message = 'Sorry,invalid reply! please give\n correct *PINcode*.'
#                                 simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#                             else:
#                                 if len(message) == 6:
#                                     customerName = ''
#                                     customerAddressLine1 = ''
#                                     customerLandmark = ''
#                                     fillAddressObject = customer_address.objects.get(customer_number=toUser,
#                                                                                      client_id=clientId,
#                                                                                      bot_page_count=8)
#                                     fillAddressObject.customer_pincode = message
#                                     fillAddressObject.customer_addressline2 = 'yes'
#                                     customerName = customerName + fillAddressObject.customer_name
#                                     customerAddressLine1 = customerAddressLine1 + fillAddressObject.customer_addressline1
#                                     customerLandmark = customerLandmark + fillAddressObject.customer_area
#                                     fillAddressObject.save()
#
#                                     pageNumber = 8
#                                     innerPageNumber = 5
#                                     pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                                     pd1_a2c_object = order_details.objects.filter(customer_number=toUser,
#                                                                                   client_id=clientId,
#                                                                                   order_status='a2c')
#                                     pd1_cart_d = ''
#                                     pd1_cart_count = 1
#                                     Total_amount = 0
#                                     for pd1_i in pd1_a2c_object:
#                                         pd1_pdt_object = product_info.objects.filter(id=pd1_i.product_fk_id)
#                                         for pd2_i in pd1_pdt_object:
#                                             chart_len = pd2_i.product_name.capitalize()
#                                             if len(chart_len) < 5:
#                                                 ch = chart_len.ljust(13, ' ')
#                                                 pd1_cart_d = pd1_cart_d + str(
#                                                     pd1_cart_count) + ". " + ch + '             ' + str(
#                                                     pd1_i.product_quantity) + '       ' + str(
#                                                     pd1_i.product_value) + '\n'
#                                                 pd1_cart_count = pd1_cart_count + 1
#                                                 Total_amount = Total_amount + pd1_i.product_value
#                                             else:
#                                                 ch = chart_len.ljust(11, ' ')
#
#                                                 pd1_cart_d = pd1_cart_d + str(
#                                                     pd1_cart_count) + ". " + ch + '             ' + str(
#                                                     pd1_i.product_quantity) + '       ' + str(
#                                                     pd1_i.product_value) + '\n'
#                                                 pd1_cart_count = pd1_cart_count + 1
#                                                 Total_amount = Total_amount + pd1_i.product_value
#                                     # print(pd1_cart_d)
#                                     # print(pd1_cart_count)
#
#                                     # Dynamic_Message = ' *Your Cart Details* :\n\n' + "  Items" + '                  ' + " Qty " + '  ' + "Price(Rs)" + '\n\n' + pd1_cart_d + "\n" + '______________________________\n\n' + " *Your shipping address is :* \n\n *" + customerName + "*\n *" + customerAddressLine1 + "* \n *" + customerLandmark + "* \n Pincode  *:  " + message + "* \n" + '______________________________\n' + "\n\t\t\t\t\t\tTotal Amount  : " + " *" + str(
#                                     #                 Total_amount) + '* '
#                                     # simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                                     payload = json.dumps({
#
#                                         "messaging_product": "whatsapp",
#                                         "recipient_type": "individual",
#                                         "to": toUser,
#                                         "type": "interactive",
#                                         "interactive": {
#                                             "type": "button",
#
#                                             "body": {
#                                                 "text": ' *Your Cart Details* :\n\n' + "  Items" + '                  ' + " Qty " + '  ' + "Price(Rs)" + '\n\n' + pd1_cart_d + "\n" + '______________________________\n\n' + " *Your shipping address is :* \n\n *" + customerName + "*\n *" + customerAddressLine1 + "* \n *" + customerLandmark + "* \n Pincode  *:  " + message + "* \n" + '______________________________\n' + "\n\t\t\t\t\t\tTotal Amount  : " + " *" + str(
#                                                     Total_amount) + '* '
#                                             },
#
#                                             "action": {
#                                                 "buttons": [
#                                                     {
#                                                         "type": "reply",
#                                                         "reply": {
#                                                             "id": "unique-id-121",
#                                                             "title": "Continue To Pay"
#                                                         }
#                                                     },
#                                                     {
#                                                         "type": "reply",
#                                                         "reply": {
#                                                             "id": "unique-id-123",
#                                                             "title": "Modify Address"
#                                                         }
#                                                     },
#                                                     {
#                                                         "type": "reply",
#                                                         "reply": {
#                                                             "id": "unique-id-122",
#                                                             "title": "Modify Cart"
#                                                         }
#                                                     }
#
#                                                 ]
#                                             }
#                                         }
#                                     })
#
#                                     response = requests.request("POST", url, headers=headers, data=payload)
#                                     counterSent(request, clientId, id_date1)
#
#
#                                 else:
#                                     Dynamic_Message = 'Sorry,invalid reply! please give\n correct *PINcode*.'
#                                     simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                         elif botPageCount1 == 8 and botModifyPage == 5:
#                             pass
#
#                 elif messageType == 'interactive':
#
#                     # print("_____________________________interactive Message REply_____________________________")
#                     button_type = res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['type']
#
#                     if button_type == 'button_reply':
#
#                         # print("_____________________________Button Replay Message REply_____________________________")
#                         button_text = \
#                         res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['button_reply'][
#                             'title']
#
#                         # __________________________________________________________________________________________________________-------
#
#                         if button_text == 'Shop' or button_text == 'Shop More':
#
#                             pageNumber = 2
#                             innerPageNumber = 0
#                             pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                             product_cat = []
#                             product_desc = []
#                             ll1 = product_category.objects.filter(client_id=clientId)
#
#                             for l2_i in ll1:
#                                 product_cat.append(l2_i.product_category_name.capitalize())
#                                 product_desc.append(l2_i.product_category_Description.capitalize())
#
#                             categoryList = []
#                             for categoryList_i in range(len(product_cat)):
#                                 categoryList.append({"id": "unique-id-12" + str(categoryList_i),
#                                                      "title": product_cat[categoryList_i],
#                                                      "description": product_desc[categoryList_i]})
#
#                             payload = json.dumps({
#                                 "messaging_product": "whatsapp",
#                                 "recipient_type": "individual",
#                                 "to": toUser,
#                                 "type": "interactive",
#                                 "interactive": {
#                                     "type": "list",
#                                     "header": {
#                                         "type": "text",
#                                         "text": "Our Catagory"
#                                     },
#                                     "body": {
#                                         "text": "Welcome to Our siteBot"
#                                     },
#                                     "footer": {
#                                         "text": "Click to Shop"
#                                     },
#                                     "action": {
#                                         "button": "Our Catalogue",
#                                         "sections": [
#                                             {
#                                                 "title": "____PART A____",
#                                                 "rows": categoryList
#                                             },
#
#                                         ]
#                                     }
#                                 }
#                             })
#
#                             response = requests.request("POST", url, headers=headers, data=payload)
#                             counterSent(request,clientId,id_date1)
#
#
#                         # ----------------------------------------------------------------------------------------------
#
#                         elif button_text == 'Check Status':
#
#                             pageNumber = 3
#                             innerPageNumber = 0
#                             pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                             Dynamic_Message = 'Now Its Not Working ...Process going on...'
#                             simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                         # ----------------------------------------------------------------------------------------------
#
#                         elif button_text == 'Contact Us':
#
#                             pageNumber = 4
#                             innerPageNumber = 0
#                             pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                             Dynamic_Message = 'Now Its Not Working ...Process going on...'
#                             simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                         # ----------------------------------------------------------------------------------------------
#
#                         elif button_text == 'Check Out':
#
#                             pageNumber = 8
#                             innerPageNumber = 1
#                             pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#                             EmtyCheck = order_details.objects.filter(customer_number=toUser, client_id=clientId,
#                                                                      order_status='a2c')
#                             if len(EmtyCheck) != 0:
#                                 addressObject = customer_address.objects.filter(customer_number=toUser,
#                                                                                 client_id=clientId)
#                                 for address_objx_i in addressObject:
#                                     if ((address_objx_i.customer_name == '') and (
#                                             address_objx_i.customer_addressline1 == '') and (
#                                             address_objx_i.customer_area == '') and (
#                                             address_objx_i.customer_pincode == '')):
#                                         print("emty")
#
#                                         Dynamic_Message = ' *Your shipping address is :* \n\n\t\t\t\t\t\t\t\t  Name   *:  _______________*\n Address Line 1  *:  _______________*\nArea/Landmark  *:  _______________*\n\t\t\t\t\t\t\t\tPincode  *:  _______________* '
#                                         simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                                         Dynamic_Message = '\t\t\tPleasefill *Name* '
#                                         simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                                     elif address_objx_i.customer_addressline2 == 'yes':
#                                         customerName = ''
#                                         customerAddressLine1 = ''
#                                         customerLandmark = ''
#                                         customerPincode = ''
#                                         fillAddressObject = customer_address.objects.filter(customer_number=toUser,
#                                                                                             client_id=clientId,
#                                                                                             bot_page_count=8)
#                                         for fill_i in fillAddressObject:
#                                             customerName = customerName + fill_i.customer_name
#                                             customerAddressLine1 = customerAddressLine1 + fill_i.customer_addressline1
#                                             customerLandmark = customerLandmark + fill_i.customer_area
#                                             customerPincode = customerPincode + fill_i.customer_pincode
#
#                                         pageNumber = 8
#                                         innerPageNumber = 5
#                                         pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                                         pd1_a2c_object = order_details.objects.filter(customer_number=toUser,
#                                                                                       client_id=clientId,
#                                                                                       order_status='a2c')
#                                         pd1_cart_d = ''
#                                         pd1_cart_count = 1
#                                         Total_amount = 0
#                                         for pd1_i in pd1_a2c_object:
#                                             pd1_pdt_object = product_info.objects.filter(id=pd1_i.product_fk_id)
#                                             for pd2_i in pd1_pdt_object:
#                                                 chart_len = pd2_i.product_name.capitalize()
#                                                 if len(chart_len) < 5:
#                                                     ch = chart_len.ljust(13, ' ')
#                                                     pd1_cart_d = pd1_cart_d + str(
#                                                         pd1_cart_count) + ". " + ch + '             ' + str(
#                                                         pd1_i.product_quantity) + '       ' + str(
#                                                         pd1_i.product_value) + '\n'
#                                                     pd1_cart_count = pd1_cart_count + 1
#                                                     Total_amount = Total_amount + pd1_i.product_value
#                                                 else:
#                                                     ch = chart_len.ljust(11, ' ')
#
#                                                     pd1_cart_d = pd1_cart_d + str(
#                                                         pd1_cart_count) + ". " + ch + '             ' + str(
#                                                         pd1_i.product_quantity) + '       ' + str(
#                                                         pd1_i.product_value) + '\n'
#                                                     pd1_cart_count = pd1_cart_count + 1
#                                                     Total_amount = Total_amount + pd1_i.product_value
#
#                                         payload = json.dumps({
#
#                                             "messaging_product": "whatsapp",
#                                             "recipient_type": "individual",
#                                             "to": toUser,
#                                             "type": "interactive",
#                                             "interactive": {
#                                                 "type": "button",
#
#                                                 "body": {
#                                                     "text": ' *Your Cart Details* :\n\n' + "  Items" + '                  ' + " Qty " + '  ' + "Price(Rs)" + '\n\n' + pd1_cart_d + "\n" + '______________________________\n\n' + " *Your shipping address is :* \n\n *" + customerName + "*\n *" + customerAddressLine1 + "* \n *" + customerLandmark + "* \n Pincode  *:  " + customerPincode + "* \n" + '______________________________\n' + "\n\t\t\t\t\t\tTotal Amount  : " + " *" + str(
#                                                         Total_amount) + '* '
#                                                 },
#
#                                                 "action": {
#                                                     "buttons": [
#                                                         {
#                                                             "type": "reply",
#                                                             "reply": {
#                                                                 "id": "unique-id-121",
#                                                                 "title": "Continue To Pay"
#                                                             }
#                                                         },
#                                                         {
#                                                             "type": "reply",
#                                                             "reply": {
#                                                                 "id": "unique-id-123",
#                                                                 "title": "Modify Address"
#                                                             }
#                                                         },
#                                                         {
#                                                             "type": "reply",
#                                                             "reply": {
#                                                                 "id": "unique-id-122",
#                                                                 "title": "Modify Cart"
#                                                             }
#                                                         }
#
#                                                     ]
#                                                 }
#                                             }
#                                         })
#
#                                         response = requests.request("POST", url, headers=headers, data=payload)
#                                         counterSent(request, clientId, id_date1)
#
#
#                             else:
#                                 emptyCart(request, url, headers, toUser,clientId,id_date1)
#
#                         # ----------------------------------------------------------------------------------------------
#
#                         elif button_text == 'Modify Address':
#                             EmtyCheck = order_details.objects.filter(customer_number=toUser, client_id=clientId,
#                                                                      order_status='a2c')
#                             if len(EmtyCheck) != 0:
#                                 removeAddressObject = customer_address.objects.get(customer_number=toUser,
#                                                                                    client_id=clientId,
#                                                                                    bot_page_count=8)
#                                 removeAddressObject.customer_name = ''
#                                 removeAddressObject.customer_addressline1 = ''
#                                 removeAddressObject.customer_addressline2 = ''
#                                 removeAddressObject.customer_area = ''
#                                 removeAddressObject.customer_pincode = ''
#                                 removeAddressObject.save()
#
#                                 pageNumber = 8
#                                 innerPageNumber = 1
#                                 pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                                 Dynamic_Message = ' *Your shipping address is :* \n\n\t\t\t\t\t\t\t\t  Name   *:  _______________*\n Address Line 1  *:  _______________*\nArea/Landmark  *:  _______________*\n\t\t\t\t\t\t\t\tPincode  *:  _______________* '
#                                 simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                                 Dynamic_Message = '\t\t\tPleasefill *Name* '
#                                 simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#
#                             else:
#                                 emptyCart(request, url, headers, toUser,clientId,id_date1)
#
#                         # ----------------------------------------------------------------------------------------------
#
#                         elif button_text == 'Modify' or button_text == 'Modify Cart':
#
#                             pageNumber = 7
#                             innerPageNumber = 1
#                             pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                             modify_object1 = order_details.objects.filter(client_id=clientId, customer_number=toUser,
#                                                                           order_status="a2c")
#
#                             if len(modify_object1) != 0:
#                                 # print("product there")
#                                 addCartDesign(request, url, headers, toUser, clientId,id_date1)
#                                 Dynamic_Message = 'Please type line number of the\n\t\t\t\t cart that you need to modify'
#                                 simpleMessageDesign(request, url, headers, toUser, Dynamic_Message,id_date1,clientId)
#                             else:
#                                 # print('product not there')
#                                 emptyCart(request, url, headers, toUser,clientId,id_date1)
#
#                         # ----------------------------------------------------------------------------------------------
#
#                         elif button_text == 'Continue To Pay':
#                             payment_objectsEmtyCheck = order_details.objects.filter(customer_number=toUser,
#                                                                                     client_id=clientId,
#                                                                                     order_status='a2c')
#                             if len(payment_objectsEmtyCheck) != 0:
#
#                                 payment_objects1 = order_details.objects.filter(customer_number=toUser,
#                                                                                 client_id=clientId,
#                                                                                 order_status='process')
#                                 for i_1 in payment_objects1:
#                                     process_object12 = order_details.objects.get(id=i_1.id)
#                                     process_object12.order_status = 'linked'
#                                     process_object12.save()
#
#                                 Totel_amount = 0
#                                 payment_objects2 = order_details.objects.filter(customer_number=toUser,
#                                                                                 client_id=clientId,
#                                                                                 order_status='a2c')
#                                 for i_2 in payment_objects2:
#                                     Totel_amount = Totel_amount + i_2.product_value
#
#                                 bb2 = url_for_domain + "/payments/" + toUser + str(clientId) + '/' + str(
#                                     Totel_amount) + '/'
#
#                                 payload = json.dumps({
#                                     "messaging_product": "whatsapp",
#
#                                     "to": toUser,
#
#                                     "text": {
#                                         "preview_url": True,
#                                         "body": bb2
#                                     }
#                                 })
#
#                                 response = requests.request("POST", url, headers=headers, data=payload)
#                                 counterSent(request, clientId, id_date1)
#
#
#                                 payment_objects3 = order_details.objects.filter(customer_number=toUser,
#                                                                                 client_id=clientId,
#                                                                                 order_status='a2c')
#                                 order_headerAmount = 0
#                                 order_headerQuantity = 0
#                                 for i_4 in payment_objects3:
#                                     order_headerAmount += i_4.product_value
#                                     order_headerQuantity += i_4.product_quantity
#
#                                 orderHeadObjects = order_header.objects.filter(customer_number=toUser,
#                                                                                client_id=clientId,
#                                                                                order_status='process')
#                                 if len(orderHeadObjects) == 0:
#                                     orderHeadCreate = order_header()
#                                     orderHeadCreate.customer_number = toUser
#                                     orderHeadCreate.order_date = now
#                                     orderHeadCreate.order_status = 'process'
#                                     orderHeadCreate.order_value = order_headerAmount
#                                     orderHeadCreate.order_quantity = order_headerQuantity
#                                     orderHeadCreate.order_id = ''
#                                     orderHeadCreate.payment_id = ''
#                                     orderHeadCreate.client_id = clientId
#                                     orderHeadCreate.save()
#
#                                 for i_3 in payment_objects3:
#                                     process_object12 = order_details.objects.get(id=i_3.id)
#                                     process_object12.order_status = 'process'
#                                     process_object12.save()
#
#                                 pageNumber = 10
#                                 innerPageNumber = 0
#                                 pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                             else:
#                                 emptyCart(request, url, headers, toUser,clientId,id_date1)
#
#                         # ----------------------------------------------------------------------------------------------
#
#                         elif button_text[-8:] == 'Add2Cart':
#                             print('add2cart')
#
#                             pageNumber = 6
#                             innerPageNumber = 0
#                             pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                             product_variable = button_text[:-9]
#                             product_Id = 0
#                             product_IdObjects = product_info.objects.filter(client_id=clientId,
#                                                                             product_name=product_variable)
#                             for product_IdObjects_i in product_IdObjects:
#                                 product_Id = product_Id + product_IdObjects_i.id
#                             print('user send add2cart product id', product_Id)
#                             add2CartObject = order_details.objects.filter(client_id=clientId, customer_number=toUser,
#                                                                           order_status="a2c", product_fk_id=product_Id)
#
#                             print(len(add2CartObject))
#                             if len(add2CartObject) == 0:
#
#                                 for product_var_i in product_IdObjects:
#                                     add2CartObject1 = order_details()
#                                     add2CartObject1.order_date = now
#                                     add2CartObject1.customer_number = toUser
#                                     add2CartObject1.order_status = 'a2c'
#                                     add2CartObject1.product_price = product_var_i.product_price
#                                     add2CartObject1.product_quantity = 1
#                                     add2CartObject1.product_value = product_var_i.product_price
#                                     add2CartObject1.bot_page_count_1 = pageNumber
#                                     add2CartObject1.product_fk_id = product_var_i.id
#                                     add2CartObject1.client_id = clientId
#                                     add2CartObject1.js_cartid = ''
#                                     add2CartObject1.save()
#
#                                 # __________________product details_________________________ *Your Cart Details* :\n\n' + ' *Items*
#                                 addCartDesignBtn(request, url, headers, toUser, clientId,id_date1)
#
#                             else:
#                                 # print('already there your product')
#                                 for product_var_i in product_IdObjects:
#                                     add2CartObject1 = order_details.objects.get(product_fk_id=product_var_i.id,
#                                                                                 client_id=clientId,
#                                                                                 customer_number=toUser,
#                                                                                 order_status="a2c")
#                                     add2CartObject1.product_quantity = add2CartObject1.product_quantity + 1
#                                     add2CartObject1.product_value = product_var_i.product_price * add2CartObject1.product_quantity
#                                     add2CartObject1.bot_page_count_1 = pageNumber
#                                     add2CartObject1.save()
#
#                                 # __________________product details_________________________ *Your Cart Details* :\n\n' + ' *Items*
#
#                                 addCartDesignBtn(request, url, headers, toUser, clientId,id_date1)
#
#                         # ----------------------------------------------------------------------------------------------
#
#                     # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#                     elif button_type == 'list_reply':
#                         # print("_____________________________List Message REply_____________________________")
#                         button_text = \
#                         res['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['list_reply'][
#                             'title']
#                         pageNumber = 5
#                         innerPageNumber = 0
#                         pageUpdate(request, pageNumber, toUser, clientId, innerPageNumber,id_date1)
#
#                         if product_category.objects.filter(client_id=clientId,
#                                                            product_category_name=button_text.lower()):
#                             categoryObject1 = product_category.objects.filter(client_id=clientId,
#                                                                               product_category_name=button_text.lower())
#                             for categoryObject1_i in categoryObject1:
#                                 zz_cata = product_info.objects.filter(product_category_id=categoryObject1_i.id,
#                                                                       client_id=clientId,
#                                                                       product_status=True)
#
#                                 print(len(zz_cata))
#
#                                 if len(zz_cata) != 0:
#                                     for categoryObject1_i in zz_cata:
#                                         payload = json.dumps({
#
#                                             "messaging_product": "whatsapp",
#                                             "recipient_type": "individual",
#                                             "to": toUser,
#                                             "type": "interactive",
#                                             "interactive": {
#                                                 "type": "button",
#                                                 "header": {
#                                                     "type": "image",
#                                                     "image": {
#                                                         "link": url_for_domain + '/media/' + str(
#                                                             categoryObject1_i.product_image)
#                                                     }
#
#                                                 },
#                                                 "body": {
#                                                     "text": " *" + categoryObject1_i.product_name.capitalize() + '* '
#                                                 },
#                                                 "footer": {
#                                                     "text": "Price:" + str(
#                                                         categoryObject1_i.product_price) + ', ~' + str(
#                                                         categoryObject1_i.product_mrp) + '~ ( *' + str(
#                                                         categoryObject1_i.product_offer) + '* %)'
#                                                 },
#                                                 "action": {
#                                                     "buttons": [
#                                                         {
#                                                             "type": "reply",
#                                                             "reply": {
#                                                                 "id": "199" + str(categoryObject1_i.product_id),
#                                                                 "title": categoryObject1_i.product_name.capitalize() + ' ' + "Add2Cart"
#                                                                 #
#                                                             }
#                                                         },
#                                                         # {
#                                                         #     "type": "reply",
#                                                         #     "reply": {
#                                                         #         "id": "200"+str(categoryObject1_i.product_id),
#                                                         #         "title": categoryObject1_i.product_name.capitalize()+' '+"ViewCart"
#                                                         #     }
#                                                         # }
#
#                                                     ]
#                                                 }
#                                             }
#                                         })
#
#                                         response = requests.request("POST", url, headers=headers, data=payload)
#                                         counterSent(request, clientId, id_date1)
#
#
#                                 else:
#                                     print('yes catalog not available')
#                                     emptyCart(request, url, headers, toUser,clientId,id_date1)
#
#             else:
#
#                 Dynamic_Message = 'This Shop Temporarily out of service'
#                 payload = json.dumps({
#                     "messaging_product": "whatsapp",
#                     "recipient_type": "individual",
#                     "to": toUser,
#                     "type": "text",
#                     "text": {
#                         "body": Dynamic_Message
#                     }
#                 })
#
#                 response = requests.request("POST", url, headers=headers, data=payload)
#
#     return HttpResponse('hi')