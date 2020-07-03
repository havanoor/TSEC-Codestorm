from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns=[
    path('',views.list_crops,name="display"),

    path('suggestion/',views.suggestion, name = "suggestion"),
    path('order/<str:pref>',views.order,name = "order"),
    path('farmershop/',views.farmersell,name = "FS"),
    path('dashboard/',views.dashboard,name = "dashboard"),



    path('signup',views.register, name='signup'),
    path('signup/farmer', views.register_farmer, name='farmer_add'),
    path('signup/buyer',views.register_buyer, name='buyer_add'),
    path('login/', views.login_view, name='login'),
    path('farmer',views.farmerHome, name='farmer_home'),
    path('buyer',views.buyerHome, name='buyer_home'),
]
