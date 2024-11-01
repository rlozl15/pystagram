from django.contrib import admin
from posts.models import Post, PostImage, Comment, HashTag
import admin_thumbnails
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin_thumbnails.thumbnail("photo")
class PostImangeInline(admin.TabularInline):
    model = PostImage
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "content"]
    inlines = [CommentInline, PostImangeInline]
    # 다대다 필드를 체크박스로 출력
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple},
    }

@admin.register(PostImage)
class PostImangeAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "photo"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "content"]

@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]