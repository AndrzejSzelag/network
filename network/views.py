import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Follow, Like
from django.core import serializers
from django.core.paginator import Paginator


def index(request):
    try:
        all_posts = Post.objects.all().order_by("-timestamp")
        items_count = len(all_posts)
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = None

    try:
        likes_list = Like.objects.filter(likedby=request.user.username)
        liked_ids = []
        for l in likes_list:
            liked_ids.append(l.postid)
    except:
        liked_ids = None
    cuser = []
    cuser.append(request.user.username)
    return render(request, 'network/index.html', {
        'items_count': items_count,
        'page_obj': page_obj,
        'liked_ids': liked_ids,
        'cuser': cuser
    })


@login_required
def create(request):
    if request.user.username:
        return render(request, "network/create.html")
    else:
        return redirect('index')


@csrf_exempt
@login_required
def save(request):
    if request.user.username:
        if request.method == "POST":
            blog = Post()
            blog.username = request.user
            blog.content = request.POST.get('content')
            blog.likes = 0

            # Verify textarea
            if blog.content == "":
                message = "Content cannot be empty!"
                return render(request, "network/create.html", {
                    "message": message
                })
            else:
                blog.save()
            return redirect('index')
        else:
            return redirect('index')
    else:
        return redirect('index')


def profile(request, uname):
    try:
        userposts = Post.objects.filter(username=uname)
        userposts = userposts.order_by("timestamp").reverse()
        items_count = len(userposts)
        paginator = Paginator(userposts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        userposts = None
    try:
        if Follow.objects.filter(username=uname, follower=request.user.username):
            is_follow = True
        else:
            is_follow = False
    except:
        is_follow = False
    try:
        followerlist = Follow.objects.filter(username=uname)
        followers = followerlist.count()
    except:
        followers = 0
    try:
        followinglist = Follow.objects.filter(follower=uname)
        following = followinglist.count()
    except:
        following = 0
    try:
        likes_list = Like.objects.filter(likedby=request.user.username)
        liked_ids = []
        for l in likes_list:
            liked_ids.append(l.postid)
    except:
        liked_ids = None
    cuser = []
    cuser.append(request.user.username)
    return render(request, 'network/profile.html',
                  {
                      'items_count': items_count,
                      'page_obj': page_obj,
                      'profilename': uname,
                      'isfollow': is_follow,
                      "followers": followers,
                      "following": following,
                      "liked_ids": liked_ids,
                      "cuser": cuser
                  })


@csrf_exempt
@login_required
def follow(request, name):
    try:
        flist = Follow.objects.get(
            username=name, follower=request.user.username)
    except:
        flist = Follow()
        flist.username = name
        flist.follower = request.user.username
        flist.save()
    return redirect('profile', uname=name)


@csrf_exempt
@login_required
def unfollow(request, name):
    try:
        flist = Follow.objects.get(
            username=name, follower=request.user.username)
        flist.delete()
    except:
        return redirect('profile', uname=name)
    return redirect('profile', uname=name)


@login_required
def following(request):
    try:
        following = Follow.objects.filter(follower=request.user.username)
        item = []
        items = []
        funames = []
        for f in following:
            funames.append(f.username)
        for f in funames:
            bpost = Post.objects.filter(username=f)
            bpost = bpost.order_by("-timestamp").all()
            items.append(bpost)
        for n in range(0, len(items)):
            item.extend(items[n])

        paginator = Paginator(item, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = None

    try:
        likes_list = Like.objects.filter(likedby=request.user.username)
        liked_ids = []
        for l in likes_list:
            liked_ids.append(l.postid)
    except:
        liked_ids = None
    cuser = []
    cuser.append(request.user.username)
    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "liked_ids": liked_ids,
        "cuser": cuser
    })


@csrf_exempt
@login_required
def followapi(request, name):
    try:
        if User.objects.get(username=name):
            try:
                followerlist = Follow.objects.filter(username=name)
                followers = followerlist.count()
            except:
                followers = 0
            try:
                followinglist = Follow.objects.filter(follower=name)
                following = followinglist.count()
            except:
                following = 0
            try:
                if Follow.objects.filter(username=name, follower=request.user.username):
                    is_follow = True
                else:
                    is_follow = False
            except:
                is_follow = False

    except:
        return JsonResponse({"error": "No such user found"}, status=404)

    if request.method == "GET":
        return JsonResponse({"user": name, "followers": followers, "following": following, "is_follow": is_follow})
    else:
        return JsonResponse({"error": "INVALID ACCESS"}, status=404)


@csrf_exempt
@login_required
def likesapi(request, postid):
    if request.method == "GET":
        try:
            postlike = Like.objects.get(
                postid=postid, likedby=request.user.username)
            return JsonResponse(postlike.serialize())
        except Like.DoesNotExist:
            return JsonResponse({"error": "No like activity found"}, status=404)
    elif request.method == "POST":
        data = json.loads(request.body)
        if request.user.username == data.get("likedby"):
            likerow = Like()
            likerow.postid = data.get("id")
            likerow.likedby = data.get("likedby")
            likerow.likes = data.get("likes")
            blikes = Post.objects.get(id=data.get("id"))
            blikes.likes = data.get("likes")
            blikes.save()
            likerow.save()
            return JsonResponse({"message": "Success!!!", "status": 201}, status=201)
        else:
            return JsonResponse({"error": "INVALID ACCESS"}, status=404)
    elif request.method == "DELETE":
        data = json.loads(request.body)
        if request.user.username == data.get("unlikedby"):
            likerow = Like.objects.get(postid=data.get(
                "id"), likedby=data.get("unlikedby"))
            likerow.delete()
            blikes = Post.objects.get(id=data.get("id"))
            blikes.likes = data.get("likes")
            blikes.save()
            return JsonResponse({"message": "Unlike successful", "status": 201}, status=201)
    else:
        return JsonResponse({"error": "Try GET request"}, status=404)


@csrf_exempt
def postapi(request, postid):
    try:
        blog = Post.objects.get(id=postid)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "GET":
        return JsonResponse(blog.serialize())
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("username") == request.user.username:
            if data.get("content") is not None:
                blog.content = data["content"]
        else:
            return JsonResponse({"error": "INVALID ACCESS"}, status=404)
        blog.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "Try using GET request"}, status=404)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
