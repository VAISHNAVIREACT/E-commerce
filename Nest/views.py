from django.shortcuts import render,redirect,reverse,get_object_or_404
from . import forms,models
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings
from .models import Product,Customer
from .forms import AddressForm








# Create your views here.


def home_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids =request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
         product_count_in_cart=0
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')     
    return render(request,"index.html",{'products':products,'product_count_in_cart':product_count_in_cart})

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')

def is_customer(user):
    return user.groups.filter(name='customer-home').exists()



def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-home')
    else:
        return redirect('admin-dashboard')
    



@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    customercount=models.Customer.objects.all().count()
    productcount=models.Product.objects.all().count()
    ordercount=models.Orders.objects.all().count()

    orders=models.Orders.objects.all() 
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id=order.Customer.id) 
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)  
    dict={
        'customercount':customercount,
        'productcount':productcount,
        'ordercount':ordercount,
        'data':zip(ordered_products,ordered_bys,orders),
    }    
    return render(request,'admin_dashboard.html',context=dict)

def aboutus_view(request):
    return render(request,'aboutus.html')


def contactus_view(request):
    return render(request,'contactus.html')

# def register_view(request):
#     return render(request,'register.html')

# def login_view(request):
#     return render(request,'customerlogin.html')

def customer_view(request):
    return render(request,'customer.html')

@login_required(login_url='adminlogin')
def product_view(request):
    products=models.Product.objects.all()
    return render(request,'product_view.html',{'products':products})

    
    

@login_required(login_url='adminlogin')
def delete_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    product.delete()
    return redirect('product-view')

@login_required(login_url='adminlogin')
def update_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    productForm=forms.ProductForm(instance=product)
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST,request.FILES,instance=product)
        if productForm.is_valid():
            productForm.save()
            return redirect('product-view')
    return render(request,'update_product_view.html',{'productForm':productForm})



@login_required(login_url='adminlogin')
def booking_view(request):
    orders=models.Orders.objects.all() 
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id=order.Customer.id) 
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)  
    return render(request,'booking.html',{'data':zip(ordered_products,ordered_bys,orders)})


def customer_signup_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm} 
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password) 
            user.save()

            customer = customerForm.save(commit=False)
            customer.user = user  
            customer.save()

            my_customer_group, _ = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('logincust')

    return render(request, 'customer_signup.html', context=mydict)


    # admin add product by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_product_view(request):
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('product-view')
    return render(request,'admin_add_products.html',{'productForm':productForm})

# 
# @user_passes_test(is_customer)
# def customer_home_view(request):
#     products=models.Product.objects.all()
#     if 'product_ids' in request.COOKIES:
#         product_ids =request.COOKIES['product_ids']
#         counter=product_ids.split('|')
#         product_count_in_cart=len(set(counter))
#     else:
#          product_count_in_cart=0
#     return render(request,'customer_home.html')
@user_passes_test(is_customer)
@login_required(login_url='customerlogin')     
def customer_home_view(request):
    products = Product.objects.all()

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    context = {
        'products': products,
        'product_count_in_cart': product_count_in_cart,
    }

    return render(request, 'customer_home.html', context)


# def customer_home_view(request):
#     return render(request,'customer_home.html')



def search_view(request):
    query=request.GET['query']
    products=models.Product.objects.all().filter(name__icontains=query)
    if 'product_ids'in request.COOKIES:
        product_ids=request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0
    word="Searched Result"
    if request.user.is_authenticated:
        return render(request,'customer_home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})
    return render(request,'index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})

# def cart_view(request):
#     if 'product_ids' in request.COOKIES:
#         product_ids=request.COOKIES['product_ids']
#         counter=product_ids.split('|')
#         product_count_in_cart=len(set(counter))
#     else:
#         product_count_in_cart=0

#     products=None
#     total=0
#     if 'product_ids' in request.COOKIES:
#         product_ids=request.COOKIES['product_ids']

#         if product_ids !="":
#             product_id_in_cart=product_ids.split('|')
#             products=models.Product.objects.all().filter(id__in = product_id_in_cart)

#             for p in products:
#                 total=total+p.price
#     return render(request,'cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})             


def cart_view(request):
    product_count_in_cart = 0
    products = None
    total = 0

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']

        if product_ids:
            product_id_in_cart = [int(pid) for pid in product_ids.split('|') if pid.isdigit()]

            if product_id_in_cart:
                products = models.Product.objects.filter(id__in=product_id_in_cart)
                product_count_in_cart = len(set(product_id_in_cart))

                for p in products:
                    total += p.price

    return render(request, 'cart.html', {'products': products, 'total': total, 'product_count_in_cart': product_count_in_cart})


def add_to_cart_view(request,pk):
    products=models.Product.objects.all()

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 1
    response= render(request,'index.html',{'products':products,'product_count_in_cart':product_count_in_cart})    
    
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(pk)
        else:
            product_ids=product_ids+"|"+str(pk)
        response.set_cookie('product_ids',product_ids)
    else:
        response.set_cookie('product_ids',pk)

    product=models.Product.objects.get(id=pk)
    # messages.info(request,product.name + 'added to your cart successfully!')

    return response

      
# def remove_from_cart_view(request,pk):
#     if 'product_ids' in request.COOKIES:
#         product_ids = request.COOKIES['product_ids']
#         counter=product_ids.split('|')
#         product_count_in_cart=len(set(counter))
#     else:
#         product_count_in_cart=0 
#     total=0
#     if 'product_ids' in request.COOKIES:
#         product_ids = request.COOKIES['product_ids']
#         product_id_in_cart=product_ids.split('|')
#         product_id_in_cart=list(set(product_id_in_cart))
#         product_id_in_cart.remove(str(pk))
#         products=models.Product.objects.all().filter(id__in = product_id_in_cart)
#         for p in products:
#             total=total+p.price
#         value = ""
#         for i in range(len(product_id_in_cart)):
#             if i==0:
#                 value = value+"|"+product_id_in_cart[0]
#             else:
#                 value = value+"|"+product_id_in_cart[i]
#         response = render(request,'cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart}) 
#         if value=="":
#             response.delete_cookie('product_ids')
#         response.set_cookie('product_ids',value) 
#         return response




def remove_from_cart_view(request, pk):
 if 'product_ids' in request.COOKIES:
    product_ids = request.COOKIES['product_ids']
    
    if product_ids:
        product_id_in_cart = [int(pid) for pid in product_ids.split('|') if pid.isdigit()]
        product_id_in_cart = list(set(product_id_in_cart))
        
        if str(pk) in product_id_in_cart:
            product_id_in_cart.remove(str(pk))
            products = models.Product.objects.all().filter(id__in=product_id_in_cart)
            
            total = sum(p.price for p in products)
            
            value = '|'.join(map(str, product_id_in_cart))
            
            response = render(request, 'cart.html', {'products': products, 'total': total, 'product_count_in_cart': len(product_id_in_cart)})

            if not product_id_in_cart:
                response.delete_cookie('product_ids')
            else:
                response.set_cookie('product_ids', value)
            
            return response

 return HttpResponse("Error: Product not found in the cart or other issues.")

def signup_view(request):
    return render(request,'signup.html')

def customer_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Check if a customer with the provided username and password exists
            customer = Customer.objects.get(username=username, password=password)

            # If the customer is found, set some session variables or perform any other desired actions
            request.session['customer_id'] = customer.id

            # Redirect to the customer home page or any other desired page
            return redirect('customer_home')  # Change 'customer_home' to the actual name of your customer home URL

        except Customer.DoesNotExist:
            # If customer not found, you might want to display an error message or handle it accordingly
            error_message = "Invalid username or password. Please try again."

    else:
        error_message = None

    return render(request, 'logincust.html', {'error_message': error_message})




def customers_home_view(request):
    products = Product.objects.all()

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    context = {
        'products': products,
        'product_count_in_cart': product_count_in_cart,
    }

    return render(request,'customers_home.html')



# def customer_address_view(request):
#     return render(request,'customer_address.html')

# @login_required(login_url='customerlogin')
def customer_address_view(request):
    product_in_cart=False
    if 'product_ids' in request.COOKIES:
        product_ids=request.COOKIES['product_ids']
        if product_ids !="":
            product_in_cart=True

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    addressForm=forms.AddressForm()

    if request.method == 'POST':
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            Email= addressForm.cleaned_data['Email']
            Mobile= addressForm.cleaned_data['Mobile']
            Address= addressForm.cleaned_data['Address']
            total=0
            if 'product_ids' in request.COOKIES:
                product_ids=request.COOKIES['product_ids']
                if product_ids !="":
                    product_id_in_cart=product_ids.split('|')
                    products=models.Product.objects.all().filter(id__in=product_id_in_cart)
                    for p in products:
                        total=total+p.price
            response = render(request,'payment.html',{'total':total})
            response.set_cookie('Email',Email)
            response.set_cookie('Mobile',Mobile)
            response.set_cookie('Address',Address)
            return response
    return render(request, 'customer_address.html', {'addressForm':addressForm,'product_in_cart':product_in_cart,'product_count_in_cart':product_count_in_cart})

def payment_view(request):
    return render(request,'payment.html')


def payment_completed_view(request):
    return render(request,'paymentcompleted.html')


