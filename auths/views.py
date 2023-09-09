from django.shortcuts import render,redirect
from django.http import HttpResponse
from auths.models import User
from django.contrib.auth.models import auth
from media_app.models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.

def sign_up_view(request):
    page_name = 'sign_up.html'
    if request.method == "GET":
        return render(request, page_name)
    else:
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        if email is None:
            return render(request,page_name,context= {"error":True,"error_msg": "Email is required"})
        if username is None:
            return render(request,page_name,context={"error":True, "error_msg":"Username is required"})
        if password is None:
            return render(request,page_name,context={"error":True, "error_msg":"Password is required"})
        if User.objects.filter(username=username).exists():
            return render(request,page_name,context={"error":True, "error_msg":"User already exists"})
        if User.objects.filter(email=email).exists():
            return render(request, page_name, context={"error": True, "error_msg":"Email already exists"})
       # return HttpResponse("Sign up")
        User.objects.create_user(username = username, email = email, password = password)
        user = auth.authenticate(username=username, password=password)
        Profile.objects.get_or_create(user = user)
        auth.login(request,user)
        return redirect("index")
    
    
def sign_in_view(request):
    page_name = 'sign_in.html'
    if request.method == "GET":
        return render(request, page_name)
    else:
       # email = request.post['email']
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if not user:
            return render(request, page_name, context = {"error":True, "error_msg":"Invalid Credentials buddy!"})
        Profile.objects.get_or_create(user = user)
        auth.login(request,user)
        return redirect("index")
    
@login_required(login_url='sign_in')
def sign_out_view(request):
    auth.logout(request)
    return redirect("index")
