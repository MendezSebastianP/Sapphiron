from django.contrib import admin
from .models import CustomUser

# Register the CustomUser model to appear in the admin interface
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active')