# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone,encoding

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

# Imports the Item class
from socialnetwork.models import *
from socialnetwork.forms  import *
from operator import attrgetter
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.http import JsonResponse
from django.db import transaction

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

from socialnetwork.forms import RegistrationForm


@ensure_csrf_cookie
@login_required
def search(request):
    posts = Post.objects.all().order_by('-published_date')
    comments = Comment.objects.all().order_by('published_date')
    context = {'posts': posts, 'comments':comments}
    return render(request, 'socialnetwork/create.html', context)

@login_required
def get_list_json(request):
    response_posts = serializers.serialize('json', Post.objects.all())
    response_comments = serializers.serialize('json', Comment.objects.all())
    authors = []
    for post in Post.objects.all():
        authors.append(post.author.username)

    commenters = []
    for comment in Comment.objects.all():
        commenters.append(comment.commenter.username)

    data = { 'posts'    :   response_posts,
            'this_user' :   request.user.id,
            'comments'  :   response_comments,
            'commenters'  :   commenters,
            'author_username' : authors,
            'commenter_username' : commenters,
            }
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def create(request):
    errors = []

    if not 'post' in request.POST or not request.POST['post']:
        message = 'You must enter an item to add.'
        json_error = '{ "error": "'+message+'" }'
        return HttpResponse(json_error, content_type='application/json')

    else:
        new_post = Post(text=request.POST['post'],
                        author=request.user)
        new_post.publish()
        new_post.save()
        print(new_post.author.username)

    authors = []
    for post in Post.objects.all():
        authors.append(post.author.username)

    response_posts = serializers.serialize('json', Post.objects.all())


    data = { 'posts'    :   response_posts,
            'this_user' :   request.user.id,
            'author_username'   :   authors
            }
    
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def add_comment(request, post_id):
    context = {}
    if request.method != 'POST':
        raise Http404

    if not 'comment' in request.POST or not request.POST['comment']:
        message = 'You must enter a comment to add'
        json_error = '{ "error": "'+message+'" }'
        return HttpResponse(json_error, content_type='application/json')

    if 'hidden_id' in request.POST:
        print("hello")
    

    this_post = Post.objects.get(id=post_id)
    new_comment = Comment(text=request.POST['comment'],
                          commenter=request.user,
                          post=this_post)
    new_comment.publish()
    new_comment.save()

    commenters = []
    for comment in Comment.objects.all():
        commenters.append(comment.commenter.username)

    response_comments = serializers.serialize('json', Comment.objects.all())

    data = {'comments'  :   response_comments,
            'this_user' :   request.user.id,
            'commenter_username' : commenters
            }
    # prev_id = Comment.objects.latest('id').id
    return HttpResponse(json.dumps(data), content_type='application/json')


@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    
    # Initialize user profile
    new_profile = Profile(content_type="",
            picture="",
            bio="Welcome To BlankNote :)",
            id=new_user.id,
            profile_user=new_user,
            followers="")
    new_user.is_active = False
    new_profile.save()


    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
Please click the link below to verify your email address and
complete the registration of your account:

  http://{host}{path}
""".format(host=request.get_host(), 
           path=reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="seonwoo1@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'socialnetwork/needs-confirmation.html', context)

    # # Logs in the new user and redirects 
    # new_user = authenticate(username=form.cleaned_data['username'],
    #                         password=form.cleaned_data['password1'])
    # login(request, new_user)
    # return redirect(reverse('home'))

def get_photo(request, id):
    profile = get_object_or_404(Profile, id=id)

    # Probably don't need this check as form validation requires a picture be uploaded.
    if not profile.picture:
        raise Http404

    return HttpResponse(profile.picture, content_type=profile.content_type)

@login_required
def my_profile(request):
    context = {}

    if request.method == 'GET':
        # when the request is GET method
        # 1. read the stored profile 
        # 2. store into context
        # 3. render context 
        my_profile = Profile.objects.filter(profile_user__exact=request.user).latest('id')
        context['form'] = ProfileForm()
        context['profile'] = my_profile

        followees_list = []
        for each in Profile.objects.filter(followers=request.user):
            followees_list.append(each.profile_user)
        context['followees'] = followees_list
        return render(request, 'socialnetwork/my_profile.html', context)

    # when the request is POST method
    # 1. get new bio and picture 
    # 2. save them into the user's profile model in each field
    # 3. store into the context
    # 4. render context
    new_profile = Profile(profile_user=request.user)
    form = ProfileForm(request.POST, request.FILES, instance=new_profile)
    if not form.is_valid():
        context['form'] = form
    else:
        # Must copy content_type into a new model field because the model
        # FileField will not store this in the database.  (The uploaded file
        # is actually a different object than what's return from a DB read.)
        new_profile = Profile(content_type=form.cleaned_data['picture'].content_type,
            picture=form.cleaned_data['picture'],
            bio=form.cleaned_data['bio'],
            id=request.user.id,)
        # if new_profile.followers.all():
        #     context['followers'] = my_profile.followers.all()

        followees_list = []
        for each in Profile.objects.filter(followers=request.user):
            followees_list.append(each.profile_user)
        context['followees'] = followees_list

        new_profile = form.save()
        new_profile.save()
        context['form'] = ProfileForm()
        context['profile'] = new_profile

    return render(request, 'socialnetwork/my_profile.html', context)

    

@login_required
def other_profile(request):
    last = request.GET['last']
    context={}

    if Profile.objects.filter(profile_user_id__exact=last):
        user_profile = Profile.objects.filter(profile_user_id__exact=last).latest('id')

        if request.method == "GET":
            context['profile'] = user_profile
            if request.user in user_profile.followers.all():
                context['following'] = True
            else:
                context['following'] = False

            # print(user_profile.followers.all())
            return render(request, 'socialnetwork/other_profile.html', context)


        else:
            if request.user in user_profile.followers.all():
                return unfollow(request)
            else:
                return follow(request)

    else:
        context['message'] = "Sorry. I can't find this profile :("
        return render(request, 'socialnetwork/create.html', context)


@login_required
def follow(request):
    context = {}
    last = request.GET['last']
    user_profile = Profile.objects.filter(profile_user_id__exact=last).latest('id')
    context['following'] = True
    user_profile.followers.add(request.user)
    user_profile.save()
    context['profile'] = user_profile
    # print(user_profile.followers.all())
    return render(request, 'socialnetwork/other_profile.html', context)

@login_required
def unfollow(request):
    context = {}
    last = request.GET['last']
    user_profile = Profile.objects.filter(profile_user_id__exact=last).latest('id')
    context['following'] = False
    user_profile.followers.remove(request.user)
    user_profile.save()
    context['profile'] = user_profile
    # print(user_profile.followers.all())
    return render(request, 'socialnetwork/other_profile.html', context)


    
@login_required
def follow_stream(request):
    context={}
    if request.method == 'GET':
        my_profile = Profile.objects.filter(profile_user_id__exact=request.user).latest('id')
        context['profile'] = my_profile
        followees_list = []
        following_posts = []

        for p in Profile.objects.filter(followers__exact=request.user):
            followees_list.append(p.profile_user)

        for profile in Profile.objects.filter(followers__exact=request.user):
            for post in Post.objects.filter(author__exact=profile.profile_user).order_by('-published_date'):
                following_posts.append(post)

        comments = Comment.objects.all().order_by('published_date')
        context['followees'] = followees_list
        context['following_posts'] = sorted(following_posts, key=attrgetter('published_date'), reverse=True)
        context['comments'] = comments

        return render(request, 'socialnetwork/following.html', context)

    else:
        context['message'] = "Your request should be a get method :("
        return render(request, 'socialnetwork/create.html', context)


@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()

    return render(request, 'socialnetwork/confirmed.html', {})








