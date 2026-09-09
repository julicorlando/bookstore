from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm, ProfileUpdateForm, SignUpForm, UserUpdateForm
from .models import Follow, Like, Post

User = get_user_model()


def home(request):
    return redirect("feed" if request.user.is_authenticated else "login")


def signup(request):
    if request.user.is_authenticated:
        return redirect("feed")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Conta criada com sucesso!")
        return redirect("feed")
    return render(request, "core/signup.html", {"form": form})


@login_required
def feed(request):
    following_ids = Follow.objects.filter(follower=request.user).values_list("following_id", flat=True)
    posts = (
        Post.objects.filter(author_id__in=following_ids)
        .select_related("author", "author__profile")
        .prefetch_related("likes", "comments__author")
    )
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post publicado.")
            return redirect("profile", username=request.user.username)
    else:
        form = PostForm()
    liked_ids = set(Like.objects.filter(user=request.user, post__in=posts).values_list("post_id", flat=True))
    return render(request, "core/feed.html", {"posts": posts, "form": form, "comment_form": CommentForm(), "liked_ids": liked_ids})


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User.objects.select_related("profile"), username=username)
    posts = profile_user.posts.select_related("author", "author__profile").prefetch_related("likes", "comments__author")
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    liked_ids = set(Like.objects.filter(user=request.user, post__in=posts).values_list("post_id", flat=True))
    context = {
        "profile_user": profile_user,
        "posts": posts,
        "is_following": is_following,
        "followers_count": profile_user.follower_relations.count(),
        "following_count": profile_user.following_relations.count(),
        "liked_ids": liked_ids,
        "comment_form": CommentForm(),
    }
    return render(request, "core/profile.html", context)


@login_required
def edit_profile(request):
    user_form = UserUpdateForm(request.POST or None, instance=request.user)
    profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, "Perfil atualizado.")
        return redirect("profile", username=request.user.username)
    return render(request, "core/edit_profile.html", {"user_form": user_form, "profile_form": profile_form})


@login_required
def explore(request):
    users = User.objects.exclude(pk=request.user.pk).select_related("profile").annotate(follower_count=Count("follower_relations"))
    following_ids = set(Follow.objects.filter(follower=request.user).values_list("following_id", flat=True))
    return render(request, "core/explore.html", {"users": users, "following_ids": following_ids})


@login_required
def follow_toggle(request, username):
    if request.method != "POST":
        return redirect("profile", username=username)
    target = get_object_or_404(User, username=username)
    if target == request.user:
        messages.error(request, "Você não pode seguir a si mesmo.")
        return redirect("profile", username=username)
    relation = Follow.objects.filter(follower=request.user, following=target)
    if relation.exists():
        relation.delete()
    else:
        Follow.objects.create(follower=request.user, following=target)
    return redirect(request.POST.get("next") or "profile", username=username) if not request.POST.get("next") else redirect(request.POST["next"])


@login_required
def like_toggle(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
    return redirect(request.POST.get("next") or "feed")


@login_required
def comment_add(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect(request.POST.get("next") or "feed")


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        raise Http404
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post excluído.")
    return redirect("profile", username=request.user.username)


@login_required
def connections(request, username, kind):
    profile_user = get_object_or_404(User, username=username)
    if kind == "followers":
        users = User.objects.filter(following_relations__following=profile_user).select_related("profile")
        title = "Seguidores"
    elif kind == "following":
        users = User.objects.filter(follower_relations__follower=profile_user).select_related("profile")
        title = "Seguindo"
    else:
        raise Http404
    return render(request, "core/connections.html", {"profile_user": profile_user, "users": users, "title": title})
