from rest_framework import serializers
from django.contrib.auth import authenticate
from sitraved.apps.users.models.user import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'].lower(), password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid user or password')

        self.context['user'] = user
        return data

    def create(self, unused_data):
        return self.context['user']


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=20)
    password_confirmation = serializers.CharField(min_length=8, max_length=20)

    class Meta:
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirmation': {'write_only': True},
        }

    def validate(self, data):
        password = data['password']
        password_confirmation = data['password_confirmation']
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, data):
        creation_data = {
            'username': data['username'].lower(),
            'email': data['email'].lower(),
            'password': data['password'],
        }
        user = User.objects.create_user(**creation_data)
        return user
