from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=250)
    
    # Adding a Category (Defaults to 'General' if they don't type one)
    category = models.CharField(max_length=100, default="General")
    
    # Adding an Image (upload_to creates a folder inside your project for these images)
    # blank=True, null=True means an image isn't strictly required to publish a post
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    
    content = models.TextField()
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Profile(models.Model):
    # Links this profile strictly to one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # The creative fields
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')

    def __str__(self):
        return f"@{self.user.username}'s Profile"    