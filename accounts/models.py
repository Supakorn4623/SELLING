from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    ROLE_CHOICES = [
        ('salesperson', 'Salesperson'),
        ('owner', 'Owner'),
    ]

    id = models.AutoField(primary_key=True)  # รหัสที่ไม่ซ้ำกันสำหรับแต่ละบัญชี
    username = models.CharField(max_length=50, unique=True)  # ชื่อที่ใช้เข้าสู่ระบบ
    password = models.CharField(max_length=255)  # รหัสผ่านที่เข้ารหัส
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # บทบาทของผู้ใช้
    created_at = models.DateTimeField(auto_now_add=True)  # วันที่ผู้ใช้สร้างบัญชี

    def save(self, *args, **kwargs):
        # เข้ารหัสรหัสผ่านใหม่ถ้ารหัสผ่านที่มีอยู่ยังไม่ได้เข้ารหัส
        if not self.pk or 'pbkdf2_' not in self.password:  # 'pbkdf2_' จะมีอยู่ในรหัสผ่านที่ถูกเข้ารหัสแล้ว
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
