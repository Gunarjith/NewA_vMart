from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
import razorpay

razorpay_api_key = 'rzp_test_ax8keBqGYvI1W9'
razorpay_secret_key = 'vu3aVQja4ZP8CacGK39fm0wu'

# Create your views here.



from datetime import datetime,date
import pytz
format = "%Y-%m-%d %H:%M:%S"

converted_tz = pytz.timezone('Asia/Kolkata')

datetime_object = str(datetime.now(converted_tz ))

now = datetime_object[:len(datetime_object)-6]




# def billing(request):
#     #____________________________points_________________
#
#     points_objects=client_wallet_balance.objects.filter(client_id=request.user.id)
#
#
#     cliend_idd=request.user.id
#     client_received_messages_1 = client_received_messages.objects.filter(client_id=cliend_idd)
#     day_date = ''
#     id_date = ''
#
#     for i_k in client_received_messages_1:
#         if now[:10]== str(i_k.message_date.date()):
#             day_date = day_date + str(i_k.message_date.date())
#             id_date = id_date + str(i_k.id)
#             print(i_k.message_date.date())
#
#     # print(now)
#     # counter_receive(request, cliend_idd)
#     print(now[:10], 'str(now.date())')
#     print(day_date, 'dayyyyyyyy')
#     print(id_date, "idddddddddddddddddddddddd")
#
#     client_received_messages_1zz = client_sent_messages.objects.filter(client_id=cliend_idd)
#     day_datezz = ''
#     id_datezz = ''
#
#     for i_kzz in client_received_messages_1zz:
#         if now[:10] == str(i_kzz.message_date.date()):
#             day_datezz = day_datezz + str(i_kzz.message_date.date())
#             id_datezz = id_datezz + str(i_kzz.id)
#             print(i_kzz.message_date.date())
#
#     # print(now)
#     # counter_receive(request, cliend_idd)
#     print(now[:10], 'str(now.date())')
#     print(day_datezz, 'dayyyyyyyy')
#     print(id_datezz, "idddddddddddddddddddddddd")
#
#     today_recive=client_received_messages.objects.filter(client_id=request.user.id,)
#     today_send=client_sent_messages.objects.filter(client_id=request.user.id)
#
#     # id = int(id_date)
#     # id = int(id_datezz),
#
#     sendd=0
#     recivee=0
#     if len(today_send):
#         for i in today_send:
#             print(i.message_date.date(),'-',now[:10])
#             if i.message_date.date()==now[:10]:
#                 sendd = sendd + i.s_day_count
#
#     if len(today_recive):
#         for j in today_recive:
#             print(j.message_date.date(),'-',now[:10])
#             if j.message_date.date()==now[:10]:
#                 recivee = recivee + j.r_day_count
#     return render(request,'C_billing/billing.html',{'reci':today_recive,'send':today_send,'se':sendd,'re':recivee,'pointde':points_objects})
#


def payment(request):

    return render(request,'C_billing/payment2.html')


# @csrf_exempt
# def payment2(request):
#
#
#     if request.method == "POST":
#         client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))
#         print(request.POST.get('amounttt'))
#         order_amount = int(request.POST.get('amounttt'))
#         order_currency = 'INR'
#
#         payment_order = client.order.create(dict(amount=order_amount * 100, currency=order_currency, payment_capture=1))
#         payment_order_id = payment_order['id']
#         order_status = payment_order['status']
#
#         if order_status == 'created':
#             payto_weObjects = client_payment_details(
#
#                 client_payment_date=now,
#                 amount=order_amount,
#                 razorpay_order_id=payment_order_id,
#                 client_id=request.user.id
#
#             )
#             payto_weObjects.save()
#         context = {
#             "amount": order_amount,
#             "currency": "INR",
#             'api_key': razorpay_api_key,
#             'order_id': payment_order_id,
#             'clint_id':request.user.id
#
#
#         }
#         print(payment_order)
#         print(order_amount)
#         return render(request, 'C_billing/payment.html', context)



# @csrf_exempt
# def payment_done(request):
#     print('ajxxxxxx')
#     response = request.POST
#     print(response['client_id'])
#     params_dict = {
#
#         'razorpay_order_id': response['razorpay_order_id'],
#         'razorpay_payment_id': response['razorpay_payment_id'],
#         'razorpay_signature': response['razorpay_signature']
#     }
#     client = razorpay.Client(auth=(razorpay_api_key, razorpay_secret_key))
#
#     print(response['razorpay_order_id'])
#     print(response['razorpay_payment_id'])
#     print(response['razorpay_signature'])
#     try:
#         status = client.utility.verify_payment_signature(params_dict)
#         aa2 = client_payment_details.objects.get(razorpay_order_id=response['razorpay_order_id'])
#         aa2.razorpay_payment_id = response['razorpay_payment_id']
#         aa2.payment_status = True
#         aa2.save()
#         aa3=client_payment_details.objects.filter(razorpay_order_id=response['razorpay_order_id'])
#         ex_amount=0
#
#         for i in aa3:
#
#             aa4=client_wallet_balance.objects.filter(client_id=i.client_id)
#             if len(aa4)!=0:
#                 for j in aa4:
#                     ex_amount = ex_amount + j.wallet_balance_point
#                 aa5 = client_wallet_balance.objects.get(client_id=i.client_id)
#                 aa5.wallet_balance_point = ex_amount + int(i.amount)
#                 aa5.payment_status = 'available'
#                 aa5.save()
#
#                 adminPermissionObjects = admin_permission.objects.get(client_id=i.client_id)
#                 adminPermissionObjects.client_permission = True
#                 adminPermissionObjects.save()
#
#             else:
#                 clientWalletBalanceobject=client_wallet_balance()
#                 clientWalletBalanceobject.wallet_balance_point=int(i.amount)
#                 clientWalletBalanceobject.payment_status='available'
#                 clientWalletBalanceobject.client_id=i.client_id
#                 clientWalletBalanceobject.save()
#
#                 adminPermissionObjects = admin_permission.objects.get(client_id=i.client_id)
#                 adminPermissionObjects.client_permission = True
#                 adminPermissionObjects.save()
#
#
#         return render(request, 'C_billing/success.html')
#     except:
#         return render(request, 'C_billing/success.html')




# def payment_history(request):
#     paymentHistoryObject=client_payment_details.objects.filter(client_id=request.user.id,payment_status=True)
#
#     return render(request,'C_billing/payment_history.html',{'paymentHistoryObject':paymentHistoryObject})