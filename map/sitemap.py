from django.core.urlresolvers import reverse

from map.models import Location, Type, Point, Track
from django.contrib.sitemaps import Sitemap

class LocationSitemap(Sitemap):
    def __init__(self, location):
        self._location = location

    def items(self):
        list1 = [(self._location.name, )]
        list2 = [[self._location.name, t.slug] for t in Type.objects.all() \
                 if self._location.point_set.filter(type=t, state='0').count() or self._location.track_set.filter(type=t, state='0').count()]
        list3 = [[self._location.name, t.slug, o.uid] for o in self._location.point_set.filter(state='0')]
        list4 = [[self._location.name, t.slug, o.uid] for o in self._location.track_set.filter(state='0')]
        return list1 + list2 + list3 + list4

    def location(self, item):
        if len(item) == 1:
            return reverse('show_location', args=item)
        if len(item) == 2:
            return reverse('show_category', args=item)
        if len(item) == 3:
            return reverse('show_object', args=item)
