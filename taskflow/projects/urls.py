from django.urls import path
from .views import ProjectCreateView,ProjectListView,ProjectDetailView,KanbanBoardView,ProjectDeleteView,ProjectUpdateView

app_name = 'projects'

urlpatterns = [
    path('<uuid:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<uuid:pk>/delete/', ProjectDeleteView.as_view(), name='delete'),
    path('<uuid:pk>/kanban-board/', KanbanBoardView.as_view(), name='kanban-board'),
    path('create/', ProjectCreateView.as_view(), name='create'),
    path('<uuid:pk>/update/', ProjectUpdateView.as_view(), name='update'),
    path('<str:filter>/', ProjectListView.as_view(), name='list_filtered'),
    path('', ProjectListView.as_view(), name='list'),
]