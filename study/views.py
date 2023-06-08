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
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginPage(View):
    
    def get(self,request):

        # There is a single page for login and registration
        # variable "page" help django template to display login part
        # for LoginPage class.
        page ='login'
        context= {'page':page}
        return render(request, 'study/login_register.html', context)
    
    def post(self,request):
        page ='login'

        # stop user from accessing login url if already loggedIn
        if request.user.is_authenticated:
            return redirect('home')

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

class RegisterPage(View):
    def get(self,request):
        # There is a single page for login and registration
        # variable "register" help django template to display registeration part
        # for RegisterPage class.
        page = 'register'
        form = UserCreationForm()
        context ={'page':page, 'form': form}
        return render(request, 'study/login_register.html', context) 
    
    def post(self,request):
        page = 'register'
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

class LogoutUser(View):
    def get(self,request):
        logout(request)
        return redirect('home')

class Home(View):
    def get(self,request):

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

        topics = Topic.objects.all()[0:5]
        room_count = rooms.count()
        room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:4]

        context = {'rooms':rooms, 
        'topics':topics, 
        'room_count':room_count, 
        'room_messages':room_messages}
        return render(request, 'study/home.html', context)

class GetRoom(View):
    def get(self,request,pk):
        room = Room.objects.get(id=pk)
        # using the child element of room and importing set of all messages
        room_messages = room.message_set.all().order_by('-created')
        participants = room.participants.all()

        context = {'room': room, 'room_messages': room_messages, 'participants':participants}
        return render(request, 'study/room.html', context)

    def post(self,request,pk):
        room = Room.objects.get(id=pk)
        
        message = Message.objects.create(
            user =  request.user,
            room = room,
            body  = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
       
class UserProfile(View):
    def get(self,request,pk):
        user = User.objects.get(id=pk)
        rooms= user.room_set.all()
        room_message = user.message_set.all()
        topics = Topic.objects.all()
        context = {'user':user, 'rooms': rooms, 'room_message':room_message,'topics':topics}
        return render(request, 'study/profile.html', context) 

class CreateRoom(LoginRequiredMixin,View):
    login_url='login'
    def get(self,request):
        form =  RoomForm()
        topics = Topic.objects.all()
        context = {'form': form, 'topics':topics} 
        return render(request, 'study/room_form.html', context)
    
    def post(self,request):
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic= topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')

class UpdateRoom(LoginRequiredMixin,View):
    login_url='login'
    def get(self,request,pk):
        room = Room.objects.get(id=pk)
        topics = Topic.objects.all()
        form = RoomForm(instance = room)

        if request.user != room.host:
            return HttpResponse('You are not the room host')
        context ={'form': form, 'topics':topics, 'room': room}
        return render(request, 'study/room_form.html', context)

    def post(self,request,pk):
        room = Room.objects.get(id=pk)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST, instance = room)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
class DeleteRoom(LoginRequiredMixin,View):
    login_url='login'
    def get(self,request,pk):
        room = Room.objects.get(id=pk)
        if request.user != room.host:
            return HttpResponse(' You are not allowed here')
        context = {'obj': room}
        return render(request, 'study/delete.html', context)
    
    def post(self,request,pk):
        room = Room.objects.get(id=pk)
        room.delete()
        return redirect('home')
    
class DeleteMessage(LoginRequiredMixin,View):
    login_url='login'

    def get(self,request,pk):
        try:
            message = Message.objects.get(id=pk)
            if request.user != message.user:
                return HttpResponse(' You have to login first')
            context = {'obj': message}
            return render(request, 'study/delete.html', context)
        except:
            return HttpResponse('Message does not exist')
    
    def post(self,request,pk):
        message = Message.objects.get(id=pk)
        message.delete()
        return redirect('home')

class UpdateUser(LoginRequiredMixin,View):
    login_url='login'
    def get(self,request):
        user = request.user
        form =  UserForm(instance = request.user)
        context = {'form':form}
        return render(request, 'study/update-user.html', context)

    def post(self,request):
        user = request.user
        form =UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk= user.id)
        
class TopicsPage(View):
    def get(self,request):
        q = request.GET.get('q') if request.GET.get('q') !=None else ''
        topics = Topic.objects.filter(name__icontains=q)
        context = {'topics':topics}
        return render(request, 'study/topics.html',context)
    
class ActivityPage(View):
    def get(self,request):
        room_messages = Message.objects.all()[0:2]
        context = {'room_messages':room_messages}
        return render(request, 'study/activity.html',context)
    