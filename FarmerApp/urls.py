from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns=[
    #path('',views.list_crops,name="display"),

    path('suggestion/',views.suggestion, name = "suggestion"),
    path('order/<str:pref>',views.order,name = "order"),
    path('farmershop/',views.farmersell,name = "FS"),
    path('cropseeds/',views.CropView.as_view()),
    path('',views.register, name='signup'),
    path('farmer',views.farmerHome, name='farmer_home'),
    path('farmer/<int:id>/crop',views.CropCreate, name="crop_add"),
    path('f',views.cropd, name='category'),
    #path('dashboard/',views.dashboard,name = "dashboard"),
    path('sug/<str:state>',views.sugs, name= "getcrops"),
    path('indi/<str:model>/<int:sc_id>',views.individual_product,name="individual"),
    path('buyer/shop', views.product_list, name='product_list'),
    path('buyer/shop/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('buyer/shop/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),


    path('buyer', views.product_list, name='product_list'),
    path('buyer/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('buyer/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('buyer/cart',views.cart_detail,name='cart_detail'),
    path('buyer/cart/add/<int:product_id>',views.cart_add,name='cart_add'),

    path('buyer/cart/remove/<int:pid>',views.cart_remove,name='cart_remove'),

    path('buyer/Order/create',views.order_create, name='order_create'),


  ]
