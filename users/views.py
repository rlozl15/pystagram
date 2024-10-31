from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from users.forms import LoginForm
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect("/posts/feeds/")

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        # 유효성 검사
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # username과 password에 해당하는 사용자가 있는지 검사
            # None or User 객체
            user = authenticate(username=username, password=password)

            # 사용자가 있다면 로그인 처리
            if user:
                login(request, user)
                return redirect("/posts/feeds/")
            else:
                messages.error(request, "실패했습니다.")
    else:
        form = LoginForm()

    context = {
        "form": form,
    }

    return render(request, "users/login.html", context)

def logout_view(request):
    logout(request)
    return redirect("/users/login/")