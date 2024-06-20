from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

def articles_directory_path(instance, filename):
    return 'articles/{0}'.format(filename)


class CustomUser(AbstractUser):
    dob = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    def __str__(self):
        return self.username


class SkinImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField()


class Articles(models.Model):
    title = models.CharField(max_length=9999)
    body = models.TextField()
    image = models.ImageField(upload_to=articles_directory_path)

    def __str__(self):
        return self.title

