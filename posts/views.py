from django.shortcuts import render, redirect
from posts.models import Post, Comment
from posts.forms import CommentForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseForbidden

def feeds(request):
    # 로그인 되어 있지 않으면 로그인 페이지로 이동
    if not request.user.is_authenticated:
        return redirect("/users/login/")

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
        return HttpResponseRedirect(f"/posts/feeds/#post-{comment.post.id}")

@require_POST
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user == request.user:
        comment.delete()
        return HttpResponseRedirect(f"/posts/feeds/#post-{comment.post.id}")
    return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다.")