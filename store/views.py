from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.http import JsonResponse

import razorpay
from django.conf import settings

from .models import Product, Category, Order, OrderItem, Wishlist


# =========================================================
# HOME
# =========================================================

def home(request):

    products = Product.objects.all().order_by('-created_at')

    search = request.GET.get('search', '')
    category = request.GET.get('category', '')

    if search:
        products = products.filter(
            name__icontains=search
        )

    if category:
        products = products.filter(
            category_id=category
        )

    categories = Category.objects.all()

    return render(
        request,
        'store/home.html',
        {
            'products': products,
            'categories': categories,
            'search': search,
            'selected_category': category,
        }
    )


# =========================================================
# PRODUCT DETAILS
# =========================================================

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'store/product_detail.html',
        {
            'product': product
        }
    )


# =========================================================
# CART
# =========================================================

def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    current_quantity = cart.get(product_id, 0)

    if current_quantity >= product.stock:

        messages.error(
            request,
            f'Only {product.stock} units of {product.name} are available.'
        )

        return redirect('cart')

    cart[product_id] = current_quantity + 1

    request.session['cart'] = cart

    request.session.modified = True

    messages.success(
        request,
        f'{product.name} added to cart.'
    )

    return redirect('cart')


def remove_from_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        del cart[product_id]

    request.session['cart'] = cart

    request.session.modified = True

    return redirect('cart')


def cart(request):

    cart_data = request.session.get(
        'cart',
        {}
    )

    cart_items = []

    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append(
            {
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            }
        )

    return render(
        request,
        'store/cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        email = request.POST.get(
            'email'
        )

        password = request.POST.get(
            'password'
        )

        confirm_password = request.POST.get(
            'confirm_password'
        )

        if password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return redirect('register')

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                'Username already exists.'
            )

            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            'Registration successful. Please login.'
        )

        return redirect('login')

    return render(
        request,
        'store/register.html'
    )


# =========================================================
# LOGIN
# =========================================================

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect('home')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'store/login.html'
    )


# =========================================================
# LOGOUT
# =========================================================

def user_logout(request):

    logout(request)

    return redirect('home')


# =========================================================
# CHECKOUT PAGE
# =========================================================

def checkout(request):

    if not request.user.is_authenticated:

        messages.warning(
            request,
            'Please login before checkout.'
        )

        return redirect('login')

    cart_data = request.session.get(
        'cart',
        {}
    )

    if not cart_data:

        messages.warning(
            request,
            'Your cart is empty.'
        )

        return redirect('cart')

    cart_items = []

    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        if quantity > product.stock:

            messages.error(
                request,
                f'Only {product.stock} units of {product.name} are available.'
            )

            return redirect('cart')

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append(
            {
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            }
        )

    return render(
        request,
        'store/checkout.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


# =========================================================
# CREATE RAZORPAY ORDER
# =========================================================

def create_razorpay_order(request):

    if not request.user.is_authenticated:

        return JsonResponse(
            {
                'error': 'Please login before making a payment.'
            },
            status=401
        )

    cart_data = request.session.get(
        'cart',
        {}
    )

    if not cart_data:

        return JsonResponse(
            {
                'error': 'Your cart is empty.'
            },
            status=400
        )

    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        if quantity > product.stock:

            return JsonResponse(
                {
                    'error': (
                        f'Only {product.stock} units of '
                        f'{product.name} are available.'
                    )
                },
                status=400
            )

        total += product.price * quantity

    amount = int(
        total * 100
    )

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    razorpay_order = client.order.create(
        {
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1
        }
    )

    request.session[
        'razorpay_order_id'
    ] = razorpay_order['id']

    request.session[
        'razorpay_amount'
    ] = str(total)

    request.session.modified = True

    return JsonResponse(
        {
            'order_id': razorpay_order['id'],
            'amount': amount,
            'currency': 'INR',
            'key_id': settings.RAZORPAY_KEY_ID,
        }
    )


# =========================================================
# VERIFY RAZORPAY PAYMENT
# =========================================================

@transaction.atomic
def verify_razorpay_payment(request):

    if not request.user.is_authenticated:

        return JsonResponse(
            {
                'error': 'Please login before completing payment.'
            },
            status=401
        )

    if request.method != 'POST':

        return JsonResponse(
            {
                'error': 'Invalid request method.'
            },
            status=405
        )

    razorpay_payment_id = request.POST.get(
        'razorpay_payment_id'
    )

    razorpay_order_id = request.POST.get(
        'razorpay_order_id'
    )

    razorpay_signature = request.POST.get(
        'razorpay_signature'
    )

    session_order_id = request.session.get(
        'razorpay_order_id'
    )

    if not session_order_id:

        return JsonResponse(
            {
                'error': 'Payment session expired. Please try again.'
            },
            status=400
        )

    if razorpay_order_id != session_order_id:

        return JsonResponse(
            {
                'error': 'Invalid Razorpay order.'
            },
            status=400
        )

    if not razorpay_payment_id or not razorpay_signature:

        return JsonResponse(
            {
                'error': 'Payment information is incomplete.'
            },
            status=400
        )

    # -----------------------------------------------------
    # Create Razorpay client
    # -----------------------------------------------------

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    # -----------------------------------------------------
    # 1. Verify payment signature
    # -----------------------------------------------------

    try:

        client.utility.verify_payment_signature(
            {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            }
        )

    except razorpay.errors.SignatureVerificationError:

        return JsonResponse(
            {
                'error': 'Payment verification failed.'
            },
            status=400
        )

    except Exception as e:

        print(
            'Razorpay signature verification error:',
            e
        )

        return JsonResponse(
            {
                'error': 'Unable to verify payment.'
            },
            status=400
        )

    # -----------------------------------------------------
    # 2. Fetch payment details from Razorpay
    # -----------------------------------------------------

    try:

        payment = client.payment.fetch(
            razorpay_payment_id
        )

    except Exception as e:

        print(
            'Razorpay payment fetch error:',
            e
        )

        return JsonResponse(
            {
                'error': 'Unable to fetch payment details.'
            },
            status=400
        )

    # -----------------------------------------------------
    # 3. Verify payment status
    # -----------------------------------------------------

    if payment.get('status') != 'captured':

        return JsonResponse(
            {
                'error': 'Payment was not successfully captured.'
            },
            status=400
        )

    # -----------------------------------------------------
    # 4. Verify payment amount
    # -----------------------------------------------------

    session_amount = request.session.get(
        'razorpay_amount'
    )

    if not session_amount:

        return JsonResponse(
            {
                'error': 'Payment amount information is missing.'
            },
            status=400
        )

    try:

        expected_amount = int(
            float(session_amount) * 100
        )

    except (ValueError, TypeError):

        return JsonResponse(
            {
                'error': 'Invalid payment amount.'
            },
            status=400
        )

    if payment.get('amount') != expected_amount:

        return JsonResponse(
            {
                'error': (
                    'Payment amount does not match '
                    'the order amount.'
                )
            },
            status=400
        )

    # -----------------------------------------------------
    # 5. Get cart
    # -----------------------------------------------------

    cart_data = request.session.get(
        'cart',
        {}
    )

    if not cart_data:

        return JsonResponse(
            {
                'error': 'Your cart is empty.'
            },
            status=400
        )

    # -----------------------------------------------------
    # 6. Validate products and stock
    # -----------------------------------------------------

    cart_items = []

    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        if quantity > product.stock:

            return JsonResponse(
                {
                    'error': (
                        f'Only {product.stock} units of '
                        f'{product.name} are available.'
                    )
                },
                status=400
            )

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append(
            {
                'product': product,
                'quantity': quantity,
            }
        )

    # -----------------------------------------------------
    # 7. Verify calculated cart amount
    # -----------------------------------------------------

    calculated_amount = int(
        float(total) * 100
    )

    if calculated_amount != payment.get('amount'):

        return JsonResponse(
            {
                'error': (
                    'Cart amount does not match '
                    'payment amount.'
                )
            },
            status=400
        )

    # -----------------------------------------------------
    # 8. Get customer details
    # -----------------------------------------------------

    full_name = request.POST.get(
        'full_name'
    )

    email = request.POST.get(
        'email'
    )

    phone = request.POST.get(
        'phone'
    )

    address = request.POST.get(
        'address'
    )

    city = request.POST.get(
        'city'
    )

    state = request.POST.get(
        'state'
    )

    pincode = request.POST.get(
        'pincode'
    )

    # -----------------------------------------------------
    # 9. Create order
    # -----------------------------------------------------

    order = Order.objects.create(

        user=request.user,

        full_name=full_name,

        email=email,

        phone=phone,

        address=address,

        city=city,

        state=state,

        pincode=pincode,

        total_amount=total,

        razorpay_order_id=razorpay_order_id,

        razorpay_payment_id=razorpay_payment_id,

        razorpay_signature=razorpay_signature,

        payment_status='Paid',

        status='Confirmed'
    )

    # -----------------------------------------------------
    # 10. Create order items and reduce stock
    # -----------------------------------------------------

    for item in cart_items:

        product = item['product']

        quantity = item['quantity']

        OrderItem.objects.create(

            order=order,

            product=product,

            quantity=quantity,

            price=product.price
        )

        product.stock -= quantity

        product.save()

    # -----------------------------------------------------
    # 11. Clear cart and Razorpay session
    # -----------------------------------------------------

    request.session['cart'] = {}

    request.session.pop(
        'razorpay_order_id',
        None
    )

    request.session.pop(
        'razorpay_amount',
        None
    )

    request.session.modified = True

    # -----------------------------------------------------
    # 12. Return success
    # -----------------------------------------------------

    return JsonResponse(
        {
            'success': True,
            'order_id': order.id,
        }
    )


# =========================================================
# ORDER SUCCESS
# =========================================================

def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'store/order_success.html',
        {
            'order': order
        }
    )


# =========================================================
# ORDER HISTORY
# =========================================================

def order_history(request):

    if not request.user.is_authenticated:

        messages.warning(
            request,
            'Please login to view your orders.'
        )

        return redirect('login')

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'store/order_history.html',
        {
            'orders': orders
        }
    )


# =========================================================
# WISHLIST
# =========================================================

def wishlist(request):

    if not request.user.is_authenticated:

        messages.warning(
            request,
            'Please login to view your wishlist.'
        )

        return redirect('login')

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related('product')

    return render(
        request,
        'store/wishlist.html',
        {
            'wishlist_items': wishlist_items
        }
    )


def add_to_wishlist(request, product_id):

    if not request.user.is_authenticated:

        messages.warning(
            request,
            'Please login to add products to wishlist.'
        )

        return redirect('login')

    product = get_object_or_404(
        Product,
        id=product_id
    )

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:

        messages.success(
            request,
            f'{product.name} added to wishlist.'
        )

    else:

        messages.info(
            request,
            f'{product.name} is already in your wishlist.'
        )

    return redirect(
        'product_detail',
        product_id=product.id
    )


def remove_from_wishlist(request, product_id):

    if not request.user.is_authenticated:

        messages.warning(
            request,
            'Please login first.'
        )

        return redirect('login')

    Wishlist.objects.filter(
        user=request.user,
        product_id=product_id
    ).delete()

    messages.success(
        request,
        'Product removed from wishlist.'
    )

    return redirect('wishlist')