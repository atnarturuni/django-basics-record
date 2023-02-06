from rest_framework import serializers

from web.models import User, TimeSlotTag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlotTag
        fields = ('id', 'title')


class TimeSlotSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    user = UserSerializer()
    tags = TagSerializer(many=True)
