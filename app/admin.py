
from django.contrib import admin
from .models import Profile, Wallet, Order


class AdminProfile(admin.ModelAdmin):
  list_display = ["_id", "user", "ips"]

class AdminWallet(admin.ModelAdmin):
  list_display = ["_id", "user", "btc_balance", "usd_balance", "profit"]
  
class AdminOrder(admin.ModelAdmin):
  list_display = ["_id", "profile", "status", "type", "datetime", "price", "quantity"]

admin.site.register(Profile, AdminProfile)
admin.site.register(Wallet, AdminWallet)
admin.site.register(Order, AdminOrder)