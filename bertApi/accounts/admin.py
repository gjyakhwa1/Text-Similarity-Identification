from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,LoginHistory

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'approvalStatus')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'approvalStatus')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

class CustomLoginHistory(admin.ModelAdmin):
    readonly_fields =('login_at',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(LoginHistory,CustomLoginHistory)
