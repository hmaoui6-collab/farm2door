from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from .forms import RegisterForm, ProductForm
from .models import Product, Profile, Order, OrderItem


def home(request):
    products = Product.objects.select_related('farmer').all().order_by('-id')[:8]
    return render(request, 'home.html', {'products': products})


def products(request):
    products = Product.objects.select_related('farmer').all().order_by('-id')
    return render(request, 'products.html', {'products': products})


def about(request):
    return render(request, 'about.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            Profile.objects.create(
                user=user,
                user_type=form.cleaned_data['user_type']
            )
            login(request, user)
            messages.success(request, "Compte cree avec succes.")
            return redirect('home')
        messages.error(request, "Veuillez corriger les informations saisies.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def _is_farmer(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.user_type == 'farmer'


@login_required
def add_product(request):
    if not _is_farmer(request.user):
        messages.error(request, "Cette action est reservee aux agriculteurs.")
        return redirect('home')

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()
            messages.success(request, "Produit ajoute.")
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    current_qty = cart.get(str(product_id), 0)

    if current_qty >= product.stock:
        messages.warning(request, "Stock insuffisant pour ce produit.")
        return redirect('products')

    cart[str(product_id)] = current_qty + 1
    request.session['cart'] = cart
    messages.success(request, f"{product.name} ajoute au panier.")
    return redirect('products')


def cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, qty in list(cart.items()):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            cart.pop(product_id, None)
            continue
        product.qty = qty
        product.total = product.price * qty
        total += product.total
        products.append(product)

    request.session['cart'] = cart
    return render(request, 'cart.html', {'products': products, 'total': total})


def increase_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    current_qty = cart.get(str(product_id), 0)

    if current_qty < product.stock:
        cart[str(product_id)] = current_qty + 1
        request.session['cart'] = cart
    else:
        messages.warning(request, "Stock insuffisant pour ce produit.")

    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    key = str(product_id)
    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            cart.pop(key)
    request.session['cart'] = cart
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    messages.success(request, "Produit retire du panier.")
    return redirect('cart')


def _cart_products(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, qty in list(cart.items()):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            cart.pop(product_id, None)
            continue
        product.qty = qty
        product.total = product.price * qty
        total += product.total
        products.append(product)

    request.session['cart'] = cart
    return products, total


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Votre panier est vide.")
        return redirect('products')

    products, total = _cart_products(request)
    if request.method != "POST":
        return render(request, 'checkout.html', {'products': products, 'total': total})

    payment_method = request.POST.get('payment_method', 'cash')
    if payment_method not in ['cash', 'card']:
        payment_method = 'cash'

    delivery_address = request.POST.get('delivery_address', '').strip()
    if not delivery_address:
        messages.error(request, "Veuillez saisir l'adresse de livraison.")
        return render(request, 'checkout.html', {'products': products, 'total': total})

    if payment_method == 'card':
        card_name = request.POST.get('card_name', '').strip()
        card_number = request.POST.get('card_number', '').replace(' ', '').strip()
        card_expiry = request.POST.get('card_expiry', '').strip()
        card_cvc = request.POST.get('card_cvc', '').strip()

        if not card_name or len(card_number) < 12 or not card_number.isdigit() or not card_expiry or len(card_cvc) < 3:
            messages.error(request, "Veuillez remplir correctement les informations de la carte.")
            return render(request, 'checkout.html', {'products': products, 'total': total})

    payment_status = 'paid' if payment_method == 'card' else 'pending'
    order = Order.objects.create(
        customer=request.user,
        payment_method=payment_method,
        payment_status=payment_status,
        delivery_address=delivery_address,
    )

    total = 0
    for product_id, qty in cart.items():
        product = get_object_or_404(Product, id=product_id)
        if qty > product.stock:
            messages.error(request, f"Stock insuffisant pour {product.name}.")
            order.delete()
            return redirect('cart')

        OrderItem.objects.create(order=order, product=product, quantity=qty)
        total += product.price * qty
        product.stock -= qty
        product.save(update_fields=['stock'])

    order.total = total
    order.save()

    request.session['cart'] = {}
    items = OrderItem.objects.filter(order=order).select_related('product')
    messages.success(request, "Commande confirmee. Merci pour votre achat.")
    return render(request, 'order_success.html', {'order': order, 'items': items})


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {
        'orders': orders,
        'paid_orders': orders.filter(payment_status='paid').count(),
        'pending_orders': orders.filter(payment_status='pending').count(),
        'total_spent': sum(order.total for order in orders),
    })


def _pdf_text(text):
    return str(text).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


def _build_receipt_pdf(order, items):
    def text(x, y, value, size=11, font='F1'):
        return f'BT /{font} {size} Tf {x} {y} Td ({_pdf_text(value)}) Tj ET'

    def line(x1, y1, x2, y2):
        return f'{x1} {y1} m {x2} {y2} l S'

    def rect(x, y, width, height):
        return f'{x} {y} {width} {height} re S'

    content = [
        '0.13 0.45 0.28 RG',
        '0.13 0.45 0.28 rg',
        '50 755 495 42 re f',
        '1 1 1 rg',
        text(68, 770, 'Farm2Door', 18, 'F2'),
        text(392, 770, "BON D'ACHAT", 16, 'F2'),
        '0 0 0 RG',
        '0 0 0 rg',
        text(50, 725, f'Commande numero: {order.id}', 12, 'F2'),
        text(50, 705, f'Client: {order.customer.username}', 11),
        text(50, 685, f'Date: {order.created_at.strftime("%d/%m/%Y %H:%M")}', 11),
        text(330, 705, f'Paiement: {order.get_payment_method_display()}', 11),
        text(330, 685, f'Statut: {order.get_payment_status_display()}', 11, 'F2'),
        text(50, 665, f'Adresse: {order.delivery_address[:70]}', 10),
        rect(50, 625, 495, 28),
        text(62, 635, 'Produit', 11, 'F2'),
        text(300, 635, 'Qte', 11, 'F2'),
        text(360, 635, 'Prix', 11, 'F2'),
        text(455, 635, 'Total', 11, 'F2'),
    ]

    y = 600
    for item in items:
        line_total = item.product.price * item.quantity
        content.extend([
            text(62, y, item.product.name, 10),
            text(305, y, item.quantity, 10),
            text(360, y, f'{item.product.price} DH', 10),
            text(455, y, f'{line_total} DH', 10),
            line(50, y - 10, 545, y - 10),
        ])
        y -= 25

    content.extend([
        rect(330, y - 35, 215, 42),
        text(350, y - 15, 'Total commande', 12, 'F2'),
        text(455, y - 15, f'{order.total} DH', 12, 'F2'),
        text(50, 95, 'Ce bon confirme la finalisation de votre commande Farm2Door.', 10),
        text(50, 78, 'Merci pour votre confiance.', 10, 'F2'),
        text(50, 45, 'Farm2Door - Produits frais directement des agriculteurs locaux', 9),
    ])
    stream = '\n'.join(content).encode('latin-1', errors='replace')

    objects = [
        b'<< /Type /Catalog /Pages 2 0 R >>',
        b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
        b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>',
        b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
        b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>',
        b'<< /Length ' + str(len(stream)).encode('ascii') + b' >>\nstream\n' + stream + b'\nendstream',
    ]

    pdf = bytearray(b'%PDF-1.4\n')
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f'{number} 0 obj\n'.encode('ascii'))
        pdf.extend(obj)
        pdf.extend(b'\nendobj\n')

    xref_offset = len(pdf)
    pdf.extend(f'xref\n0 {len(objects) + 1}\n'.encode('ascii'))
    pdf.extend(b'0000000000 65535 f \n')
    for offset in offsets[1:]:
        pdf.extend(f'{offset:010d} 00000 n \n'.encode('ascii'))
    pdf.extend(
        f'trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n'.encode('ascii')
    )
    return bytes(pdf)


@login_required
def purchase_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    allowed_farmer = OrderItem.objects.filter(order=order, product__farmer=request.user).exists()

    if order.customer != request.user and not request.user.is_staff and not allowed_farmer:
        messages.error(request, "Vous n'avez pas acces a ce bon d'achat.")
        return redirect('home')

    items = OrderItem.objects.filter(order=order).select_related('product')
    pdf = _build_receipt_pdf(order, items)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bon_achat_{order.id}.pdf"'
    return response


@login_required
def dashboard(request):
    if not _is_farmer(request.user):
        messages.error(request, "Cette page est reservee aux agriculteurs.")
        return redirect('home')

    products = Product.objects.filter(farmer=request.user)
    items = OrderItem.objects.filter(product__farmer=request.user).select_related('product', 'order')
    total_revenue = sum(item.product.price * item.quantity for item in items)
    total_orders = items.values('order_id').distinct().count()
    low_stock_products = products.filter(stock__lte=5).order_by('stock')
    sold_quantities = {}
    for item in items:
        sold_quantities[item.product.name] = sold_quantities.get(item.product.name, 0) + item.quantity
    best_product = max(sold_quantities, key=sold_quantities.get) if sold_quantities else None

    return render(request, 'farmer_dashboard.html', {
        'products': products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'low_stock_products': low_stock_products,
        'best_product': best_product,
    })


@login_required
def farmer_orders(request):
    if not _is_farmer(request.user):
        messages.error(request, "Cette page est reservee aux agriculteurs.")
        return redirect('home')

    order_items = (
        OrderItem.objects
        .filter(product__farmer=request.user)
        .select_related('order', 'order__customer', 'product')
        .order_by('-order__created_at')
    )
    return render(request, 'farmer_orders.html', {'order_items': order_items})


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Cette page est reservee a l'administration.")
        return redirect('home')

    orders = Order.objects.select_related('customer').order_by('-created_at')[:10]
    paid_revenue = sum(order.total for order in Order.objects.filter(payment_status='paid'))
    pending_revenue = sum(order.total for order in Order.objects.filter(payment_status='pending'))
    total_revenue = paid_revenue + pending_revenue
    return render(request, 'admin_dashboard.html', {
        'total_users': User.objects.count(),
        'total_farmers': Profile.objects.filter(user_type='farmer').count(),
        'total_customers': Profile.objects.filter(user_type='customer').count(),
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'revenue': total_revenue,
        'paid_revenue': paid_revenue,
        'pending_revenue': pending_revenue,
        'orders': orders,
    })


@login_required
def admin_products(request):
    if not request.user.is_staff:
        messages.error(request, "Cette page est reservee a l'administration.")
        return redirect('home')

    products = Product.objects.select_related('farmer').all().order_by('name')
    return render(request, 'admin_products.html', {'products': products})


@login_required
def admin_add_product(request):
    if not request.user.is_staff:
        messages.error(request, "Cette page est reservee a l'administration.")
        return redirect('home')

    farmers = User.objects.filter(profile__user_type='farmer').order_by('username')
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        farmer = User.objects.filter(id=request.POST.get('farmer')).first()
        if form.is_valid() and farmer:
            product = form.save(commit=False)
            product.farmer = farmer
            product.save()
            messages.success(request, "Produit ajoute par l'administration.")
            return redirect('admin_products')
        messages.error(request, "Veuillez remplir tous les champs du produit.")
    else:
        form = ProductForm()

    return render(request, 'admin_product_form.html', {
        'form': form,
        'farmers': farmers,
        'title': 'Ajouter un produit',
    })


@login_required
def admin_edit_product(request, product_id):
    if not request.user.is_staff:
        messages.error(request, "Cette page est reservee a l'administration.")
        return redirect('home')

    product = get_object_or_404(Product, id=product_id)
    farmers = User.objects.filter(profile__user_type='farmer').order_by('username')
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        farmer = User.objects.filter(id=request.POST.get('farmer')).first()
        if form.is_valid() and farmer:
            product = form.save(commit=False)
            product.farmer = farmer
            product.save()
            messages.success(request, "Produit modifie par l'administration.")
            return redirect('admin_products')
        messages.error(request, "Veuillez corriger les champs du produit.")
    else:
        form = ProductForm(instance=product)

    return render(request, 'admin_product_form.html', {
        'form': form,
        'farmers': farmers,
        'product': product,
        'title': 'Modifier un produit',
    })


@login_required
def admin_delete_product(request, product_id):
    if not request.user.is_staff:
        messages.error(request, "Cette page est reservee a l'administration.")
        return redirect('home')

    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Produit supprime par l'administration.")
        return redirect('admin_products')
    return render(request, 'delete_product.html', {'product': product, 'back_url': 'admin_products'})


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, farmer=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit modifie.")
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, farmer=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Produit supprime.")
        return redirect('dashboard')
    return render(request, 'delete_product.html', {'product': product})
