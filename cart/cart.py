from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from products.models import Product


class Cart:
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')  # cart dafe haye ghbl ro biyar

        if not cart:  # agar ghablan nadashtt barash ye jadid besaz
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1, replace_current_quantity=False):
        """
        Add the specified product to the cart if it exists
        """
        product_id = str(product.id)

        if product_id not in self.cart:  # agar nabood besaz agar bood ezafe kon
            self.cart[product_id] = {'quantity': quantity}

        elif replace_current_quantity:
            self.cart[product_id] = {'quantity': quantity}

        else:
            self.cart[product_id]['quantity'] += quantity

        messages.success(self.request, _('Product successfully added to cart'))

        self.save()

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            messages.error(self.request, _('Product successfully removed from cart'))
            self.save()

    def save(self):
        """
        Mark session as modified to save changes
        """
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()

        # Product.objects.filter(id=1)
        # Product.objects.filter(id__in[1,2,3,])
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = item['product_obj'].price * item['quantity']
            yield item

    def __len__(self):
        # return len(self.cart.keys()) # tedad anvaye mahsolat ro bar migardone
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        return sum(item['quantity'] * item['product_obj'].price for item in self.cart.values())
