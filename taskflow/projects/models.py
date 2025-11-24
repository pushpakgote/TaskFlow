from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
from teams.models import Team
from .utils import STATUS_CHOICES,PRIORITY_CHOICES
from datetime import timedelta,datetime
import os

# Create your models here.

class ProjectQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def upcomming(self):
        return self.filter(due_date__gte=timezone.now())
    
    def due_in_two_days_or_less(self):
        today = timezone.now().date()
        two_days_later = today + timezone.timedelta(days=2)
        return self.active().upcomming().filter(due_date__lte=two_days_later)
    
    def for_user(self, user):
        return self.filter(models.Q(owner=user) | models.Q(team__members=user)).distinct()
        
    
class ProjectManager(models.Manager.from_queryset(ProjectQuerySet)):
    # def get_queryset(self):
    #     return ProjectQuerySet(self.model,using=self._db)
    
    def all(self):
        return self.get_queryset().active().upcomming()
    
class Project(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='projects')
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='projects')
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True,null=True)
    client_company = models.CharField(max_length=100, blank=True, null=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='To Do')
    priority=models.CharField(max_length=20,choices=PRIORITY_CHOICES,default='Medium')

    #Budget details
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    estimated_duration = models.IntegerField(blank=True, null=True, help_text="Estimated duration in days")


    start_date=models.DateField()
    due_date=models.DateField()
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects=ProjectManager()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

    def days_until_due(self):
        if self.due_date:
            return (self.due_date -timezone.now().date()).days
        return None
    
    @property
    def progress(self):
        progress_dict={
            'To Do':0,
            'In Progress':50,
            'Completed':100,
        }
        return progress_dict.get(self.status,0)
    
    @property
    def status_color(self):
        if self.progress==100:
            return 'green'
        elif self.progress==50:
            return 'blue'
        else:
            return 'gray'

    def priority_color(self):
        if self.priority == 'Low':
            return 'green'
        elif self.priority == 'Medium':
            return 'yellow'
        else:
            return 'red'
        
def project_attachment_path_location(instance, filename):
    todays_date = datetime.now().strftime('%Y-%m-%d')
    return f"attachments/{instance.project.name}/{todays_date}/{filename}"

class Attachments(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='attachments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=project_attachment_path_location)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return f"Attachment by {self.user.username} for {self.project.name}"

    class Meta:
        ordering = ['-uploaded_at']
