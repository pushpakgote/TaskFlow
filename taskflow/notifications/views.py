from django.shortcuts import redirect
from django.views.generic import ListView
from .models import Notification

# Create your views here.
class NotificationListView(ListView):
    model = Notification
    context_object_name = 'notifications'
    template_name = 'notifications/notification_list.html'
    paginate_by = 10

    def post(self, request,notification_id, *args, **kwargs):
        if notification_id:
            notification = Notification.objects.get(id=notification_id)
            notification.mark_as_read()
        return redirect('notifications:notification-list')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread()
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Notifications"
        context["title"] = "All Notifications"
        return context
    
    def get_queryset(self):
        return self.request.user.notifications.unread()