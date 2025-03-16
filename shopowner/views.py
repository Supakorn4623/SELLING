from django.shortcuts import render, redirect,get_object_or_404
from accounts.models import User 
from shopsales.models import SaleItem , Shelf, Product,Sale
from accounts.forms import EmployeeCreationForm
from django.contrib import messages
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.utils.timezone import datetime
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.utils import timezone
import datetime as dt


def dashboard_view(request):
    # Get total number of products
    total_products = Product.objects.count()
    
    # Get today's date
    today = timezone.now().date()
    
    # Calculate today's sales
    today_sales = Sale.objects.filter(
        sale_date__date=today
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    # Get current month
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    # Calculate month's sales
    month_sales = Sale.objects.filter(
        sale_date__month=current_month,
        sale_date__year=current_year
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    context = {
        'total_products': total_products,
        'today_sales': today_sales,
        'month_sales': month_sales
    }
    
    return render(request, 'shopowner/dashboard.html', context)



def employee_list(request):
    employees = User.objects.filter(role='salesperson')  # แสดงพนักงานขาย
    return render(request, 'shopowner/employee_list.html', {'employees': employees})

def create_employee_view(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create(username=username, password=password, role='salesperson')
            messages.success(request, "Employee created successfully!")
            return redirect('owner_dashboard')
    else:
        form = EmployeeCreationForm()

    return render(request, 'shopowner/create_employee.html', {'form': form})

def edit_employee(request, pk):
    employee = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()  # อัปเดตพนักงาน
            return redirect('employee_list')
    else:
        form = EmployeeCreationForm(instance=employee)
    return render(request, 'shopowner/edit_employee.html', {'form': form})

def delete_employee(request, pk):
    employee = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        employee.delete()  # ลบพนักงาน
        return redirect('employee_list')
    return render(request, 'shopowner/confirm_delete.html', {'employee': employee})


#รายงาน   
def sales_report_by_range(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    page = int(request.GET.get("page", 1))
    per_page = 50  # 🔥 เปลี่ยนจาก 50 เป็น 2 เพื่อลองทดสอบ

    if not start_date or not end_date:
        return JsonResponse({"success": False, "message": "กรุณาระบุวันที่เริ่มต้นและวันที่สิ้นสุด"}, status=400)

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        sales_data = SaleItem.objects.filter(
            sale__sale_date__date__range=[start_date, end_date]
        ).values(
            'sale__id', 'sale__sale_date'
        ).annotate(
            total_items=Count('id'),  
            total_amount=Sum('item_total')  
        ).order_by('-sale__sale_date')

        total_sales_amount = sales_data.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        # ✅ คำนวณการแบ่งหน้า
        total_pages = (len(sales_data) // per_page) + (1 if len(sales_data) % per_page else 0)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        sales_data = sales_data[start_index:end_index]

        return JsonResponse({
            "success": True,
            "sales": list(sales_data),
            "total_sales_amount": total_sales_amount,
            "total_pages": total_pages,
            "current_page": page,
        })
    except ValueError:
        return JsonResponse({"success": False, "message": "รูปแบบวันที่ไม่ถูกต้อง"}, status=400)
    
def sales_report_page(request):
    """ แสดงหน้า HTML รายงานยอดขาย """
    return render(request, 'sales_report.html')  # เชื่อมกับไฟล์ HTML    


def sale_detail(request, sale_id):
    """ ดึงรายละเอียดสินค้าภายในใบเสร็จ """
    try:
        sale_items = SaleItem.objects.filter(sale_id=sale_id).values(
            'product__product_code', 'product__product_name', 'quantity', 'item_total'
        )

        return JsonResponse({
            "success": True,
            "sale_id": sale_id,
            "items": list(sale_items)
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
    
def stock_report(request):
    page = int(request.GET.get("page", 1))
    per_page = 50 # แสดง 50 รายการต่อหน้า

    product_stock = Product.objects.values(
        "product_code",
        "product_name",
        "price",
        "stock"
    )

    shelf_stock = Shelf.objects.select_related("product").values(
        "product__product_code",
        "product__product_name",
        "shelf_quantity"
    )

    stock_data = []
    product_map = {
        item["product_code"]: {
            "stock": item["stock"],
            "price": item["price"]  
        }
        for item in product_stock
    }

    for shelf_item in shelf_stock:
        product_code = shelf_item["product__product_code"]
        stock_data.append({
            "product_code": product_code,
            "product_name": shelf_item["product__product_name"],
            "price": product_map.get(product_code, {}).get("price", 0),
            "stock": product_map.get(product_code, {}).get("stock", 0),
            "shelf_quantity": shelf_item["shelf_quantity"],
        })

    # ✅ คำนวณจำนวนหน้าเหมือน `sales_report_by_range`
    total_pages = (len(stock_data) // per_page) + (1 if len(stock_data) % per_page else 0)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    stock_data = stock_data[start_index:end_index]  # ✅ ตัดข้อมูลเฉพาะหน้าที่ร้องขอ

    return JsonResponse({
        "success": True,
        "stocks": list(stock_data),
        "total_pages": total_pages,
        "current_page": page,
    })
def stock_report_page(request):
    """ แสดงหน้า HTML รายงานสต็อกสินค้า """
    return render(request, 'shopowner/stock_report.html')

###Dashboard
def sales_chart_data(request):
    """ API สำหรับดึงข้อมูลยอดขาย รายวัน / รายเดือน / รายปี """
    time_range = request.GET.get("range", "daily")

    if time_range == "yearly":
        sales_data = Sale.objects.annotate(period=TruncYear("sale_date")).values("period").annotate(
            total_sales=Sum("total_price")
        ).order_by("period")
        sales_data = [{"period": item["period"].strftime("%Y"), "total_sales": item["total_sales"]} for item in sales_data]

    elif time_range == "monthly":
        sales_data = Sale.objects.annotate(period=TruncMonth("sale_date")).values("period").annotate(
            total_sales=Sum("total_price")
        ).order_by("period")
        sales_data = [{"period": item["period"].strftime("%Y-%m"), "total_sales": item["total_sales"]} for item in sales_data]

    else:  # รายวัน
        sales_data = Sale.objects.annotate(period=TruncDay("sale_date")).values("period").annotate(
            total_sales=Sum("total_price")
        ).order_by("period")
        sales_data = [{"period": item["period"].strftime("%Y-%m-%d"), "total_sales": item["total_sales"]} for item in sales_data]

    return JsonResponse({"success": True, "data": sales_data})


def low_stock_alerts(request):
    stock_threshold = 10       # กำหนดจำนวนขั้นต่ำของสินค้าในสต็อกที่ถือว่า "ใกล้หมด"
    shelf_threshold = 5        # กำหนดจำนวนขั้นต่ำของสินค้าในชั้นวางที่ถือว่า "ใกล้หมด"

    # 🔹 ค้นหาสินค้าในสต็อกที่เหลือน้อย
    low_stock_items = Product.objects.filter(stock__lte=stock_threshold)

    # 🔹 ค้นหาสินค้าในชั้นวางที่เหลือน้อย
    low_shelf_items = Shelf.objects.filter(shelf_quantity__lte=shelf_threshold)

    return JsonResponse({
        "count": low_stock_items.count() + low_shelf_items.count(),
        "low_stock": [
            {"name": item.product_name, "type": "สต็อก", "amount": item.stock}
            for item in low_stock_items
        ] + [
            {"name": shelf.product.product_name, "type": "ชั้นวาง", "amount": shelf.shelf_quantity}
            for shelf in low_shelf_items
        ]
    })


