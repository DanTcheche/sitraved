import datetime

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from sitraved.apps.users.serializers.user_serializers import UserModelSerializer


def generate_jwt_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }


def generate_response_with_tokens(user):
    serialized_user = UserModelSerializer(user).data
    jwt_tokens = generate_jwt_tokens_for_user(user)
    response_dict = {
        "success": True,
        'user': serialized_user,
        'refresh_token': jwt_tokens['refresh_token'],
        'access_token': jwt_tokens['access_token'],
    }

    response = Response(response_dict)

    response.set_cookie("refresh", value=jwt_tokens["refresh"],
                        expires=datetime.datetime.now() + datetime.timedelta(days=20),
                        httponly=True)
    return response
