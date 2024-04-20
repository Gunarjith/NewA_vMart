# from django.shortcuts import render
# from django.http import HttpResponse,JsonResponse
#
# # Create your views here.
# from A_webhook.models import order_details,order_header,customer_address
# from E_product.models import product_info
# from B_profile.models import admin_permission
#
#
#
# def order(request):
#     order_objects=order_details.objects.filter(order_status="paid",client_id=request.user.id)
#     # for i in order_objects:
#     #     print()
#     return render(request,'F_order/order.html',{'order_s':order_objects})
#
#
# def placeOrder(request):
#     return render(request,'F_order/placeorder.html')
#
#
# def orderAjax(request):
#     order_objects = order_header.objects.filter(order_status="paid", client_id=request.user.id)
#
#     return JsonResponse({"paidUsers": list(order_objects.values())})
#
# def acceptAjax(request):
#     order_objects = order_header.objects.filter(order_status="accept", client_id=request.user.id)
#     # for i in order_objects:
#     #     print()
#     return JsonResponse({"paidUsers": list(order_objects.values())})
#
# def orderAjaxRight(request,orderID,orderStatus):
#     adminPbjects = admin_permission.objects.filter(client_id=request.user.id)
#     cliendStatus=''
#     for i_cliendId in adminPbjects:
#         cliendStatus=cliendStatus+i_cliendId.client_status
#     print(cliendStatus)
#     orderRight = order_header.objects.filter(id=int(orderID), order_status=orderStatus, client_id=request.user.id)
#
#     orderRight1 = []
#     orderRight2 = []
#     innnerDict = {}
#     for i in orderRight:
#         product_detailsObjects = order_details.objects.filter(customer_number=i.customer_number,
#                                                               order_status=orderStatus, client_id=request.user.id)
#
#         for j in product_detailsObjects:
#             product_detailsObjects2 = product_info.objects.filter(client_id=request.user.id, id=j.product_fk_id)
#
#             for k in product_detailsObjects2:
#                 print(k.product_name)
#                 orderRight1.append({
#
#                     'productName': k.product_name,
#                     'productId': k.product_id,
#                     'productPrice': k.product_price,
#                     'productValues': j.product_value,
#                     'productQuantity': j.product_quantity,
#                     'productImage': str(k.product_image),
#                 }
#
#                 )
#
#             if cliendStatus=='online':
#
#                 for l in customer_address.objects.filter(client_id=request.user.id, customer_number=i.customer_number):
#                     innnerDict.update({
#                         'userNumber': j.customer_number,
#                         'totalPrice': i.order_value,
#                         'customerNumber': l.customer_number,
#                         'customerName': l.customer_name,
#                         'customerAddressline1': l.customer_addressline1,
#                         'customerArea': l.customer_area,
#                         'customerPincode': l.customer_pincode,
#                         'orderHeaderId': int(orderID),
#                     })
#             elif cliendStatus=='offline':
#
#                 innnerDict.update({
#                         'userNumber': j.customer_number,
#                         'totalPrice': i.order_value,
#
#                         'tablenumber':i.tableNumber,
#                         'orderHeaderId': int(orderID),
#                     })
#
#     orderRight2.append(innnerDict)
#     orderRight2.append(orderRight1)
#     print(innnerDict)
#     print(orderRight1)
#
#     # print(orderRight2)
#     return JsonResponse({"orderHeaderDetails": orderRight2,'cliendStatus':cliendStatus})
#
#
# def acceptPost(request,orderID):
#     print(orderID,'oooooooooooooooooooooooooo')
#     orderRight = order_header.objects.filter(id=int(orderID), order_status="paid", client_id=request.user.id)
#     for i in orderRight:
#         orderHeaderObjects=order_header.objects.get(id=i.id)
#         orderHeaderObjects.order_status='accept'
#         orderHeaderObjects.save()
#         product_detailsObjects = order_details.objects.filter(customer_number=i.customer_number, order_status="paid",
#                                                               client_id=request.user.id)
#         for j in product_detailsObjects:
#             orderDetailsObjects=order_details.objects.get(id=j.id)
#             orderDetailsObjects.order_status='accept'
#             orderDetailsObjects.save()
#
#     return HttpResponse('hi')
#
#
# def ajaxUpdate(request):
#     LiveUpdateObjectsPaid=order_header.objects.filter(order_status='paid',client_id=request.user.id)
#     LiveUpdateObjectsAccept=order_header.objects.filter(order_status='accept',client_id=request.user.id)
#     LiveUpdateObjectsDelivered = order_header.objects.filter(order_status='delivered',client_id=request.user.id)
#     return JsonResponse({"LiveUpdate": [len(LiveUpdateObjectsPaid),len(LiveUpdateObjectsAccept),len(LiveUpdateObjectsDelivered)]})