from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth import get_user_model
from .models import Member
from .forms import MemberForm
def login(request):
    # POST 요청 들어오면 로그인
    if request.method == 'POST':
        usr = request.POST['username']
        pwd = request.POST['password']
        # User 모델에 usr와 pwd가 일치하는 객체 있는지 확인
        # 있으면 해당 객체, 없으면 None 반환
        user = auth.authenticate(request, username=usr, password=pwd)

        if user is not None: # 유저가 존재할 경우
            auth.login(request, user)
            return redirect('/shop')
        else:
            # 만약 유저 없을경우 다시 로그인 화면으로
            return render(request, 'accounts/login.html')
    
    # GET 요청 들어오면 login form 담은 html 보여줌
    elif request.method == 'GET':
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def mypage(request):
    user = request.user

    member = Member.objects.get(user=user)
  

    context = {
        'member':member,
    }
    return render(request, 'accounts/mypage.html', context)

def newinfo(request):
    return render(request, 'accounts/register.html')

def register(request):
    user= request.user
    new_info = Member()
    new_info.user = request.user
    new_info.name = request.POST['name']
    # new_info.address = request.POST['address']
    new_info.phone = request.POST['phone']
    new_info.email = request.POST['email']
    new_info.save()
    return redirect('accounts:mypage')

# 마이 페이지_수정 페이지
def mypage_edit(request):
    
    user = request.user
    edit_member = Member.objects.get(user=user)
    return render(request, 'accounts/mypage_edit.html', {'member':edit_member})

def updateInfo(request):
    user = request.user
    update_member = Member.objects.get(user=user)
    update_member.name = request.POST['name']
    update_member.phone = request.POST['phone']
    update_member.email = request.POST['email']
    update_member.save()
    return redirect('accounts:mypage')

# 마이 페이지 - 결제 관리
def mypage_cash(request):
    return render(request, 'accounts/mypage_cash.html')

# 마이 페이지 - 나의 전시장
def mypage_exhibit(request):
    return render(request, 'accounts/mypage_exhibit.html')