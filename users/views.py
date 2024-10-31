from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from users.forms import LoginForm, SignupForm
from users.models import User

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
                # form에 에러를 추가
                form.add_error(None, "해당하는 사용자가 없습니다.")
    else:
        form = LoginForm()

    context = {
        "form": form,
    }

    return render(request, "users/login.html", context)

def logout_view(request):
    logout(request)
    return redirect("/users/login/")

def signup(request):
    if request.method == "POST":
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            profile_image = form.cleaned_data["profile_image"]
            short_description = form.cleaned_data["short_description"]

            user = User.objects.create_user(
                username=username,
                password=password1,
                profile_image=profile_image,
                short_description=short_description,
            )
            login(request, user)
            return redirect("/posts/feeds/")

        # 에러가 있는 경우 회원가입 페이지로 이동
        else:
            context = {"form": form}
            return render(request, "users/signup.html", context)
    # GET
    else:
        form = SignupForm()
        context = { "form": form }
        return render(request, "users/signup.html", context)