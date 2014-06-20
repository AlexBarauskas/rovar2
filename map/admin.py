from django.contrib import admin

from map.models import Location


admin.site.register(Location, admin.ModelAdmin)
