from django.contrib import admin
from django.urls import path,include
from .views import *
from .views import Login,Signup,Index
urlpatterns = [

    path('',Index.as_view(), name ='homepage'),
    path('signup',Signup.as_view()),
    path('loguser',Login.as_view(),name = 'loguser'),
    path('cart',Cart.as_view(),name = 'cart'),
    path('checkout',Checkout.as_view(),name = 'checkout'),
    path('order',Order.as_view(),name = 'order'),
    path('logout',logout,name = 'logout'),
    path('contact',Contact,name = 'contact'),
    path('aboutus',Aboutus,name = 'aboutus'),

]