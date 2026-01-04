from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import F
from .models import Category, Product, Order, OrderItem
from .cart import Cart


def index(request):
    """Homepage"""
    context = {
        'featured_products': Product.objects.filter(is_featured=True, is_active=True)[:8],
        'new_arrivals': Product.objects.filter(is_new_arrival=True, is_active=True)[:8],
        'best_sellers': Product.objects.filter(is_best_seller=True, is_active=True)[:8],
        'on_sale': Product.objects.filter(is_on_sale=True, is_active=True)[:4],
    }
    return render(request, 'store/index.html', context)


def category(request, slug):
    """Category page"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products_list = Product.objects.filter(category=category, is_active=True)

    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'store/category.html', {
        'category': category,
        'products': products,
    })


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })


def search(request):
    """Search results"""
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        title__icontains=query,
        is_active=True
    ) if query else []

    return render(request, 'store/search.html', {
        'query': query,
        'products': products,
    })


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))

    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect(product.get_absolute_url())

    if quantity > product.stock:
        messages.error(request, f"Only {product.stock} items available.")
        return redirect(product.get_absolute_url())

    cart.add(product=product, quantity=quantity)
    messages.success(request, f"{product.title} added to cart.")
    return redirect('store:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, "Item removed from cart.")
    return redirect('store:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def checkout(request):
    cart = Cart(request)

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('store:index')

    if request.method == 'POST':
        order = Order.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city', 'Nairobi'),
            postal_code=request.POST.get('postal_code', ''),
            delivery_notes=request.POST.get('delivery_notes', ''),
            payment_method=request.POST.get('payment_method', 'cod'),
            total_amount=cart.get_total_price()
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

            Product.objects.filter(
                id=item['product'].id
            ).update(stock=F('stock') - item['quantity'])

        cart.clear()
        return redirect('store:order_success', order_id=order.id)

    return render(request, 'store/checkout.html', {'cart': cart})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {'order': order})
