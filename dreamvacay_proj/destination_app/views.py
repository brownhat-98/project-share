from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib import messages
from django.conf import settings

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

import os,requests

from .serializers import *
from .forms import *
from .models import *
from .utils import get_weather_data




# Base URL for API endpoints
API_BASE_URL = f"http://{settings.API_HOST}/api"

#__________________________________________________________DEST_API↓

class add_destination(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = destination_serializer
    permission_classes = [AllowAny]

class view_destination(generics.RetrieveAPIView):
    queryset = Destination.objects.all()
    serializer_class = destination_serializer

class edit_destination(generics.RetrieveUpdateAPIView):
    queryset = Destination.objects.all()
    serializer_class = destination_serializer


class del_destination(generics.DestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = destination_serializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class search_destination(generics.ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = destination_serializer

    def get_queryset(self):
        name=self.kwargs.get('name')
        return self.queryset.filter(name__icontains=name)  
            
#__________________________________________________________DEST_API↑
def base(request):

    context = {
    }
    return render(request, 'base.html', context)

#__________________________________________________________USER_ACCOUNTS↓

def Register_user(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='User')
            user.groups.add(group)
            name = f"{user.first_name} {user.last_name}"
            email = user.email
            UserProfile.objects.create(user=user, name=name, email=email)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
   
    return render(request, 'User/register.html', {'form': form})


def loginUser(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            messages.info(request, 'Username or password is wrong')
            return redirect('login')

    return render(request, 'User/login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('base')

#____________________________________________________________USERPROFILE
@login_required(login_url='login')
def user_details(request):
    userprofile = request.user.userprofile
    context={'userprofile':userprofile}
    return render(request,'User/userprofile.html',context) 

#____________________________________________________________EDITPROFILE
@login_required(login_url='login')
def edit_profile(request):
    userprofile = request.user.userprofile

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')  
    else:
        form = EditProfileForm(instance=userprofile)
    
    context = {'form': form}
    return render(request, 'User/edit_profile.html', context)

#_________________________________________________________USER_ACCOUNTS↑

#_________________________________________________________DESTINATIONS↓

@login_required(login_url='login')
def detail_destination(request, pk):
    response = requests.get(f'{API_BASE_URL}/dest/{pk}/')

    if response.status_code == status.HTTP_200_OK:
        destination = response.json() 
    else:
        destination = None
    
    # if destination:
    #     name = destination['name']
    #     dest = Destination.objects.get(name=name)
    #     images = Dest_Images.objects.filter(destination=dest)
    # else:
    #     destination = None
    #     images = None
    
    weather = get_weather_data(destination['name'])
    context = {
        'destination': destination,
        'weather': weather,
        # 'images':images
    }
    return render(request, 'destination/detail_destination.html', context)


@login_required(login_url='login')
def add_destination_view(request):
    dest_form = DestinationForm()
    # image_form = DestImageForm()

    if request.method == 'POST':
        dest_form = DestinationForm(request.POST, request.FILES)
        # image_form = DestImageForm(request.POST, request.FILES)

        if dest_form.is_valid(): #and image_form.is_valid():
            dest_instance = dest_form.save()

        
            # images = request.FILES.getlist('images')
            # for img in images:
            #     Dest_Images.objects.create(destination=dest_instance, images=img)

            messages.success(request, 'Destination and images were added successfully')
            return redirect('view_dest')
        else:
            messages.error(request, 'Failed to add destination or images. Please check the form.')

    context = {
        'form': dest_form,
        # 'image_form': image_form,
    }

    return render(request, 'destination/add_destination.html', context)

@login_required(login_url='login')
def view_destination_view(request):

    response = requests.get(f'{API_BASE_URL}/dest/')
    if response.status_code == status.HTTP_200_OK:
        destinations = response.json()
    else:
        destinations = []

    context = {
        'destinations': destinations,
    }
    return render(request, 'destination/view_destination.html', context)


@login_required(login_url='login')
def edit_destination_view(request, pk):
    api_url = f'{API_BASE_URL}/dest/{pk}/'
    response = requests.get(api_url)
    
    if response.status_code == status.HTTP_200_OK:
        destination_data = response.json()
        instance = get_object_or_404(Destination, pk=pk)
        
        if request.method == 'POST':
            dest_form = DestinationForm(request.POST, request.FILES, instance=instance)
            
            if dest_form.is_valid():
                dest_form.save()
                messages.success(request, 'Destination was edited successfully')
                return redirect('view_dest')
            else:
                messages.error(request, 'Form is not valid')
        else:
            dest_form = DestinationForm(instance=instance)
    else:
        messages.error(request, 'Destination not found')
        return redirect('view_dest')
    
    context = {
        'form': dest_form
    }
    
    return render(request, 'destination/edit_destination.html', context)


@login_required(login_url='login')
def delete_destination_view(request, pk):
    value = requests.get(f'{API_BASE_URL}/dest/{pk}/')
    if value.status_code == status.HTTP_200_OK:
        destination = value.json()
    else:
        destination = None

    if request.method == 'POST':
        response = requests.delete(f'{API_BASE_URL}/dest/{pk}/delete/')

        if response.status_code == status.HTTP_204_NO_CONTENT:
            messages.success(request, 'Destination was deleted successfully')
        else:
            messages.error(request, 'Failed to delete destination')

        return redirect('view_dest')

    context = {
        'destination_id': pk,
        'destination': destination

    }
    return render(request, 'destination/del_destination.html', context)


@login_required(login_url='login')
def search_destination_view(request):
    if request.method == 'POST':
        search_term = request.POST.get('search_term')
        response = requests.get(f'{API_BASE_URL}/dest/search/{search_term}/')

        if response.status_code == status.HTTP_200_OK:
            destinations = response.json()
        else:
            destinations = []
    else:
        destinations = []

    context = {
        'destinations': destinations
    }
    return render(request, 'search_destination.html', context)

#_________________________________________________________DESTINATIONS↑
