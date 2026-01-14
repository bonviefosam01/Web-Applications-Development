from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('', views.stream_action, name='stream'),
    path('home/', views.stream_action, name='stream'), #global stream viewing
    path('login/', views.login_action, name='login'),
    path('register/', views.register_action, name='register'),
    path('stream/', views.stream_action, name='stream'), #post creation
    path('profile/', views.profile_action, name='profile'),
    path('follower/', views.follower_stream_action, name='follower_stream'), #this shows the follower stream
    path('follower_page/<int:user_id>', views.follower_page_action, name='follower_page'), #this shows the profile page of someone you're following
    path('logout/', views.logout_action, name='logout'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('unfollow/<int:user_id>', views.unfollow, name='unfollow'),
    path('follow/<int:user_id>', views.follow, name='follow'),
    path('get-global', views.get_global, name='get-global'),
    path('add-comment', views.add_comment, name='add-comment'),
    path('get-follower', views.get_follower, name='get-follower'),
]