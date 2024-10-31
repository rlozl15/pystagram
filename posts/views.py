from django.shortcuts import render, redirect

def feeds(request):
    # 로그인 되어 있지 않으면 로그인 페이지로 이동
    if not request.user.is_authenticated:
        return redirect("/users/login/")
    return render(request, "posts/feeds.html")