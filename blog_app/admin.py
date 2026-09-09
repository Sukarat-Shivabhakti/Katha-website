from django.contrib import admin
from .models import Post, Profile  # Profile is imported

admin.site.register(Post)
admin.site.register(Profile)       