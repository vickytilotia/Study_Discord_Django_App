from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic,Message
from django.db.models import Q
from .forms import RoomForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# for django flash messages
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm


def loginPage(request):

    page ='login'

    # stop user from accessing login url if already loggedIn
    if request.user.is_authenticated:
        return redirect('home')


    if request.method=="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user =User.objects.get(username=username)
        except:
            messages.error(request, 'User does NOT exist!!')
        
        user = authenticate(username=username, password =password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does NOT exist!!')



    context= {'page':page}
    return render(request, 'study/login_register.html', context)

def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            # commit =  false, we are freezing the user before saving so that
            # we can access the user values right here

            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during the registration')

    context ={'page':page, 'form': form}
    return render(request, 'study/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    # Set q ='' if it is none 
    q = request.GET.get('q') if request.GET.get('q') !=None else ''
    # filter topic->name-> that contains-> q string partially or fully
    # i stands for case insensitivity
    # Now when q=''or None then empty string match with all the topic name
    # so that filter return all the room objects
    # rooms= Room.objects.filter(topic__name__icontains=q)

    # Now we update it to dynamic search so that it will take otherparameters also
    rooms= Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |     
        Q(description__icontains=q)      
                            )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms':rooms, 
    'topics':topics, 
    'room_count':room_count, 
    'room_messages':room_messages}
    return render(request, 'study/home.html', context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    # using the child element of room and importing set of all messages
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user =  request.user,
            room = room,
            body  = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants':participants}
    return render(request, 'study/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms= user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms': rooms, 'room_message':room_message,'topics':topics}
    return render(request, 'study/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form =  RoomForm()
    topics = Topic.objects.all()
    if request.method=='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic= topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host =request.user 
        #     room.save()
        return redirect('home')

    context = {'form': form, 'topics':topics} 
    return render(request, 'study/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance = room)

    if request.user != room.host:
        return httpResponse('You are not allowed here')

    if request.method =="POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST, instance = room)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context ={'form': form, 'topics':topics, 'room': room}
    return render(request, 'study/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return httpResponse(' You are not allowed here')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'study/delete.html', context)

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return httpResponse(' You are not allowed here')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request, 'study/delete.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form =  UserForm(instance = request.user)

    if request.method == "POST":
        form =UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk= user.id)

    context = {'form':form}
    return render(request, 'study/update-user.html', context)