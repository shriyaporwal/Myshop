from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from .models.category import Category
from .models.product import Product
from .models.orders import Orders
from .models.customers import Customers
from django.contrib import messages
from django.views import View
from django.contrib.auth.hashers import make_password ,check_password
from store.middleware.auth import auth_middleware
from django.utils.decorators import method_decorator
class Index(View):
    def get(self , request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        categories = Category.objects.all()
        category_id = request.GET.get('category')
        print(category_id)
        if category_id:
            print(category_id)

            product = Product.get_all_products_id(category_id)
        else:
            product = Product.get_all_products()
        d = {}
        d['product'] = product
        d['categories'] = categories

        return render(request, 'orders/home.html', d)
    def post(self,request):

        product = request.POST.get('p_id')
        remove_cart = request.POST.get('remove')
        print(remove_cart)
        # product_quantity = request.POST.get('p_quantity')
        #print("prduct_quantity",product_quantity)

        product_cart = request.session.get('cart')
        if product_cart:
            quantity = product_cart.get(product)
            if quantity:
                if remove_cart:
                    if quantity <= 1:
                        product_cart.pop(product)
                    else:
                        product_cart[product] = quantity - 1

                else:
                    product_cart[product] = quantity + 1
            else:

                product_cart[product] =  1

        else:
            product_cart = {}
            product_cart[product] = 1

        request.session['cart'] = product_cart
        print('you are:',request.session.get('cust_username'))
        print("CART",)
        print('product' ,product)
        return redirect('homepage')

def search(request):
    if request.method == 'POST':
        name = request.POST.get('category')
        products = Product.get_all_products()
        catproduct = []
        category = Category.objects.all()
        parameter ={}
        product = category.objects.filter(i=name)
        print(product.category)
        #     if(product.category == name):
        #         catproduct.append(product)
        # parameter = {'category':catproduct}
        # print(parameter)
    return render(request,'orders/order.html',parameter)

class Signup(View):
    def get(self, request):
        return render(request, 'orders/signup.html')

    def post(self, request):
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        error = None
        # validations

        if not name:
            messages.warning(request, "Name requried")

        if not email:
            messages.warning(request, "Email requried")

        if not username:
            messages.warning(request, "Username requried")

        if not phone:
            messages.warning(request, "Phone requried")

        if not password2:
            messages.warning(request, "Confirm Password requried")

        if not password1:
            messages.warning(request, "Password requried")

        # create objects
        print(name, username, email, phone)

        user1 = Customers(name=name, username=username, email=email, phone=phone, password2=password2,
                          password1=password1)
        check_email = user1.isExists()
        check_username = user1.isusername()
        if check_email:
            print("hiii1")
            error = "Email Already taken"


        elif check_username:
            print("hiii2")
            error = "Username Already taken"


        elif (password1 != password2):
            print("hiii3")
            error = "Password not equal"


        elif (not len(phone) >= 10):
            print("hiii4")
            error = "Phone number atleast 10 digit "

        else:
            user1.password1 = make_password(user1.password1)
            user1.password2 = make_password(user1.password2)
            user1.register()
            messages.success(request, "user created")
            return redirect('homepage')

        if error:
            d = {}
            d['error'] = error
            return render(request, 'orders/signup.html', d)

class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        print(request.GET.get('return_url'))
        return render(request,'orders/loguser.html')
    def post(self ,request):
        user = request.POST['username']
        password = request.POST['password']
        print(user, password)
        customer = Customers.get_customer_by_username(user)
        if customer:
            flag = check_password(password, customer.password1)
            if flag:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None

                return redirect('homepage')

            else:
                messages.warning(request, 'Email or p8assword invalid!!')
                return redirect('loguser')
        else:
            messages.warning(request, 'Email or password invalid!!')
            return redirect('loguser')

def logout(request):
    request.session.clear()
    return redirect('homepage')

class Cart(View):
    def get(self ,request):

        p_id = list(request.session.get('cart').keys())
        product = Product.product_by_id(p_id)
        print(request.session['cart'])
        q ={}
        for i in request.session['cart']:
            q[i] = request.session['cart'].values()
        return render(request,'orders/cart.html',{"cart_product":product})

class Checkout(View):
    def get(self ,request):
        print(request.POST)
        return render(request,'orders/checkout.html')

    def post(self, request):
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.product_by_id(list(cart.keys()))


        for product in products:
            order1 = Orders(address = address,
                           city = city,
                           state = state,
                           zip = zip,
                           phone=phone,
                           customer= Customers(id = customer ),

                           product= product,
                           price=product.price,
                           quantity = cart.get(str(product.id)))
            order1.save()
        request.session['cart'] = {}
        return render(request ,'orders/cart.html')

class Order(View):
    @method_decorator(auth_middleware)
    def get(self ,request):
        customer = request.session.get('customer')
        orders = Orders.get_orders_by_customer(customer)

        return render(request,'orders/order.html',{'orders' :orders})

def Aboutus(request):
    return render(request,'orders/about.html')

def Contact(request):
    if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            desc = request.POST.get('desc')
            print(name)
            contact = Contact(name = name,email=email,phone = phone,desc=desc)
            contact.save()
            messages.success(request, 'Thank you for contacting us we will respond soon. Have a nice day.')
    return render(request,'orders/contact.html')
# print(make_password('1234'))
# print(check_password('1234','pbkdf2_sha256$260000$JHSHNu97WMjw6i12bKioUt$O0BbceuKKEyqb1Pbgo2dOZ7heCBqC8ux6G55ItsKyIY='))

   # value ={
            #     'name':name,
            #     'email': email,
            #     'username':username,
            #     'phone':phone
            # }
