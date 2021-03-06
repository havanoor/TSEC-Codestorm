from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns=[
    #path('',views.list_crops,name="display"),
    path('',views.register, name='signup'),
    path('logout',views.logout_view, name = "logout"),

    path('suggestion/',views.suggestion, name = "suggestion"),
    path('order/<str:pref>',views.order,name = "order"),
    path('farmershop/',views.farmersell,name = "FS"),
    path('cropseeds/',views.CropView.as_view()),

    path('farmer',views.farmerHome, name='farmer_home'),

    #path('dashboard/',views.dashboard,name = "dashboard"),


    path('farmer/<int:id>/crop',views.CropCreate, name="crop_add"),
    path('f',views.cropd, name='category'),
    path('farmer/crop/', views.Crop_View, name = 'crop_view'),
    path('farmer/crop/<int:pk>/update', views.UpdateCrop.as_view(),name='update_crop'),
    path('farmer/crop/<int:pk>/delete', views.DeleteCrop.as_view(), name = 'delete_crop'),




    path('sug/<str:state>',views.sugs, name= "getcrops"),
    path('indi/<str:sc_id>',views.individual_product,name="individual"),
    path('buyer/shop', views.product_list, name='product_list'),
    path('buyer/shop/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('buyer/shop/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('logout',views.logout_view, name = "logout"),
    path('hin/farmer',views.hin_view, name='farmer_home_hin'),

    path('buyer', views.product_list, name='product_list'),
    path('buyer/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('buyer/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('buyer/cart',views.cart_detail,name='cart_detail'),
    path('buyer/cart/add/<int:product_id>',views.cart_add,name='cart_add'),
    path('buyer/cart/remove/<int:pid>',views.cart_remove,name='cart_remove'),
    path('buyer/Order/create',views.order_create, name='order_create'),
    path('logout',views.logout, name='logout'),

    path('farmer/shop', views.farm_product_list, name='farmer_product_list'),
    path('farmer/shop/<str:sc_id>', views.farm_product_detail, name='farmer_product_detail'),
    path('farmer/cart',views.farm_cart_detail,name='farmer_cart_detail'),
    path('farmer/cart/add/<str:sc_id>',views.farm_cart_add,name='farmer_cart_add'),
    path('farmer/cart/remove/<str:pid>',views.farm_cart_remove,name='farmer_cart_remove'),
    path('farmer/Order/create',views.farm_order_create, name='farmer_order_create'),





  ]
