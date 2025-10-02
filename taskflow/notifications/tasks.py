from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from projects.models import Project

@shared_task
def create_notification(actor_username, verb, object_id):
    try:
        actor = User.objects.get(username=actor_username)
        content_type = ContentType.objects.get_for_model(Project)
        project = Project.objects.get(id=object_id)

        members=project.team.members.all()
        for recipient in members:
            if recipient != actor:
                notification=Notification.objects.create(actor=actor, recipient=recipient, verb=verb, content_type=content_type, object_id=object_id, content_object=project, read=False)

        return notification.verb
    except User.DoesNotExist:
        return None
    except ContentType.DoesNotExist:
        return None