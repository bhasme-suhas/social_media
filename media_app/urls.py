from django.urls import path
from .views import index_view,submit_post,like_post,profile_view,upload_image

urlpatterns = [
    path("",index_view, name = 'index'),
    path("submit-post/",submit_post, name = 'submit_post'),
    #path("like-post/<int:post_id>",like_post, name = 'like_post'),
    path("like-post/",like_post, name = 'like_post'),
    path("profile/<str:username>/",profile_view, name = 'profile_view'),
    path("upload_image",upload_image, name = 'upload_image'),
]