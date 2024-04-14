from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .forms import PostForm

from .models import Post

# Create your views here.
def home(request):
    posts = Post.objects.filter(active=True, featured=True)[0:3]

    context = {'posts':posts}
    return render(request, "port/index.html", context)

def posts(request): 
    posts = Post.objects.filter(active=True)

    context = {'posts':posts}
    return render(request, "port/posts.html", context)


def post(request,slug):
    post = Post.objects.get(slug=slug)
    context = {'post':post}
    return render(request, "port/post.html", context)


def profile(request):
    return render(request, "port/profile.html")

#CRUD VIEWS
@login_required(login_url="home")

def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts')

    context = {'form':form}
    return render(request, "port/post_form.html", context)



@login_required(login_url="home")
def update_post(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts')

    context = {'form':form}
    return render(request, "port/post_form.html", context)

@login_required(login_url="home")
def delete_post(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    context = {'item':post}
    return render(request, "port/delete.html", context)




def sendEmail(request):
    if request.method == 'POST':
        template = render_to_string("port/email_template.html", {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })
        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['aakashgopi123@gmail.com']
        )
        email.fail_silently = False
        email.send()
    return render(request, "port/email_sent.html")



