from email.policy import default
from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem, Post, PostImage
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from order.models import Order, OrderItem
from .forms import PostForm, PosteidtForm

# Create your views here.
def _cart_id(request) :
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()
    return cart

def add_cart(request, product_id) :
    product = Product.objects.get(id = product_id)
    try :
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist :
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()

    try :
        cart_item = CartItem.objects.get(product = product, cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist :
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
    
    return redirect('cart:cart_detail')

def cart_detail(request, total = 0, counter = 0, cart_items = None) :
    try :
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, active = True)
        for cart_item in cart_items :
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist :
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'PRE.ART - New Order'
    data_key = settings.STRIPE_PUBLIC_KEY

    if request.method == "POST" :
        print(request.POST)
        try :
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingCity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            
            customer = stripe.Customer.create(
                email = email,
                source = token
            )
            charge = stripe.Charge.create(
                amount = stripe_total,
                currency = "aud",
                description = description,
                customer = customer
            )
            try :
                order_details = Order.objects.create(
                    token = token,
                    total = total,
                    emailAddress = email,
                    billingName = billingName,
                    billingAddress1 = billingAddress1,
                    billingCity = billingCity,
                    billingPostcode =billingPostcode,
                    billingCountry =billingCountry
                )
                order_details.save()
                for order_item in cart_items :
                    oi = OrderItem.objects.create(
                        product = order_item.product.name,
                        quantity = order_item.quantity,
                        price = order_item.product.price,
                        order = order_details
                    )
                    oi.save()
                    products = Product.objects.get(id = order_item.product.id)
                    products.save()
                    order_item.delete()
                    print('The order has been created')
                return redirect('shop:allProdCat')
            except ObjectDoesNotExist :
                pass
        except stripe.error.CardError as e :
            return False, e

    return render(request, 'cart/cart.html', dict(cart_items = cart_items, total = total, counter = counter,
                    data_key = data_key, stripe_total = stripe_total, description = description ))

def cart_remove(request, product_id) :
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)

    if cart_item.quantity > 1 :
        cart_item.quantity -= 1
        cart_item.save()
    else :
        cart_item.delete()
    
    return redirect('cart:cart_detail')

def full_remove(request, product_id) :
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)
    cart_item.delete()

    return redirect('cart:cart_detail')

# 전시 등록페이지
def regist_1(request):
    # 로그인하고 누를 수 있게 수정 필요
    if not request.session.get('user'):
        return redirect('/accounts/login/')

    return render(request, 'cart/regist_1.html')
def regist_2(request):
    return render(request, 'cart/regist_2.html')
def regist_3(request):
    return render(request, 'cart/regist_3.html')

def post_list(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session':login_session}
    # posts = Post.objects.all()
    # context['posts'] = posts
    manager_post = Post.objects.filter(option='승인 대기')
    context['manager_post']=manager_post
    
    return render(request, 'cart/post_list.html', context)

def user_post_list(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session':login_session}

    user_post = Post.objects.filter(option='승인 완료')
    context['user_post']=user_post

    return render(request, 'cart/list.html', context)

def post_detail(request,id):
    post = get_object_or_404(Post, pk = id)
    return render(request, 'cart/post_detail.html', {'post':post})

def user_post_detail(request,id):
    post = get_object_or_404(Post, pk = id)
    return render(request, 'cart/user_post_detail.html', {'post':post})

def post_edit(request, id):
    login_session = request.session.get('login_session', '')
    context = {'login_session':login_session}
    edit_post = get_object_or_404(Post, pk=id)
    context['post'] = edit_post

    if request.method == 'GET':
        edit_form = PosteidtForm(instance=edit_post)
        context['forms'] = edit_form
        return render(request, 'cart/post_edit.html', context)
    elif request.method == 'POST':
        edit_form = PosteidtForm(request.POST)
        if edit_form.is_valid():
            post = Post(
                realname = edit_form.realname,
                artist_name = edit_form.artist_name,
                team = edit_form.team,
                email = edit_form.email,
                artist_intro = edit_form.artist_intro,
                post_intro = edit_form.post_intro,
                post_plan= edit_form.post_plan,
                # post_img = edit_form.post_img,
                post_price = edit_form.post_price,
                post_place = edit_form.post_place,
                option = edit_form.option
            )
            post.save()
            return redirect('/')
        else:
            context['forms'] = edit_form
            if edit_form.errors:
                for value in edit_form.errors.values():
                    context['error']=value
            return render(request, 'cart/post_edit.html', context)

def regist_4(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session':login_session}

    if request.method == 'GET':
        post_form = PostForm()
        context['forms'] = post_form
        return render(request, 'cart/regist_4.html', context)

    elif request.method == 'POST':
        post_form = PostForm(request.POST)

        if post_form.is_valid():
            post = Post(
                realname = post_form.realname,
                artist_name = post_form.artist_name,
                team = post_form.team,
                email = post_form.email,
                artist_intro = post_form.artist_intro,
                post_intro = post_form.post_intro,
                post_plan= post_form.post_plan,
                # post_img = post_form.post_img,
                post_price = post_form.post_price,
                post_place = post_form.post_place,
                option = post_form.option

            )
            post.save()
            for img in request.FILES.getlist('imgs'):
                photo = PostImage()
                photo.post = post
                photo.image = img
                photo.save()
            return redirect('/')
        else:
            context['forms'] = post_form
            if post_form.errors:
                for value in post_form.errors.values():
                    context['error'] = value
            return render(request, 'cart/regist_4.html', context)