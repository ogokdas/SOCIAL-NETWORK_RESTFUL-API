from requests import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from categories.models import Category
from profiles.models import Profile
from profiles.serializers import ProfileSerializer, UserSerializer
from categories.serializers import CategorySerializer
from posts.serializers import PostSerializer
from django.contrib.auth.models import User


# categories and counts
class CategoriesApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        category_counts = {}
        for c in category:
            count = c.post.count()
            category_counts[str(c.id)] = count

        category_serializer = CategorySerializer(category, many=True)
        data = {
            "categories": category_serializer.data,
            "category_counts": category_counts,
        }

        if category_serializer:
            return Response({"data": data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


# category and posts
class CategoryApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug):
        username = request.user.username
        user = User.objects.get(username=username)
        serialized_user = UserSerializer(user)
        user_profile = Profile.objects.get(user=user)
        category = get_object_or_404(Category, slug=slug)
        posts = Category.objects.get(slug=slug).post.all()
        profile_all = Profile.objects.all()
        profile_all_serializer = ProfileSerializer(profile_all, many=True)

        category_serializer = CategorySerializer(category)
        posts_serializer = PostSerializer(posts, many=True)
        user_profile_serializer = ProfileSerializer(user_profile)
        count = category.post.count()

        data = {
            "user": serialized_user.data,
            "count": count,
            "kategoriler": category_serializer.data,
            "posts": posts_serializer.data,
            "profile__": user_profile_serializer.data,
            "profile": profile_all_serializer.data
        }

        if data:
            return Response({'data': data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Records Found"},
                            status=status.HTTP_404_NOT_FOUND)