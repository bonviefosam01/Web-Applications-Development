from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from socialnetwork.forms import postForm, commentForm, LoginForm, RegisterForm, ProfileForm
from socialnetwork.models import Post, Profile

# Create your views here.
@login_required
def start_site(request): #initial state
    print("start site is happening")
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        post_form = postForm(request.POST)
        comment_form = commentForm(request.POST)
        context = {'post_form': post_form, 'comment_form': comment_form}
        return render(request, "socialnetwork/stream.html", context)
    else:
        context = {}
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

def login_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters
    # And makes the form available in the request context dictionary.
    form = LoginForm(request.POST)
    # Validates the form.
    if not form.is_valid():
        context['form'] = form
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect('stream')

def register_action(request):
    print(request.path)
    context = {}
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        # initialize a new form object (unbound form)
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters
    # and makes the form available in the request context dictionary
    form = RegisterForm(request.POST)

    # Validates the form.
    if not form.is_valid():
        # the form object has errors built into it
        context['form'] = form
        return render(request, 'socialnetwork/register.html', context)
    
    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    
    #add data to the profile db
    new_profile = Profile(bio="Default User Bio", user=new_user, profile_pic="", content_type="")
    new_profile.save()


    login(request, new_user)
    return redirect('stream')

@login_required
def logout_action(request):
    return redirect('login')

@login_required
def stream_action(request): #gloabal stream page
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-creation_time') #CITE CREATION TIME!!
        context = {'post_form': postForm(), 'comment_form': commentForm(), 'posts': posts}
        return render(request, 'socialnetwork/stream.html', context)

    #getting the information passed into the post/comment thing
    post_form = postForm(request.POST)
    comment_form = commentForm(request.POST)

    # Validates the form.
    if not post_form.is_valid() or not comment_form.is_valid() or 'message' not in request.POST:
        posts = Post.objects.all().order_by('-creation_time') #CITE CREATION TIME!!
        return render(request, 'socialnetwork/stream.html', context)

    new_post = Post(message=post_form.cleaned_data['message'], user = request.user, creation_time=timezone.now())
    new_post.save()

    #Get the data from the database and pass it back to the html for html loop
    posts = Post.objects.all().order_by('-creation_time') #CITE CREATION TIME!!
    context = {'post_form': postForm(), 'comment_form': commentForm(), 'posts': posts}
    #return render(request, 'socialnetwork/stream.html', context)
    return redirect('stream')

@login_required
def profile_action(request):
    print("mypic start")
    if request.method == 'GET':
        context= {'profile_form': ProfileForm(initial={'bio': request.user.profile.bio})}
        return render(request, 'socialnetwork/profile.html', context)
    profile = Profile.objects.get(user = request.user)
    profile_form = ProfileForm(request.POST, request.FILES)
    print("profile form" + str(profile_form))
    if not profile_form.is_valid():
        context = {'profile_form': profile_form}
        return render(request, 'socialnetwork/profile.html', context)
    
    pic = profile_form.cleaned_data['profile_pic']

    profile.profile_pic.delete()
    profile.profile_pic = pic
    profile.content_type = pic.content_type
    profile.bio = profile_form.cleaned_data['bio']
    profile.save()

    print(f"{request.user.profile.following.all()}")

    context = {'profile': profile, 'profile_form': profile_form}
    return render(request, 'socialnetwork/profile.html', context)

@login_required
def follower_page_action(request, user_id):
    print("other profile start")
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(Profile, user=user)
    print(user_profile)
    context = {'profile': user_profile}
    return render(request, 'socialnetwork/follower_page.html', context)
        
@login_required
def unfollow(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    request.user.profile.following.remove(user_to_unfollow)
    request.user.profile.save()
    user_profile = get_object_or_404(Profile, user=user_to_unfollow)
    context = {'profile': user_profile}
    #return render(request, 'socialnetwork/follower_page.html', context)
    return redirect('follower_page', user_id=user_id)

@login_required
def follow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    request.user.profile.following.add(user_to_follow)
    request.user.profile.save()
    #p = Profile.objects.get(user=request.user)
    #print(p.following.all())  # Check if it reflects the update immediately
    print(f"{request.user.username} is now following: {request.user.profile.following.all()}")

    user_profile = get_object_or_404(Profile, user=user_to_follow)
    context = {'profile': user_profile}
    #return render(request, 'socialnetwork/follower_page.html', context)
    return redirect('follower_page', user_id=user_id)


@login_required
def follower_stream_action(request):
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-creation_time') #CITE CREATION TIME!!
        context = {'post_form': postForm(), 'comment_form': commentForm(), 'posts': posts}
        return render(request, 'socialnetwork/follower_stream.html', context)

    #getting the information passed into the post/comment thing
    post_form = postForm(request.POST)
    comment_form = commentForm(request.POST)

    # Validates the form.
    if not post_form.is_valid() or not comment_form.is_valid() or 'message' not in request.POST:
        posts = Post.objects.all().order_by('-creation_time') #CITE CREATION TIME!!
        return render(request, 'socialnetwork/follower_stream.html', context)

    new_post = Post(message=post_form.cleaned_data['message'], user = request.user, creation_time=timezone.now())
    new_post.save()

    #Get the data from the database and pass it back to the html for html loop
    posts = Post.objects.all().order_by('-creation_time') #CITE CREATION TIME!!
    context = {'post_form': postForm(), 'comment_form': commentForm(), 'posts': posts}
    #return render(request, 'socialnetwork/stream.html', context)
    return redirect('follower_stream')


@login_required
def get_photo(request, id):
    item = get_object_or_404(Profile, id=id)
    print(f'Picture #{id} fetched from db: {item.profile_pic} (content_type={item.content_type}, type of file={type(item.profile_pic)})')

    if not item.profile_pic:
        raise Http404

    return HttpResponse(item.profile_pic, content_type=item.content_type)