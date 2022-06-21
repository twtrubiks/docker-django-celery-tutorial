from django.urls import path

from . import views

urlpatterns = [
    # ex: /
    path('', views.dashboard, name='dashboard'),
    # ex: /task/
    path('task/',views.task_use_celery),

]
