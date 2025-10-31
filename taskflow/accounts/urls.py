from django.urls import path
from .views import DashBoardView,MemberListView,ProfileDetailView

app_name = 'accounts'

urlpatterns = [
    path('', DashBoardView.as_view(), name='dashboard'),
    path('members/', MemberListView.as_view(), name='members-list'),
    path('<int:pk>/user/', ProfileDetailView.as_view(), name='profile-detail'),
]