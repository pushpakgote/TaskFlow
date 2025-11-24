from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,DetailView,DeleteView,UpdateView
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from .models import Project
from .forms import ProjectForm,AttachmentForm
from notifications.tasks import create_notification
from comments.models import Comment
from comments.forms import CommentForm
from tasks.forms import TaskUpdateForm

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
        context["submit_button_text"] = "Create New Project"
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()

        #Send notification
        actor_username = self.request.user.username
        verb = f"New Project Assigned, { project.name }"
        create_notification.delay(actor_username=actor_username, verb=verb, object_id=project.id, content_type_model='project',content_type_app_label='projects')

        return super().form_valid(form)
    
class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'
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
            return Project.objects.for_user(self.request.user).due_in_two_days_or_less()
        else:
            return Project.objects.all().for_user(self.request.user)
        
        # return super().get_queryset()
    
class ProjectUpdateView(UpdateView):
    model=Project
    form_class = ProjectForm
    template_name = 'projects/project_create.html'
    success_url = reverse_lazy("projects:list")

    def get_object(self, queryset = None):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        if project.owner != self.request.user:
            raise Http404("You are not allowed to edit this project.")
        return project
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Project Update"
        context["title"] = "Project Update"
        context["submit_button_text"] = "Update Project"
        return context

class ProjectDeleteView(DeleteView):
    model=Project
    template_name = 'projects/confirm_delete.html'
    success_url = reverse_lazy("projects:list")
    context_object_name = 'project'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            print(next_url)
            return next_url
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Project Delete"
        context["title"] = "Project Delete"
        return context
    
    def post(self, request, *args, **kwargs):
        project = self.get_object()
        next_url = request.GET.get('next') or self.get_success_url()

        if request.user != project.owner:
            messages.warning(request, "You are not allowed to delete this project.")
            return redirect(next_url)
        
        messages.success(request, f"Project '{project.name}' deleted successfully.")
        return super().post(request, *args, **kwargs)

class ProjectDetailView(DetailView):
    model=Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        project = self.get_object()
        
        # comments
        comments = Comment.objects.filter_by_instance(project)
        paginator = Paginator(comments, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Project Details"
        context["title"] = project.name
        context["my_company"] = project.name
        context["my_company_description"] = project.description
        context["comments"] = comments
        context["page_obj"] = page_obj
        context['comments_count'] = comments.count()
        context['comment_form'] = CommentForm()
        context['attachment_form'] = AttachmentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        project = self.get_object()
        if request.user in project.team.members.all():
            if "comment_submit" in request.POST:
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.user = request.user
                    comment.content_object = project
                    comment.save()

                    #Send notification
                    actor_username = request.user.username
                    actor_fullname = request.user.profile.full_name
                    verb = f"{actor_fullname} commented on { project.name }"
                    create_notification.delay(actor_username=actor_username, verb=verb, object_id=project.id, content_type_model='project',content_type_app_label='projects')

                    messages.success(request, 'Comment added successfully.')
                else:
                    messages.warning(request, form.errors.get("comment", ["Failed to add comment. Please try again."])[0])

            if "attachment_submit" in request.POST:
                attachment_form = AttachmentForm(request.POST, request.FILES)
                if attachment_form.is_valid():
                    attachment = attachment_form.save(commit=False)
                    attachment.user = request.user
                    attachment.project = project
                    attachment.save()
                    messages.success(request, 'Attachment added successfully.')
                else:
                    messages.warning(request, attachment_form.errors.get("file", ["Failed to add attachment. Please try again."])[0])


        else:
            messages.warning(request, 'Only team members can add comments to this project.')
        
        
        return redirect('projects:project-detail', pk=project.id)  # or use Super().get(request, *args, **kwargs)
    
class KanbanBoardView(DetailView):
    model=Project
    template_name = 'projects/kanbanboard.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        project = self.get_object()
        
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Kanban Board"
        context["title"] = f"{project.name} Kanban Board"
        context["is_kanban"]=True
        
        #Seperate tasks by status
        context['backlog_tasks'] = project.tasks.filter(status='Backlog').upcomming()
        context['todo_tasks'] = project.tasks.filter(status='To Do').upcomming()
        context['in_progress_tasks'] = project.tasks.filter(status='In Progress').upcomming()
        context['completed_tasks'] = project.tasks.filter(status='Completed').upcomming()
        context['form'] = TaskUpdateForm(team=project.team.members.all())
        return context
    