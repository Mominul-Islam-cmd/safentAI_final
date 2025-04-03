from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=200, blank=True)
    profile_picture = models.FileField(upload_to='profile_pics', default='profile_pics/default.svg')
    phone_number = models.CharField(max_length=20, blank=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
