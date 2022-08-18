from django.shortcuts import render
from cart.models import Post
from django.db.models import Q, query

# Create your views here.
def searchResult(request) :
    products = None
    query = None
    if 'q' in request.GET :
        query = request.GET.get('q')
        products = Post.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
    
    return render(request, 'search_app/search.html', {'query':query, 'products':products})