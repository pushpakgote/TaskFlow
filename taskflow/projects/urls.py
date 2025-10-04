from django.urls import path
from .views import ProjectCreateView,ProjectListView

app_name = 'projects'

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('<str:filter>/', ProjectListView.as_view(), name='list_filtered'),
    path('', ProjectListView.as_view(), name='list'),
]