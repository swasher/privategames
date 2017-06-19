#from django.db import models

#from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
#from django.contrib.auth.models import BaseUserManager


# class UserManager(BaseUserManager):
#     def create_user(self, email, password, **kwargs):
#         if not email:
#             raise ValueError('Email должен быть указан')
#
#         user = self.model(
#             email=UserManager.normalize_email(email),
#             **kwargs
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password, **kwargs):
#         user = self.create_user(email, password, **kwargs)
#         user.is_admin = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user


# class CustomizedUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField('EMAIL', max_length=255, unique=True, db_index=True)
#     first_name = models.CharField('Имя', max_length=30, blank=True)
#     last_name = models.CharField('Фамилия', max_length=30, blank=True)
#     verified_email = models.BooleanField(default=False)
#     register_date = models.DateField('Дата регистрации', auto_now_add=True)
#     is_active = models.BooleanField('Активен', default=True)
#     is_admin = models.BooleanField('Суперпользователь', default=False)
#     #is_staff = models.BooleanField('Суперпользователь', default=False)
#
#     # Этот метод обязательно должен быть определён
#     def get_full_name(self):
#         return self.email
#
#     def get_short_name(self):
#         return self.email
#
#     # Требуется для админки
#     @property
#     def is_staff(self):
#         # "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin
#
#     def __str__(self):
#         return self.email
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     objects = UserManager()
#
#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'
