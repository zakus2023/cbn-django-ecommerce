from django.urls import path

from . import views

# urlpatterns = [
#     path('search/', views.search, name='search'),
#     path('cart/', views.view_cart_view, name='view_cart_view'),
#     path('cart/checkout/', views.checkout, name='checkout'),
#     path('update_quantity/<product_id>', views.update_quantity, name='update_quantity'),
#     path('remove_item/<product_id>/', views.remove_item, name='remove_item'),
#     path('add-to-cart/<int:product_id>', views.add_to_cart, name="add_to_cart"),
#     path('<slug:slug>/', views.product_category, name='product_category'),
#     path('<slug:category_slug>/<slug:slug>/', views.products, name="products"),
# ]

urlpatterns = [
    path('search/', views.search, name='search'),
    path('cart/', views.view_cart_view, name='view_cart_view'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('cart/success/', views.success, name='success'),
    path('update_quantity/<product_id>/', views.update_quantity, name='update_quantity'),
    path('remove_item/<product_id>/', views.remove_item, name='remove_item'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('<slug:slug>/', views.product_category, name='product_category'),
    path('<slug:category_slug>/<slug:slug>/', views.products, name='products'),
]