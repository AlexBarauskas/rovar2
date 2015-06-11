from modeltranslation.translator import translator, TranslationOptions
from map.models import Point, Track


class PointTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'address')


class TrackTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

translator.register(Point, PointTranslationOptions)
translator.register(Track, TrackTranslationOptions)
