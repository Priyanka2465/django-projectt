from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('',views.indexx,name='indexx'),
    path('index',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('changepass/',views.changepass,name='changepass'),
    path('forgotpass/',views.forgotpass,name='forgotpass'),
    path('otp/',views.otp,name='otp'),
    path('npass/',views.npass,name='npass'),
    path('fpassword_email/',views.fpassword_email,name='fpassword_email'),
    path('password/',views.password,name='password'),
    path('email_newpassword/',views.email_newpassword,name='email_newpassword'),
    path('add/',views.add,name='add'),
    path('profile/',views.profile,name='profile'),
    path('viewp/',views.viewp,name='viewp'),
    path('editp/<int:pk>',views.editp,name='editp'),
    path('deletep/<int:pk>',views.deletep,name='deletep'),
    path('showp/<str:cat>/',views.showp,name='showp'),
    path('searchproduct/',views.searchproduct,name="searchproduct"),
    path('details/<int:pk>/',views.details,name='details'),
    path('addlike/<int:pk>/',views.addlike,name='addlike'),
    path('dlike/<int:pk>/',views.dlike,name='dlike'),
    path('like/',views.like,name='like'),
    path('cart/',views.view_cart, name='cart'),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('change-qty/<int:pk>/',views.change_qty,name='change-qty'),
    path('removecart/<int:pk>/', views.removecart, name='removecart'),
    path('checkout/',views.checkout,name='checkout'),
    path('invoice/',views.invoice,name='invoice'),
    # path('item_increment/<int:pk>/',views.item_increment, name='item_increment'),
    # path('decrement/<int:pk>/',views.decrement, name='decrement'),
    # path('addcart/<int:pk>/',views.addcart,name='addcart'),
    # path('dcart/<int:pk>/',views.dcart,name='dcart'),
    # path('cart/',views.cart,name='cart'),
]