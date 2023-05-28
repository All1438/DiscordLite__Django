from django.contrib import admin
from .models import Room, Topic, Message, User

# Register your models here.

admin.site.register(User)
# permet d'afficher le models de class Room dans l'administration de Django
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
