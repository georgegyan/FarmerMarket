from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from django import forms
from django.contrib import messages
from .models import Farm, Product, Order, Cart
from .forms import FarmForm, ProductForm, UserProfileForm

def home(request):
    products = Product.objects.all()
    return render(request, 'core/home.html', {'products': products})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'core/login.html'

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email or Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

def login(request):
    return render(request, 'core/login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def product_search(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category=category)
    if min_price:
        products = products.filter(price__gte=float(min_price))
    if max_price:
        products = products.filter(price__lte=float(max_price))

    return render(request, 'core/search.html', {
        'products': products,
        'query': query,
        'selected_category': category
    })


@login_required
def create_farm(request):
    if request.method == 'POST':
        form = FarmForm(request.POST, request.FILES)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.user = request.user
            farm.save()
            return redirect('home')
    else:
        form = FarmForm()
    return render(request, 'core/farm_form.html', {'form': form})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farm = request.user.farm
            product.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'core/product_form.html', {'form': form})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    cart_item, created = Cart.objects.get_or_create(
        session_id=session_key,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

def cart_view(request):
    cart_items = Cart.objects.filter(session_id=request.session.session_key)
    total = sum (item.prouct.price * item.quantity for item in cart_items)
    return render (request, 'core/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def profile(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    saved_farms = request.user.userprofile.saved_farms.all()
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'core/profile.html', {
        'orders': orders,
        'saved_farms': saved_farms,
        'form': form
    })

def product_search(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()
    
    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    return render(request, 'core/search.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'core/products.html', {'products': products})

def custom_logout(request):
    logout(request)
    return redirect('home')  