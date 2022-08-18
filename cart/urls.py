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
    path('post_list/', views.post_list, name='post_list'),
    path('post_detail/<int:id>/', views.post_detail, name="post_detail"),
    path('post_detail/edit/<int:id>', views.post_edit, name="post_edit"),
    path('post_detail/delete/<int:id>', views.post_delete, name="post_delete"),
    path('user_post_detail/<int:id>/', views.user_post_detail, name='user_post_detail'),
    path('user_post_detail/post_delete/<int:id>/', views.user_post_delete, name='user_post_delete'),
    path('list/', views.user_post_list, name="user_post_list"),
    path('like_toggle/<int:post_id>/', views.like_toggle, name="like_toggle"),
]