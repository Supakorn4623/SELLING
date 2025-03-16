from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('shopowner/', include('shopowner.urls')),
    path('shopsales/', include('shopsales.urls')),
    path('', include('shopsales.urls')),
]
