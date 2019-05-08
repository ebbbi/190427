from django.shortcuts import render, 
from django .models import Post
from django.http import HttpResponse
from .forms import ProfileForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Create your views here.
# Create your views here.
def signup(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('index')
    else:
        form = ProfileForm()
        return render(request, 'blog/join.html', {'form': form})
        
def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else: 
            return HttpResponse('아이디와 비밀번호를 확인해주세요')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
        
        
def some_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            picked = form.cleaned_data.get('picked')
            # do something with your results
    else:
        form = PostForm

    return render_to_response('some_template.html', {'form':form },
        context_instance=RequestContext(request))
        
def home(request):
    posts = Post.objects.all
    return render(request, 'home.html', {'posts_list':posts})
    
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
    return render(request, 'new.html', {'form': form})