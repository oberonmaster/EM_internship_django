from rest_framework import serializers
from .models import Video, VideoFile, Like
from django.contrib.auth import get_user_model


User = get_user_model()


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ('id', 'file', 'quality')


class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    files = VideoFileSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = ('id', 'owner', 'name', 'total_likes', 'created_at', 'files')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('video',)

class UserLikeStatSerializer(serializers.Serializer):
    username = serializers.CharField()
    likes_sum = serializers.IntegerField()