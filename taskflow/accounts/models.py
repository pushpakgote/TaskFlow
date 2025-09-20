from django.db import models
from django.contrib.auth.models import User
#importing signals
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.timesince import timesince
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile/',blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    location = models.CharField(max_length=255,blank=True,null=True)
    date_of_birth = models.DateField(blank=True,null=True)
    join_date = models.DateField(auto_now_add=True)

    @property
    def profile_picture_url(self):
        try:
            url = self.profile_picture.url
        except:
            url = "https://www.shutterstock.com/image-vector/user-profile-icon-vector-avatar-600nw-2558760599.jpg"
        return url
    
    @property
    def full_name(self):
        return self.user.get_full_name() if self.user.get_full_name() else self.user.get_username()
        # return f"{self.user.first_name} {self.user.last_name}" if self.user.first_name and self.user.last_name else self.user.username
    
    @property
    def date_joined(self):
        time_diff = timezone.now() - self.user.date_joined
        if time_diff < timedelta(days=2):
            return timesince(self.user.date_joined) + "ago"
        else:
            return self.user.date_joined.strftime("%d-%b")

    def __str__(self):
        return self.user.username
    
@receiver(post_save,sender=User)
def create_user_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)