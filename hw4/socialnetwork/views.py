from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from socialnetwork.forms import postForm, commentForm, LoginForm, RegisterForm


# Create your views here.
@login_required
def start_site(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return render(request, "socialnetwork/home.html")
    else:
        context = {}
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
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
    return redirect('home')

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

    login(request, new_user)
    return redirect('home')

@login_required
def logout_action(request):
    return redirect('login')

@login_required
def stream_action(request):
    #context = {'post_form': postForm(), 'comment_form': commentForm()}
    #print(context)
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context = {'post_form': postForm(), 'comment_form': commentForm()}
        return render(request, 'socialnetwork/home.html', context)

    # Creates a bound form from the request POST parameters
    # And makes the form available in the request context dictionary.
    post_form = postForm(request.POST)
    comment_form = commentForm(request.POST)

    # Validates the form.
    if not post_form.is_valid() or not comment_form.isvalid:
        #context['form'] = form
        context['post_form'] = post_form
        context['comment_form'] = comment_form
        return render(request, 'socialnetwork/home.html', context)

    post = {'newPost': post_form.cleaned_data['newPost']}
    comment = {'comment': comment_form.cleaned_data['comment']}
    context = {'post': post, 'comment': comment}
    return render(request, 'socialnetwork/home.html', context)
    #return redirect('home')

@login_required
def follower_stream_action(request):
    pass

@login_required
def profile_action(request):
    return render(request, 'socialnetwork/profile.html')

@login_required
def follower_action(request):
    #this shows the follower stream
    return render(request, 'socialnetwork/follower.html')

@login_required
def follower_page_action(request):
    return render(request, 'socialnetwork/follower_page.html')