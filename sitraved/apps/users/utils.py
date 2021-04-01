import datetime
import json
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.utils.deprecation import MiddlewareMixin

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

    response.set_cookie("refresh", value=jwt_tokens["refresh_token"],
                        expires=datetime.datetime.now() + datetime.timedelta(days=20),
                        httponly=True)
    return response


class RefreshTokenFromHeaderToBody(MiddlewareMixin):
    """
    djangorestframework-jwt expects the refresh token to be in the request payload.
    However, we generate it as an httpOnly cookie thus the client can not read it to send it as a payload.
    This middleware solves this by extracting the refresh token from the Cookies and adding it to the body payload.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path == '/api/jwt/refresh/' and 'refresh' in request.COOKIES:
            data = json.loads(request.body)
            if data.get('refresh'):
                return None
            data['refresh'] = request.COOKIES['refresh']
            request._body = json.dumps(data).encode('utf-8')
        return None
