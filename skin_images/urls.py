from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import SkinImagesAnalyzerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


api_router = DefaultRouter()
api_router.register('', SkinImagesAnalyzerView, basename='')
urlpatterns = api_router.urls

urlpatterns += [
    path('sign_in/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]