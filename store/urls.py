from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(next_page='store:products'), name='login'),
    path('logout/', LogoutView.as_view(next_page='store:home'), name='logout'),
    path('products/', views.products_list, name='products'),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<slug:category_slug>/<slug:product_slug>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:id>/', views.cart_remove, name='cart_remove'),
    path('wishlist/', views.wishlist_detail, name='wishlist_detail'),
    path('<slug:category_slug>/', views.products_list, name='products_list_by_category'),
    path('wishlist/add/<slug:category_slug>/<slug:product_slug>/', views.wishlist_add, name='wishlist_add'),
    path('wishlist/remove/<slug:category_slug>/<slug:product_slug>/', views.wishlist_remove, name='wishlist_remove'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)