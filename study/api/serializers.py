# Object of type Room is not JSON serializable
# It serialize the data or convert the python object to json objects


from rest_framework.serializers import ModelSerializer
from study.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'