from django.shortcuts import render
from django.views.generic import View,ListView,DetailView
from django.core.paginator import Paginator
from projects.models import Project
from tasks.models import Task
from .models import Profile
from teams.models import Team
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment

# Create your views here.
class DashBoardView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        
        if user.is_superuser:
            latest_projects = Project.objects.all()
            latest_tasks = Task.objects.all()
            latest_members = Profile.objects.all()
            team_count = Team.objects.all().count()
        else:
            latest_projects = Project.objects.all().for_user(user)
            latest_tasks = Task.objects.all().for_user(user)
            latest_members = Profile.objects.filter(user__teams__in=user.teams.all()).distinct()
            team_count = user.teams.all().count()

        context = {
            'latest_projects': latest_projects[:5],
            'projects_near_due_date': latest_projects.due_in_two_days_or_less()[:5],
            # 'latest_tasks': latest_tasks[:5],
            'latest_members': latest_members[:8],
        }
        
        latest_notifications = request.user.notifications.unread(user)
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        
        context['latest_projects_count'] = latest_projects.count()
        context['latest_tasks_count'] = latest_tasks.count()
        context['latest_members_count'] = latest_members.count()
        context['latest_teams_count'] = team_count
        context["header_text"] = "Dashboard"
        context["title"] = "Dashboard"
        context["title"] = "Dashboard"
        return render(request, 'accounts/dashboard.html', context)

class MemberListView(ListView):
    model = Profile
    context_object_name = 'members'
    template_name = 'accounts/profile_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Members"
        context["title"] = "All Members"
        return context
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user__teams__in=user.teams.all()).distinct()
        
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        profile = self.get_object()
        context = super().get_context_data(**kwargs)

        user_projects = Project.objects.all().for_user(profile.user)

        #Paginator projects
        paginator = Paginator(user_projects, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        #Users comments
        user_comments = profile.user.comments.all()
        project_content_type = ContentType.objects.get_for_model(Project)
        project_comments = Comment.objects.filter(content_type=project_content_type, object_id__in=[str(id) for id in user_projects.values_list('id', flat=True)])

        #Paginator comments
        comment_paginator = Paginator(project_comments, 5)
        comment_page_number = self.request.GET.get('comment_page')
        comment_page_obj = comment_paginator.get_page(comment_page_number)

        #User tasks
        user_tasks = Task.objects.all().for_user(profile.user)

        #user tasks paginator
        task_paginator = Paginator(user_tasks, 5)
        task_page_number = self.request.GET.get('task_page')
        task_page_obj = task_paginator.get_page(task_page_number)


        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Profile"
        context["title"] = f"{self.get_object().full_name}"

        context['user_task_count'] = user_tasks.count()
        context['tasks'] = task_page_obj
        context['user_project_count'] = user_projects.count()
        context['user_projects'] = user_projects
        context['page_obj'] = page_obj
        context['project_comments'] = project_comments
        context['comments'] = comment_page_obj
        context['all_user_comments_count'] = project_comments.count()
        
        return context