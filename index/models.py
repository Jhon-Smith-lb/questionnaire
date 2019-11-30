from django.db import models


class TableName(models.Model):
    title = models.TextField(verbose_name='问卷名称')
    description = models.TextField(verbose_name='问卷说明', blank=True)


class TableData(models.Model):
    title = models.TextField(verbose_name='问题名称')
    type
