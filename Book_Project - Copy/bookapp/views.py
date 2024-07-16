from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from django.contrib import auth,messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.shortcuts import render,redirect

# Create your views here.
from .forms import BookForm,AuthorForm,CreateUserForm
from .models import *
from userapp.models import *
from .decorators import unauth_user,allowed_users,loggeduser
import stripe



#___________________________________________________________CREATEVIEW
# def createBook(request):
#     books = Book.objects.all()

#     if request.method='POST":
#         title=reques'POST.get('title')
#         author=reques'POST.get('author')
#         price=reques'POST.get('price')
#         img_url=reques'POST.get('URL')

#         book=Book(title=title,author=author,price=price,url=img_url)
#         book.save()

#     return render(request,'book.html',{'books':books})    

#___________________________________________________________CREATEBOOK
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def createBook(request):
    books = Book.objects.all()

    if request.method=='POST':
        form=BookForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')   
    
    else:
        form=BookForm()
        
    return render(request,'book.html',{'form':form,'books':books})


#___________________________________________________________LISTVIEW
def listbook(request):
    books = Book.objects.all()

    paginator=Paginator(books,4)
    page_number=request.GET.get('page')

    try:
        page=paginator.get_page(page_number)

    except EmptyPage:
        page=paginator.page(page_number.num_pages)


    return render(request,'listbook.html',{'books':books,'page':page})


#___________________________________________________________DETAILSVIEW
def detailsView(request,book_id):
    book=Book.objects.get(id=book_id)
    return render(request,'detailsview.html',{'book':book})


#___________________________________________________________UPDATEVIEW
@allowed_users(allowed_roles=['Admin'])
def updateBook(request,book_id):
    book= Book.objects.get(id=book_id)

    if request.method=='POST':
        form = BookForm(request.POST,instance=book)

        if form.is_valid():
            form.save()
            return redirect('/')   
    
    else:
        form=BookForm(instance=book)
        
    return render(request,'updateview.html',{'form':form})   


#____________________________________________________________DELETEVIEW
@allowed_users(allowed_roles=['Admin'])
def deleteView(request,book_id):

    book=Book.objects.get(id=book_id)
    if request.method=='POST':
        book.delete()
        return redirect('/')    

    return render(request,'deleteview.html',{'book':book})


#____________________________________________________________CREATEAUTHOR
@allowed_users(allowed_roles=['Admin'])
def CreateAuthor(request):
    authors=Author.objects.all()
 
    if request.method=='POST':
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')    

    else:
        form=AuthorForm()
    return render(request,'author.html',{'form':form,'authors':authors})


#____________________________________________________________DELETEAUTHOR
@allowed_users(allowed_roles=['Admin'])
def DeleteAuthor(request,book_id):

    book=Author.objects.get(id=book_id)

    if request.method=="POST":

        book.delete()

        return redirect('/')

    return render(request,'deleteview.html',{'book':book})

#____________________________________________________________UPDATEAUTHOR
@allowed_users(allowed_roles=['Admin'])
def UpdateAuthor(request,book_id):

   book = Author.objects.get(id=book_id)
   if request.method=='POST':
       form = BookForm(request.POST,instance=book)

       if form.is_valid():
           form.save()

           return redirect('/')
   else:
       form=AuthorForm(instance=book)

   return render(request,'updateview.html',{'form':form})


#____________________________________________________________SEARCH
def Search_Book(request):
    query=None
    books=None

    if 'q' in request.GET:

        query=request.GET.get('q')
        books=Book.objects.filter(Q(title__icontains=query))
        
    else:
        books=[]

    paginator=Paginator(books,4)
    page_number=request.GET.get('page')

    try:
        page=paginator.get_page(page_number)

    except EmptyPage:
        page=paginator.page(page_number.num_pages)

    return render(request,'search.html',{'books':books,'query':query,'page':page})

#____________________________________________________________REGISTER
@unauth_user
def Register_user(request):
    form=CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():

            User = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Customer')
            User.groups.add(group)
            Name = f"{User.first_name} {User.last_name}"
            Email = User.email
            Customer.objects.create(
                user= User,
                name=Name,
                email= Email
                )

            messages.success(request,'Account was created for ' + username)
            return redirect('login')
    else:
            # messages.success(request,'Account was not created for ' + username)
            form=CreateUserForm()
    return render(request,'register.html',{'form':form})
    

#____________________________________________________________LOGIN
@unauth_user
def loginUser(request):

    if request.method=='POST':
        Username=request.POST.get('username')
        Password=request.POST.get('password')
        user = authenticate(request, username=Username , password=Password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or password is wrong')
            return redirect('login')
        
    return render(request,'login.html')

#___________________________________________________________LISTVIEW
@allowed_users(allowed_roles=['Admin'])
def Registered_users(request):
    users = User.objects.all()

    paginator=Paginator(users,4)
    page_number=request.GET.get('page')

    try:
        page=paginator.get_page(page_number)

    except EmptyPage:
        page=paginator.page(page_number.num_pages)


    return render(request,'registered_users.html',{'users':users,'page':page})

#____________________________________________________________LOGOUT
def logoutUser(request):
    logout(request)
    return redirect('login')


#____________________________________________________________ADMINBASE
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def admindash(request):
    
    #Customer Pagination
    cdata = Customer.objects.all()
    cpaginator = Paginator(cdata, per_page=5)
    cpage_number = request.GET.get('cpage')
    cpage = cpaginator.get_page(cpage_number)

    #Order Pagination
    odata = Order.objects.all()
    opaginator = Paginator(odata, per_page=5)
    opage_number = request.GET.get('opage')
    opage = opaginator.get_page(opage_number)

    
    total_orders = Order.objects.count()
    delivered = Order.objects.filter(status='Delivered').count()
    pending = Order.objects.filter(status='Pending').count()

    context={
             'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        'cpage': cpage,
        'opage': opage,
            }

    return render(request, 'admindash.html', context)


#____________________________________________________________BASE
@login_required(login_url='login')
@loggeduser
def base(request):

    return render(request,'base.html')
