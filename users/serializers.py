from rest_framework import serializers
from .models import users
from django.db.models import Q # for queries
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import users
from django.core.exceptions import ValidationError
from uuid import uuid4
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    EmailId = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=users.objects.all())]
        )
    UserId = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=users.objects.all())]
        )
    Password = serializers.CharField(max_length=50)

    class Meta:
        model = users
        fields = (
            'UserId',
            'EmailId',
            'Password'
        )


class UserLoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
    UserId = serializers.CharField()
    Password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        # user,email,password validator
        UserId = data.get("UserId", None)
        Password = data.get("Password", None)
        if not UserId and not Password:
            raise ValidationError("Details not entered.")
        user = None
        # if the email has been passed
        if '@' in UserId:
            user = users.objects.filter(
                Q(email=UserId) &
                Q(password=Password)
                ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = users.objects.get(email=UserId)
        else:
            user = users.objects.filter(
                Q(UserId=UserId) &
                Q(Password=Password)
            ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = users.objects.get(UserId=UserId)
        if user.ifLogged:
            raise ValidationError("User already logged in.")
        user.ifLogged = True
        data['token'] = uuid4()
        user.token = data['token']
        user.save()
        return data

    class Meta:
        model = users
        fields = (
            'UserId',
            'Password',
            'token',
        )

        read_only_fields = (
            'token',
        )


class UserLogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        print(token)
        user = None
        try:
            user = users.objects.get(token=token)
            if not user.ifLogged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.ifLogged = False
        user.token = ""
        user.save()
        data['status'] = "User is logged out."
        return data

    class Meta:
        model = users
        fields = (
            'token',
            'status',
        )


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
# class RegistrationSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = users
#         fields=('UserId',
#                 'FirstName',
#                 'LastName',
#                 'EmailId',
#                 'MobileNumber',
#                 'Password')

#         extra_kwargs = {"password": {"write_only": True}}
#         password = self.validated_data["password"]
#         account.set_password(password)
#         account.save()
#         return account
# # class Userserializer(serializers.ModelSerializer):
# #     class Meta:
# #         model=users
# #         fields=('UserId',
# #                 'FirstName',
# #                 'LastName',
# #                 'EmailId',
# #                 'MobileNumber',
# #                 'Password')