

from django.urls import path
from django.contrib import admin
from .views import products,add_to_cart,get_cart,get_total,product_description,create_account,validateCreditCard

urlpatterns = [
    path('',products),
    path('add-to-cart/',add_to_cart),
    path("get-cart/",get_cart),
    path("get-total/",get_total),
    path("product-description/",product_description),
    path("create-account/",create_account),
    path("make-payment/",validateCreditCard)

]
