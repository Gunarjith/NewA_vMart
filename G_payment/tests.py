from django.shortcuts import render,redirect

from G_payment.models import customer_payment_details,payment_settings
from A_webhook.models import order_details,order_header,customer_address
from E_product.models import product_info
import razorpay
from django.http import JsonResponse
# Create your views here.



def payment_page(request):
    if request.method=="POST":
        razorpay_object=payment_settings.objects.filter(client_id=request.user.id)
        if len(razorpay_object)==0:
            razorpay_creation=payment_settings()
            razorpay_creation.razorpay_contact_name=request.POST.get('Contact_Name')
            razorpay_creation.razorpay_contact_number=request.POST.get('Contact_Number')
            razorpay_creation.razorpay_cilent_id=request.POST.get('your_id')
            razorpay_creation.razorpay_client_secret=request.POST.get('your_secret')
            razorpay_creation.client_id=request.user.id
            razorpay_creation.save()
            return redirect('payment_page')

        else:
            for razor_i in razorpay_object:
                razorpay_edit=payment_settings.objects.get(id=razor_i.id)
                razorpay_edit.razorpay_contact_name = request.POST.get('Contact_Name')
                razorpay_edit.razorpay_contact_number = request.POST.get('Contact_Number')
                razorpay_edit.razorpay_cilent_id = request.POST.get('your_id')
                razorpay_edit.razorpay_client_secret = request.POST.get('your_secret')
                razorpay_edit.save()
            return redirect('payment_page')

    else:
        razorpay_object = payment_settings.objects.filter(client_id=request.user.id)
        if len(razorpay_object) != 0:

            return render(request, 'G_payment/payment.html',{'razor':razorpay_object})
        else:
            return render(request, 'G_payment/payment_form.html')



def payment_success(request):

    return render(request,'payment_status.html')

def payment_failed(request):

    return render(request,'payment_failed.html')


def payment_form(request):
    return render(request,'G_payment/payment_form.html')




def customerPaymentFunction(request,linkNumber,linkAmount):
    pk1 = str(linkNumber)
    us_number = pk1[:12]
    our_client = pk1[-1]
    amount = linkAmount
    object_pagefill = order_details.objects.filter(customer_number=us_number, client_id=int(our_client), order_status='process')
    object_useraddress = customer_address.objects.filter(customer_number=us_number, client_id=int(our_client))
    user_name=''
    for userNameI in object_useraddress:
        user_name=user_name+userNameI.customer_name

    object_list = []
    Total_price = 0
    for pay_page_i in object_pagefill:

        for pay_page_i1 in product_info.objects.filter(id=pay_page_i.product_fk_id):
            dict_me = {'product_name': pay_page_i1.product_name,
                       'product_qty': pay_page_i.product_quantity,
                       'product_image': pay_page_i1.product_image,
                       'product_price': pay_page_i.product_value
                       }
            object_list.append(dict_me)
            Total_price = Total_price + pay_page_i.product_value
    print(object_list)
    razorpay_clientid = payment_settings.objects.filter(client_id=our_client)

    ray_id = ''
    ray_secret = ''
    ray_client_name = ''

    for I in razorpay_clientid:
        ray_id = ray_id + I.razorpay_cilent_id
        ray_secret = ray_secret + I.razorpay_client_secret
        ray_client_name = ray_client_name + I.razorpay_contact_name
    print(Total_price,type(Total_price),'total price')
    print(amount, type(amount), 'amount')
    if Total_price== amount:
        client = razorpay.Client(auth=(ray_id, ray_secret))

        # create order

        response_payment = client.order.create(dict(amount=amount * 100, currency='INR'))
        print(response_payment)  # Must Imporatant

        order_id = response_payment['id']
        order_status = response_payment['status']

        if order_status == 'created':
            customerPaymentObjects = customer_payment_details(
                order_value=amount,
                order_id=order_id,
                customer_name=user_name,
                customer_number=us_number,
                client_id=our_client
                )
            customerPaymentObjects.save()
            customerPaymentObjectsHeader = order_header.objects.filter(customer_number=us_number,
                                                                       order_status='process', client_id=our_client)
            for order_header_i in customerPaymentObjectsHeader:
                order_headerEditObjects = order_header.objects.get(id=order_header_i.id)
                order_headerEditObjects.order_id = order_id
                order_headerEditObjects.save()

            return render(request, 'userspayment.html',
                          {'pay_key': ray_id, 'payment': response_payment, 'total_p': Total_price * 100,
                           'address': object_useraddress, 'cart_p': object_list, 'total': Total_price, 'user_nu': us_number,
                           'contt': ray_client_name.upper(), 'clikl': our_client})
    else:
        return render(request, 'userspayment_em.html')

def payment_order(request):
    a = request.POST.get('payment_mode')
    # print(request.POST.get('payment_id'))
    print("___________________________")
    response = request.POST
    print(response)
    print(',.,.,.,.,.,.', request.POST.get('client_id'))

    razorpay_clientid = payment_settings.objects.filter(client_id=request.POST.get('client_id'))
    ray_id = ''
    ray_secret = ''
    ray_client_name = ''
    for I in razorpay_clientid:
        ray_id = ray_id + I.razorpay_cilent_id
        ray_secret = ray_secret + I.razorpay_client_secret
        ray_client_name = ray_client_name + I.razorpay_contact_name

    if a == "Razorpay":
        params_dict = {

            'razorpay_order_id': request.POST.get('razorpay_order_id'),
            'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
            'razorpay_signature': request.POST.get('razorpay_signature')
        }
        print(params_dict)
        client = razorpay.Client(auth=(ray_id, ray_secret))
        try:
            status = client.utility.verify_payment_signature(params_dict)
            aa2 = customer_payment_details.objects.get(order_id=request.POST.get('razorpay_order_id'))
            aa2.razorpay_payment_id = request.POST.get('razorpay_payment_id')
            aa2.payment_status = True
            aa2.save()

            aaa2=order_header.objects.get(order_id=request.POST.get('razorpay_order_id'),client_id=request.POST.get('client_id'))
            aaa2.payment_id=request.POST.get('razorpay_payment_id')
            aaa2.order_status = "paid"
            aaa2.save()

            aa3 = customer_payment_details.objects.filter(order_id=request.POST.get('razorpay_order_id'))
            for aa3_i in aa3:
                if aa3_i.payment_status==True:
                    aa4 = order_details.objects.filter(customer_number=aa3_i.customer_number, client_id=aa3_i.client_id
                                                     , order_status='process')
                    for aa4_i in aa4:
                        aa5 = order_details.objects.get(id=aa4_i.id)
                        aa5.order_status = 'paid'
                        aa5.save()
            
            return JsonResponse({'status': "your Order id successful!"})

        except:
            return JsonResponse({'status': "Sorry! Your transaction was faild"})
    return redirect('/')
