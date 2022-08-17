from unicodedata import name
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.allProdCat, name = 'allProdCat'),
    path('<slug:c_slug>/', views.allProdCat, name = 'products_by_category'),
    # path('<slug:c_slug>/<slug:product_slug>', views.ProdCatDetail, name = 'ProdCatDetail'),
    path('<str:id>', views.product, name="product"), 
    # path('spon//', views.spon, name = 'spon'),
]