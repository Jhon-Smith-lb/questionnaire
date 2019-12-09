from django.db import models
from user.models import MyUser


class Table(models.Model):
    STATUS_PUB = 0
    STATUS_UNPUB = 1
    STATUS_IETEMS = [
        (STATUS_PUB, '发布'),
        (STATUS_UNPUB, '暂不发布'),
    ]
    title = models.TextField(verbose_name='问卷标题')
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='问卷说明', blank=True)
    time = models.DateTimeField(verbose_name='创建时间')
    status = models.IntegerField(default=STATUS_PUB,
                                 choices=STATUS_IETEMS,
                                 verbose_name='状态')

    class Meta:
        verbose_name_plural = verbose_name = '问卷'

    def __str__(self):
        return self.title


class Question(models.Model):
    STATUS_PUB = 0
    STATUS_UNPUB = 1
    STATUS_IETEMS = [
        (STATUS_PUB, '发布'),
        (STATUS_UNPUB, '暂不发布'),
    ]
    TYPE_SINGLE = 0
    TYPE_MULTIPLY = 1
    TYPE_TEXT = 2
    TYPE = [
        (TYPE_SINGLE, '单选'),
        (TYPE_MULTIPLY, '多选'),
        (TYPE_TEXT, '简答'),
    ]
    title = models.TextField(verbose_name='问题名称')
    table = models.ForeignKey(Table, verbose_name='问卷',
                              on_delete=models.CASCADE)
    type = models.IntegerField(default=TYPE_SINGLE,
                               choices=TYPE,
                               verbose_name='问题类型')
    status = models.IntegerField(default=STATUS_PUB,
                                 choices=STATUS_IETEMS,
                                 verbose_name='状态')

    class Meta:
        verbose_name_plural = verbose_name = '问题'

    def __str__(self):
        return self.title


class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name='问题',
                                 on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name='选项内容')
    poll = models.IntegerField(default=0, verbose_name='选择人数')

    class Meta:
        verbose_name_plural = verbose_name = '选项'

    def __str__(self):
        return self.title


class Advice(models.Model):
    question_text = models.ForeignKey(Question, verbose_name='问题', on_delete=models.CASCADE)
    advice_text = models.TextField(verbose_name='建议内容')

    class Meta:
        verbose_name = verbose_name_plural = '简答内容'

    def __str__(self):
        return self.advice_text



