#-*- coding: utf-8 -*-

import requests
from django.shortcuts import render, redirect ,render_to_response
from django.utils import timezone
from .models import Post, F
from .forms import CityForm, LoginForm, CommentForm, PostForm
from django.http import HttpResponse
from .forms import LoginForm, CityForm, PostForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required


# Create your views here.
#class CreateUserView(CreateView):
    #template_name = 'blog/join.html'
    #form_class = CreateUserForm
    #success_url = reverse_lazy('create_user_done')
    
def signup(request):
    if request.method == "POST":
        if request.POST["password1"]==request.POST[" password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],password=request.POST["password1"])
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'blog/join.html')
    else:
        return render(request, 'blog/join.html')
        
def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else: 
            return redirect('home')
    else:
        form = LoginForm()
        return render(request, 'blog/home.html', {'login_form':form})
        
        
def some_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            picked = form.cleaned_data.get('picked')
            # do something with your results
    else:
        form = PostForm
    return render_to_response('some_template.html', {'form':form }, context_instance=RequestContext(request))
        
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts_list':posts})

@login_required    
def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/new.html', {'form': form})
    
def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=9d41bfa0a0254f6f5373e5038c1b117b'
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city=form.cleaned_data['name']
            r = requests.get(url.format(city)).json()
            temperature=r['main']['temp']
            description=r['weather'][0]['description']
            form.save()
            return render(request, 'blog/weather.html', {'cityname':city, 'temperature':temperature, 'description':description})
    else:
        form = CityForm()
        return render(request, 'blog/home2.html',{'form':form})
    
def post_detail(request, index):
    post = get_object_or_404(Post, pk=index)
    return render(request, 'blog/post_detail.html', {'post': post})
    
def post_edit(request, index):
    post=get_object_or_404(Post, pk=index)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect('post_detail', {'form': form})
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
    
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk) 
    post.delete()
    return redirect('post_list')
