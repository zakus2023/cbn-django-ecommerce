from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from . models import Userprofile
from django.utils.text import slugify
from django.contrib import messages

from products.models import Product, Category
from products.forms import ProductForm

# Create your views here.

def vendor_detail(request, id):
    user = User.objects.get(id=id)
    products = user.products.filter(status=Product.ACTIVE)
    return render(request, 'userprofile/vendor_detail.html', {
        'user':user,
        'products':products
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            userprofile = Userprofile.objects.create(user=user)

            return redirect('frontpage')
    else:
        form = UserCreationForm()
    return render(request, 'userprofile/signup.html',{
        'form':form
    })
        
@login_required
def myaccount(request):
    return render(request, 'userprofile/myaccount.html')

@login_required
def mystore(request):
    products = request.user.products.exclude(status = Product.DELETED)

    return render(request, 'userprofile/mystore.html', {
        'products':products
    })

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            user_name = request.user.username
            product_slug = title + '_' + user_name
            
            print(title)

            product = form.save(commit=False)
            product.user= request.user
            product.slug = slugify(product_slug)
            product.save()
            messages.success(request, "Product added successfully")
            return redirect('mystore')
    else:
        form = ProductForm()

    return render(request, 'userprofile/add_product.html',{
        'title':'Add Product',
        'form':form
    })

def update_product(request, id):
    product = Product.objects.filter(user=request.user).get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            
            form.save()
            messages.success(request, "Product updated successfully")

            return redirect('mystore')
            
    else:
        form = ProductForm(instance=product)
    return render(request, 'userprofile/update_product.html',{
        'title':'Update Product',
        'product':product,
        'form':form
    })

def delete_product(request, id):
    product = Product.objects.filter(user=request.user).get(id=id)
    product.status = Product.DELETED
    product.save()
    messages.success(request, "Product Deleted successfully")
    return redirect('mystore')