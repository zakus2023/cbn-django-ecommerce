from django.shortcuts import render, get_object_or_404, redirect
from . models import Category, Product
from django.db.models import Q

from . cart import Cart

# Create your views here.

def product_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    product = category.products.filter(status=Product.ACTIVE)
    return render(request, 'products/product_category.html',{
        
        'category':category,
        'product':product
    })


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query)| Q(description__icontains=query))
    return render(request, 'products/search.html', {
        "query":query,
        "products":products
    })

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('frontpage')

def view_cart_view(request):
    cart = Cart(request)
    return render(request, 'products/view_cart_view.html',{
        'cart':cart
    })

def remove_item(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('view_cart_view')

def update_quantity(request, product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1
        
        if action == 'decrease':
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)
    return redirect('view_cart_view')


def products(request, category_slug, slug):
    product = get_object_or_404(Product, slug = slug, status=Product.ACTIVE)

    return render(request, 'products/products.html',{
        'product':product
    })

