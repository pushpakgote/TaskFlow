from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,UpdateView,DeleteView,DetailView
from .models import Team
from .forms import TeamForm
from django.contrib import messages


# Create your views here.
class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/create_team.html'
    success_url = reverse_lazy('teams:team-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Teams Add"
        context["title"] = "Teams Add"
        context["submit_button_text"] = "Create New Team"
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        if not form.cleaned_data['team_lead']:
            form.cleaned_data['team_lead'] = self.request.user

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    
class TeamListView(ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Team.objects.all()
        else:
            user_created_teams = Team.objects.filter(created_by=user)
            user_belonged_teams = Team.objects.filter(members=user)
            user_team= user_created_teams | user_belonged_teams
            return user_team.distinct()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Teams List"
        context["title"] = "Teams List"
        # context["submit_button_text"] = "Create New Team"
        return context
    
class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    # template_name = 'teams/update_team.html'
    template_name = 'teams/create_team.html'
    success_url = reverse_lazy('teams:team-list')

    def get_object(self, queryset = None):
        team = get_object_or_404(Team, pk=self.kwargs['pk'])

        if team.created_by != self.request.user and not self.request.user.is_superuser and team.team_lead != self.request.user:
            raise Http404("You do not have permission to edit this team.")
        
        return team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Teams Update"
        context["title"] = "Teams Update"
        context["submit_button_text"] = "Update Team"
        return context
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class TeamDeleteView(DeleteView):
    model=Team
    template_name = 'teams/confirm_delete.html'
    success_url = reverse_lazy("teams:team-list")
    # context_object_name = 'team'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            print(next_url)
            return next_url
        return super().get_success_url()
    
    def get_object(self, queryset = None):
        team = get_object_or_404(Team, pk=self.kwargs['pk'])

        if team.created_by != self.request.user and not self.request.user.is_superuser:
            raise Http404("You do not have permission to delete this team.")
        
        return team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_notifications = self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications[:5]
        context['notification_count'] = latest_notifications.count()
        context["header_text"] = "Project Delete"
        context["title"] = "Project Delete"
        return context
    
    def post(self, request, *args, **kwargs):
        team = self.get_object()
        next_url = request.GET.get('next') or self.get_success_url()

        if request.user != team.created_by:
            messages.warning(request, "You are not allowed to delete this project.")
            return redirect(next_url)
        
        # messages.success(request, f"Team '{team.name}' deleted successfully.")
        return super().post(request, *args, **kwargs)

