from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    message = models.CharField(max_length=200, verbose_name="New Post") #NEED TO SITE VERBOSE NAME
    user = models.ForeignKey(User, on_delete = models.PROTECT, related_name="post")
    creation_time = models.DateTimeField()
    #will probably need to have a comment id or something

    def __str__(self):
        return f"Post(id={self.id}, Post_Message = {self.message}, Posted_By={self.user}, Creation_Time={self.creation_time})"
    
class Profile(models.Model): #one to one relationship with users, many to many relationship between users
    bio = models.CharField(max_length = 200)
    profile_pic = models.FileField(blank=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT) #these are the followers on a profile i think
    content_type = models.CharField(blank=True, max_length=50)
    following = models.ManyToManyField(User, related_name='followers')

    def __str__(self):
        return f"Profile(id={self.id}, bio = {self.bio}, profile_pic={self.profile_pic}, user={self.user}, content_type={self.content_type}, following={self.following})"

class UserFollower(models.Model): #many to many
    user= models.ForeignKey(User, on_delete = models.PROTECT, related_name="logged_in_user") #these are the followers on a profile i think
    follower = models.ForeignKey(User, on_delete = models.PROTECT, related_name="follower") #these are the followers on a profile i think

    def __str__(self):
        return f"UserFollower(user={self.user}, follower'{self.follower})"