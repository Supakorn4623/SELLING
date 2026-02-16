from django.urls import path
from .views import dashboard_view ,create_employee_view , employee_list,edit_employee, delete_employee 
from shopowner.views import sales_report_page, sales_report_by_range, sale_detail ,stock_report,stock_report_page,sales_chart_data,low_stock_alerts

urlpatterns = [
    path('dashboard/', dashboard_view, name='owner_dashboard'),
    path('create_employee/', create_employee_view, name='create_employee'),
    path('employees/', employee_list, name='employee_list'),
    path('edit-employee/<int:pk>/', edit_employee, name='edit_employee'),  
    path('delete-employee/<int:pk>/', delete_employee, name='delete_employee'),
    path('sales_report/', sales_report_page, name='sales_report'),
    path('sales_report_by_range/', sales_report_by_range, name='sales_report_by_range'),  
    path('sale_detail/<int:sale_id>/', sale_detail, name='sale_detail'),
    path('stock_report/', stock_report_page, name='stock_report_page'),  
    path('api/stock_report/', stock_report, name='stock_report'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('api/sales_chart/', sales_chart_data, name='sales_chart_data'),
    path('api/low_stock_alerts/', low_stock_alerts, name='low_stock_alerts'),
]
