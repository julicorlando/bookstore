from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Post, Profile

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content",)
        widgets = {"content": forms.Textarea(attrs={"rows": 3, "maxlength": 280, "placeholder": "O que está acontecendo?"})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {"content": forms.TextInput(attrs={"maxlength": 280, "placeholder": "Escreva um comentário..."})}


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "bio")
        widgets = {"bio": forms.Textarea(attrs={"rows": 3, "maxlength": 160})}
