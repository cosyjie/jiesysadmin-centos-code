from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):

    name = models.CharField(verbose_name='姓名', max_length=100, blank=True)
    email = models.EmailField(verbose_name="邮箱地址", unique=True)
    description = models.TextField(verbose_name="备注", blank=True)

    first_name = None
    last_name = None

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        default_permissions = ()
        verbose_name = verbose_name_plural = '用户'
