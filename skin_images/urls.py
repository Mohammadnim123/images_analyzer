from rest_framework.routers import DefaultRouter
from .views import SkinImagesAnalyzerView


api_router = DefaultRouter()
api_router.register('', SkinImagesAnalyzerView, basename='')
urlpatterns = api_router.urls