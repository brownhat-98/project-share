from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField 


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True, unique=True)
    phone = models.CharField(max_length=15, null=True)
    profile_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Portfolio(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username}'s Portfolio"

class CustomField(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=200)
    field_value = models.TextField(blank=True)
    field_image = models.ImageField(upload_to='custom_field_images/', blank=True, null=True)

    def __str__(self):
        return self.field_name

class Project(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='intern_images/', blank=True, null=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='project_images/') 

    def __str__(self):
        return f"{self.project.title} - Image"  


class CertificateFiles(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    certificate_pdf = models.FileField(upload_to='certificate_pdfs/', blank=True, null=True)

