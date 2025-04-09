from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class researcher_form(models.Model):
    id=models.AutoField(primary_key=True)
    first_Name = models.CharField(max_length=100)
    last_Name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)

    def clean(self):
        super().clean()
        if self.profile_pic and self.profile_pic.size > 2 * 1024 * 1024:
            raise ValidationError("Profile picture file size should be less than 2MB")

    current_project = models.CharField(max_length=100)
    uv_name = models.CharField(max_length=100)
    dept_name = models.CharField(max_length=100)
    session=models.CharField(max_length=100)
    interested_domain=models.CharField(max_length=200)
    experiences=models.CharField(max_length=200)
    
    # join_date = models.DateField(default=datetime.date.today)
    # ratings=(
    # (1,"Active"),
    # (2,"Very Active"),
    # (3,"Hardworking"),
    # (4,"Excellent Hardworking"),
    # (5,"Extraordinary"),
    # )
    
    # Ranking=models.IntegerField(choices=ratings)

    Ranking = models.IntegerField(default=60)


    linekdin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    personal_website = models.URLField(blank=True)
    google_scholar_url = models.URLField(blank=True)


   

    def __str__(self):
        return f"{self.first_Name} {self.last_Name}"

class researcher_recommend(models.Model):
    researcher_id=models.ForeignKey(researcher_form,on_delete=models.CASCADE)
    Details=models.CharField(max_length=300)

    def __str__(self):
     return f"{self.researcher_id} - {str(self.Details)}"

