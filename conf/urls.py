from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('sitraved.apps.users.urls')),
    path('api/media/', include('sitraved.apps.media_api.urls')),
    path('api/recommendations/', include('sitraved.apps.recommendations.urls')),
    # JWT
    path('api/jwt/create/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/jwt/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
