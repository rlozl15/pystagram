from django.shortcuts import render, redirect
from posts.models import Post

def feeds(request):
    # 로그인 되어 있지 않으면 로그인 페이지로 이동
    if not request.user.is_authenticated:
        return redirect("/users/login/")

    # 모든 글 목록 전달
    posts = Post.objects.all()
    context = {"posts":posts}
    return render(request, "posts/feeds.html", context)