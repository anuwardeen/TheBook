from django.contrib import admin
from .models import *

admin.site.register(Topic)
admin.site.register(AccessLevel)
admin.site.register(Comment)