from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class Publication(models.Model):
    id=models.AutoField(primary_key=True)
    paper_title = models.CharField(max_length=100)
    publication_pic = models.ImageField(upload_to='publication_pics/', blank=True)

    def clean(self):
        super().clean()
        if self.publication_pic and self.publication_pic.size > 3 * 1024 * 1024:
            raise ValidationError("Publication picture file size should be less than 2MB")
        
    # Publication_details=models.CharField(max_length=500)
    publication_url=models.URLField(max_length=200)


   

    def __str__(self):
        return f"{self.paper_title}"

# class publication_details(models.Model):
#     publication_id=models.ForeignKey(Publication,on_delete=models.CASCADE)
#     Details=models.CharField(max_length=500)
#     publication_url=models.URLField(max_length=200)


#     def __str__(self):
#      return f"{self.publication_id} - {str(self.Details)}"


# Projects Form


class Project(models.Model):
    id=models.AutoField(primary_key=True)
    project_title = models.CharField(max_length=100)
    project_pic = models.ImageField(upload_to='project_pics/', blank=True)

    def clean(self):
        super().clean()
        if self.project_pic and self.project_pic.size > 3 * 1024 * 1024:
            raise ValidationError("project picture file size should be less than 2MB")
        
    # Publication_details=models.CharField(max_length=500)
    Githuv_url=models.URLField(max_length=200)


   

    def __str__(self):
        return f"{self.project_title}"