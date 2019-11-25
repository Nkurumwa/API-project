from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=100)

    def __str__(self):
        return f'{self.user.username} Profile'

class Project(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='project_images/')
    design = models.IntegerField(default=0)
    usability = models.IntegerField(default=0)
    content = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField(max_length=250)
    link = models.URLField(max_length=60)
    date_posted = date_posted = models.DateTimeField(default=timezone.now)
    
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_posted']   

    @classmethod
    def search_project(cls,term):
        searched_project = cls.objects.filter(title__icontains=term)
        return searched_project

    @classmethod
    def get_profile_projects(cls, user):
        projects = Project.objects.filter(user__pk = user)
        return projects
    


class Rate(models.Model):
    design = models.PositiveIntegerField(default=0,validators=[MaxValueValidator(10)])
    usability = models.PositiveIntegerField(default=0,validators=[MaxValueValidator(10)])
    content = models.PositiveIntegerField(default=0,validators=[MaxValueValidator(10)])
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)


class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    review = models.TextField(max_length=250)
    profile_id = models.IntegerField(default=0)
    
    def __str__(self):
        return self.review
