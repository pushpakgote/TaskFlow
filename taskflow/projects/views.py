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

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            latest_notifications = self.request.user.notifications.unread()
            context['latest_notifications'] = latest_notifications[:5]
            context['notification_count'] = latest_notifications.count()
            context["header_text"] = "Project Add"
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()
        return super().form_valid(form)