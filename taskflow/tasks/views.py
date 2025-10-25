from django.shortcuts import render
from django.views.decorators.http import require_POST
from .models import Task
from projects.models import Project
import json
from django.http import JsonResponse

@require_POST
def update_task_status_ajax(request,task_id):
    try:
        task = Task.objects.get(id=task_id)
        data = json.loads(request.body)
        new_status = data.get('status').title()
        # print(new_status)

        if new_status in ['Backlog', 'To Do', 'In Progress', 'Completed']:
            task.status = new_status
            task.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False,'error': 'Invalid status','status':400})
    except Task.DoesNotExist:
        return JsonResponse({'success': False,'error': 'Task not found','status':404})
    
@require_POST
def create_task_ajax(request):
    name = request.POST.get('name')
    project_id = request.POST.get('project_id')
    user = request.user

    if not name:
        return JsonResponse({'success': False,'error': 'Task name is required','status':400})
    if not project_id:
        return JsonResponse({'success': False,'error': 'Project is required','status':400})

    try:
        project = Project.objects.get(id=project_id)
        task = Task.objects.create(name=name, project=project, owner=user)
        return JsonResponse({'success': True,'task_id': task.id})
    except Project.DoesNotExist:
        return JsonResponse({'success': False,'error': 'Project not found','status':404})