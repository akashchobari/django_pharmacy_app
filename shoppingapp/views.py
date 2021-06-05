from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
# Create your views here.

def logoutuser(request):
    logout(request)
    return redirect('homepage')

def loginview(request):
    return render(request,"shoppingapp/login.html")

def signupview(request):
    return render(request,"shoppingapp/signup.html")

def loginuser(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username = username,password = password)
    if user is not None:
        login(request,user)

        return redirect("homepage")
    messages.add_message(request, messages.INFO, 'invalid credentials')
    return redirect(request.META["HTTP_REFERER"])

def registeruser(request):
    username = request.POST["username"]
    password = request.POST["password"]
    repassword = request.POST["repassword"]
    if not User.objects.filter(username = username).exists():
        if password==repassword:
            User.objects.create_user(username = username,password=password).save()
            messages.add_message(request, messages.INFO, 'user succesfully created')
        else:
            messages.add_message(request, messages.INFO, 'passwords didnt match')
            return redirect(request.META["HTTP_REFERER"])
    else:
        messages.add_message(request, messages.INFO, 'user already exists')
        return redirect(request.META["HTTP_REFERER"])
    # create user

    
    return redirect("loginpage")

def homepageview(request):
    if not request.user.is_authenticated:
        return redirect('loginpage')
    context = {'user' : request.user,'items' : ItemModel.objects.all(),'categories' : CategoryModel.objects.all()}
    return render(request,"shoppingapp/homepage.html",context)

def categoryview(request,categoryid):
    category = CategoryModel.objects.get(id = categoryid)
    context = {'items' : category.items.all(),'categories' : CategoryModel.objects.all()}
    return render(request,"shoppingapp/homepage.html",context)

def searchview(request):
    search = request.POST['search']
    items = [item for item in ItemModel.objects.all() if item.name.find(search)!=-1]
    context = {'items' : items,'categories' : CategoryModel.objects.all()}
    return render(request,"shoppingapp/homepage.html",context)

def addtocart(request,itemid):
    user = request.user
    item = ItemModel.objects.get(id = itemid)
    CartModel(user = user,item = item).save()
    return redirect(request.META['HTTP_REFERER'])

def cartview(request):
    cartitems = CartModel.objects.filter(user=request.user)
    return render(request,"shoppingapp/cart.html",{'cartitems' : cartitems})
def placeorder(request):
    discount = 0
    if request.POST['promo']!='':
        try:
            discount = int(PromoCodeModel.objects.get(promo = request.POST['promo']).discount)
        except:
            pass
    
    items = [([item.item.name,item.item.price]) for item in CartModel.objects.filter(user = request.user)]

    OrderModel(user = request.user,items = items,discount = discount).save()
    messages.add_message(request,messages.INFO,'order succesfully placed')
    for cart in CartModel.objects.filter(user = request.user):
        cart.delete()
    return redirect('homepage')
def deletefromcart(request,cartid):
    CartModel.objects.get(id = cartid).delete()
    return redirect(request.META['HTTP_REFERER'])
from datetime import date
def ordersview(request):
    orders = []
    today_date = date.today()

    print(today_date)
    for order in OrderModel.objects.filter(user = request.user):
        orders.append(order)
    
    context = {'orders' : orders,'today_date' : today_date }
    return render(request,"shoppingapp/orders.html",context)

def cancelorder(request,orderid):
    order = OrderModel.objects.get(id = orderid).delete()
    return redirect(request.META['HTTP_REFERER'])

