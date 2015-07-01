# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


ACCOUNT_BACKENDS = ((u'vk', u'ВКонтакте'),
                    (u'twitter', u'Twitter'),
                    (u'facebook', u'Facebook'),
                    )



class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('User must have a valid username.')
        user = self.model(
            email=UserManager.normalize_email(email),
            username=username,
            **kwargs
        )
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
    username = models.CharField(verbose_name='Псевдоним', max_length=255, unique=True)
    email = models.EmailField(
        verbose_name='Емайл',
        max_length=255,
        unique=True,)
    img_url = models.URLField(null=True)
    phone = models.CharField(verbose_name='Телефон', max_length=255, unique=True, blank=True, null=True)
    bike = models.CharField(verbose_name='Байк', max_length=255, blank=True)

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

    def __unicode__(self):
        return self.get_full_name()

    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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
