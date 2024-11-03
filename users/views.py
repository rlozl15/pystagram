from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from users.forms import LoginForm, SignupForm
from users.models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("posts:feeds")

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
                return redirect("posts:feeds")
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
    return redirect("users:login")

def signup(request):
    if request.method == "POST":
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # form 내용을 바탕으로 사용자 객체 저장
            user = form.save()
            login(request, user)
            return redirect("posts:feeds")
    # GET 요청
    else:
        form = SignupForm()

    # GET 요청이면 빈 form, 유효하지 않으면 에러를 포함한 form이 전달됨
    context = {"form": form}
    return render(request, "users/signup.html", context)

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {
        "user":user
    }
    return render(request,"users/profile.html", context)

def followers(request,user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.follower_relationships.all()
    context = {
        "user":user,
        "relationships":relationships,
    }
    return render(request, "users/followers.html", context)

def following(request,user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.following_relationships.all()
    context = {
        "user":user,
        "relationships":relationships,
    }
    return render(request, "users/following.html", context)

def follow(request, user_id):
    # 로그인한 사용자
    user = request.user
    # 로그인한 사용자가 팔로우 하려는 사용자
    target_user = get_object_or_404(User, id=user_id)

    # 이미 팔로잉 중이면 제거
    if target_user in user.following.all():
        user.following.remove(target_user)

    else:
        user.following.add(target_user)

    url_next = request.GET.get("next") or reverse("user:profile",args=[user.id])
    return HttpResponseRedirect(url_next)