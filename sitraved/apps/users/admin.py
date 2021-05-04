from django.contrib import admin

from sitraved.apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('created_at', )
    list_display = ('username', 'email', 'created_at')
