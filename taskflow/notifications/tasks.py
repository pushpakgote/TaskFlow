from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from projects.models import Project

@shared_task
def create_notification(actor_username, verb, object_id, content_type_model,content_type_app_label):
    try:
        actor = User.objects.get(username=actor_username)
        # content_type = ContentType.objects.get_for_model(Project)
        content_type=ContentType.objects.get(model=content_type_model,app_label=content_type_app_label)
        content_object = content_type.get_object_for_this_type(id=object_id)

        # project = Project.objects.get(id=object_id)
        # members=project.team.members.exclude(id=actor.id)
        if hasattr(content_object,'team') and hasattr(content_object.team,'members'):
            recipients = content_object.team.members.all()
        else:
            recipients = [content_object.user_assigned_to]

            # members=content_object.team.members.exclude(id=actor.id)
        notification_ids=[]
        for recipient in recipients:
            notification=Notification.objects.create(actor=actor, recipient=recipient, verb=verb, content_type=content_type, object_id=object_id, content_object=content_object, read=False)
            notification_ids.append(notification.id)

        return notification.verb
    except User.DoesNotExist:
        return None
    except ContentType.DoesNotExist:
        return None
    
@shared_task
def notify_teams_due_projects_task():
    project_due_soon = Project.objects.due_in_two_days_or_less()

    for project in project_due_soon:
        verb=f"Reminder : Project Due Soon, { project.name }"
        create_notification.delay(actor_username=project.owner.username, verb=verb, object_id=project.id, content_type_model='project',content_type_app_label='projects')