from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from web.models import User, TimeSlotTag, TimeSlot


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class TagSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        self.validated_data['user_id'] = self.context['request'].user.id
        return super().save(**kwargs)

    class Meta:
        model = TimeSlotTag
        fields = ('id', 'title')


class TimeSlotSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=TimeSlotTag.objects.all(), many=True, write_only=True)

    def validate(self, attrs):
        if attrs['end_date'] < attrs['start_date']:
            raise ValidationError("Incorrect dates")
        return attrs

    def save(self, **kwargs):
        tags = self.validated_data.pop("tag_ids")
        self.validated_data['user_id'] = self.context['request'].user.id
        instance = super().save(**kwargs)
        instance.tags.set(tags)
        return instance

    class Meta:
        model = TimeSlot
        fields = ('id', 'title', 'start_date', 'end_date', 'tags', 'user', 'tag_ids')
