from django.shortcuts import render,redirect
from . models import *
import random
import requests
from django.db.models import Q
from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail



# Create your views here.
def home(request):
    return render(request,'home.html')

def indexx(request):
    return render(request,"index.html")

def index(request):
    user=User.objects.get(email=request.session['email'])
    if user.usertype=="buyer":
        return render(request,"index.html")
    else:
        return render(request,"sindex.html")

def about(request):
    return render(request,'about.html')

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Your email is already registered"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    usertype=request.POST['usertype'],
                    name=request.POST['name'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    password=request.POST['password'],
                    profile=request.FILES['profile'],
                )
                msg="Successfully signup"
                return render(request,'login.html',{'msg':msg})
            else:
                msg="Password and confirm Password not match"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                request.session['email']=user.email
                request.session['name']=user.name
                request.session['profile']=user.profile.url
                like=Like.objects.filter(user=user)
                request.session['like']=len(like)
                cart_items=Cart.objects.filter(user=user)
                request.session['cart']=len(cart_items)
                if user.usertype=="buyer":
                    return render(request,'index.html')
                else:
                    return render(request,'sindex.html')
            else:
                msg="Password wrong.."
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Email not Registration..."
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')
    
def logout(request):
    del request.session['email']
    del request.session['name']
    del request.session['profile']
    del request.session['like']
    del request.session['cart']
    return render(request,'login.html')

def changepass(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        if user.password==request.POST['opassword']:
            if request.POST['npassword']==request.POST['cnpassword']:
                user.password=request.POST['npassword']
                user.save()
                return redirect('logout')
            else:
                msg="New password and Confirm Password not match.."
                if user.usertype=="buyer":
                    return render(request,'changepass.html',{'msg':msg})
                else:
                    return render(request,'schangepass.html',{'msg':msg})
        else:
            msg="Old Password wrong"
            if user.usertype=="buyer":
                return render(request,'changepass.html',{'msg':msg})
            else:
                return render(request,'schangepass.html',{'msg':msg})
    else:
        if user.usertype=="buyer":
            return render(request,'changepass.html')
        else:
            return render(request,'schangepass.html')
    
def forgotpass(request):
    if request.method=="POST":
        user=User.objects.get(mobile=request.POST['mobile'])
        mobile=request.POST['mobile']
        otp=random.randint(1000,9999)
        url = "https://www.fast2sms.com/dev/bulkV2"

        querystring = {"authorization":"s26ti9zkLybH75TEJw8UWRMaog3hnBcNuflDjASVXC1dKQGOqYMqcZeDuLhz5NkCV3xEs0yoYrQAfj1F","variables_values":str(otp),"route":"otp","numbers":mobile}

        headers = {
                    'cache-control': "no-cache"
                    }

        response = requests.request("GET", url, headers=headers, params=querystring)
        request.session['mobile']=mobile
        request.session['otp']=otp
        return render(request,'otp.html')
    else:
        return render(request,'forgotpass.html')
    
def otp(request):
    if request.method=="POST":
        otp=int(request.session['otp'])
        uotp=int(request.POST['uotp'])

        if otp==uotp:
            del request.session['otp']
            return render(request,'npass.html')
        else:
            msg="Invalid OTP..."
            return render(request,'otp.html',{'msg':msg})
    else:
        return render(request,'otp.html')
    

def npass(request):
    if request.method=="POST":
        user=User.objects.get(mobile=request.session['mobile'])
        if request.POST['npassword']==request.POST['cnpassword']:
            user.password=request.POST['npassword']
            user.save()
            return render(request,'login.html')
        else:
            msg="New Password and Confirm New Password Not match"
            return render(request,'npass.html',{'msg':msg})
    else:
        return render(request,'npass.html')

def fpassword_email(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            otp=random.randint(1000,9999)
            subject = 'OTP for Forgot Password'
            message = 'Hello' + user.name + ',Your OTP for forgot Password is' + str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            request.session['otp']=otp
            request.session['email_otp']=user.email
            
            return render(request,'password.html')
            
        except:
            msg="Email Not registered"
            return render(request,'fpassword_email.html',{'msg':msg})
    else:
        return render(request,'fpassword_email.html')
    
        

def password(request):
    otp=int(request.POST['otp'])
    if otp==int(request.session['otp']):
        del request.session['otp']
        return render(request,"email_newpassword.html") 

    else:
        msg="Invalid Password !"
        return render(request, "email_newpassword.html",{'msg':msg}) 
        
    
def email_newpassword(request):
     if request.method=="POST":
        if request.POST['e_newpassword']==request.POST['e_cpassword']:
            user= User.objects.get(email=request.session['email_otp'])
            user.password=request.POST['e_newpassword']
            user.save()
            return render(request,"login.html")
               
        else:
            msg="New Password and Confirm Password does not match !!"
            return render(request,"email_newpassword.html",{'msg':msg})
          
     else:
          return render(request,"email_newpassword.html")
    
def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.name=request.POST['name']
        user.mobile=request.POST['mobile']
        try:
            user.profile=request.FILES['profile']
        except:
            pass
        user.save()
        msg="Update successfully"
        if user.usertype=='buyer':
            return render(request,'profile.html',{'user':user,'msg':msg})
        else:
            return render(request,'sprofile.html',{'user':user,'msg':msg})
    else:
        if user.usertype=='buyer':
            return render(request,'profile.html',{'user':user})
        else:
            return render(request,'sprofile.html',{'user':user})

def add(request):
    if request.method=="POST":
        user=User.objects.get(email=request.session['email'])
        Addproduct.objects.create(
            seller=user,
            pcategory=request.POST['pcategory'],
            pname=request.POST['pname'],
            pbrand=request.POST['pbrand'],
            pdesc=request.POST['pdesc'],
            pprice=request.POST['pprice'],
            pimg=request.FILES['pimg'],
        )
        msg="Product add successfully"
        return render(request,'add.html',{'msg':msg})
    else:
        return render(request,'add.html')

def viewp(request):
    seller=User.objects.get(email=request.session['email'])
    product=Addproduct.objects.filter(seller=seller)
    return render(request,'viewp.html',{'product':product})

def editp(request,pk):
    product=Addproduct.objects.get(pk=pk)
    if request.method=="POST":
        product.pcategory=request.POST['pcategory']
        product.pname=request.POST['pname']
        product.pbrand=request.POST['pbrand']
        product.pdesc=request.POST['pdesc']
        product.pprice=request.POST['pprice']
        try:
            product.pimg=request.FILES['pimg']
        except:
            pass
        product.save()
        msg="Product edit successfully"
        return render(request,'editp.html',{'product':product,'msg':msg}) 
    else:
        return render(request,'editp.html',{'product':product})


def deletep(request,pk):
    product=Addproduct.objects.get(pk=pk)
    product.delete()
    return redirect('viewp')

def showp(request,cat):
    product=Addproduct()
    if cat=='all':
        product=Addproduct.objects.all()
    elif cat=='apple':
        product=Addproduct.objects.filter(pcategory='apple')
    elif cat=='banana':
        product=Addproduct.objects.filter(pcategory='banana')
    elif cat=='kiwi':
        product=Addproduct.objects.filter(pcategory='kiwi')
    elif cat=='cherry':
        product=Addproduct.objects.filter(pcategory='cherry')
    elif cat=='mango':
        product=Addproduct.objects.filter(pcategory='mango')
    elif cat=='grapes':
        product=Addproduct.objects.filter(pcategory='grapes')
    return render(request,'showp.html',{'product':product})

def details(request,pk):
    try:
        w = False
        w1 = False
        user=User.objects.get(email=request.session['email'])
        product=Addproduct.objects.get(pk=pk)
        try :
            Like.objects.get(user=user,product=product)
            w =True
        except:
            pass
        

        try :
            Cart.objects.get(user=user,product=product)
            w1 =True
        except:
            pass
        return render(request,'details.html',{'product':product,'w':w,'w1':w1})
    except:
        product=Addproduct.objects.get(pk=pk)
        return render(request,"details.html",{'product':product})


def searchproduct(request):
    data1 = User.objects.filter()
    qdata = request.GET.get('q')
    data = Addproduct.objects.filter(  
         Q(pname__icontains=qdata) | Q(pprice__icontains=qdata))
    return render(request,"searchproduct.html",{'data':data,'data1':data1})

def addlike(request,pk):
    try:
        user= User.objects.get(email=request.session['email'])
        product= Addproduct.objects.get(pk=pk)
        # Like.objects.create(user=user,product=product)
        if not Like.objects.filter(user=user, product=product).exists():
            # If not, add the product to the like
            Like.objects.create(user=user, product=product)
        return redirect("like")
    except:
        msg="Login required"
        return render(request,'login.html',{'msg':msg})

def like(request):
    try:
        user= User.objects.get(email=request.session['email'])
        like=Like.objects.filter(user=user)
        request.session['like']=len(like)
        return render(request,"like.html",{'like':like})
    except:
        return redirect(index)
    
def dlike(request,pk):
    user= User.objects.get(email=request.session['email'])
    product= Addproduct.objects.get(pk=pk)
    like= Like.objects.get(user=user,product=product)
    like.delete()
    return redirect("like")

def view_cart(request):
    cart_price=0
    user= User.objects.get(email=request.session['email'])
    cart_items = Cart.objects.filter(user=user)
    request.session['cart']=len(cart_items)
    for i in cart_items:
        cart_price=cart_price+i.total_price
    
    
    return render(request,'cart.html', {'cart_items': cart_items,'cart_price': cart_price})

def add_to_cart(request, pk):
    try:
        user= User.objects.get(email=request.session['email'])
        product = Addproduct.objects.get(pk=pk)
        Cart.objects.create(
            product=product,
            user=user,
            product_price=product.pprice,
            qty=1,
            total_price=product.pprice
        )
        return redirect('cart')
    except:
        msg="Login required for Add to cart..."
        return render(request,'login.html',{'msg':msg})

def change_qty(request,pk):
	cart=Cart.objects.get(pk=pk)
	product_qty=int(request.POST['product_qty'])
	cart.qty=product_qty
	cart.total_price=product_qty*cart.product_price
	cart.save()
	return redirect('cart')

# def change_qty(request):
#     pk=request.POST['id']
#     print(pk)
#     product_qty=int(request.POST['product_qty'])
#     cart_items=Cart.objects.get(pk=pk)
#     # cart_items.qty=product_qty
#     total_price = sum(item.product.pprice * item.qty for item in cart_items)
#     # cart.total_price=cart.product_price*product_qty
#     cart_items.save()

#     return redirect(request,'cart.html',{'total_price': total_price})
#     product = Addproduct.objects.get(pk=pk)
#     cart_items=Cart.objects.get(product=product)
#     cart_items.add()
#     return redirect("view_cart")    

# def decrement(request, pk):
#     item = Cart.objects.get(pk=pk)
#     if 0 < (item.qty - 1) <= item.product:
#         item.qty -= 1
#         item.save()
#         return redirect('cart')
    

def removecart(request,pk):
    cart_item = Cart.objects.get(pk=pk)
    cart_item.delete()
    return redirect('cart')

# def checkout(request):
#     if request.method=="POST":
#         user= User.objects.get(email=request.session['email'])
#         cart=Cart.objects.filter(user=user,payment_status=False)
#         Checkout.objects.create(
#             chname=request.POST['chname'],
#             chmobile=request.POST['chmobile'],
#             add=request.POST['add']
#         )
#         msg="Checkout successfully..."
#         return render(request,'invoice.html',)
#     else:
#         return render(request,'checkout.html')

# def checkout(request):
#     user=User.objects.get(email=request.session['email'])
#     check=Checkout.objects.filter()
#     if request.method=="POST":
#         check.chname=request.POST['chname']
#         check.chmobile=request.POST['chmobile']
#         check.add=request.POST['add']
        
#         msg="Checkout successfully"
#         return render(request,'invoice.html',)
#     else:
#         return render(request,'checkout.html',{'user':user,'check':check})
    
def checkout(request):  
    if request.method=="POST":
        user=User.objects.get(email=request.session['email'])
        cart=Cart.objects.filter(user=user)

        Checkout.objects.create(
            user=user,
            
            chname=request.POST['chname'],
            chmobile=request.POST['chmobile'],
            add=request.POST['add'],
        )
        
        return redirect('invoice')
    else:
        return render(request,'checkout.html')

    
def invoice(request):
    cart_price=0
    user=User.objects.get(email=request.session['email'])
    cart=Cart.objects.filter(user=user)
    for i in cart:
        cart_price=cart_price+i.total_price
    
    return render(request,'invoice.html',{'user':user,'cart':cart,'cart_price':cart_price})   

