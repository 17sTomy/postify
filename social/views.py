from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import *
from .forms import UserRegisterForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def feed(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, 'social/feed.html', context)

def profile(request, username=None):
    current_user = request.user
    if username and (username != current_user.username):
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        user = current_user
        posts = current_user.posts.all()

    show_followers = 'followers' in request.GET
    show_followings = 'followings' in request.GET

    context = {
        'user': user,
        'posts': posts,
        'show_followers': show_followers,
        'show_followings': show_followings,
    }
        
    return render(request, 'social/profile.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            user = authenticate(username=username, password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                messages.success(request, f'Usuario {username} creado con éxito!')
                return redirect('profile', username=username)
            else:
                messages.error(request, 'Ocurrió un error.')
    else:
        form = UserRegisterForm()

    return render(request, 'social/register.html', {"form": form})

@login_required
def post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            messages.success(request, "Post publicado!")
            return redirect('feed')
    else:
        form = PostForm()
    
    return render(request, 'social/post.html', {"form": form})

@login_required
def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    rel = Relationship(from_user=current_user, to_user=to_user)
    rel.save()
    messages.success(request, f'Ahora sigues a {username}.')
    return redirect('feed')

@login_required
def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    rel = Relationship.objects.filter(from_user=current_user, to_user=to_user).get()
    rel.delete()
    messages.success(request, f'Has dejado de seguir a {username}.')
    return redirect('feed')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if Like.objects.filter(user=user, post=post).exists():
        Like.objects.filter(user=user, post=post).delete()
    else:
        Like.objects.create(user=user, post=post)

    return redirect(request.META.get('HTTP_REFERER', 'home'))


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['image']
    template_name = 'social/update_profile.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.object.user.username})

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Los cambios se guardaron con éxito.')
        return response
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['image'].label = '' 
        return form