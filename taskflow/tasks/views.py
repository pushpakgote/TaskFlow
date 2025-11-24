from django.shortcuts import render,get_object_or_404
from django.views.decorators.http import require_POST
from .models import Task
from .forms import TaskUpdateForm
from projects.models import Project
from notifications.tasks import create_notification
import json
from django.http import JsonResponse

@require_POST
def update_task_status_ajax(request,task_id):
    try:
        task = Task.objects.get(id=task_id)
        data = json.loads(request.body)
        new_status = data.get('status').title()
        print("New Status ::::::::::",new_status)

        if new_status in ['Backlog', 'To Do', 'In Progress', 'Completed']:
            task.status = new_status
            task.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False,'error': 'Invalid status','status':400})
    except Task.DoesNotExist:
        return JsonResponse({'success': False,'error': 'Task not found','status':404})
    
# @require_POST
# def create_task_ajax(request):
#     name = request.POST.get('name')
#     project_id = request.POST.get('project_id')
#     user = request.user
#     status=request.POST.get('status')

#     if not name:
#         return JsonResponse({'success': False,'error': 'Task name is required','status':400})
#     if not project_id:
#         return JsonResponse({'success': False,'error': 'Project is required','status':400})

#     try:
#         project = Project.objects.get(id=project_id)
#         task = Task.objects.create(name=name, project=project, owner=user, status=status)
#         return JsonResponse({'success': True,'task_id': task.id, 'task':serialize_task(task)})
#     except Project.DoesNotExist:
#         return JsonResponse({'success': False,'error': 'Project not found','status':404})
    
@require_POST
def create_task_ajax(request):
    form = TaskUpdateForm(request.POST)

    if not form.is_valid():
        return JsonResponse({'success': False, 'errors': form.errors, 'status': 400})

    project_id = request.POST.get("project_id")
    status = request.POST.get("status")

    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Project not found', 'status': 404})

    task = form.save(commit=False)
    task.project = project
    task.owner = request.user
    task.status = status
    task.save()

    return JsonResponse({'success': True, 'task_id': task.id, 'task': serialize_task(task)})

    
def serialize_task(task):
    return {
        'id': str(task.id),
        'name': task.name,
        'description': task.description,
        'priority': task.priority,
        'status': task.status,
        'start_date': task.start_date.isoformat() if task.start_date else "",
        'due_date': task.due_date.isoformat() if task.due_date else "",
        'assigned_to': task.user_assigned_to.pk if task.user_assigned_to else "",
        'assigned_user_profile_img': task.user_assigned_to.profile.profile_picture_url if task.user_assigned_to else "",
        'assigned_user_full_name': task.user_assigned_to.profile.full_name if task.user_assigned_to else "",
    }


def get_task(request,task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({'success': False,'error': 'Task not found','status':404})
    
    if request.method == 'GET':
        return JsonResponse({'success': True,'task': serialize_task(task)})

def update_task(request,task_id):
    task = get_object_or_404(Task, id=task_id)
    # team_members=Profile.objects.filter(user__in=task.project.team.members.all())
    # print("assigned to ::::::::::",task.__dict__)
    # print("Post request ::::::::::",request.POST)
    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            # task.user_assigned_to = form.cleaned_data['assigned_user']
            form.save()

            #Send notification
            actor_username = request.user.username
            task_user_profile = task.user_assigned_to.profile if task.user_assigned_to else ""
            verb = f"Task {task.name} assigned to {task_user_profile.full_name}" if task_user_profile else f"Task {task.name} created"
            create_notification.delay(actor_username, verb, object_id=task.id, content_type_model='task',content_type_app_label='tasks')

            return  JsonResponse({'success': True,
                                  'task' : serialize_task(task)})
        else:
            return JsonResponse({'success': False,'error': form.errors,'status':400})
    else:
        return JsonResponse({'success': False,'error': 'Invalid request method','status':405})