from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from cart.cart import Cart
from .form import OrderForm
from .models import OrderItem


@login_required
def order_create_view(request):
    order_form = OrderForm()
    this_cart = Cart(request)
    first_name = ""
    last_name = ""

    if len(this_cart) == 0:
        messages.warning(request, _('you can not proceed to checkout page because your cart is empty.'))
        return redirect('product_list')

    if request.method == 'POST':
        order_form = OrderForm(request.POST, )

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in this_cart:
                new_product = item['product_obj']
                OrderItem.objects.create(
                    order=order_obj,
                    product=new_product,
                    quantity=item['quantity'],
                    price=new_product.price,
                )

            this_cart.clear()

            if request.user.first_name is not None:
                request.user.first_name = order_obj.first_name
                request.user.last_name = order_obj.last_name
                request.user.save()

            request.session['order_id'] = order_obj.id

            return redirect('payment_process')

    else:
        if request.user.first_name is not None:
            first_name = request.user.first_name
            last_name = request.user.last_name

    return render(request, 'order/order_create.html', context={'form': order_form,
                                                               'first_name': first_name,
                                                               'last_name': last_name,
                                                               }, )
