from django.shortcuts import render
from django.views.generic import View
from projects.models import Project
from tasks.models import Task
from .models import Profile
from notifications.models import Notification

# Create your views here.
class DashBoardView(View):
    def get(self, request, *args, **kwargs):
        latest_projects = Project.objects.all()[:5]
        latest_tasks = Task.objects.all()[:5]
        latest_members = Profile.objects.all()[:8]
        context = {
            'latest_projects': latest_projects,
            'latest_tasks': latest_tasks,
            'latest_members': latest_members,
        }
        if request.user.is_authenticated:
            latest_notifications = Notification.objects.for_user(request.user)[:5]
            context['latest_notifications'] = latest_notifications
            context['notification_count'] = latest_notifications.count()

        return render(request, 'accounts/dashboard.html', context)
