from django.conf.urls import url

from tutorial import views

urlpatterns = [

    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^task/', views.task_use_celery),
]
