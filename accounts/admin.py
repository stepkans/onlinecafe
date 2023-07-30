from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, UserProfile

# Register your models here.
class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ("email", "first_name", "last_name", "role"  ,"is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    ordering = ("email",)
    search_fields = ("email",)
    fieldsets = (
    )   
    filter_horizontal=()


admin.site.register(MyUser,MyUserAdmin) 
admin.site.register(UserProfile)   