from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    mobile = models.CharField(max_length=20, verbose_name='手机号码', unique=True)

    # 设置返回值
    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = verbose_name = '用户'
