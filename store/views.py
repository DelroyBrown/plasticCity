from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .cart import Cart
from .forms import UserRegisterForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Product, Category, Wishlist


def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


def products_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    # Update the filter to show products with stock > 0
    products = Product.objects.filter(stock__gt=0)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Query products with stock between 1 and 5
    low_stock_products = products.filter(stock__lte=5)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        # Add low_stock_products to the context
        'low_stock_products': low_stock_products,
    }

    return render(request, 'store/products_list.html', context)


def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug)
    context = {
        'category': category,
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)


def cart_detail(request):
    cart = Cart(request)
    cart_subtotal = {item['product']: cart.get_subtotal(item['product']) for item in cart}
    return render(request, 'store/cart_detail.html', {'cart': cart, 'cart_subtotal': cart_subtotal})



@require_POST
def cart_add(request, category_slug, product_slug):
    cart = Cart(request)
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug)
    quantity = request.POST.get('quantity')
    cart.add(product, quantity)
    return redirect('store:cart_detail')


def cart_remove(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect('store:cart_detail')


def wishlist(request):
    wishlist = request.user.wishlist
    products = wishlist.products.all()
    context = {'products': products}
    return render(request, 'store/wishlist.html', context)


@login_required
def wishlist_add(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug)

    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if product not in wishlist.products.all():
        wishlist.products.add(product)
        messages.success(
            request, f"{product.name} has been added to your wishlist.")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")

    return redirect('store:product_detail', category_slug=category_slug, product_slug=product_slug)


@login_required
def wishlist_detail(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'store/wishlist_detail.html', {'wishlist': wishlist})


def wishlist_remove(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug)
    wishlist = request.user.wishlist
    wishlist.products.remove(product)
    return redirect('store:wishlist_detail')
