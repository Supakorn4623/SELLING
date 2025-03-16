from django.shortcuts import render, redirect
from .forms import SalespersonLoginForm, OwnerLoginForm 
from accounts.models import User
from django.contrib.auth.hashers import check_password
from accounts.models import User
from django.contrib.auth import logout as auth_logout

def salesperson_login_view(request):
    if request.method == 'POST':
        form = SalespersonLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password) and user.role == 'salesperson':
                    request.session['user_id'] = user.id  # บันทึก session โดยไม่ต้องใช้ login()
                    return redirect('sales_dashboard')
                else:
                    form.add_error(None, "Invalid username or password")
            except User.DoesNotExist:
                form.add_error(None, "User not found")
    else:
        form = SalespersonLoginForm()

    return render(request, 'accounts/salesperson_login.html', {'form': form})


def owner_login_view(request):
    if request.method == 'POST':
        form = OwnerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password) and user.role == 'owner':  # ตรวจสอบว่าเป็นเจ้าของร้าน
                    request.session['user_id'] = user.id  # บันทึก session โดยไม่ต้องใช้ login()
                    return redirect('owner_dashboard')  # เปลี่ยนไปที่ URL ที่ต้องการหลังจากเข้าสู่ระบบสำเร็จ
                else:
                    form.add_error(None, "Invalid username or password")
            except User.DoesNotExist:
                form.add_error(None, "User not found")
    else:
        form = OwnerLoginForm()

    return render(request, 'accounts/owner_login.html', {'form': form})

def logout_view(request):
    auth_logout(request)  # ทำการ Logout
    return redirect('salesperson_login')

