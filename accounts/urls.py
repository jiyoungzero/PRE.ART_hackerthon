from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.login, name = 'login'),
    path('mypage/', views.mypage, name = 'mypage'),
    path('newinfo/', views.newinfo, name='newinfo'),
    path('mypage_edit/', views.mypage_edit, name="mypage_edit"),
    path('mypage_cash/', views.mypage_cash, name = 'mypage_cash'),
    path('mypage_exhibit/', views.mypage_exhibit, name="mypage_exhibit"),
]