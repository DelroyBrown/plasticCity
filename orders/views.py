import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from store.cart import Cart
from .models import OrderItem, ShippingOption
from store.models import Customer, Order
from .forms import OrderCreateForm
from django.shortcuts import render
from django.contrib import messages


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    cart = Cart(request)

    if cart.get_total_price() <= 0:
        messages.error(request, "Your cart total must be greater than 0.")
        return redirect('store:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user

            customer = Customer.objects.get(user=request.user)
            order.customer = customer

            order.total_price = cart.get_total_price()
            order.save()

            for item in cart:
                product = item['product']
                product.stock -= item['quantity']  # Decrement the stock
                product.save()  # Save the updated product

                order_item = OrderItem(
                    order=order, product=product, price=item['price'], quantity=item['quantity'])
                if order_item:
                    order_item.save()  # Explicitly save the order item
                    print(f"Created OrderItem: {order_item}")
                else:
                    print(f"Error creating OrderItem")
                    messages.error(request, f"Error creating OrderItem")
                    return redirect('store:cart_detail')

            cart.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('orders:payment'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})



def payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id, paid=False)

    # Make sure the shipping_option is assigned to the order
    if not order.shipping_option:
        messages.error(
            request, "Shipping option is not assigned to the order.")
        return redirect('orders:checkout')

    total_cost = order.get_total_cost()

    if total_cost <= 0:
        messages.error(request, 'The total cost must be greater than 0.')
        # Add this print statement
        print("Error: The total cost must be greater than 0.")
        return redirect(reverse('orders:checkout'))

    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=int(total_cost * 100),
            currency='gbp',
            description=f'Order {order.id}',
            source=request.POST['stripeToken']
        )
        order.paid = True
        order.save()
        return redirect(reverse('orders:done'))

    context = {'order': order, 'stripe_pub_key': settings.STRIPE_PUBLIC_KEY,
               'total_cost': total_cost}
    return render(request, 'orders/payment.html', context)


def payment_done(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'orders/payment_done.html', {'order': order, 'order_items': order_items})
