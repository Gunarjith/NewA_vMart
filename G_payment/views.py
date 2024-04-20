from django.shortcuts import render, redirect
from vailodb.models import payment_gateway_details, payment_settings
from vailodb_a.models import appointment_payment_gateway_details
from vailodb.models import admin_permission,   Subclient, SubUserPreference,  SUBCLIENT_CHOICE


import razorpay
from django.http import JsonResponse

import requests
import json
from django.http import HttpResponse


def payment_page(request):

    return render(request, 'G_payment/payment_form.html')


def payment_page(request):
    admin_permission_obj = admin_permission.objects.filter(
        client_id=request.user.id).first()
    marketplace_id = request.session.get('marketplace_id')
    payment_gatewa = payment_gateway_details.objects.filter(
        client=request.user)

    if request.method == 'POST':
        for gateway in payment_gatewa:
            # Retrieve the corresponding form data based on the payment gateway
            gateway_id = request.POST.get(
                f'{gateway.payment_gateway}_gateway_id')
            gateway_key = request.POST.get(
                f'{gateway.payment_gateway}_gateway_key')
            currency = request.POST.get(f'{gateway.payment_gateway}_currency')

            # Update the payment details in the existing payment gateway
            gateway.gateway_id = gateway_id
            gateway.gateway_key = gateway_key
            gateway.currency = currency
            gateway.save()

        # Create new payment gateway entries for any selected methods that don't have existing entries
        # Modify as per your requirements
        selected_methods = ['rozorpay', 'cashfree', 'paypal', 'stripe']
        existing_methods = [
            gateway.payment_gateway for gateway in payment_gatewa]

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

        # Replace 'success_page' with your desired success page URL
        return HttpResponse('payment_formCommon')

    return render(request, 'G_payment/payment_form.html', {'payment_gatewa': payment_gatewa, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id})


def success_page(request):
    return render(request, 'G_payment/success_page.html')


def payment_pageCommon(request):
    return render(request, 'common/payment_formCommon.html')


def payment_pageCommon(request):
    admin_permission_obj = admin_permission.objects.filter(
        client_id=request.user.id).first()
    marketplace_id = request.session.get('marketplace_id')
    payment_gatewa = payment_gateway_details.objects.filter(
        client=request.user)

    if request.method == 'POST':
        for gateway in payment_gatewa:
            # Retrieve the corresponding form data based on the payment gateway
            gateway_id = request.POST.get(
                f'{gateway.payment_gateway}_gateway_id')
            gateway_key = request.POST.get(
                f'{gateway.payment_gateway}_gateway_key')
            currency = request.POST.get(f'{gateway.payment_gateway}_currency')

            # Update the payment details in the existing payment gateway
            gateway.gateway_id = gateway_id
            gateway.gateway_key = gateway_key
            gateway.currency = currency
            gateway.save()

        # Create new payment gateway entries for any selected methods that don't have existing entries
        # Modify as per your requirements
        selected_methods = ['rozorpay', 'cashfree', 'paypal', 'stripe']
        existing_methods = [
            gateway.payment_gateway for gateway in payment_gatewa]

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

        # Replace 'success_page' with your desired success page URL
        return HttpResponse('success_page')

    return render(request, 'common/payment_formCommon.html', {'payment_gatewa': payment_gatewa, 'admin_permission_obj': admin_permission_obj, 'marketplace_id': marketplace_id})


def success_page(request):
    return render(request, 'common/success_pageCommon.html')
