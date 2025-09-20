from django.shortcuts import render
from django.views.generic import View
from projects.models import Project
from tasks.models import Task
from .models import Profile

# Create your views here.
class DashBoardView(View):
    def get(self, request, *args, **kwargs):
        latest_projects = Project.objects.all()[:5]
        latest_tasks = Task.objects.all()[:5]
        latest_members = Profile.objects.all()[:8]
        for member in latest_members:
            print(member.profile_picture)
        
        context = {
            'latest_projects': latest_projects,
            'latest_tasks': latest_tasks,
            'latest_members': latest_members
        }
        return render(request, 'accounts/dashboard.html', context)
