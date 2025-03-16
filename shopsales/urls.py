from django.urls import path
from .views import sales_dashboard ,product_management, delete_product, add_stock ,move_to_shelf , process_checkout, sell_product, get_product_by_barcode
urlpatterns = [
    path('sales_dashboard/', sales_dashboard, name='sales_dashboard'),  # เพิ่ม URL pattern
    path('products/', product_management, name='product_management'),
    path('products/delete/<int:product_id>/', delete_product, name='delete_product'),
    path('add_stock/', add_stock, name='add_stock'),
    path('move_to_shelf/', move_to_shelf, name='move_to_shelf'),
    path('checkout/', process_checkout, name='process_checkout'),
    path('sell_product/', sell_product, name='sell_product'),
    path('get_product_by_barcode/<str:barcode>/', get_product_by_barcode, name='get_product_by_barcode'),
]