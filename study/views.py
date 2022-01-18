from django.shortcuts import render,redirect
from .models import Room,Topic,Message

from .forms import RoomForm



def home(request):
    # Set q ='' if it is none 
    q = request.GET.get('q') if request.GET.get('q') !=None else ''
    # filter topic->name-> that contains-> q string partially or fully
    # i stands for case insensitivity
    # Now when q=''or None then empty string match with all the topic name
    # so that filter return all the room objects
    rooms= Room.objects.filter(topic__name__icontains=q)

    topics = Topic.objects.all()

    context = {'rooms':rooms, 'topics':topics}
    return render(request, 'study/home.html', context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'study/room.html', context)


def createRoom(request):
    form =  RoomForm()
    if request.method=='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form} 
    return render(request, 'study/room_form.html', context)


def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    if request.method =="POST":
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context ={'form': form}
    return render(request, 'study/room_form.html', context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'study/delete.html', context)