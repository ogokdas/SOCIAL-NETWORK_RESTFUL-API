import base64
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from posts.models import Post, LikePost
from profiles.models import Profile
from profiles.serializers import ProfileSerializer, UserSerializer
from posts.serializers import PostSerializer
from django.contrib.auth.models import User
from categories.models import Category
from categories.serializers import CategorySerializer


class PostApiView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        user = request.user.username

        if request.data.get('image'):
            # Image data comes in JSON format, so we base64 decode it
            image_data = request.data.get('image')
            image_data = image_data.encode('utf-8')
            decoded_image_data = base64.decodebytes(image_data)

            file_name = 'image.png'

            # Write image to file
            image = ContentFile(decoded_image_data, name=file_name)

            caption = request.data.get("Title")
            content = request.data.get("message")
            category = request.data.get("select[]")
            if caption and content and category:
                if Post.objects.filter(caption=caption).exists():
                    return Response(
                        {"error": "Caption has already used"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    new_post = Post.objects.create(user=user, image=image, caption=caption, content=content)
                    for c in category:
                        new_post.categories.add(c)
                    new_post.save()
                    return Response({"message": "The post has been successfully saved"},
                        status=status.HTTP_201_CREATED
                    )
            else:
                return Response({"message": "Invalid inputs"},
                                status=status.HTTP_400_BAD_REQUEST
                                )
        elif request.data.get('image') is None:
            caption = request.data.get("Title")
            content = request.data.get("message")
            category = request.data.get("select[]")
            if caption and content and category:
                if Post.objects.filter(caption=caption).exists():
                    return Response(
                        {"error": "The caption has already used"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    new_post = Post.objects.create(user=user, caption=caption, content=content)
                    for c in category:
                        new_post.categories.add(c)
                    new_post.save()
                    return Response(
                        {"message": "The post has been successfully saved"},
                        status=status.HTTP_201_CREATED
                    )
            else:
                return Response({"message": "Invalid inputs"},
                                status=status.HTTP_400_BAD_REQUEST
                                )

    def get(self, request):
        category = Category.objects.all()
        category_seralizer = CategorySerializer(category, many=True)
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            user_profile = Profile.objects.get(user=user_object)
            user_profile_serializer = ProfileSerializer(user_profile)
            user_object_serializer = UserSerializer(user_object)

            data = {
                "user_profile": user_profile_serializer.data,
                "request_user": user_object_serializer.data,
                "category": category_seralizer.data
            }

            return Response({'data': data},
                            status=status.HTTP_200_OK)
        else:
            data = {
                "category": category_seralizer.data
            }
            return Response({'data': data},status=status.HTTP_200_OK)


class PostDetailApiView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication]

    def get(self, request, slug):
        user = request.user
        user_serializer = UserSerializer(user)
        post = get_object_or_404(Post, slug=slug)
        user = User.objects.get(username=post.user)
        profile_post = Profile.objects.get(user_id=user.id)
        profile_user = Profile.objects.get(id_user=user.id)

        post_serializer = PostSerializer(post)
        profile_post_serializer = ProfileSerializer(profile_post)
        profile_user_serializer = ProfileSerializer(profile_user)

        data = {
            "post": post_serializer.data,
            "profile_s": profile_post_serializer.data,
            "profile_user": profile_user_serializer.data,
            "user": user_serializer.data
        }
        if data:
            return Response({'data': data},
                            status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LikeApiView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        username = request.user.username
        if LikePost.objects.filter(username=username):
            likedPost_ = LikePost.objects.filter(username=username)
            likedPost = likedPost_.values_list('post_id', flat=True).distinct()
        else:
            likedPost = [999, 998]
        data = {
            "liked_post": likedPost,
        }
        return Response({"data": data},
                        status=status.HTTP_200_OK)

    def post(self, request):
        username = request.user.username
        global users, post_i
        like = request.data.get('like')
        post_id = request.data.get('post_id')

        try:
            post = Post.objects.get(id=post_id)

        except:
            return Response({"message": "inputs not valid"},
                            status=status.HTTP_400_BAD_REQUEST
                            )

        if post and like:
            if like == '1' or like == '2' or like == '3':
                like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

                if like_filter is None:
                    new_like = LikePost.objects.create(post_id=post_id, username=username)
                    new_like.save()
                    post.no_of_likes = post.no_of_likes + 1
                    post.save()
                    return Response({"message": "Like point has been successfully saved"},
                                    status=status.HTTP_201_CREATED
                                    )
                else:
                    if like_filter:
                        like_filter.delete()
                        post.no_of_likes = post.no_of_likes - 1
                        post.save()
                        return Response({"message": "The post has been successfully deleted"},
                                        status=status.HTTP_200_OK
                                        )
            else:
                return Response({"message": "Invalid inputs"},
                                status=status.HTTP_400_BAD_REQUEST
                                )

        else:
            return Response({"message": "Invalid inputs"},
                            status=status.HTTP_400_BAD_REQUEST
                            )


class PostDeleteApiView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication]

    def delete(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        post.delete()
        return Response({"message": "Deleted"},
                        status=status.HTTP_200_OK
                        )