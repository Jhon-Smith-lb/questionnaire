from django.contrib import admin
from django.contrib.auth.models import User

from .models import Table, Question, Choice, Advice, File

admin.site.site_title = '调查问卷后台管理系统'
admin.site.site_header = '调查问卷后台管理系统'
admin.site.index_title = "首页"


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    list_display = ['title']
    extra = 1


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'time', 'status']
    fieldsets = [
        (None, {'fields': ['title', 'description']}),
        ('时间信息', {'fields': ['time']}),
        ('问卷状态', {'fields': ['status']}),
    ]
    inlines = [QuestionInline]
    ordering = ['time']
    list_editable = ['status']
    list_display_links = ['title']
    list_filter = ['status', 'time']
    search_fields = ['title', 'description']
    date_hierarchy = 'time'

    # def get_queryset(self, request):
    #     """函数作用：使当前登录的用户只能看到自己出的问卷"""
    #     qs = super(TableAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(author=request.user)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'table', 'type', 'status']
    list_editable = ['status']
    inlines = [ChoiceInline]
    list_display_links = ['title']
    list_filter = ['table', 'type', 'status']
    search_fields = ['title']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'title', 'poll']
    list_display_links = ['question', 'title']
    list_filter = ['question']


@admin.register(Advice)
class AdviceAdmin(admin.ModelAdmin):
    pass

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass
