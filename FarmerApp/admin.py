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
                      'name','s_type'
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



'''
class CropSeedAdmin(ModelAdmin):
        list_display=(
                      'name','s_type'
        )

        search_fields=(
            'name',
            's_type'
        )

        filter_horizontal=()
        list_filter=()
        fieldsets=()
'''

admin.site.register(Account,AccountAdmin)
admin.site.register(Farmer)
admin.site.register(Buyer)
admin.site.register(Crops)
admin.site.register(Product)
admin.site.register(CropSeeds,CropSeedAdmin)
admin.site.register(fertilizer,FertilizerAdmin)
admin.site.register(pesticide,PesticideAdmin)
