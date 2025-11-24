from projects.models import Project
from tasks.models import Task
from accounts.models import Profile
from teams.models import Team

def global_navbar_context(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user

    if user.is_superuser:
        latest_projects = Project.objects.all()
        latest_tasks = Task.objects.all()
        latest_members = Profile.objects.all()
        team_count = Team.objects.count()
    else:
        latest_projects = Project.objects.all().for_user(user)
        latest_tasks = Task.objects.all().for_user(user)
        latest_members = Profile.objects.filter(user__teams__in=user.teams.all()).distinct()
        team_count = user.teams.count()

    latest_notifications = request.user.notifications.unread(request.user)

    return {
        "latest_notifications": latest_notifications[:5],
        "notification_count": latest_notifications.count(),
        "latest_projects_count": latest_projects.count(),
        "latest_tasks_count": latest_tasks.count(),
        "latest_members_count": latest_members.count(),
        "latest_teams_count": team_count,
    }
