from django.contrib import admin

# Register your models here.
from .models import Trick, Training, Park

admin.site.register(Trick)
admin.site.register(Training)
admin.site.register(Park)