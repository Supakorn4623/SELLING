from django.urls import path
from .views import salesperson_login_view, owner_login_view, logout_view

urlpatterns = [
    path('salesperson/login/', salesperson_login_view, name='salesperson_login'),
    path('owner/login/', owner_login_view, name='owner_login'),
    path('logout/', logout_view, name='logout'),
]