from django.contrib import admin

# Register your models here.
from .models import Post
from .models import Comment
from .models import Location
admin.site.register(Post)
admin.site.register(Location)
admin.site.register(Comment)