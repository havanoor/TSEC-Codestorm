from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *



class AccountAdmin(UserAdmin):
    list_display=(
        'email','username','is_staff','is_admin','is_farmer','is_buyer'
    )

    search_fields=(
        'email',
        'username'
    )

    filter_horizontal=()
    list_filter=()
    fieldsets=()






admin.site.register(Account,AccountAdmin)
admin.site.register(Category)
admin.site.register(Farmer)
admin.site.register(Buyer)
admin.site.register(Crops)
admin.site.register(Product)
admin.site.register(CropSeeds)
admin.site.register(fertilizer)
admin.site.register(pesticide)