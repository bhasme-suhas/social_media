from django.shortcuts import render,redirect
from .models import Post
from django.contrib.auth.decorators import login_required
# Create your views here.
def index_view(request):
    page_name = 'index.html'
    user = request.user
    data = {
        "posts":Post.objects.all().order_by('-created_at')
    }
    return render(request,page_name,context=data)

@login_required(login_url='sign_in')
def submit_post(request):
    user = request.user
    content = request.POST['post_caption']
    image = request.FILES.get('post_image')
    Post.objects.create(
        user=user,
        caption=content,
        image=image
    )
    return redirect('index')