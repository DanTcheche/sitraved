from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import logout, login

from sitraved.apps.users.models.user import User
from sitraved.apps.users.serializers.user_serializers import UserLoginSerializer, UserModelSerializer, \
    UserRegisterSerializer
from sitraved.apps.users.utils import generate_response_with_tokens


class UserViewSet(viewsets.GenericViewSet):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer

    @action(detail=False, methods=['POST'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_model = serializer.save()
        return generate_response_with_tokens(user_model)

    @action(detail=False, methods=['POST'])
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_model = serializer.save()
        return generate_response_with_tokens(user_model)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            response = Response(status=status.HTTP_200_OK)
            response.delete_cookie("refresh")
            return response
        return Response(status=status.HTTP_400_BAD_REQUEST)
