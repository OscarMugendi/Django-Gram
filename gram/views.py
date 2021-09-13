import os
import json
from decouple import config, Csv
from django.db.models import Sum, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.templatetags.static import static
from django.http  import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
import datetime as dt
from django.http  import Http404
from . models import Image ,Profile, Like, Follow, Comment
from django.contrib.auth.decorators import login_required
from . forms import ImageForm, CommentForm, ProfileUpdateForm,UpdateCaption
from django.template.defaulttags import register


# Create your views here.

@login_required(login_url='/accounts/login/')
def timeline(request):
    date = dt.date.today()
    current_user = request.user 
    followed_people= []
    user_images =[]
    following  = Follow.objects.filter(follower = current_user)
    is_following = Follow.objects.filter(follower = current_user).count()
    try:

        if is_following != 0:

            for following_object in following:
                image_set = Profile.objects.filter(id = following_object.user.id)

                for item in image_set:
                    followed_people.append(item)

            for followed_profile in followed_people:
                post = Image.objects.filter(user_key = followed_profile.user)

                for item in post:
                    user_images.append(item)
                    images= list(reversed(user_images))  

            return render(request, 'timeline.html',{"date":date})
    except:

        raise Http404

    return render(request, 'timeline.html') 
    


@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'name' in request.GET and request.GET["name"]: 

        search_name = request.GET.get("name")
        users_found = Profile.find_profile(search_name)
        message =f"{search_name}" 

        return render(request,'search_results.html',{"message":message,"users_found":users_found})
    else:

        message = "Please enter a valid username"

    return render(request,'search_results.html',{"message":message})



@login_required(login_url='/accounts/login/')
def single_user(request,id):
    try:
        user = Profile.objects.get(id=id)

    except:

        raise Http404()

    return render(request,'profile.html',{"user":user,"single_user":single_user})



@login_required(login_url='/accounts/login/')
def single_image(request,image_id): 
    try:

        image = Image.objects.get(id= image_id)
    except:

        raise Http404()

    return render(request, 'image.html',{"image":image})



@login_required(login_url='/accounts/login/')
def post(request):
    current_user = request.user

    if request.method == 'POST':

        form = ImageForm(request.POST ,request.FILES)

        if form.is_valid():
            image = form.save(commit = False)
            image.user_key = current_user
            image.likes +=0
            image.save() 

            return redirect(timeline)
    else:

        form = ImageForm() 

    return render(request, 'post.html',{"form":form}) 



@login_required(login_url='/accounts/login/')
def comment(request, image_id):
    comments = Comment.objects.filter(image_id=image_id)
    current_image = Image.objects.get(id=image_id)
    current_user = request.user

    if request.method == 'POST':

        form = CommentForm(request.POST)
        logger_in = request.user
        

        if form.is_valid():
            comment = form.save(commit = False)
            comment.user_id= current_user
            comment.image_id = current_image
            current_image.comments_number+=1
            current_image.save_image()
            comment.save()

            return redirect(timeline)

    else:

        form = CommentForm()

    return render(request,'comment.html',{"form":form,"comments":comments})  



@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user = request.user 
    title = 'Update Profile'
    try:

        requested_profile = Profile.objects.get(user_id = current_user.id)
        if request.method == 'POST':

            form = ProfileUpdateForm(request.POST,request.FILES)

            if form.is_valid():
                requested_profile.profile_photo = form.cleaned_data['profile_photo']
                requested_profile.bio = form.cleaned_data['bio']
                requested_profile.username = form.cleaned_data['username']
                requested_profile.save_profile()

                return redirect(profile)
        else:
            
            form = ProfileUpdateForm()
    except:

        if request.method == 'POST':

            form = ProfileUpdateForm(request.POST,request.FILES)

            if form.is_valid():

                new_profile = Profile(profile_photo= form.cleaned_data['profile_photo'],bio = form.cleaned_data['bio'],username = form.cleaned_data['username'],user = current_user)
                new_profile.save_profile()

                return redirect(profile)

        else:

            form = ProfileUpdateForm()

    return render(request,'updateProfile.html',{"title":title,"current_user":current_user,"form":form})



@login_required(login_url='/accounts/login/')
def profile(request):
    title = 'Profile'
    current_user = request.user
    try:

        profile = Profile.objects.get(user_id = current_user)
        following = Follow.objects.filter(follower = current_user)
        followers = Follow.objects.filter(user = profile) 
        
    except:

        profile = Profile.objects.get(username = 'default_user')
        following = Follow.objects.filter(follower = current_user)
        followers = Follow.objects.filter(user = profile)

    return render(request, 'profile.html',{"profile":profile,"current_user":current_user,"following":following,"followers":followers})



@login_required(login_url='/accounts/login/')
def update_image(request,image_id):
    image = Image.objects.get(id = image_id)

    current_user = request.user
    update_image = Image.objects.get(id= image_id)

    if request.method == 'POST':
        form = UpdateCaption(request.POST)
        if form.is_valid():
            new_caption = form.cleaned_data['caption']
            update_image.caption = new_caption
            update_image.save_image() 

            return redirect( more ,image_id)
    else:

        form = UpdateImageCaption()

    return render(request,'update_image.html',{"image":image,"form":form}) 



@login_required(login_url='/accounts/login/')
def view_profiles(request):
    all_profiles = Profile.objects.all()

    return render(request,'all_profiles.html',{"all_profiles":all_profiles}) 



@login_required(login_url='/accounts/login/')
def follow(request,profile_id):
    current_user = request.user
    requested_profile = Profile.objects.get(id = profile_id)
    is_following = Follow.objects.filter(follower = current_user,user = requested_profile).count()
    follow_object = Follow.objects.filter(follower = current_user,user = requested_profile)

    if is_following == 0:

        follower = Follow(follower = current_user,user = requested_profile)
        follower.save() 

        return redirect(viewProfiles)

    else:

        follow_object.delete()

        return redirect(viewProfiles)



@login_required(login_url='/accounts/login/')
def like(request,image_id):
    requested_image = Image.objects.get(id = image_id)
    current_user = request.user
    if_voted = Like.objects.filter(image = requested_image,user = current_user).count()
    dislike = Like.objects.filter(image = requested_image,user = current_user)
    
    if if_voted==0:

        requested_image.likes +=1
        requested_image.save_image()
        like = Like(user = current_user, image = requested_image )
        like.save_like()

        return redirect(timeline)

    else:

        requested_image.likes -=1
        requested_image.save_image()

        for single_unlike in dislike:

            single_unlike.delete_like()

        return redirect(timeline)
    
    return render(request,'timeline.html')



def home(request):
    return render(request,'home.html')


def welcome(request):
    return render(request,'welcome.html')