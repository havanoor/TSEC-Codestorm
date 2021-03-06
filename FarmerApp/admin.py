
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.admin import ModelAdmin



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



class CropSeedAdmin(ModelAdmin):
        list_display=(
                      'name','s_type','p_id'
        )

        search_fields=(
            'name',
            's_type'
        )

        filter_horizontal=()
        list_filter=()
        fieldsets=()




class FertilizerAdmin(ModelAdmin):
        list_display=(
                      'name','f_type'
        )

        search_fields=(
            'name',
            'f_type'
        )

        filter_horizontal=()
        list_filter=()
        fieldsets=()


class PesticideAdmin(ModelAdmin):
        list_display=(
                      'name','p_type'
        )

        search_fields=(
            'name',
            'p_type'
        )

        filter_horizontal=()
        list_filter=()
        fieldsets=()


class CropFilterAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price' ,'farmer']

    list_filter = ['name',]
    list_editable = ['price', ]
    prepopulated_fields = {'slug': ('name',)}



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email','address', 'postal_code', 'city', 'paid','created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Account,AccountAdmin)
admin.site.register(Farmer)
admin.site.register(Buyer)
admin.site.register(Crops,CropAdmin)
admin.site.register(CropFilter,CropFilterAdmin)
admin.site.register(CropSeeds,CropSeedAdmin)
admin.site.register(fertilizer,FertilizerAdmin)
admin.site.register(pesticide,PesticideAdmin)
