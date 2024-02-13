"""
URL configuration for NovaNest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Nest import views
from django.contrib.auth.views import LoginView,LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    # path('Templates/register.html', views.register_view, name='register'),
    path('afterlogin',views.afterlogin_view,name='afterlogin'),
    path('aboutus',views.aboutus_view,name='aboutus'),
    path('contactus',views.contactus_view,name='contactus'),
    path('logout',LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('adminclick',views.adminclick_view),
    path('adminlogin/',LoginView.as_view(template_name='adminlogin.html'),name='adminlogin'),
    path('admin-dashboard',views.admin_dashboard_view,name='admin-dashboard'),
    path('booking',views.booking_view,name='booking'),
    path('customer',views.customer_view,name='customer'),

    path('admin-add-product',views.admin_add_product_view,name='admin-add-product'),
    path('delete-product/<int:pk>',views.delete_product_view,name='delete-product'),
    path('update-product/<int:pk>',views.update_product_view,name='update-product'),
    path('product-view',views.product_view,name='product-view'),

    path('customerlogin', LoginView.as_view(template_name='customerlogin.html'), name='customerlogin'),
    path('customer-signup',views.customer_signup_view,name='customer-signup'),
    path('customer-home',views.customer_home_view,name='customer-home'),
    path('search',views.search_view,name='search'),
    path('cart',views.cart_view,name='cart'),
    path('add-to-cart/<int:pk>',views.add_to_cart_view,name='add-to-cart'),
    path('remove-from-cart/<int:pk>',views.remove_from_cart_view,name='remove-from-cart'),
    path('signup',views.signup_view,name='signup'),
    path('logincust', LoginView.as_view(template_name='logincust.html'), name='logincust'),
    path('customers-home',views.customers_home_view,name='customers-home'),
    path('customer-address',views.customer_address_view,name='customer-address'),
    path('payment',views.payment_view,name='payment'),
    path('paymentcompleted',views.payment_completed_view,name='paymentcompleted'),

    
    
]



