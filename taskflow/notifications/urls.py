from django.urls import path
from .views import NotificationListView

app_name = 'notifications'

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:notification_id>', NotificationListView.as_view(), name='mark-as-read'),

]