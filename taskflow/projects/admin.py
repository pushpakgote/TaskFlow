from django.contrib import admin
from .models import Project
from notifications.tasks import create_notification

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'team', 'status', 'priority', 'start_date', 'due_date')
    list_filter = ('status', 'priority', 'team')
    search_fields = ('name', 'description', 'client_company')
    # date_hierarchy = 'start_date'

    def save_model(self, request, obj, form, change):
        if not change:
            # obj.owner = request.user
            verb = f"New Project Assigned, { obj.name }"
        else:
            verb = f"Project Updated, { obj.name }"
        super().save_model(request, obj, form, change)

        #Send notification
        actor_username = request.user.username
        object_id = obj.id
        create_notification.delay(actor_username=actor_username, verb=verb, object_id=object_id)


admin.site.register(Project,ProjectAdmin)