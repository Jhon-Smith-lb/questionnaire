from django.urls import path
from . import views

urlpatterns = [
    path('<int:status>', views.result, name='result'),
    path('<int:table_id>/<int:type_id>', views.question, name='question'),
    path('answer/<int:table_id>/<int:answer_id>', views.answer, name='answer'),
    path('export/<int:table_id>', views.export, name='export'),
    path('import/<int:table_id>', views.Import, name='Import'),
]
