from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User # User par defaut

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm): # permet de créer une class de formulaire a partir d'un modèle django
    class Meta:
        model = Room # le nom de la class dans models a spécifié
        fields = '__all__' # les field a recuperer
        exclude = ['host', 'participants'] # les champs du modèles qui ne sont pas inclus dans le formulaire (ignorer et ne seront pas sauvegarder dans la BD)
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
