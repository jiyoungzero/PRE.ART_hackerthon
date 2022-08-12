from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('', views.cart_detail, name='cart_detail'),
    path('remove/<int:product_id>/', views.cart_remove, name = 'cart_remove'),
    path('full_delete/<int:product_id>/', views.full_remove, name = 'full_remove'),
    path('regist_1/', views.regist_1, name="regist_1"),
    path('regist_2/', views.regist_2, name= "regist_2"),
    path('regist_3/', views.regist_3, name= "regist_3"),
    path('regist_4/', views.regist_4, name= "regist_4"),
    path('list/', views.post_list, name='post_list'),
]