from django.shortcuts import render


def order_create_view(reqeust):
    return render(reqeust, 'order/order_create.html')
