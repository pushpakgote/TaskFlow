from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,DetailView
from .models import Project
from .forms import ProjectForm
from notifications.tasks import create_notification

# Create your views here.
class ProjectCreateView(CreateView):
    model=Project
    form_class = ProjectForm
    template_name = 'projects/project_create.html'
    success_url = reverse_lazy("accounts:dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Project Add"
        context["title"] = "Project Add"
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()

        #Send notification
        actor_username = self.request.user.username
        verb = f"New Project Assigned, { project.name }"
        object_id = project.id
        create_notification.delay(actor_username=actor_username, verb=verb, object_id=object_id)

        return super().form_valid(form)
    
class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/project_details.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Projects"
        context["title"] = "All Projects"
        return context
    
    def get_queryset(self):
        filter = self.kwargs.get('filter')
        if filter == 'near-due-date':
            return Project.objects.due_in_two_days_or_less()
        
        return super().get_queryset()
    

class ProjectDetailView(DetailView):
    model=Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Project Details"
        context["title"] = self.get_object().name
        context["my_company"] = "TaskFlow"
        context["my_company_description"] = "TaskFlow is an open source project management system."
        return context