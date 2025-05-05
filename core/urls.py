from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register_view

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile, name='profile'),
    path('register/', register_view, name='register'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('products/', views.product_list, name='products'),
]