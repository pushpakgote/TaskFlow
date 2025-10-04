from django.urls import path
from .views import DashBoardView,MemberListView

app_name = 'accounts'

urlpatterns = [
    path('', DashBoardView.as_view(), name='dashboard'),
    path('members/', MemberListView.as_view(), name='members-list'),
]