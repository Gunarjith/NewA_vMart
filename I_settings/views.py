from django.shortcuts import render,redirect
from vailodb.models import admin_permission, facebook_details

from A_vMart.settings import DomainName
from django.http import HttpResponse,JsonResponse
#
# # Create your views here.
# from A_webhook.models import order_details

# from I_settings.models import client_table_count,client_table_links
# from E_product.models import product_info,product_category
import secrets
import json
from json import dumps
#
#
#
#
# # import pyqrcode
# # import png
# # from pyqrcode import QRCode
#
# # from PIL import Image
# # import PIL
#
# # from django.contrib.sites.shortcuts import get_current_site
#
def settings(request):
    cliendId = ''
    cliendSecrat = ''
    clientStatus=''

    ClientObject=admin_permission.objects.filter(client_id=request.user.id)
    # ClientObject1=client_table_count.objects.filter(client_id=request.user.id)
    # LinksObject = client_table_links.objects.filter(client_id=request.user.id)
    for statusI in ClientObject:
        clientStatus=clientStatus+statusI.client_type

    for ii in ClientObject:
        cliendId = cliendId + ii.client_auth_key
        cliendSecrat = cliendSecrat + ii.client_auth_secret

    CallbackUrl = DomainName + 'webhook/' + cliendId
    VerifyToken = cliendSecrat

    clientName = 'a'
    # for kk in facebook_details.objects.filter(client_id=request.user.id):
    #     clientName = clientName + kk.fb_name

    ClientMenuUrl = DomainName + clientName + '/' + secrets.token_hex(16)

    print(clientStatus)
    if clientStatus=='online':

        if len(ClientObject) == 1:
            # Link=''
            # for k in LinksObject:
            #     Link+=k.table_link
            return render(request, 'I_settings/setting.html',
                      {'already':['F'],'CallbackUrl': CallbackUrl, 'VerifyToken': VerifyToken, 'ClientMenuUrl': ClientMenuUrl,
                       'action':['online']})

        else:

            return render(request, 'I_settings/setting.html',
                          { 'already': ['T'],'CallbackUrl': CallbackUrl, 'VerifyToken': VerifyToken, 'ClientMenuUrl': ClientMenuUrl,
                           'action': ['online'],'Linky':'ABA'})

    elif clientStatus=='offline':
        return render(request, 'I_settings/setting.html',
                      {'CallbackUrl': CallbackUrl, 'VerifyToken': VerifyToken, 'ClientMenuUrl': ClientMenuUrl,
                       'action': ['both'], 'Linky': 'ABA'})
        # # ClientObject1 = client_table_links.objects.filter(client_id=request.user.id)
        # if len(ClientObject1) == 0:
        #     return render(request, 'I_settings/setting.html',
        #               {'CallbackUrl': CallbackUrl, 'VerifyToken': VerifyToken, 'ClientMenuUrl': ClientMenuUrl,
        #                'clinettableNumber':ClientObject1,'action':['offline'],'Linky':'ABA','obj':0})
        # else:
        #     ClientObject1 = client_table_links.objects.filter(client_id=request.user.id)
        #
        #     return render(request, 'I_settings/setting.html',
        #                   {'CallbackUrl': CallbackUrl, 'VerifyToken': VerifyToken, 'ClientMenuUrl': ClientMenuUrl,
        #                    'clinettableNumber':ClientObject1, 'action':['offline'],'Linky':'ABA','obj':1})



    elif clientStatus=='both':
        return render(request, 'I_settings/setting.html',
                      {'CallbackUrl': CallbackUrl, 'VerifyToken': VerifyToken, 'ClientMenuUrl': ClientMenuUrl,
                       'action':['both'],'Linky':'ABA'})

    else:
        Fb_setup=facebook_details.objects.filter(client_id=request.user.id)
        if len(Fb_setup)!=0:

            return render(request, 'I_settings/setting.html',{'Fb_Done':'Emty'})
        elif len(Fb_setup)==0:

            return render(request, 'I_settings/setting.html',{'Fb_Done':'Client'})

    #     if len(ClientObject) == 1:
    #         for ii in ClientObject:
    #             cliendId = cliendId + ii.client_auth_key
    #             cliendSecrat = cliendSecrat + ii.client_auth_secret
    #
    #         CallbackUrl = DomainName + 'webhook/' + cliendId
    #         VerifyToken = cliendSecrat
    #
    #         # print(request.path,'path for code')
    #         # print(get_current_site,'dddd')
    #         # print( request.build_absolute_uri(),'____')
    #         clientName = ''
    #         for kk in facebook_details.objects.filter(client_id=request.user.id):
    #             clientName = clientName + kk.fb_name
    #         # + secrets.token_hex(16)
    #         ClientMenuUrl = DomainName + clientName + '/' + secrets.token_hex(16)
    #         # print(ClientMenuUrl)
    #
    #         return render(request, 'I_settings/setting.html',
    #                       {'CallbackUrl': CallbackUrl, 'VerifyToken': VerifyToken, 'ClientMenuUrl': ClientMenuUrl,'action':False})
    #
    # if clientStatus == 'offline':
    #     if len(ClientObject) == 1:
    #         for ii in ClientObject:
    #             cliendId = cliendId + ii.client_auth_key
    #             cliendSecrat = cliendSecrat + ii.client_auth_secret
    #
    #         CallbackUrl = DomainName + 'webhook/' + cliendId
    #         VerifyToken = cliendSecrat
    #
    #
    #         clientName = ''
    #         for kk in facebook_details.objects.filter(client_id=request.user.id):
    #             clientName = clientName + kk.fb_name
    #
    #         ClientMenuUrl = DomainName + clientName + '/' + secrets.token_hex(16)
    #
    #         if len(ClientObject1) == 0:
    #             return render(request, 'I_settings/setting.html',
    #                       {'CallbackUrl': CallbackUrl, 'VerifyToken': VerifyToken, 'ClientMenuUrl': ClientMenuUrl,'action':True})
    #         else:
    #             ClientObject1 = client_table_links.objects.filter(client_id=request.user.id)
    # return render(request, 'I_settings/setting.html',
    #                           {'CallbackUrl': CallbackUrl, 'VerifyToken': VerifyToken, 'ClientMenuUrl': ClientMenuUrl
    #                            })


    return HttpResponse('<h3>First complete facebook setup</h3>')
#
#
#
def tables(request):
    return HttpResponse("waiting for admin verification")

    # print("hi good one da")
    # print(request.POST.get('tableCount'))
    # clientName = ''
    # cliendId = ''
    # cliendSecrat = ''
    # for kk in facebook_details.objects.filter(client_id=request.user.id):
    #     clientName = clientName + kk.fb_name
    # ClientObject1=client_table_count.objects.filter(client_id=request.user.id)
    # ClientObject = admin_permission.objects.filter(client_id=request.user.id)
    # for ii in ClientObject:
    #     cliendId = cliendId + ii.client_auth_key
    #     cliendSecrat = cliendSecrat + ii.client_auth_secret
    # if len(ClientObject1)==0:
    #     CountObject = client_table_count()
    #     CountObject.table_count=int(request.POST.get('tableCount'))
    #     CountObject.client_id=request.user.id
    #     CountObject.save()
    #     for i in range(0,int(request.POST.get('tableCount'))):
    #         LinksObject=client_table_links()
    #         LinksObject.table_number=i+1
    #         LinksObject.table_link=DomainName + clientName + '/' +cliendSecrat+ '/'+ secrets.token_hex(16)
    #         LinksObject.client_id=request.user.id
    #         LinksObject.save()
    # else:
    #     pass
    #
    # ClientObject1 =client_table_links.objects.filter(client_id=request.user.id)
    # return  JsonResponse({"result":ClientObject1})

#
#
def linkss(request):
    return HttpResponse("waiting for admin verification")

#     print("hi good one da")
#     print()
#     clientName = ''
#     cliendId = ''
#     cliendSecrat = ''
#     for kk in facebook_details.objects.filter(client_id=request.user.id):
#         clientName = clientName + kk.fb_name
#     ClientObject1 = client_table_count.objects.filter(client_id=request.user.id)
#     ClientObject = admin_permission.objects.filter(client_id=request.user.id)
#     for ii in ClientObject:
#         cliendId = cliendId + ii.client_auth_key
#         cliendSecrat = cliendSecrat + ii.client_auth_secret
#     if len(ClientObject1) == 0:
#         CountObject = client_table_count()
#         CountObject.table_count = 1
#         CountObject.client_id = request.user.id
#         CountObject.save()
#         for i in range(0, 1):
#             LinksObject = client_table_links()
#             LinksObject.table_number = i + 1
#             LinksObject.table_link = DomainName + clientName + '/' + cliendSecrat
#             LinksObject.client_id = request.user.id
#             LinksObject.save()
#     else:
#         pass
#
#     ClientObject12 = client_table_links.objects.filter(client_id=request.user.id)
#     return JsonResponse({"result1":  json.dumps(ClientObject12)})
# #
#
#
# def offlineBack(request, client, clientId, tableId, JsId):
#
#     if tableId=='0':
#         AddMore = order_details.objects.filter(js_cartid=JsId)
#         if len(AddMore) != 0:
#
#             NewTableNumber = []
#             NewProductCart = {}
#             NewTotalPrice = 0
#             NewCartNumber = 0
#             NewToken = ''
#             for addMore_ii in range(1):
#                 NewToken = NewToken + JsId
#
#             for addMore_i in AddMore:
#                 # print('===',addMore_i.id)
#
#                 productInfoObject = product_info.objects.filter(id=addMore_i.product_fk_id)
#                 for addMore_j in productInfoObject:
#                     # print('===',addMore_j.product_name)
#                     iinner1 = {
#                         'id': addMore_i.product_fk_id,
#                         'product_id': addMore_j.product_id,
#                         'product_name': addMore_j.product_name,
#                         'product_original_name': addMore_j.product_original_name,
#                         'product_price': addMore_i.product_value,
#                         'product_mrp': addMore_j.product_mrp,
#                         "product_unit": addMore_i.product_quantity,
#                         "product_net_unit": addMore_j.product_net_unit,
#                         'product_offer': addMore_j.product_offer,
#                         "product_status": addMore_j.product_status,
#                         "product_category_id": addMore_j.product_category_id,
#                         'product_image': str(addMore_j.product_image),
#                         'product_bot_image': str(addMore_j.product_bot_image),
#                         'product_description': addMore_j.product_description.capitalize(),
#                         "client_id": addMore_j.client_id
#
#                     }
#                     print(iinner1, 'gggggg')
#                     NewProductCart.update({str(addMore_i.product_fk_id): iinner1})
#
#                 NewCartNumber = NewCartNumber + addMore_i.product_quantity
#                 NewTableNumber.append(addMore_i.tableNumber)
#                 NewTotalPrice = NewTotalPrice + addMore_i.product_value
#
#             print(NewProductCart, '____________++++++')
#             NewProductCart = dumps(NewProductCart)
#             NewTableNumber = set(NewTableNumber)
#             NewTableNumber = list(NewTableNumber)
#             NewTableNumber = NewTableNumber[0]
#             linkFind = DomainName + client + '/' + clientId
#             print(linkFind,'1111111111')
#             LinksObject = client_table_links.objects.filter(table_link=linkFind)
#             clientID = 0
#             tableCount = 0
#
#             for i in LinksObject:
#                 clientID = clientID + i.client_id
#                 tableCount = tableCount + i.table_number
#
#             client_statusHtml = ''
#             clientLOgo=''
#             color4=''
#             color5=''
#             adminObjects = admin_permission.objects.filter(client_id=clientID)
#             for ij1 in adminObjects:
#                 client_statusHtml = client_statusHtml + ij1.client_status
#                 if str(ij1.client_image)=='':
#                     clientLOgo=clientLOgo+'https://vmart.ai/static/img/testimonailBlankImg.png'
#                     color4 = color4 + ij1.client_color4
#                     color5 = color5 + ij1.client_color5
#                     print(ij1.client_image)
#                 else:
#                     clientLOgo=clientLOgo+'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/'+str(ij1.client_image)
#                     print(ij1.client_image)
#                     color4 = color4 + ij1.client_color4
#                     color5 = color5 + ij1.client_color5
#
#             face_details = facebook_details.objects.filter(client_id=clientID)
#
#             num_num = 0
#             for num_i in face_details:
#                 num_num = num_num + num_i.fb_whatsapp_number
#
#             final_dict = {}
#
#             for us_i in face_details:
#
#                 p_view = product_category.objects.filter(client_id=clientID)
#                 for us_i2 in p_view:
#                     product_detai = []
#                     # inner_dict.update({'cata_name': us_i2.product_category_name})
#
#                     p_product_object = product_info.objects.filter(client_id=us_i.client_id,
#                                                                    product_category_id=us_i2.id,
#                                                                    product_status=True)
#                     # print(len(p_product_object))
#                     if len(p_product_object) != 0:
#                         for us_i3 in p_product_object:
#                             iinner = {
#
#                                 'product_id': us_i3.id,
#                                 'product_name': us_i3.product_name,
#                                 'product_price': us_i3.product_price,
#                                 'product_mrp': us_i3.product_mrp,
#                                 'product_offer': us_i3.product_offer,
#                                 'product_image': us_i3.product_image,
#                                 'product_bot_image': us_i3.product_bot_image,
#                                 'product_description': us_i3.product_description.capitalize()
#
#                             }
#                             product_detai.append(iinner)
#
#                         final_dict.update({us_i2.product_category_name: product_detai})
#                 # print(final_dict, '_________', clientID)
#
#             return render(request, 'offline.html',
#                           {'color5':color5,'color4':color4,'im': final_dict, 'cilentId': clientID, 'Product_ca': client, 'num_num': num_num,
#                            'tableNumber': tableCount, 'client_statusHtml': client_statusHtml, 'UserModifiy': True,
#                            'NewTableNumber': NewTableNumber, 'NewProductCart': NewProductCart,
#                            'NewTotalPrice': NewTotalPrice,
#                            'NewCartNumber': NewCartNumber, 'NewToken': JsId,'CliendImage':clientLOgo})
#         else:
#             redirect(str(DomainName + client + '/' + clientId + '/' + tableId))
#
#     else:
#         AddMore = order_details.objects.filter(js_cartid=JsId)
#         if len(AddMore) != 0:
#
#             NewTableNumber=[]
#             NewProductCart={}
#             NewTotalPrice=0
#             NewCartNumber=0
#             NewToken=''
#             for addMore_ii in range(1):
#                 NewToken=NewToken+JsId
#
#             for addMore_i in AddMore:
#                 # print('===',addMore_i.id)
#
#                 productInfoObject=product_info.objects.filter(id=addMore_i.product_fk_id)
#                 for addMore_j in productInfoObject:
#                     # print('===',addMore_j.product_name)
#                     iinner1={
#                         'id':addMore_i.product_fk_id,
#                         'product_id': addMore_j.product_id,
#                         'product_name': addMore_j.product_name,
#                         'product_original_name':addMore_j.product_original_name,
#                         'product_price': addMore_i.product_value,
#                         'product_mrp': addMore_j.product_mrp,
#                         "product_unit":addMore_i.product_quantity,
#                         "product_net_unit":addMore_j.product_net_unit,
#                         'product_offer': addMore_j.product_offer,
#                         "product_status":addMore_j.product_status,
#                         "product_category_id":addMore_j.product_category_id,
#                         'product_image': str(addMore_j.product_image),
#                         'product_bot_image': str(addMore_j.product_bot_image),
#                         'product_description': addMore_j.product_description.capitalize(),
#                         "client_id":addMore_j.client_id
#
#                         }
#                     print(iinner1,'gggggg')
#                     NewProductCart.update({str(addMore_i.product_fk_id):iinner1})
#
#                 NewCartNumber=NewCartNumber+addMore_i.product_quantity
#                 NewTableNumber.append(addMore_i.tableNumber)
#                 NewTotalPrice=NewTotalPrice+addMore_i.product_value
#
#             print(NewProductCart,'____________++++++')
#             NewProductCart=dumps(NewProductCart)
#             NewTableNumber=set(NewTableNumber)
#             NewTableNumber=list(NewTableNumber)
#             NewTableNumber=NewTableNumber[0]
#             linkFind = DomainName + client + '/' + clientId + '/' + tableId
#             LinksObject = client_table_links.objects.filter(table_link=linkFind)
#             clientID = 0
#             tableCount = 0
#
#             for i in LinksObject:
#                 clientID = clientID + i.client_id
#                 tableCount = tableCount + i.table_number
#
#             client_statusHtml = ''
#             clientLOgo=''
#             color4 = ''
#             color5 = ''
#             adminObjects = admin_permission.objects.filter(client_id=clientID)
#             for ij1 in adminObjects:
#                 client_statusHtml = client_statusHtml + ij1.client_status
#                 if str(ij1.client_image)=='':
#                     clientLOgo=clientLOgo+'https://vmart.ai/static/img/testimonailBlankImg.png'
#                     print(ij1.client_image)
#                     color4 = color4 + ij1.client_color4
#                     color5 = color5 + ij1.client_color5
#                 else:
#                     clientLOgo=clientLOgo+'https://s3.us-east-2.amazonaws.com/vailo.ai-bucket/'+str(ij1.client_image)
#                     print(ij1.client_image)
#                     color4 = color4 + ij1.client_color4
#                     color5 = color5 + ij1.client_color5
#             face_details = facebook_details.objects.filter(client_id=clientID)
#
#             num_num = 0
#             for num_i in face_details:
#                 num_num = num_num + num_i.fb_whatsapp_number
#             print(num_num,'_______________________________')
#             print(clientLOgo,'++++++++')
#             final_dict = {}
#
#             for us_i in face_details:
#
#                 p_view = product_category.objects.filter(client_id=clientID)
#                 for us_i2 in p_view:
#                     product_detai = []
#                     # inner_dict.update({'cata_name': us_i2.product_category_name})
#
#                     p_product_object = product_info.objects.filter(client_id=us_i.client_id, product_category_id=us_i2.id,
#                                                                    product_status=True)
#                     # print(len(p_product_object))
#                     if len(p_product_object) != 0:
#                         for us_i3 in p_product_object:
#                             iinner = {
#
#                                 'product_id': us_i3.id,
#                                 'product_name': us_i3.product_name,
#                                 'product_price': us_i3.product_price,
#                                 'product_mrp': us_i3.product_mrp,
#                                 'product_offer': us_i3.product_offer,
#                                 'product_image': us_i3.product_image,
#                                 'product_bot_image': us_i3.product_bot_image,
#                                 'product_description': us_i3.product_description.capitalize()
#
#                             }
#                             product_detai.append(iinner)
#
#                         final_dict.update({us_i2.product_category_name: product_detai})
#                 # print(final_dict, '_________', clientID)
#
#             return render(request, 'offline.html',
#                           {'color5':color5,'color4':color4,'im': final_dict, 'cilentId': clientID, 'Product_ca': client, 'num_num': num_num,
#                            'tableNumber': tableCount, 'client_statusHtml': client_statusHtml,'UserModifiy':True,
#                            'NewTableNumber':NewTableNumber,'NewProductCart':NewProductCart,'NewTotalPrice':NewTotalPrice,
#                            'NewCartNumber':NewCartNumber,'NewToken':JsId,'CliendImage':clientLOgo})
#         else:
#             redirect(str(DomainName + client + '/' + clientId + '/' + tableId))
#
#
#
#
#
# def offline(request,client,clientId,tableId):
#
#     linkFind=DomainName+client+'/'+clientId+'/'+tableId
#     LinksObject = client_table_links.objects.filter(table_link=linkFind)
#     clientID=0
#     tableCount=0
#     for i in LinksObject:
#         clientID=clientID+i.client_id
#         tableCount=tableCount+i.table_number
#     client_statusHtml=''
#     color4 = ''
#     color5 = ''
#     adminObjects=admin_permission.objects.filter(client_id=clientID)
#     for ij in adminObjects:
#         client_statusHtml=client_statusHtml+ij.client_status
#         color4 = color4 + ij.client_color4
#         color5 = color5 + ij.client_color5
#
#     face_details = facebook_details.objects.filter(client_id=clientID)
#
#     num_num = 0
#     for num_i in face_details:
#         num_num = num_num + num_i.fb_whatsapp_number
#
#     final_dict = {}
#
#     for us_i in face_details:
#
#         p_view = product_category.objects.filter(client_id=clientID)
#         for us_i2 in p_view:
#             product_detai = []
#             # inner_dict.update({'cata_name': us_i2.product_category_name})
#
#             p_product_object = product_info.objects.filter(client_id=us_i.client_id, product_category_id=us_i2.id,
#                                                            product_status=True)
#             # print(len(p_product_object))
#             if len(p_product_object) != 0:
#                 for us_i3 in p_product_object:
#                     iinner = {
#
#                         'product_id':us_i3.id,
#                         'product_name': us_i3.product_name,
#                         'product_price': us_i3.product_price,
#                         'product_mrp': us_i3.product_mrp,
#                         'product_offer': us_i3.product_offer,
#                         'product_image':us_i3.product_image,
#                         'product_bot_image':us_i3.product_bot_image,
#                         'product_description':us_i3.product_description.capitalize()
#
#                     }
#                     product_detai.append(iinner)
#
#                 final_dict.update({us_i2.product_category_name: product_detai})
#         print(final_dict,'_________',clientID)
#
#     return render(request,'offline.html',{'color4':color4,'color5':color5,'im': final_dict,'cilentId':clientID,'Product_ca':client,'num_num':num_num,'tableNumber':tableCount,'client_statusHtml':client_statusHtml})
#
#
# # def qrCode(request):
# #     clientName=''
# #     for kk in facebook_details.objects.filter(client_id=request.user.id):
# #         clientName=clientName+kk.fb_name
# #     # + secrets.token_hex(16)
# #     ClientMenuUrl=DomainName+clientName+'/'+secrets.token_hex(16)
#
#
#
# #     s =ClientMenuUrl
#
# #     url = pyqrcode.create(s)
#
#
# #     url.svg("myqr.svg", scale = 8)
#
#
# #     a=url.png('myqr.png', scale = 6)
# #     im1 = Image.open(a)
# #     im1 = im1.save()
# #     return redirect('settings')