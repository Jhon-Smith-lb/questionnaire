from io import BytesIO

import xlrd
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from xlwt import Workbook
from index.models import Table, Question


def result(request, status):
    if status == 0:
        tables = Table.objects.all()
    elif status == 1:
        tables = Table.objects.filter(status=0)
    elif status == 2:
        tables = Table.objects.filter(status=1)
    else:
        search = request.POST.get("query")
        tables = Table.objects.filter(Q(title__contains=search) | Q(description__contains=search))
    return render(request, 'result/results.html', locals())


def question(request, table_id, type_id):
    a = 0
    b = 0
    c = 0
    d = 0
    table = Table.objects.get(id=table_id)
    table_id2 = table_id
    tables = Table.objects.all()
    All = Question.objects.filter(table=table).all()
    search = request.POST.get("query")
    if type_id == 0:
        d = 1
        singles = Question.objects.filter(table=table).filter(status=0).filter(type=0)
        multiplies = Question.objects.filter(table=table).filter(status=0).filter(type=1)
        advices = Question.objects.filter(table=table).filter(status=0).filter(type=2)
    elif type_id == 1:
        a = 1
        singles = Question.objects.filter(table=table).filter(status=0).filter(type=0)
    elif type_id == 2:
        b = 1
        multiplies = Question.objects.filter(table=table).filter(status=0).filter(type=1)
    elif type_id == 3:
        c = 1
        advices = Question.objects.filter(table=table).filter(status=0).filter(type=2)
    else:
        d = 2
        question2 = Question.objects.filter(table=table).filter(Q(title__contains=search))
    return render(request, 'result/questions.html', locals())


def answer(request, table_id, answer_id):
    table = Table.objects.get(id=table_id)
    x = Question.objects.filter(table=table).get(id=answer_id)
    if x.type == 0 or x.type == 1:
        flag = 0
    else:
        flag = 1
    return render(request, 'result/test.html', locals())


def export(request, table_id):
    table = Table.objects.get(id=table_id)
    list_obj = Question.objects.filter(table=table)
    if list_obj:
        """创建工作簿"""
        ws = Workbook(encoding="UTF-8")
        w = ws.add_sheet(table.title)
        w.write(0, 0, u'序号')
        w.write(0, 1, u'题目')
        w.write(0, 2, u'题型')
        w.write(0, 3, u'题目状态')
        excel_row = 1
        for obj in list_obj:
            data_id = excel_row
            data_title = obj.title
            data_type = obj.type
            data_status = obj.status
            w.write(excel_row, 0, data_id)
            w.write(excel_row, 1, data_title)
            if data_type == 0:
                w.write(excel_row, 2, u'单选')
            elif data_type == 1:
                w.write(excel_row, 2, u'多选')
            else:
                w.write(excel_row, 2, u'简答')

            if data_status == 0:
                w.write(excel_row, 3, u'发布')
            else:
                w.write(excel_row, 3, u'暂未发布')

            excel_row += 1
        sio = BytesIO()
        ws.save(sio)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=question.xls'
        response.write(sio.getvalue)
        return response


def Import(request, table_id):
    """批量导入数据"""
    if request.method == 'GET':
        table_id2 = table_id
        return render(request, 'result/import.html', locals())
    else:
        file_obj = request.FILES.get('file')

        # 保存文件
        # upload_file = File()
        # upload_file.title = file_obj.name
        # upload_file.files = file_obj

        type_excel = file_obj.name.split('.')[1]
        if type_excel == 'xlsx':
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=file_obj.read())
            table = wb.sheets()[0]
            nrows = table.nrows
            ncole = table.ncols
            try:
                # 正常的数据库操作应该是原子性操作
                with transaction.atomic():
                    for i in range(1, nrows):
                        # i/o
                        row_value = table.row_values(i)  # 一行的数据

                        # 题型转换
                        if row_value[2] == '单选':
                            type2 = 0
                        elif row_value[2] == '多选':
                            type2 = 1
                        else:
                            type2 = 2

                        # 状态转换
                        if row_value[3] == '发布':
                            status2 = 0
                        else:
                            status2 = 1

                        # 生成问题对象
                        table2 = Table.objects.get(id=table_id)
                        question_obj = Question.objects.create(
                            table=table2,
                            title=row_value[1],
                            type=type2,
                            status=status2,
                        )
            except Exception as e:
                return HttpResponse('出现错误...%s' % e)
            return HttpResponse("上传成功！")
        return HttpResponse('上传的文件格式不是xlsx')
