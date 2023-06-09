import requests
import json

from django.shortcuts import get_object_or_404, reverse, redirect
from django.contrib import messages

from django.conf import settings
from order.models import Order
from products.models import Product


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    riyal_total_price = order.get_total_price() * 10

    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'

    request_header = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': riyal_total_price,
        'description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'callback_url': request.build_absolute_uri(reverse('payment_callback')),
    }

    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = res.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')
    else:
        messages.error(request, 'error from zarinpal')
        return redirect('home')


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)

    toman_total_price = order.get_total_price()
    riyal_total_price = order.get_total_price() * 10

    if payment_status == 'OK':

        request_header = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        request_data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': riyal_total_price,
            'authority': payment_authority,
        }

        zarinpal_callback_url = 'https://api.zarinpal.com/pg/v4/payment/verify.json'

        res = requests.post(url=zarinpal_callback_url, data=json.dumps(request_data), headers=request_header)

        if 'data' in res.json() and ('errors' not in res.json() or len(res.json()['errors']) == 0):
            data = res.json()['data']

            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.ref_id = data['ref_id']
                order.zarinpal_data = data
                for item in order.items:
                    f_product = get_object_or_404(Product, item.product)
                    messages.success(request, f_product.stock)

                order.save()

                messages.success(request, 'payment successful')
                return redirect('home')

            elif payment_code == 101:
                messages.warning(request, 'payment successful. but this payment was already registered.contact support')
                return redirect('home')
            else:
                error_code = res.json()['errors']['code']
                error_message = res.json()['errors']['message']
                messages.error(request, 'there was an error on your payment')
                messages.error(request, f'error message : {error_message} {error_code}')
                return redirect('home')

    else:
        messages.error(request, 'payment unsuccessful')
        return redirect('home')


def payment_process_sandbox(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    riyal_total_price = order.get_total_price() * 10

    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'

    request_header = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    request_data = {
        'MerchantID': settings.ZARINPAL_MERCHANT_ID,
        'Amount': riyal_total_price,
        'Description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'CallbackURL': request.build_absolute_uri(reverse('payment_callback')),
    }

    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = res.json()
    authority = data['Authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect(f'https://sandbox.zarinpal.com/pg/StartPay/{authority}')
    else:
        messages.error(request, 'error from zarinpal')
        return redirect('home')


def payment_callback_sandbox(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)

    toman_total_price = order.get_total_price()
    riyal_total_price = order.get_total_price() * 10

    if payment_status == 'OK':

        request_header = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        request_data = {
            'MerchantID': 'ABCDABCDABCDABCDABCDABCDABCDABCDABCD',
            'Amount': riyal_total_price,
            'Authority': payment_authority,
        }

        zarinpal_callback_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json'

        res = requests.post(url=zarinpal_callback_url, data=json.dumps(request_data), headers=request_header)

        if 'errors' not in res.json() or len(res.json()['errors']) == 0:
            data = res.json()
            payment_code = data['Status']

            if payment_code == 100:
                order.is_paid = True
                order.ref_id = data['RefID']
                order.zarinpal_data = data

                for item in order.items.all():
                    messages.success(request, item.product.stock)
                    item.product.stock = item.product.stock - item.quantity
                    messages.success(request, item.quantity)
                    messages.success(request, item.product.stock)
                    item.product.save()

                order.save()

                messages.success(request, 'payment successful')

                return redirect('home')

            elif payment_code == 101:
                messages.warning(request, 'payment successful. but this payment was already registered.contact support')
                return redirect('home')
            else:
                error_code = res.json()['errors']['code']
                error_message = res.json()['errors']['message']
                messages.error(request, 'there was an error on your payment')
                messages.error(request, f'error message : {error_message} {error_code}')
                return redirect('home')

    else:
        messages.error(request, 'payment unsuccessful')
        return redirect('home')
