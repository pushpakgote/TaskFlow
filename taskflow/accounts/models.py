from django.db import models
from django.contrib.auth.models import User
#importing signals
from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver

from django.utils.timesince import timesince
from django.utils import timezone
from datetime import timedelta,datetime
import os
from phonenumber_field.modelfields import PhoneNumberField

def profile_image_path_location(instance, filename):
    todays_date = datetime.now().strftime('%Y-%m-%d')
    return f"profile/{instance.user.username}/{todays_date}/{filename}"

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    job_title = models.CharField(max_length=255,blank=True,null=True)
    profile_picture = models.ImageField(upload_to=profile_image_path_location,blank=True,null=True)
    education_level = models.TextField(blank=True,null=True)
    skills = models.TextField(blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    phone_number = PhoneNumberField(blank=True,null=True,unique=True)
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

@receiver(pre_save, sender = Profile)
def delete_old_profile_picture(sender, instance, **kwargs):
    print()
    if not instance.pk:
        return 
    
    try:
        old_profile = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return
    
    old_file=old_profile.profile_picture
    new_file=instance.profile_picture

    if old_file and new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

# Delete profile image file when Profile is deleted
@receiver(post_delete, sender=Profile)
def delete_profile_picture_on_delete(sender, instance, **kwargs):
    file = instance.profile_picture
    if file and os.path.isfile(file.path):
        os.remove(file.path)