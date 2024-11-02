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

class LikeUserInline(admin.TabularInline):
    model = Post.like_users.through
    verbose_name = "좋아요 한 User"
    verbose_name_plural = f"{verbose_name} 목록"
    extra = 1

    def has_change_permission(selfself, request, obj=None):
        return False

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "content"]
    inlines = [CommentInline, PostImangeInline, LikeUserInline]
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