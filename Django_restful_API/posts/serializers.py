from rest_framework import serializers
from .models import Post, LikePost


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = '__all__'
