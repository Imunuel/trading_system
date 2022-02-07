from django.contrib import admin
from .models import Share, InventoryShare, GlobalInventory

admin.site.register(Share)
admin.site.register(InventoryShare)
admin.site.register(GlobalInventory)