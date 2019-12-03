from django.http import HttpResponse
from django.shortcuts import render

from .models import Table, Question, Choice, Advice


# 访问调查问卷
def index(request, table_id):
    table = Table.objects.get(id=table_id)
    single = Question.objects.filter(table=table).filter(status=0).filter(type=0)
    multiply = Question.objects.filter(table=table).filter(status=0).filter(type=1)
    advice = Question.objects.filter(table=table).filter(status=0).filter(type=2)
    return render(request, 'index/index.html', locals())


# 选择投票
def vote(request):
    if request.method == 'POST':
        # cnt1 = 0
        # cnt2 = 0
        # cnt3 = 0
        questions = Question.objects.all()
        for question in questions:
            if request.POST.get(str(question.id), ''):
                if question.type == 0:
                    # 单选
                    choice_id = request.POST.get(str(question.id))
                    choice = Choice.objects.get(id=int(choice_id))
                    choice.poll += 1
                    choice.save()
                    # cnt1 += 1
                elif question.type == 1:
                    # 多选
                    choices_id = request.POST.getlist(str(question.id))
                    for choice_id in choices_id:
                        choice = Choice.objects.get(id=int(choice_id))
                        choice.poll += 1
                        choice.save()
                        # cnt2 += 1
                else:
                    # 简答
                    advice_text = request.POST.get(str(question.id))
                    advice = Advice()
                    advice.advice_text = advice_text
                    advice.question_text = question
                    advice.save()
                    # cnt3 += 1

        return render(request, 'index/Thanks.html', locals())
    else:
        return HttpResponse('提交失败！')
