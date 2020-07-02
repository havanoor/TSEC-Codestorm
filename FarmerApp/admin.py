from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display=(
        'email','username','is_staff','is_admin'
    )

    search_fields=(
        'email',
        'username'
    )

    filter_horizontal=()
    list_filter=()
    fieldsets=()



admin.site.register(Account,AccountAdmin)

