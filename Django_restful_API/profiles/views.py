import base64
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post, LikePost
from profiles.models import Profile
from profiles.serializers import ProfileSerializer, UserSerializer
from posts.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


# user authenticated profile
class ProfileApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_object = request.user
        user_serializer = UserSerializer(user_object)
        user_profile = get_object_or_404(Profile, user=user_object)
        user_profile_serializer = ProfileSerializer(user_profile)
        data = {
            "user_profile": user_profile_serializer.data,
            "user_object": user_serializer.data
        }

        if data:
            return Response({"data": data},
                            status=status.HTTP_200_OK
                            )


# slug profile
class ProfileDetailApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug):
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        profile_slug = Profile.objects.get(slug=slug)
        profile_slug_serializer = ProfileSerializer(profile_slug)
        user_slug = User.objects.get(id=profile_slug.user_id)
        user_slug_serializer = UserSerializer(user_slug)
        post_slug = Post.objects.filter(user=user_slug.username)
        post_slug_serializer = PostSerializer(post_slug, many=True)
        liked_post = LikePost.objects.filter(username=user_slug.username)
        post_ids = [like.post_id for like in liked_post]
        post_liked = Post.objects.filter(id__in=post_ids)
        post_liked_serializer = PostSerializer(post_liked, many=True)

        context = {
            "profiledetail": profile_slug_serializer.data,
            "posts": post_slug_serializer.data,
            "postliked": post_liked_serializer.data,
            "users": users_serializer.data,
            "user_profile": user_slug_serializer.data
        }

        if context:
            return Response({"context": context},
                            status=status.HTTP_200_OK
                            )


# setting authenticated profile
class ProfileSettingApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_object = request.user
        user_profile = get_object_or_404(Profile, user=user_object)
        user_profile_serializer = ProfileSerializer(user_profile)
        data = {
            "profile": user_profile_serializer.data
        }

        return Response({"data": data},
                        status=status.HTTP_200_OK
                        )

    def put(self, request):
        user_object = request.user
        user_profile = get_object_or_404(Profile, user=user_object)

        if request.data.get('profileImage_name') is None:
            job = request.data.get('job_name')
            location = request.data.get('location_name')

            if job or location:
                user_profile.job = job
                user_profile.location = location
                user_profile.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid inputs"},
                                status=status.HTTP_400_BAD_REQUEST
                                )

        elif request.data.get('profileImage_name'):
            # Resim verisi JSON formatında geliyor, bu nedenle base64 decode ediyoruz
            image_data = request.data.get('profileImage_name')
            image_data = image_data.encode('utf-8')
            decoded_image_data = base64.decodebytes(image_data)
            # Dosya adını ve uzantısını ayarlayın
            file_name = 'image.png'
            # Resmi dosyaya yazın
            image = ContentFile(decoded_image_data, name=file_name)

            job = request.data.get('job_name')
            location = request.data.get('location_name')

            user_profile.profile_img = image
            user_profile.job = job
            user_profile.location = location
            user_profile.save()
            return Response(status=status.HTTP_200_OK)


class ProfileSearchApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        query = request.data.get('profile_s', '')

        if query:
            user_results = User.objects.filter(first_name__istartswith=query)
        else:
            user_results = []

        profile_results = []
        for user in user_results:
            profile = Profile.objects.filter(user=user).first()
            if profile:
                profile_results.append(profile)

        profile_serializer = ProfileSerializer(profile_results, many=True)
        return Response(profile_serializer.data,
                        status=status.HTTP_200_OK
                        )
