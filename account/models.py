# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


ACCOUNT_BACKENDS = ((u'vk', u'ВКонтакте'),
                    (u'twitter', u'Twitter'),
                    (u'facebook', u'Facebook'),
                    )

GENDER_CHOICES = (
    (u'male', u'Мужской'),
    (u'female', u'Женский'),
)

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **kwargs):
        if not username:
            raise ValueError('User must have a valid username.')
        user = self.model(
            username=username,
            **kwargs
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **kwargs):
        user = self.create_user(email=UserManager.normalize_email(email),
                                password=password,
                                username=username,
                                **kwargs)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(verbose_name='Имя', max_length=255, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255, blank=True)
    username = models.CharField(verbose_name='Псевдоним', max_length=255, unique=True)
    email = models.EmailField(
        verbose_name='Емайл',
        max_length=255,
        # unique=True,
        blank=True,
        null=True
    )
    img_url = models.URLField(null=True)
    gender = models.CharField(verbose_name='Пол', max_length=10, blank=True, null=True, choices=GENDER_CHOICES)
    phone = models.CharField(verbose_name='Телефон', max_length=255, unique=True, blank=True, null=True)
    address = models.CharField(verbose_name='Адрес', max_length=255, blank=True, null=True)
    bike = models.CharField(verbose_name='Байк', max_length=255, blank=True, null=True)

    backend = models.CharField(max_length=16, choices=ACCOUNT_BACKENDS, null=True)
    id_from_backend = models.CharField(max_length=32, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name='Активен?')
    is_admin = models.BooleanField(default=False, verbose_name='Администратор?')

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def is_full_profile(self):
        """ Все поля заполнены? """
        fields = ['first_name', 'last_name', 'username', \
                  'email', 'gender', 'phone', 'address', 'bike']
        for field in fields:
            if not getattr(self, field):
                return False
        return True

    def __unicode__(self):
        return self.get_full_name()

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Author(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to="thubnails/")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
