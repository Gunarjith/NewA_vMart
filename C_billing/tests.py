# from django.test import TestCase
#
# # Create your tests here.
# for i in aa3:
#
#     aa4 = client_wallet_balance.objects.filter(client_id=i.client_id, payment_status='available')
#     if len(aa4) != 0:
#         for j in aa4:
#             ex_amount = ex_amount + j.wallet_balance_point
#         aa5 = client_wallet_balance.objects.get(client_id=i.client_id, payment_status='available')
#         aa5.wallet_balance_point = 0
#         aa5.payment_status = 'unavailable'
#         aa5.save()
#         aa6 = client_wallet_balance()
#
#         aa6.wallet_balance_point = ex_amount + int(i.amount)
#         aa6.payment_status = 'available'
#         aa6.client_id = response['client_id']
#         aa6.save()
#     else:
#         aa6 = client_wallet_balance()
#
#         aa6.wallet_balance_point = int(i.amount)
#
#         aa6.payment_status = 'available'
#         aa6.client_id = response['client_id']
#         aa6.save()
