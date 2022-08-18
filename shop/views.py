from django.core import paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category
from cart.models import Post
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.
def allProdCat(request, c_slug = None) :

    posts = Post.objects.all()

    c_page = None;
    products_list = None;
    if c_slug != None :
        c_page = get_object_or_404(Category, slug = c_slug)
        products_list = Post.objects.filter(category = c_page)
    else :
        products_list = Post.objects.all()
    
    paginator = Paginator(products_list, 6)
    try :
        page = int(request.GET.get('page', 1))
    except :
        page = 1

    try :
        products = paginator.page(page)
    except(EmptyPage, InvalidPage) :
        products = paginator.page(paginator.num_pages)
    
    return render(request, 'shop/category.html', {'posts':posts,'category' : c_page, 'products' : products})

def ProdCatDetail(request, c_slug, product_slug) :
    try :
        product = Post.objects.get(category__slug = c_slug, slug = product_slug)
    except Exception as e :
        raise e
    
    return render(request, 'shop/product.html', {'product' : product})

def product(request, id):
    post = get_object_or_404(Post, pk = id)
    return render(request, 'shop/product.html',{'post':post})