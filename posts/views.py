from django.shortcuts import render, redirect
from posts.models import Post, Comment, PostImage, HashTag
from posts.forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

def feeds(request):
    # 로그인 되어 있지 않으면 로그인 페이지로 이동
    if not request.user.is_authenticated:
        return redirect("users:login")

    # 모든 글 목록 전달
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        "posts":posts,
        "comment_form":comment_form,
    }
    return render(request, "posts/feeds.html", context)

@require_POST
def comment_add(request):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # 메모리상에 Comment 객체 생성
        comment = form.save(commit=False)
        # 사용자 정보 할당
        comment.user = request.user
        # DB에 저장
        comment.save()
        url_next = request.GET.get("next")
        return HttpResponseRedirect(url_next)

@require_POST
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
        url_next = request.GET.get("next")
        return HttpResponseRedirect(url_next)
    return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다.")

def post_add(request):
    if request.method == "POST":
        form = PostForm(data=request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            for image_file in request.FILES.getlist("images"):
                PostImage.objects.create(
                    post=post,
                    photo=image_file,
                )

            tag_string = request.POST.get("tags")
            if tag_string:
                tag_names = [tag_name.strip() for tag_name in tag_string.split("#")]
                for tag_name in tag_names[1:]:
                    tag, _ = HashTag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            url = reverse("posts:feeds") + f"#post-{post.id}"
            return HttpResponseRedirect(url)
    else:
        form = PostForm()
    context = {"form":form}
    return render(request, "posts/post_add.html", context)

def tags(request, tag_name):
    try:
        tag = HashTag.objects.get(name=tag_name)
    except HashTag.DoesNotExist:
        posts = Post.objects.none()
    else:
        posts = Post.objects.filter(tags=tag)

    context = {
        "tag_name":tag_name,
        "posts":posts,
    }
    return render(request, "posts/tags.html", context)

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_form = CommentForm()
    context = {
        "post": post,
        "comment_form": comment_form,
    }
    return render(request, "posts/post_detail.html", context)

def post_like(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    # 좋아요 해제
    if user.like_post.filter(id=post.id).exists():
        user.like_post.remove(post)
    # 좋아요 추가
    else:
        user.like_post.add(post)

    url_next = request.GET.get("next")
    return HttpResponseRedirect(url_next)
