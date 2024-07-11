from django.shortcuts import render

from products.models import Product




# Create your views here.

def frontpage(request):
    
    # products = Product.objects.all()[0:4] this was the initial statement
    products = Product.objects.filter(status=Product.ACTIVE)[0:4]
    return render(request, 'frontpage/frontpage.html',{
        'products':products,
        
    })

