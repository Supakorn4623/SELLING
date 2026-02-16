from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_code', 'product_name', 'price', 'stock']
        labels = {
            'product_code': 'รหัสสินค้า/บาร์โค้ด',
            'product_name': 'ชื่อสินค้า',
            'price': 'ราคา',
            'stock': 'จำนวนคงคลัง',
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # ทำให้ฟิลด์ stock เป็น read-only เมื่อแก้ไขข้อมูล
        if self.instance and self.instance.pk:
            self.fields['stock'].disabled = True

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is None:
            return 0  # ถ้าไม่มีการกรอกค่าให้ใช้ 0
        return stock

class StockForm(forms.Form):
    product_code = forms.CharField(max_length=100, label="รหัสสินค้า")
    received_quantity = forms.IntegerField(min_value=1, label="จำนวนสินค้าที่รับมา")    

    def clean_received_quantity(self):
        quantity = self.cleaned_data.get('received_quantity')
        if quantity <= 0:
            raise forms.ValidationError("จำนวนสินค้าที่รับมาจะต้องมากกว่าศูนย์")
        return quantity
    
class ShelfForm(forms.Form):
    product_code = forms.CharField(label="รหัสสินค้า")
    shelf_quantity = forms.IntegerField(label="จำนวนที่ต้องการขึ้นชั้น", min_value=1)    