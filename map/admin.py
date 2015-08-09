from django.contrib import admin

from map.models import Location, Point, Track

admin.site.register(Point)
admin.site.register(Track)
admin.site.register(Location, admin.ModelAdmin)
