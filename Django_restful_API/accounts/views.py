from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib import auth
from profiles.models import Profile
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication
from profiles.serializers import ProfileSerializer, UserSerializer


class RegisterApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            user_object = User.objects.get(username=request.user.username)
            user_profile = Profile.objects.get(user=user_object)
            user_profile_serializer = ProfileSerializer(user_profile)
            user_object_serializer = UserSerializer(user_object)

            data = {
                "user_profile": user_profile_serializer.data,
                "request_user": user_object_serializer.data
            }

            return Response({'data': data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Records Found"},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        name = request.data.get("name")
        surname = request.data.get("surname")
        password = request.data.get("password")
        repassword = request.data.get("repassword")

        if password != repassword:
            return Response(
                {"error": "password is not matched"},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username is being used"},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email is being used"},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif username and email and name and surname and password and repassword:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=name,
                last_name=surname,
                password=password
            )
            user.save()

            # create a Profile object for the new user
            profile_ = Profile.objects.create(user=user, id_user=user.id)
            profile_serializer = ProfileSerializer(profile_)

            # log user in
            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)

            return Response({'message': 'Profile informations', 'data': profile_serializer.data},
                            status=status.HTTP_201_CREATED
                            )
        else:
            return Response({"message": "inputs not validated"},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({'error': 'username or password is incorrect'},
                            status=status.HTTP_401_UNAUTHORIZED)
        else:
            login(request, user)
            return Response({'message': 'Successfully logged in'},
                            status=status.HTTP_200_OK)


class LogoutApiView(APIView):

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({"message": "Logged out"},
                            status=status.HTTP_200_OK
                            )
        else:
            return Response({"message": "Users who are logged out cannot be logged out"},
                            status=status.HTTP_401_UNAUTHORIZED)