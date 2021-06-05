from django.urls import path

from .views import *
urlpatterns = [
    path('',homepageview,name = "homepage"),
    path('category/<int:categoryid>/',categoryview),
    path('search/',searchview,name = "search"),
    path('cart/add/<int:itemid>/',addtocart),
    path('cart/',cartview,name = "cartpage"),
    path('placeorder/',placeorder,name = "placeorder"),
    path('cancelorder/<int:orderid>/',cancelorder,name = "cancelorder"),
    path('cart/delete/<int:cartid>/',deletefromcart),
    path('orders/',ordersview,name = "orders"),


    path('login/',loginview,name = "loginpage"),
    path('login/validate/',loginuser,name = "loginuser"),
    path('signup/',signupview,name = "signuppage"),
    path('signup/register/',registeruser,name = "registeruser"),
    path('logout/',logoutuser,name = "logoutuser")
]