from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .services import SkinImagesAnalyzerService
from .serializers import UserSerializer, SkinImageSerializer, ArticlesSerializer
from .models import SkinImage, Articles

class SkinImagesAnalyzerView(ViewSet):


    @action(['post'], detail=False, permission_classes=[AllowAny])
    def sign_up(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.pop('password')
            hashed_password = make_password(password)
            user = User.objects.create(password=hashed_password, **serializer.validated_data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(['post'], detail=False, permission_classes=[IsAuthenticated])
    def upload_image(self, request):
        image = request.data.get('image') 
        if not image:
            return Response({'error': 'No image provided.'}, status=status.HTTP_400_BAD_REQUEST)

        valid_image_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if image.content_type not in valid_image_types:
            return Response({'error': 'Invalid file type. Only JPG, JPEG, PNG, and GIF images are allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        description = SkinImagesAnalyzerService.analyze_image(image)

        skin_image = SkinImage(user=request.user)
        skin_image.image = image
        skin_image.description = description
        skin_image.save()

        serializer = SkinImageSerializer(skin_image, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(['get'], detail=False, permission_classes=[IsAuthenticated])
    def history(self, request):
        """
        Retrieve a list of skin image analyses for the authenticated user.
        """
        user_images = SkinImage.objects.filter(user=request.user)

        serializer = SkinImageSerializer(user_images, many=True, context={'request': request})
        return Response(serializer.data)


    @action(['get'], detail=False, permission_classes=[AllowAny])
    def articles(self, request):
        articles = Articles.objects.all()
        serializer = ArticlesSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)
