from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
import json
from django.utils import timezone
from socialnetwork.forms import postForm, commentForm, LoginForm, RegisterForm, ProfileForm
from socialnetwork.models import Post, Profile, Comment

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

    form = LoginForm(request.POST)

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

    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    form = RegisterForm(request.POST)

    if not form.is_valid():

        context['form'] = form
        return render(request, 'socialnetwork/register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    
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
        posts = Post.objects.all().order_by('-creation_time')
        context = {'post_form': postForm(), 'comment_form': commentForm(), 'posts': posts}
        return render(request, 'socialnetwork/stream.html', context)

    post_form = postForm(request.POST)
    comment_form = commentForm(request.POST)

    if not post_form.is_valid():
        posts = Post.objects.all().order_by('-creation_time')
        context = {'post_form': postForm(), 'comment_form': commentForm(), 'posts': posts}
        return render(request, 'socialnetwork/stream.html', context)

    new_post = Post(message=post_form.cleaned_data['message'], user = request.user, creation_time=timezone.now())
    new_post.save()

    posts = Post.objects.all().order_by('-creation_time')
    context = {'post_form': postForm(), 'comment_form': commentForm(), 'posts': posts}
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

    context = {'profile': profile, 'profile_form': profile_form}
    return render(request, 'socialnetwork/profile.html', context)

@login_required
def follower_page_action(request, user_id):
    print("other profile start")
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(Profile, user=user)
    context = {'profile': user_profile}
    return render(request, 'socialnetwork/follower_page.html', context)
        
@login_required
def unfollow(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    request.user.profile.following.remove(user_to_unfollow)
    request.user.profile.save()
    user_profile = get_object_or_404(Profile, user=user_to_unfollow)
    context = {'profile': user_profile}
    return redirect('follower_page', user_id=user_id)

@login_required
def follow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    request.user.profile.following.add(user_to_follow)
    request.user.profile.save()

    user_profile = get_object_or_404(Profile, user=user_to_follow)
    context = {'profile': user_profile}
    return redirect('follower_page', user_id=user_id)


@login_required
def follower_stream_action(request):
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-creation_time') 
        context = {'post_form': postForm(), 'comment_form': commentForm(), 'posts': posts}
        return render(request, 'socialnetwork/follower_stream.html', context)

    post_form = postForm(request.POST)
    comment_form = commentForm(request.POST)

    if not post_form.is_valid() or not comment_form.is_valid() or 'message' not in request.POST:
        posts = Post.objects.all().order_by('-creation_time') 
        return render(request, 'socialnetwork/follower_stream.html', context)

    new_post = Post(message=post_form.cleaned_data['message'], user = request.user, creation_time=timezone.now())
    new_post.save()
    
    posts = Post.objects.all().order_by('-creation_time') 
    context = {'post_form': postForm(), 'comment_form': commentForm(), 'posts': posts}
    return redirect('follower_stream')


@login_required
def get_photo(request, id):
    item = get_object_or_404(Profile, id=id)
    print(f'Picture #{id} fetched from db: {item.profile_pic} (content_type={item.content_type}, type of file={type(item.profile_pic)})')

    if not item.profile_pic:
        raise Http404

    return HttpResponse(item.profile_pic, content_type=item.content_type)


def get_global(request):

    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    
    post_response_data = [{
            'id': model_item.id,
            'user': model_item.user.username,
            'user_id': model_item.user.id,
            'user_first': model_item.user.first_name,
            'user_last': model_item.user.last_name,
            'message':model_item.message,
            'creation_time': str(model_item.creation_time),
        } for model_item in Post.objects.all()]
    
    comment_response_data = [{
            'id': model_item.id,
            'user': model_item.comment_user.username,
            'user_id': model_item.comment_user.id,
            'user_first': model_item.comment_user.first_name,
            'user_last': model_item.comment_user.last_name,
            'post_id': model_item.post.id,
            'message':model_item.text,
            'creation_time': str(model_item.creation_time),
        } for model_item in Comment.objects.all()]
    
    
    response_data = {'posts': post_response_data, 'comments': comment_response_data}


    response_json = json.dumps(response_data)
    response = HttpResponse(response_json, content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response

def _my_json_error_response(message, status=200):
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)

def add_comment(request):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    
    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)
    
    if not 'comment_text' in request.POST or not request.POST['comment_text'] or not 'post_id' in request.POST or not request.POST['post_id']:
        return _my_json_error_response("You must enter an item to add.", status=400)

    try:
        post = Post.objects.get(id=request.POST['post_id'])
    except Post.DoesNotExist:
        return _my_json_error_response("Invalid Post ID.", status=400)
    except ValueError:
        return _my_json_error_response("Invalid Post ID.", status=400)
    
    new_comment = Comment(text=request.POST['comment_text'], comment_user = request.user, creation_time=timezone.now(), post=Post.objects.get(id = request.POST['post_id']))
    new_comment.save()

    return get_global(request)


def get_follower(request):

    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    post_response_data = [{
            'id': model_item.id,
            'user': model_item.user.username,
            'user_id': model_item.user.id,
            'user_first': model_item.user.first_name,
            'user_last': model_item.user.last_name,
            'message':model_item.message,
            'creation_time': str(model_item.creation_time),
        } for model_item in Post.objects.all() if model_item.user in request.user.profile.following.all()]
    
    comment_response_data = [{
            'id': model_item.id,
            'user': model_item.comment_user.username,
            'user_id': model_item.comment_user.id,
            'user_first': model_item.comment_user.first_name,
            'user_last': model_item.comment_user.last_name,
            'post_id': model_item.post.id,
            'message':model_item.text,
            'creation_time': str(model_item.creation_time),
        } for model_item in Comment.objects.all() if model_item.post.id in [post['id'] for post in post_response_data]]
    
    response_data = {'posts': post_response_data, 'comments': comment_response_data}

    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')
