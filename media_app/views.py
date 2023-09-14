from django.shortcuts import render,redirect
from media_app.models import Post,LikePost,Profile
from auths.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Avg,Count

# Create your views here.

def get_data(request, key):
    return request.GET.get(key) or request.POST.get(key)

def index_view(request):
    if request.user.is_authenticated:
        page_name = 'index.html'
        user = request.user
        data ={
            "already_liked_post_ids" : list(set(LikePost.objects.filter(user=user).values_list('post_id', flat=True))),
            "posts" : Post.objects.all().order_by('-created_at')
            }
        return render(request, page_name,context = data)
    else:
        return render(request,"index.html")

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

@login_required(login_url='sign_in')
#def like_post(request,post_id):
def like_post(request):
    user = request.user
    post_id = get_data(request,'post_id')
    #post_id = request.POST['post_id']
    LikePost.objects.create(
        user_id=user.id,
        post_id = post_id
    )
    return redirect('index')

@login_required(login_url='sign_in')
def profile_view(request,username):
    user = User.objects.get(username=username)
    page_name = 'profile.html'
    data = {
        #"top_posts": user.post.all().annotate(likes_received=Count("like_post")).order_by("-likes_received", "-created_at")[:3],
        "profile_user":user,
        "likes_made": user.like_post.count(),
        "posts_made":user.post.count(),
        "likes_received":LikePost.objects.filter(post__user=user).count()
    }
    return render(request,page_name,context = data)

@login_required(login_url='sign_in')
def upload_image(request):
    user = request.user
    image = request.FILES['profile_image']
    profile = Profile.objects.get(user=user)
    profile.image = image
    profile.save()
    return redirect(f'/profile/{user.username}')
    