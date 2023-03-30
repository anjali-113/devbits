from django.shortcuts import redirect
from rest_framework import generics,permissions,status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import users
from .serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer, ChangePasswordSerializer


class Record(generics.ListCreateAPIView):
    # get method handler
    queryset = users.objects.all()
    serializer_class = UserSerializer


class Login(generics.GenericAPIView):
    # get method handler
    queryset = users.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    queryset = users.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class ChangePasswordAPI(generics.UpdateAPIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = ChangePasswordSerializer
    model = users

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return redirect('/api/login')