from django.urls import path
from . import views

urlpatterns = [
    path('<int:table_id>', views.index, name='index'),
    path('vote', views.vote, name='vote'),
]