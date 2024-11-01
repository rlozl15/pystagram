from django.shortcuts import render, redirect
from posts.models import Post, Comment, PostImage
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
        url = reverse("posts:feeds") + f"#post-{comment.post.id}"
        return HttpResponseRedirect(url)

@require_POST
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
        url = reverse("posts:feeds") + f"#post-{comment.post.id}"
        return HttpResponseRedirect(url)
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

            url = reverse("posts:feeds") + f"#post-{post.id}"
            return HttpResponseRedirect(url)
    else:
        form = PostForm()
    context = {"form":form}
    return render(request, "posts/post_add.html", context)