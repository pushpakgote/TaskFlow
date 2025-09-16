from django.db import models
from django.contrib.auth.models import User
#importing signals
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(blank=True,null=True)
    location = models.CharField(max_length=255,blank=True,null=True)
    date_of_birth = models.DateField(blank=True,null=True)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    # @receiver(post_save,sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    
    @receiver(post_save,sender=User)
    def create_user_profile(sender, instance, **kwargs):
        Profile.objects.get_or_create(user=instance)