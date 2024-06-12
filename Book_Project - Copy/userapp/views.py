from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import JsonResponse

from .models import *
from .forms import OrderForm,EditProfileForm
from bookapp.models import *
from userapp.cart import *
from bookapp.decorators import *

# Create your views here.
#____________________________________________________________USERDASH
@login_required(login_url='login')
def userdash(request):
    user = request.user.customer
    pk=user.id
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()

    context={'orders':orders,
             'total_orders':total_orders,'delivered':delivered,'pending':pending,
            'pk':pk,
            }
    return render(request,'userapp/userdash.html',context)



#____________________________________________________________USERPRODUCTS
@login_required(login_url='login')
def user_products(request):
    products = Book.objects.all()
    context={'products':products}
    return render(request,'userapp/user_products.html',context)


#____________________________________________________________USERORDERS
@login_required(login_url='login')
def user_orders(request,pk):
    user = request.user.customer
    pk=user.id
    customer = Customer.objects.get(id=pk)
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    context={'total_orders':total_orders,'delivered':delivered,'pending':pending,
             'orders': orders,'customer':customer}
    return render(request,'userapp/user_orders.html',context)


#____________________________________________________________USERPROFILE
@login_required(login_url='login')
def user_details(request):
    Customer = request.user.customer
    context={'customer':Customer}
    return render(request,'userapp/userdetails.html',context) 

#____________________________________________________________EDITPROFILE
@login_required(login_url='login')
def edit_profile(request):
    customer = request.user.customer
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('userdetails')  # Redirect to user profile page
    else:
        form = EditProfileForm(instance=customer)
    
    context = {'form': form}
    return render(request, 'userapp/edit_profile.html', context)


#____________________________________________________________CREATEORDER
@login_required(login_url='login')
def create_order(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','quantity','status'))
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet()
    # form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset=OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
        
    context={'formset': formset}
    return render(request,'userapp/createorder.html',context) 


#____________________________________________________________UPDATEORDER
@login_required(login_url='login')
def update_order(request,pk):

    order=Order.objects.get(id=pk)
    url = reverse('userorders', kwargs={'pk': pk})
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect(url)
        
    else:
            form = OrderForm(instance=order)
        
    context={'form': form}
    return render(request,'userapp/updateorder.html',context) 


#____________________________________________________________DELETEORDER
@login_required(login_url='login')
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    user = request.user
    uid = user.customer.id
    url = reverse('userorders', kwargs={'pk': uid})

    if request.method == 'POST':
        order.delete()
        return redirect(url)
    context = {'order': order}
    return render(request,'userapp/deleteorder.html', context)


#____________________________________________________________CARTADD
@login_required(login_url='login')
def cart_add(request):
    cart = Cart(request)

    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Book, id=product_id)
        quantity = int(request.POST.get('quantity')) 
        cart.add(product=product, quantity=quantity) 
        cart_qty = len(cart)

        return JsonResponse({'qty': cart_qty, 'success': True, 'message': 'Product added to cart successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request.'})
    

#____________________________________________________________CARTSUMMARY
@login_required(login_url='login')    
def cart_sum(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    
    for product in cart_products:
        product.quantity = cart.get_quantity(product.id)

    total_price=sum(product.price*product.quantity for product in cart_products)    
    
    context = {
        'cart_products': cart_products,
        'total_price':total_price
    }
    return render(request,'userapp/user_cart.html', context)


#____________________________________________________________CARTUPDATE
@login_required(login_url='login')
def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Book, id=product_id)
        cart.update(product=product, quantity=quantity)
        cart_qty = cart.__len__()
        return JsonResponse({'qty': cart_qty, 'success': True, 'message': 'Cart updated successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request.'})


#____________________________________________________________CARTDELETE
@login_required(login_url='login')
def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Book, id=product_id)
        cart.remove(product)
        cart_qty = cart.__len__()
        return JsonResponse({'qty': cart_qty, 'success': True, 'message': 'Product removed from cart successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request.'})
    



#____________________________________________________________PLACEORDER
@login_required(login_url='login')
def place_order(request):
    cart = Cart(request)
    customer = request.user.customer

    if request.method == 'POST':
        for item in cart.get_product():
            order = Order.objects.create(
                customer=customer,
                product=item,
                quantity=cart.cart[str(item.id)]['quantity'],
                status='Pending'
            )
        cart.clear()
        return redirect('userorders', pk=customer.id)

    context = {
        'cart_products': cart.get_products()
    }
    return render(request, 'userapp/place_order.html', context)