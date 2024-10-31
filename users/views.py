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

            # 비밀번호와 비밀번호 확인값이 같은가
            if password1 != password2:
                form.add_error("password2", "비밀번호 확인 값이 다릅니다.")

            # username을 가진 사용자가 있는가
            if User.objects.filter(username=username).exists():
                form.add_error("username", "입력한 사용자명은 이미 사용중입니다.")

            # 에러가 존재한다면 에러를 포함한 form을 회원가입 페이지에 렌더링
            if form.errors:
                context = {"form": form}
                return render(request, "users/signup.html", context)
            # 에러가 없다면 사용자 생성하고 로그인 처리 후 피드 페이지로 이동
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    profile_image=profile_image,
                    short_description=short_description,
                )
                login(request, user)
                return redirect("/posts/feeds/")

    else:
        form = SignupForm()
        context = { "form": form }
        return render(request, "users/signup.html", context)