from django.urls import path
from ecommerceapp import views

urlpatterns = [
    path('',views.index,name="index"),
    path('checkout',views.checkout,name="checkout"),
    path('contact',views.contact,name="contact"),
    path('profile',views.profile,name="profile")
     ]
