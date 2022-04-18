"""
    exchange URL Configuration
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # account
    path('', include('accounts.urls')),
    # app
    path('app/', include('app.urls')), 
]