from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Project
from .forms import ProjectForm

# Create your views here.
class ProjectCreateView(CreateView):
    model=Project
    form_class = ProjectForm
    template_name = 'projects/project_create.html'
    success_url = reverse_lazy("accounts:dashboard")