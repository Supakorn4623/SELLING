from django.db import models
from django.utils.timezone import now

class Product(models.Model):
    id = models.AutoField(primary_key=True)  
    product_code = models.CharField(max_length=100, unique=True) #รหัสเฉพาะของสินค้า (ไม่ซ้ำกัน)
    product_name = models.CharField(max_length=255)  #ชื่อสินค้า
    price = models.PositiveIntegerField() #ราคาสินค้า
    stock = models.PositiveIntegerField(default=0, blank=True, null=True) #จำนวนสินค้าคงคลัง 

    def __str__(self):
        return f"{self.product_name} ({self.product_code})"
    
class Shelf(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    shelf_quantity = models.PositiveIntegerField(default=0)  #จำนวนสินค้าที่อยู่บนชั้นวาง
    created_date = models.DateTimeField(default=now) #วันที่เพิ่มสินค้าเข้าชั้นวาง

    def __str__(self):
        return f"{self.product.product_name} - {self.shelf_quantity} ชิ้น"
    
class Sale(models.Model):
    sale_date = models.DateTimeField(auto_now_add=True)  #วันที่และเวลาที่ขาย
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  #ยอดรวมของรายการขาย 
    amount_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)  #จำนวนเงินที่ลูกค้าจ่าย 
    change_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)   #เงินทอนที่ต้องคืนลูกค้า 
    payment_method = models.CharField(max_length=50, default="เงินสด")  

    def __str__(self):
        return f"Sale #{self.id} - {self.sale_date} | รับเงิน {self.amount_received} บาท | ทอน {self.change_amount} บาท"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField()  #จำนวนสินค้าที่ขาย
    item_total = models.DecimalField(max_digits=10, decimal_places=2)  # ราคารวมของสินค้าชิ้นนั้น (จำนวนสินค้า * ราคาต่อชิ้น)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"    
