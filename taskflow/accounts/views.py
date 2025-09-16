from django.shortcuts import render
from django.views.generic import View
from projects.models import Project
from tasks.models import Task


# Create your views here.
class DashBoardView(View):
    def get(self, request, *args, **kwargs):
        latest_projects = Project.objects.all()[:5]
        latest_tasks = Task.objects.all()[:5]
        
        context = {
            'latest_projects': latest_projects,
            'latest_tasks': latest_tasks
        }
        return render(request, 'accounts/dashboard.html', context)
