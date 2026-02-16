from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from .models import User # ตรวจสอบชื่อ Model ของคุณ
from .forms import SalespersonLoginForm, OwnerLoginForm
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def salesperson_login_view(request):
    if request.method == 'POST':
        form = SalespersonLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)
                # ตรวจสอบรหัสผ่านและบทบาทในขั้นตอนเดียว
                if check_password(password, user.password) and user.role == 'salesperson':
                    # ใช้ login() มาตรฐานเพื่อความปลอดภัยสูงสุด
                    login(request, user) 
                    return redirect('sales_dashboard')
            except User.DoesNotExist:
                pass # ปล่อยให้ไปแสดง error เดียวกันที่ด้านล่าง
            
            # ใช้ข้อความ Error เดียวกันทั้งหมดเพื่อความปลอดภัย
            form.add_error(None, "Invalid username or password")
    else:
        form = SalespersonLoginForm()

    return render(request, 'accounts/salesperson_login.html', {'form': form})

@csrf_exempt
def owner_login_view(request):
    if request.method == 'POST':
        form = OwnerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)
                # ตรวจสอบว่าเป็นเจ้าของร้าน (owner)
                if check_password(password, user.password) and user.role == 'owner':
                    login(request, user)
                    return redirect('owner_dashboard')
            except User.DoesNotExist:
                pass
            
            form.add_error(None, "Invalid username or password")
    else:
        form = OwnerLoginForm()

    return render(request, 'accounts/owner_login.html', {'form': form})

def logout_view(request):
    auth_logout(request)  # ทำการ Logout
    return redirect('salesperson_login')

