# -*- coding: utf-8 -*-

from django.contrib import admin

from account.models import Author, User, Rating
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class MyUserAdmin(UserAdmin):
    list_display = ('username', 'id', 'first_name', 'last_name', 'gender', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'gender')}),
        ('Дополнительная информация', {'fields': ('phone', 'address', 'bike')}),
        ('Доступ', {'fields': ('is_active', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Rating)
admin.site.register(User, MyUserAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.unregister(Group)
