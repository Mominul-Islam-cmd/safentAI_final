from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
  
class TeamMembers(models.Model):
    id=models.AutoField(primary_key=True)
    first_Name = models.CharField(max_length=100)
    last_Name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='team_members_pics/', blank=True)

    def clean(self):
        super().clean()
        if self.profile_pic and self.profile_pic.size > 2 * 1024 * 1024:
            raise ValidationError("Profile picture file size should be less than 2MB")

    
    current_job = models.CharField(max_length=100)
    work_experience = models.CharField(max_length=100)

    Role = models.CharField(max_length=100)


    uv_name = models.CharField(max_length=100)
    dept_name = models.CharField(max_length=100)
    domain_expertise=models.CharField(max_length=100)
  
 

    linekdin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    personal_website = models.URLField(blank=True)
    google_scholar_url = models.URLField(blank=True)


   

    def __str__(self):
        return f"{self.first_Name} {self.last_Name}"