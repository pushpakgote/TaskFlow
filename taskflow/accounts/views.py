from django.shortcuts import render
from django.views.generic import View
from projects.models import Project
from tasks.models import Task
from .models import Profile
from teams.models import Team

# Create your views here.
class DashBoardView(View):
    def get(self, request, *args, **kwargs):
        latest_projects = Project.objects.all()
        latest_tasks = Task.objects.all()
        latest_members = Profile.objects.all()

        context = {
            'latest_projects': latest_projects[:5],
            'projects_near_due_date': latest_projects.due_in_two_days_or_less()[:5],
            # 'latest_tasks': latest_tasks[:5],
            'latest_members': latest_members[:8],
        }
        if request.user.is_authenticated:
            latest_notifications = request.user.notifications.unread()
            context['latest_notifications'] = latest_notifications[:5]
            context['notification_count'] = latest_notifications.count()
        
        context['latest_projects_count'] = latest_projects.count()
        # context['latest_tasks_count'] = latest_tasks.count()
        context['latest_members_count'] = latest_members.count()
        context['latest_teams_count'] = Team.objects.all().count()
        context["header_text"] = "Dashboard"


        return render(request, 'accounts/dashboard.html', context)
