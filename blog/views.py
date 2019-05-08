#-*- coding: utf-8 -*-

import requests
from django.shortcuts import render, redirect , render_to_response
from django.utils import timezone
from .models import Post, City, Comment, Location
from .forms import CityForm, LoginForm, CommentForm, PostForm, SignForm
from django.http import HttpResponse
from .forms import LoginForm, CityForm, PostForm
from django.contrib.auth.models  import User
from django.contrib.auth import login, logout, authenticate
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
        username = request.POST['username']
        password = request.POST['password1']
        location = request.POST['location']
        if request.POST["password1"]==request.POST["password2"]:
                if User.objects.filter(username=username).exists():
                    return redirect('join_fail2')
                else:
                    user = User.objects.create_user(
                        username=request.POST["username"],password=request.POST["password1"])
                    Location.objects.create(user=user, location=request.POST['location'])
                    return redirect('home')
        else:
            return redirect('join_fail')
    else:
        return render(request, 'blog/join.html')
        
def signin(request):
    form = LoginForm(request.POST or None)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username = username, password = password)
    if user is not None:
        login(request, user)
    return redirect('home')
        
def signout(request):
    logout(request)
    return redirect('home')

def some_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            picked = form.cleaned_data.get('picked')
            # do something with your results
    else:
        form = PostForm
    return render_to_response('some_template.html', {'form':form })
        
def home(request):
    l_form = LoginForm()
    c_form = CityForm()
    return render(request, 'blog/home.html', {'login_form':l_form, 'form':c_form})

def images(request):
    posts = Post.objects.all()
    return render(request, 'blog/images.html', {'posts':posts})

def join_fail(request):
    return redirect(request, 'blog/join_fail.html')
    
def join_fail2(request):
    return render(request, 'blog/join_fail2.html')

def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            locs = Location.objects.all()
            for loc in locs:
                if loc.user == post.author:
                    post.city = loc.location
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/new.html', {'form': form})
    
def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?id={}&units=imperial&&appid=9d41bfa0a0254f6f5373e5038c1b117b'
    list = [
        {'cname':'서울','city_id':1835847},
        {'cname':'부산','city_id':1838524},
        {'cname':'대구','city_id':1835329},
        {'cname':'인천','city_id':1843564},
        {'cname':'광주','city_id':1841811},
        {'cname':'대전','city_id':1835235},
        {'cname':'울산','city_id':1833747},
        {'cname':'세종','city_id':1835235},
        {'cname':'경기','city_id':1841610},
        {'cname':'강원','city_id':1843125},
        {'cname':'제주','city_id':1846266},
        {'cname':'하남','city_id':1897007},
        {'cname':'고양','city_id':1842485},
]
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city=form.cleaned_data['name']
            for x in list:
                if city.encode('utf8') == x['cname']:
                    key = x['city_id']
                    r = requests.get(url.format(key)).json()
                    temperature=(r['main']['temp']-32)/2
                    description=r['weather'][0]['description']
                    form.save()
                    posts = Post.objects.all()
                    return render(request, 'blog/home.html', {'cityname':city, 'temperature':temperature, 'description':description, 'posts':posts})
    
def post_detail(request, index):
    post = get_object_or_404(Post, pk=index)
    if request.method =='POST':
        form=CommentForm(request.POST)
        if form.is_valid:
            comment=form.save(commit=False)
            comment.author=request.user
            comment.post=post
            comment.save()
            return redirect('post_detail', index=post.pk)
    else:
        form=CommentForm()
        comments=Comment.objects.filter(post=post)
        return render(request, 'blog/post_detail.html', {'form':form, 'post':post, 'comments':comments})
        
    
    
def post_edit(request, index):
    post=get_object_or_404(Post, pk=index)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect('post_detail', index=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
    
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk) 
    post.delete()
    return redirect('home')

def comment_edit(request, index, cindex):
    comment=get_object_or_404(Comment, pk=cindex)
    post=get_object_or_404(Post, pk=index)
    if request.method=='POST':
        form=CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.author=request.user
            comment.save()
            return redirect('post_detail', index=post.pk)
    else:
        form=CommentForm(instance=comment)
        return render(request,'blog/comment_edit.html', {'form':form })
        
def comment_delete(request, index, cindex):
    comment=get_object_or_404(Comment, pk=cindex)
    post=get_object_or_404(Post, pk=index)
    comment.delete()
    return redirect('post_detail', index=post.pk)
    