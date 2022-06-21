# from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django_celery_results.models import TaskResult

from tutorial.tasks import chain_tasks

# Create your views here.

def dashboard(request):
    results = TaskResult.objects.all()
    return render(request,
                  'dashboard.html',
                  {'results': results})


@require_http_methods(["POST", ])
@csrf_exempt
def task_use_celery(request):
    if request.method == 'POST':
        task_id = chain_tasks('python')
        return JsonResponse({"data": task_id})
