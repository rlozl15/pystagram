from django.contrib import admin
from posts.models import Post, PostImage, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "content"]

@admin.register(PostImage)
class PostImangeAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "photo"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "content"]