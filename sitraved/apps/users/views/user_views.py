from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.utils import IntegrityError
from sitraved.apps.users.models.user import User
from sitraved.apps.users.serializers.user_serializers import UserLoginSerializer, UserModelSerializer, \
    UserRegisterSerializer
from sitraved.apps.users.utils import generate_response_with_tokens


class UserViewSet(viewsets.GenericViewSet):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer

    @action(detail=False, methods=['GET'])
    def current(self, request):
        if request.user.is_authenticated:
            return generate_response_with_tokens(request.user)
        return Response(status=status.HTTP_404_NOT_FOUND)

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
        try:
            user_model = serializer.save()
        except IntegrityError as exception:
            if 'username' in str(exception):
                message = 'An user with that username already exists.'
            elif 'email' in str(exception):
                message = 'An user with that email already exists.'
            else:
                message = 'Unexpected error'
            return Response({'success': False, 'message': message},
                            status=status.HTTP_400_BAD_REQUEST)
        return generate_response_with_tokens(user_model)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        if request.user.is_authenticated:
            response = Response(status=status.HTTP_200_OK)
            response.delete_cookie("refresh")
            return response
        return Response(status=status.HTTP_400_BAD_REQUEST)
