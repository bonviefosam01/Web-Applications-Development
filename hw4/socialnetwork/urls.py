from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('', views.start_site, name='home'),
    path('home/', views.start_site, name='home'),
    path('login/', views.login_action, name='login'),
    path('register/', views.register_action, name='register'),
    path('profile/', views.profile_action, name='profile'),
    path('follower/', views.follower_action, name='follower'), #this shows the follower stream
    path('follower_page/', views.follower_page_action, name='follower_page'), #this shows the profile page of someone you're following
    path('logout/', views.logout_action, name='logout'),
    path('stream/', views.stream_action, name='stream'),
]