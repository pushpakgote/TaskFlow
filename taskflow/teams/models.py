from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=255,unique=True)
    description = models.TextField(blank=True,null=True)
    team_lead = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='teams_lead')
    members = models.ManyToManyField(User,related_name='teams')
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='created_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)