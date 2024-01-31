from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from .models import Product,Cart,Address,Order
from .forms import ProductForm
from django.contrib import messages 
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail 
from django.conf import settings
from datetime import date,timedelta,datetime
import uuid 
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def Email(request):
    send_mail('Welcome', 'Nothing Special.......',settings.EMAIL_HOST_USER,['sakshimore277@gmail.com','sakshimore4178@gmail.com'])
    return HttpResponse('Mail Sending.....')

def Index(request):
    if request.user.is_superuser and request.user.is_authenticated:
        if request.method == 'POST':
            pass
            # fm=ProductForm(request.POST,request.FILES)
            # print(fm)
            # if fm.is_valid():
            #     fm.save()
            #     fm=ProductForm()
            #     return HttpResponseRedirect('/display/')
            # fm=ProductForm()
        # else:
        #     fm=ProductForm()
        return render(request,'admin/index1.html')
    else:
        return HttpResponse('please sign up or login')
    
def Display(request):
    data = Product.objects.all()
    print(data)
    return render(request,'admin/display.html',{'data':data})

def Delete(request,id):
    if request.method == 'POST':
        os=Product.objects.get(pk=id)
        os.delete()
        messages.success(request,'Data Delelte succsesfully')
        return HttpResponseRedirect('/display/')    


def Update(request,id):
    if request.method=='POST':
        os = Product.objects.get(pk=id)
        fm = ProductForm(request.POST,request.FILES, instance=os)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Data Update Successfully')
            return HttpResponseRedirect('/display/')
    else:
        os = Product.objects.get(pk=id)    
        fm = ProductForm(instance=os)
    return render(request,'admin/update.html',{'updateform':fm})

def UserBase(request):
    if request.user.is_authenticated:
        count = Cart.objects.all().count()
        print()

        return render(request,'user/base.html',{'count':count})
    else:
        return HttpResponseRedirect('/')



def UserIndex(request):
    if request.user.is_authenticated:
        data = Product.objects.all()
        count = Cart.objects.filter(user_id=request.user).count()
        order1 = Order.objects.all()
        date1 =date.today()
        days=timedelta(days=7)
        delivery_date= date1+days
        return render(request,'user/index.html',{'data':data,'count':count,'date':delivery_date,'order1':order1})
    else:
        return HttpResponseRedirect('/')


def AddToCart(request):
    if request.user.is_authenticated:
        cid=request.POST.get('cid')
        order1 = Order.objects.filter(product_id=cid)
        if order1.exists():
            messages.success(request,'This Product is already sold and cannot be added to the cart.')
            return HttpResponseRedirect('/userindex/')
        
        if request.method == "POST":
            cid = request.POST.get('cid')
            filter1 = Cart.objects.filter(user_id=request.user).values_list('product_id',flat=True)
            print(type(filter1))
            if int(cid) not in filter1:
                Cart.objects.create(product_id=cid,user=request.user)
                return HttpResponseRedirect('/cart/')
            else:
                messages.success(request,'This Product is already added to cart')
        
        cid= Cart.objects.filter(user_id=request.user).values_list('product_id',flat=True)     
        cartdata = Product.objects.filter(id__in=cid)
        amount=Product.objects.filter(id__in=cid).values_list('price',flat=True)
        amt=0
        for i in amount:
            amt=amt+i
            return render(request,'user/cart.html',{'cdata':cartdata,'amt':amt})
        else:
            messages.success(request,'Product is sold!')
            return HttpResponseRedirect('/userindex/')

    else:
        return HttpResponseRedirect('/')


def RemoveCart(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            Cart.objects.filter(product_id=id).delete()
            return HttpResponseRedirect('/cart/')
    else:
        return HttpResponseRedirect('/')

def ComponentSearch(request):
    if request.user.is_authenticated:
        try:

            if request.method == 'POST':
                search= request.POST.get('search')
                
                sdata= Product.objects.filter(Q(category=search) | Q(pname=search) | Q(description__contains=search)| Q(price__contains=search))
                print(sdata)
            return render(request,'user/search.html',{'sdata':sdata})
        except:
            return HttpResponseRedirect('/userindex')
    else:
        return HttpResponseRedirect('/')


def Details(request,id):
    if request.user.is_authenticated:
        data_detail = Product.objects.filter(pk=id)
    

        return render(request,'user/details.html',{'data':data_detail})
    else:
        return HttpResponseRedirect('/') 

    
def Signup(request):
    if request.method =="POST":
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass')
        # print(uname,pass1,email)
        User.objects.create_user(uname,email,pass1)

        subject = f'Welcome To Pet Store {uname}'
        message = f"""
                    Dear {uname},
                        
                    You have successfully register to The_Pet_Store
                    with {email} this email,

                    Thank you for selecting The_Pet_Store

                    Happy Shopping...Keep Shopping...Stay In Touch

                    'Note: please do not reply to this mail because it is auto generated..'
                        
                    """
        mail_from = settings.EMAIL_HOST_USER
        mail_to = email
        send_mail(subject,message,mail_from,[mail_to])

        messages.success(request,'SignUp Successfully')
        

    return render(request,'user/signup.html')  


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/userindex/')
    return render(request,'user/login.html')


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def address(request,id):
    if request.user.is_authenticated:
        order_id =Order.objects.all().values_list('product_id',flat=True)
        if id not in list(order_id):
            if request.method == 'POST':
                cname = request.POST.get('cname')
                flat = request.POST.get('flat')
                landmark = request.POST.get('landmark')
                city = request.POST.get('city')
                state = request.POST.get('state')
                pincode = request.POST.get('pincode')
                contact = request.POST.get('contact')
                acontact = request.POST.get('acontact')
                #print(cname,flat,landmark,city,state,pincode,contact,acontact)

                Address.objects.create(user=request.user,name=cname,flat=flat,landmark=landmark,city=city,state=state,pincode=pincode,contact=contact,contactA=acontact)

            #here we are fetching data from address
            product_id=id
            data=Address.objects.filter(user_id=request.user)
            return render(request,'user/address.html',{'adata':data,'product_id':product_id})
        else:
            messages.success(request,'This product Is Already Sold')
            return HttpResponseRedirect('/userindex/')
        
    else:
        return HttpResponseRedirect('/')
def Pre_Order(request,aid,pid):
    address_data = Address.objects.filter(pk=aid)
    product_data = Product.objects.filter(pk=pid)
    date1 =date.today()
    days=timedelta(days=5)
    delivery_date= date1+days
    return render(request,'user/pre_order.html',{'adata':address_data,'pdata':product_data,'date':delivery_date,'aid':aid,'pid':pid})

@csrf_exempt
def Order_Confirm(request,aid,pid):
    try:
        product_id = pid
        address_id = aid
        date1 = datetime.now()
        datef = date1.strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4().hex)[:6]
        order_id = f'PS{datef}-{unique_id}'
        oid = request.user
        Order.objects.create(user=oid,product_id=product_id,address_id=address_id,order_id=order_id)
        return render(request,'user/order_confirm.html')
    except:
        return render(request,'user/confirmattion.html')
    

def Payment(request,aid,pid):
    import razorpay
    client = razorpay.Client(auth=("rzp_test_9BZyJ3buu1pncT","6QKQl4eZL8qSwxmeZy02o4tv" ))
    product_amt =Product.objects.filter(id=pid).values_list('price',flat=True)
    print(product_amt[0])
    amount = product_amt[0]

    data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)

    context = {}
    context['amt']=amount*100
    context['aid']=aid
    context['pid']=pid
    return render(request,'user/pay.html',context)



def Cart_Payment(request,aid):
    import razorpay
    if request.user.is_authenticated:
        client = razorpay.Client(auth=("rzp_test_9BZyJ3buu1pncT", "6QKQl4eZL8qSwxmeZy02o4tv"))

        cid = Cart.objects.filter(user_id=request.user).values_list('product_id',flat=True)
        amount = Product.objects.filter(id__in=cid).values_list('price',flat=True)
        amt=0
        for i in amount:
            amt+=i

        data = { "amount": amt, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)

        context={}
        context['amt'] = data['amount']*100
        context['aid'] = aid

        return render(request,'user/cart_payment.html',context)
    else:
        return HttpResponseRedirect('/')

def Cart_Address(request):
    order_id = Order.objects.all().values_list('product_id',flat=True)

    if request.method == 'POST':
        cname = request.POST.get('cname')
        flat = request.POST.get('flat')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        contact = request.POST.get('contact')
        acontact = request.POST.get('acontact')
                # print(cname,flat,landmark,city,state,pincode,contact,acontact)
        Address.objects.create(user=request.user,name=cname,flat=flat,landmark=landmark,city=city,state=state,pincode=pincode,contact=contact,contactA=acontact)
            #here we are fetching data from address table
    data = Address.objects.filter(user_id=request.user)
    print(data)
    return render(request,'user/cart_address.html',{'adata':data})

def Cart_Preorder(request,aid):
    product_id = Cart.objects.filter(user=request.user).values_list('product_id',flat=True)
    print(product_id)
    data = Product.objects.filter(id__in=product_id)
    adata = Address.objects.filter(id=aid)
    date1 = date.today()
    days = timedelta(days=7)
    delivery_date = date1+days
    return render(request,'user/cart_preorder.html',{'pdata':data,'adata':adata,'date':delivery_date,'aid':aid})

@csrf_exempt
def Cart_OrderConfirm(request,aid):
    try:
        product_id = Cart.objects.filter(user=request.user).values_list('product_id',flat=True)
        address_id = aid
        print(product_id,address_id)
        date1 = datetime.now()
        datef = date1.strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4().hex)[:6]
        order_id = f'PS{datef}-{unique_id}'
        oid = request.user
        for i in list(product_id):
            Order.objects.create(user=oid,product_id=i,address_id=address_id,order_id=order_id)
        return render(request,'user/cart_orderconfirm.html')
    except:
        return render(request,'user/cartconfirm.html')


def AdminSingUp(request):
    if request.method =='POST':
        uname= request.POST.get('uname')
        email=request.POST.get('email')
        password=request.POST.get('pass')
        user= User.objects.create_user(uname,email,password)
        user.is_staff=True
        user.is_superuser=True
        user.save()

    return render(request,'admin/adminsignup.html')

def AdminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
        return HttpResponseRedirect('/index/')
    return render(request,'admin/adminlogin.html')

