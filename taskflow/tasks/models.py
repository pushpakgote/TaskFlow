from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
from projects.models import Project

STATUS_CHOICES = [
    ('To Do', 'To Do'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
]
PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]

# Create your models here.
class Task(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=255)
    Project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks')
    description=models.TextField(blank=True,null=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='To Do')
    priority=models.CharField(max_length=20,choices=PRIORITY_CHOICES,default='Medium')
    start_date=models.DateField()
    due_date=models.DateField()
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
            return 'success'
        elif self.progress==50:
            return 'primary'
        else:
            return ''
    


    def priority_color(self):
        if self.priority == 'Low':
            return 'success'
        elif self.priority == 'Medium':
            return 'warning'
        else:
            return 'danger'