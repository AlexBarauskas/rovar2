from django.contrib import admin

from account.models import Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(Author, AuthorAdmin)
