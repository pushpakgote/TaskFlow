from django.urls import path
from .views import ProjectCreateView,ProjectListView,ProjectDetailView,KanbanBoardView

app_name = 'projects'

urlpatterns = [
    path('<uuid:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<uuid:pk>/kanban-board/', KanbanBoardView.as_view(), name='kanban-board'),
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('<str:filter>/', ProjectListView.as_view(), name='list_filtered'),
    path('', ProjectListView.as_view(), name='list'),
]