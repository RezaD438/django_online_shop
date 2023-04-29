from django.shortcuts import render

from .form import OrderForm

def order_create_view(reqeust):
    return render(reqeust, 'order/order_create.html',context={'form':OrderForm})
