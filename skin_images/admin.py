from django.contrib import admin
from.models import Articles
from django.contrib.auth.models import Group 


admin.site.unregister(Group)
admin.site.register(Articles)