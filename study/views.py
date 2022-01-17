from django.shortcuts import render
from .models import Room



def home(request):
    rooms= Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'study/home.html', context)


def room(request):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'study/room.html', context)