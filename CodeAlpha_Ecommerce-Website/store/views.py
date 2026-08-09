import uuid
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Category, Product, Order, OrderItem, UserProfile
from .forms import UserRegistrationForm, CheckoutForm, ProfileForm


def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:8]
    popular_products = Product.objects.filter(is_popular=True)[:8]
    if not featured_products.exists():
        featured_products = Product.objects.all()[:8]
    if not popular_products.exists():
        popular_products = Product.objects.all()[8:16]
        if not popular_products.exists():
            popular_products = Product.objects.all()[:8]

    categories = Category.objects.all()
    context = {
        'featured_products': featured_products,
        'popular_products': popular_products,
        'categories': categories,
    }
    return render(request, 'home.html', context)


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    sort_by = request.GET.get('sort', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    if min_price and min_price.isdigit():
        products = products.filter(price__gte=float(min_price))
    if max_price and max_price.isdigit():
        products = products.filter(price__lte=float(max_price))

    if sort_by == 'price_low_high':
        products = products.order_by('price')
    elif sort_by == 'price_high_low':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'query': query,
        'sort_by': sort_by,
        'min_price': min_price,
        'max_price': max_price,
        'total_count': products.count(),
    }
    return render(request, 'products.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)


def get_cart_data(request):
    cart = request.session.get('cart', {})
    items = []
    subtotal = 0

    # Ensure cart is a dictionary with string product_ids
    if not isinstance(cart, dict):
        cart = {}

    for prod_id_str, quantity in list(cart.items()):
        try:
            prod_id = int(prod_id_str)
            product = Product.objects.get(id=prod_id)
            quantity = int(quantity)
            if quantity <= 0:
                continue
            item_total = product.price * quantity
            subtotal += item_total
            items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })
        except (Product.DoesNotExist, ValueError):
            continue

    delivery_fee = 0 if subtotal >= 499 or subtotal == 0 else 40
    discount = 100 if subtotal >= 1000 else 0
    total = max(0, subtotal + delivery_fee - discount) if subtotal > 0 else 0

    return {
        'cart_items': items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'discount': discount,
        'total': total,
        'item_count': sum(item['quantity'] for item in items),
    }


def cart_detail(request):
    cart_data = get_cart_data(request)
    return render(request, 'cart.html', cart_data)


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1) or request.GET.get('quantity', 1))

    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}

    str_id = str(product_id)
    current_qty = cart.get(str_id, 0)
    new_qty = min(product.stock, current_qty + quantity)
    cart[str_id] = new_qty
    request.session['cart'] = cart
    request.session.modified = True

    messages.success(request, f"Added '{product.name}' to your cart!")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_data = get_cart_data(request)
        return JsonResponse({
            'success': True,
            'message': f"Added '{product.name}' to cart!",
            'cart_count': cart_data['item_count'],
        })

    next_url = request.POST.get('next') or request.GET.get('next') or 'cart'
    return redirect(next_url)


def cart_update(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not isinstance(cart, dict):
            cart = {}

        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        qty = request.POST.get('quantity')

        if product_id:
            str_id = str(product_id)
            if str_id in cart:
                if action == 'increase':
                    cart[str_id] += 1
                elif action == 'decrease':
                    cart[str_id] -= 1
                    if cart[str_id] <= 0:
                        del cart[str_id]
                elif action == 'set' and qty:
                    try:
                        new_q = int(qty)
                        if new_q > 0:
                            cart[str_id] = new_q
                        else:
                            del cart[str_id]
                    except ValueError:
                        pass
                elif action == 'remove':
                    del cart[str_id]

        request.session['cart'] = cart
        request.session.modified = True

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            cart_data = get_cart_data(request)
            return JsonResponse({
                'success': True,
                'cart_count': cart_data['item_count'],
                'subtotal': str(cart_data['subtotal']),
                'delivery_fee': str(cart_data['delivery_fee']),
                'discount': str(cart_data['discount']),
                'total': str(cart_data['total']),
            })

    return redirect('cart')


def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    str_id = str(product_id)
    if isinstance(cart, dict) and str_id in cart:
        del cart[str_id]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Item removed from your cart.")
    return redirect('cart')


def checkout(request):
    cart_data = get_cart_data(request)
    if cart_data['item_count'] == 0:
        messages.warning(request, "Your cart is empty! Add products before checking out.")
        return redirect('products')

    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial_data.update({
                'phone': profile.phone,
                'address': profile.address,
                'landmark': profile.landmark,
                'city': profile.city,
                'state': profile.state,
                'pincode': profile.pincode,
            })

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Server-side calculation
            subtotal = cart_data['subtotal']
            delivery_fee = cart_data['delivery_fee']
            discount = cart_data['discount']
            total_amount = cart_data['total']

            # Generate unique order number
            now = datetime.now()
            order_number = f"IK{now.strftime('%Y%m%d')}{now.strftime('%H%M%S')}"

            # Estimated delivery 3 to 7 days from today
            delivery_start = (now + timedelta(days=3)).strftime('%d %B %Y')
            delivery_end = (now + timedelta(days=7)).strftime('%d %B %Y')
            estimated_delivery = f"{delivery_start} - {delivery_end}"

            order = form.save(commit=False)
            order.order_number = order_number
            if request.user.is_authenticated:
                order.user = request.user
            order.subtotal = subtotal
            order.delivery_fee = delivery_fee
            order.discount = discount
            order.total_amount = total_amount
            order.status = 'Placed'
            order.estimated_delivery = estimated_delivery
            order.save()

            # Save order items
            for item in cart_data['cart_items']:
                product = item['product']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    quantity=item['quantity'],
                    price=product.price
                )
                # Deduct stock
                if product.stock >= item['quantity']:
                    product.stock -= item['quantity']
                    product.save()

            # Clear session cart
            request.session['cart'] = {}
            request.session.modified = True

            return redirect('order_success', order_number=order.order_number)
        else:
            messages.error(request, "Please correct the highlighted errors in your checkout form.")
    else:
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart_data': cart_data,
    }
    return render(request, 'checkout.html', context)


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    items = order.items.all()
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'order_success.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']

            # Use email as username or derive username
            username = email.split('@')[0]
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            name_parts = full_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                phone=phone
            )

            # Log in automatically
            login(request, user)
            messages.success(request, f"Welcome to IndianKart, {full_name}! Your account has been created.")
            return redirect('home')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        login_input = request.POST.get('login_input', '').strip()
        password = request.POST.get('password', '').strip()

        # Try authenticating as username or email
        user = None
        if '@' in login_input:
            try:
                user_obj = User.objects.get(email__iexact=login_input)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        else:
            user = authenticate(request, username=login_input, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email/username or password. Please try again.")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        full_name = request.POST.get('full_name', '').strip()
        if form.is_valid():
            form.save()
            if full_name:
                parts = full_name.split(' ', 1)
                request.user.first_name = parts[0]
                request.user.last_name = parts[1] if len(parts) > 1 else ''
                request.user.save()
            messages.success(request, "Your profile details have been updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please check form for errors.")
    else:
        initial = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
        }
        form = ProfileForm(instance=profile, initial=initial)

    recent_orders = Order.objects.filter(user=request.user)[:5]

    context = {
        'form': form,
        'profile': profile,
        'recent_orders': recent_orders,
    }
    return render(request, 'profile.html', context)


@login_required
def orders_view(request):
    user_orders = Order.objects.filter(user=request.user)
    context = {
        'orders': user_orders,
    }
    return render(request, 'orders.html', context)
