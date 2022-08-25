from email.policy import default
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Post, PostImage, Like
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from order.models import Order, OrderItem
from .forms import PostForm
from tag.models import *

from django.db.models import Count

import random


# 좋아요 모듈
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User

# shop 합치기
from django.core.paginator import Paginator, EmptyPage, InvalidPage
import random

# Create your views here.
def _cart_id(request) :
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()
    return cart

def add_cart(request, product_id) :
    post = Post.objects.get(id = product_id)
    try :
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist :
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()

    try :
        cart_item = CartItem.objects.get(post = post, cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist :
        cart_item = CartItem.objects.create(
            post = post,
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
            total += (cart_item.post.post_price * cart_item.quantity)
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
                    products = Post.objects.get(id = order_item.product.id)
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
    post = get_object_or_404(Post, id = product_id)
    cart_item = CartItem.objects.get(post = post, cart = cart)

    if cart_item.quantity > 1 :
        cart_item.quantity -= 1
        cart_item.save()
    else :
        cart_item.delete()
    
    return redirect('cart:cart_detail')

def full_remove(request, product_id) :
    cart = Cart.objects.get(cart_id = _cart_id(request))
    post = get_object_or_404(Post, id = product_id)
    cart_item = CartItem.objects.get(post = post, cart = cart)
    cart_item.delete()

    return redirect('cart:cart_detail')

# 전시 등록페이지
def regist_1(request):
    return render(request, 'cart/regist_1.html')
def regist_2(request):
    return render(request, 'cart/regist_2.html')
def regist_3(request):
    return render(request, 'cart/regist_3.html')

@permission_required('accounts.manager', raise_exception=True)
def post_list(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session':login_session}

    manager_post = Post.objects.filter(ok=False)
    context['manager_post']=manager_post
    
    return render(request, 'cart/post_list.html', context)

@permission_required('accounts.manager', raise_exception=True)
def user_post_list(request):
    login_session = request.session.get('login_session', '')
    context = {'login_session':login_session}

    user_post = Post.objects.filter(ok=True)
    context['user_post']=user_post

    return render(request, 'cart/list.html', context)

def post_detail(request,id):
    post = get_object_or_404(Post, pk = id)
    return render(request, 'cart/post_detail.html', {'post':post})

def user_post_detail(request,id):
    post = get_object_or_404(Post, pk = id)
    return render(request, 'cart/user_post_detail.html', {'post':post})

def post_edit(request, id):
    edit_post = Post.objects.get(pk=id)
    edit_post.ok=True
    edit_post.save()
    return redirect('cart:post_list')

def regist_4(request):
    if request.method == 'GET':
        post_form = PostForm()
        # context['forms'] = post_form
        context = {'forms':post_form }
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
                post_price = post_form.post_price,
                post_place = post_form.post_place,
                startday = post_form.startday,
                endday = post_form.endday,
                post_name = post_form.post_name,
                ok = False,
            )
            post.main_image = request.FILES.get('main_image')
            post.save()
            
            # 폼 저장하고 태그 추가
            tags = post_form.cleaned_data['tag'].split(',')
            for tag in tags:
                if not tag:
                    continue
                else:
                    tag=tag.strip()
                    tag_, created = Tag.objects.get_or_create(name = tag)
                    post.tag.add(tag_)
            
            
            for img in request.FILES.getlist('post_imgs'):
                photo = PostImage()
                photo.post = post
                photo.image = img
                photo.save()
            return redirect('/')
        else:
            context = {'forms':post_form }
            if post_form.errors:
                for value in post_form.errors.values():
                    context['error'] = value
            return render(request, 'cart/regist_4.html', context)

def post_delete(request, id):
    login_session = request.session.get('login_session', '')
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('cart:post_list')

def user_post_delete(request, id):
    login_session = request.session.get('login_session', '')
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('cart:user_post_list')

@require_POST
@login_required
def like_toggle(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_like, post_like_created = Like.objects.get_or_create(user=request.user, post=post)

    if not post_like_created:
        post_like.delete()
        result = "like_cancel"
    else:
        result="like"

    context = {
        "like_count" : post.like_count,
        "result" : result
    }

    return HttpResponse(json.dumps(context), content_type="application/json")



# def articovery(request):
    # queryset_post = Post.objects.all()
    # count_post = queryset_post.count()


# def articovery(request):
#     # queryset_post = Post.objects.all()
#     # count_post = queryset_post.count()

#     # list = []
#     # ran_num = random.randrange(1, count_post)

#     # for i in range(3):
#     #     while ran_num in list:
#     #         ran_num = random.randrange(1,count_post)
#     #     list.append(ran_num)
    
#     # for i in range(3):
#     #     choose_post = Post.objects.filter(id = list[i])
    
#     # context = {'choose_post':choose_post}
    

#     # return render(request, 'cart/articovery.html', context)
#     return render(request, 'cart/articovery.html')

    # return render(request, 'cart/articovery.html', context)
    # return render(request, 'cart/articove/ry.html')


def articovery(request, c_slug = None):
    login_session = request.session.get('login_session', '')
    context = {'login_session':login_session}

    user_post = Post.objects.filter(
        ok=True,
        id=random.randrange(1,8)
        )

    # user_post.append(user_post_3)
    context['user_post']=user_post
    
    return render(request, 'cart/articovery.html',context)


def popular(request):
    posts = Post.objects.all().annotate(count_like=Count('like_user_set')).order_by('-count_like')
    paginator = Paginator(posts,3)
    pagnum = request.GET.get('page')
    posts = paginator.get_page(pagnum)
    return render(request, 'cart/popular.html', {'posts':posts})

def my_like(request, user_id):
    user = User.objects.get(id=user_id)
    like_list = Like.objects.filter(user=user)
    context= {
        'like_list':like_list,
    }
    return render(request, 'accounts/mypage_like.html', context)
