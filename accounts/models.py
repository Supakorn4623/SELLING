from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password

class User(AbstractBaseUser): # เปลี่ยนจาก models.Model เป็น AbstractBaseUser
    ROLE_CHOICES = [
        ('salesperson', 'Salesperson'),
        ('owner', 'Owner'),
    ]

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # last_login จะถูกแถมมาให้ฟรีจาก AbstractBaseUser

    USERNAME_FIELD = 'username' # บอก Django ว่าใช้ฟิลด์นี้เป็นชื่อล๊อกอิน

    def save(self, *args, **kwargs):
        if not self.pk or not self.password.startswith(('pbkdf2_', 'argon2', 'bcrypt')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username