from django.http  import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from study.models import Room
from .serializers import RoomSerializer

# just for testing urls
# def getRoutes(request):
#     routes = [
#         'GET /api',
#         'GET /api/rooms',
#         'GET /api/rooms/:id',

#     ]
#     return JsonResponse(routes, safe=False)

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',

    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    # many means there are more than one objects to serialize
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id= pk)
    # many means there are more than one objects to serialize
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)

# simply with all these, third party cannot access the data. We have to install cors header
# python -m pip install django-cors-headers