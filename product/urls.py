
from django.urls import path
from django.views.generic.edit import UpdateView
from .views import ProductView, ProductDetailView, NewProductView, UpdateProductView, add_to_cart, wishlist, remove_from_cart,  add_to_cart, OrderSummaryView, CheckoutView, PaymentView, remove_single_product_from_cart, HomeView

urlpatterns = [
     path('', HomeView.as_view(), name='index'),
    path('product/', ProductView.as_view(), name='product'),
    path('product-detail/<int:pk>/',
         ProductDetailView.as_view(), name='product-detail'),
    path('new_product/', NewProductView.as_view(), name='new_product'),
    # path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('product-detail/edit/<int:pk>/',
         UpdateProductView.as_view(), name='update_product'),
    path('wishlist/', wishlist, name='wishlist'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('add-to-cart/<pk>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>/', remove_from_cart, name='remove-from-cart'),
    path('remove_single_product_from_cart/<pk>/',
         remove_single_product_from_cart, name='remove_single_product_from_cart'),
]
