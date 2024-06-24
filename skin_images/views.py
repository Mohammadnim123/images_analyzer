from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model
from .services import SkinImagesAnalyzerService
from .serializers import (UserSerializer, SkinImageSerializer, ArticlesSerializer,
                        ChangePasswordSerializer, ChangeEmailSerializer)
from .models import SkinImage, Articles

class SkinImagesAnalyzerView(ViewSet):


    @action(['post'], detail=False, permission_classes=[AllowAny])
    def sign_up(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.pop('password')
            hashed_password = make_password(password)
            user = get_user_model().objects.create(password=hashed_password, **serializer.validated_data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(['get'], detail=False, permission_classes=[IsAuthenticated])
    def user_data(self, request):
        user=request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


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


    @action(['post'], detail=False, permission_classes=[IsAuthenticated])
    def change_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            if not check_password(old_password, user.password):
                return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
            user.password = make_password(new_password)
            user.save()
            return Response({'status': 'Password changed successfully.'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(['post'], detail=False, permission_classes=[IsAuthenticated])
    def change_email(self, request):
        user = request.user
        serializer = ChangeEmailSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            new_email = serializer.validated_data['new_email']
            if not check_password(password, user.password):
                return Response({'error': 'Password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
            user.email = new_email
            user.save()
            return Response({'status': 'Email changed successfully.'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)