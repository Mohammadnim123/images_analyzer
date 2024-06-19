from django.contrib import admin
from.models import Articles, SkinImage
from django.contrib.auth.models import User, Group 


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Articles)