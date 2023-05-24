from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from categories.models import Category
from profiles.models import Profile
from posts.models import Post, LikePost
from profiles.serializers import ProfileSerializer, UserSerializer
from categories.serializers import CategorySerializer
from posts.serializers import PostSerializer
from django.contrib.auth.models import User


class HomeApiView(APIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        # Like
        username = request.user.username
        if LikePost.objects.filter(username=username):
            likedPost_ = LikePost.objects.filter(username=username)
            likedPost = likedPost_.values_list('post_id', flat=True).distinct().values('post_id')
        else:
            likedPost = [999, 998, 997]

        ##############

        categories = Category.objects.all()
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        category_counts = {}
        for category in categories:
            count = category.post.count()
            category_counts[str(category.id)] = count

        users = User.objects.all()
        serialized_user = UserSerializer(users, many=True)
        profiles_ = Profile.objects.all()
        profiles_serializer = ProfileSerializer(profiles_, many=True)

        posts = Post.objects.all()
        posts_serializer = PostSerializer(posts, many=True)

        categories_serializer = CategorySerializer(categories, many=True)

        user_profile_serializer = ProfileSerializer(user_profile)
        user_object_serializer = UserSerializer(user_object)

        data = {
            "kategoriler": categories_serializer.data,
            'category_counts': category_counts,
            "post": posts_serializer.data,
            "user_profile": user_profile_serializer.data,
            "users": serialized_user.data,
            "likedPost": likedPost,
            "profiles_": profiles_serializer.data,
            "request_user": user_object_serializer.data
        }

        if data:
            return Response({'data': data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"message": "No records"},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        username = request.user.username
        global users, post_id
        like = request.data.get('like')
        post_id = request.data.get('post_id')

        if post_id:
            post = Post.objects.get(id=post_id)

            if like == '1' or '2' or '3':
                like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

                if like_filter is None:
                    new_like = LikePost.objects.create(post_id=post_id, username=username)
                    new_like.save()
                    post.no_of_likes = post.no_of_likes + 1
                    post.save()

                else:
                    if like_filter:
                        like_filter.delete()
                        post.no_of_likes = post.no_of_likes - 1
                        post.save()
        ##############
        # Profile
        # Search
        query = request.data.get('profile_s')
        if query:
            user_results = User.objects.filter(first_name__istartswith=query)
        else:
            user_results = []

        user_results_serializer = UserSerializer(user_results, many=True)

        profile_results = []
        for user in user_results:
            profile = Profile.objects.filter(user=user).first()
            if profile:
                profile_results.append(profile)

        profile_results_serializer = ProfileSerializer(profile_results, many=True)

        data = {
            "profile_results": profile_results_serializer.data,
            "user_results": user_results_serializer.data
        }
        if data:
            return Response({"data": data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No data"},
                            status=status.HTTP_400_BAD_REQUEST
                            )
        ##############