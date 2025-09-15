from django.urls import path
from .views import DashBoardView

app_name = 'accounts'

urlpatterns = [
    path('', DashBoardView.as_view(), name='dashboard'),
]