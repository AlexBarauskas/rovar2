# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions

from account.models import Author


class AuthorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

translator.register(Author, AuthorTranslationOptions)
