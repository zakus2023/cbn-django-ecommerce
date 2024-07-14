from django.shortcuts import render, get_object_or_404, redirect
from . models import Category, Product, Order, OrderItem
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from . forms import OrderForm
from django.conf import settings
import json
import stripe
from django.http import JsonResponse
from django.urls import reverse
import braintree

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
        'cart':cart,
        
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



# @login_required
# def checkout(request):
#     cart = Cart(request)

#     if cart.get_total_cost() == 0:
#         return redirect('view_cart_view')

#     if request.method == 'POST':
#         data = json.loads(request.body)
#         form = OrderForm(request.POST)

#         total_price = 0
#         items = []

#         for item in cart:
#             product = item['product']
#             total_price += product.price * int(item['quantity'])

#             items.append({
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': product.title,
#                     },
#                     'unit_amount': product.price
#                 },
#                 'quantity': item['quantity']
#             })
        
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=items,
#             mode='payment',
#             success_url = 'http://127.0.0.1:8000/cart/success/',
#             cancel_url = 'http://127.0.0.1:8000/cart/'
#         )
#         payment_intent = session.payment_intent

#         order = Order.objects.create(
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             address=data['address'],
#             postalcode=data['postalcode'],
#             city=data['city'],
#             email=data['email'],
#             phone=data['phone'],
#             created_by = request.user,
#             is_paid = True,
#             payment_intent = payment_intent,
#             paid_amount = total_price
#         )

#         for item in cart:
#             product = item['product']
#             quantity = int(item['quantity'])
#             price = product.price * quantity

#             item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

#         cart.clear()

#         return JsonResponse({'session': session, 'order': payment_intent})
#     else:
#         form = OrderForm()

#     return render(request, 'products/checkout.html', {
#         'cart': cart,
#         'form': form,
#         'pub_key': settings.STRIPE_PUB_KEY,
#     })




@login_required
def checkout(request):
    cart = Cart(request)

    if cart.get_total_cost() == 0:
        return redirect('view_cart_view')
    
    if request.method == 'POST':
        data = json.loads(request.body)

        fisrt_name = data['first_name']
        last_name = data['last_name']
        address = data['address']
        city = data['city']
        postalcode = data['postalcode']
        email = data['email']
        phone = data['phone']

        if fisrt_name  and  last_name and address and city and postalcode and email and phone:

            form = OrderForm(request.POST)

            
            total_price = 0
            items = []
            
                
            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])

                items.append({
                    'price_data':{
                        'currency':'usd',
                        'product_data':{
                            'name': product.title,
                        },
                        'unit_amount': product.price,
                    },
                    'quantity': item['quantity'],
                })
                    
            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items = items,
                mode='payment',
                success_url = settings.WEBSITE_URL+'/cart/success/',
                cancel_url = settings.WEBSITE_URL+'/cart/'
                    
            )
                    

            payment_intent = session.payment_intent

            order = Order.objects.create(
                first_name = fisrt_name,
                last_name = last_name,
                address = address,
                city = city,
                postalcode = postalcode,
                email = email,
                phone = phone,
                is_paid = True,
                payment_intent = payment_intent,
                paid_amount = total_price,
                created_by = request.user
            )
                
                
                
            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

            cart.clear()

            return JsonResponse({'session': session, 'order': payment_intent})
        
    else:
        form = OrderForm()

        return render(request, 'products/checkout.html',{
            'cart':cart,
            'form':form,
            'pub_key':settings.STRIPE_PUB_KEY
     
    }) 

    

def success(request):
    return render(request,'products/success.html')    
