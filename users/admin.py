from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    """
    Пользовательская настройка администратора для модели пользователя.
    Добавляет дополнительные поля (phone, city, avatar) к полям пользователя в административной панели Django.
    """
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'city', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone', 'city', 'avatar')}),
    )


# Регистрация пользовательского администратора для модели пользователя в административной панели Django.
admin.site.register(User, CustomUserAdmin)
