from django.contrib import admin
from .models import Profile, Post, Relationship

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'content')
    list_filter = ('user',)
    search_fields = ('content',)

admin.site.register(Profile)
admin.site.register(Post, PostAdmin)
admin.site.register(Relationship)
