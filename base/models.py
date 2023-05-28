from django.db import models
#from django.contrib.auth.models import User  # permet d'importer User par défaut
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser): # AbstractUser = permet de personaliser le modèle d'utilisateur de base fourni par django
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    # .EmailField() = champ de texte permet de stocker les Email
    # unique=True = indique que chaque adresse email stocké doit être unique
    # null=True = permet a ce champ d'être facultative
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    # .ImageField() = permet de stocké des images
    # default="" = la valeur par défaut de l'image
    
    USERNAME_FIELD = 'email' # indique a Django que l'attribut 'email' doit être utilisé comme nom d'utilisateur a la place du champ "username
    REQUIRED_FIELDS = [] # champ supplémentaire
    
class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    topic = models.ForeignKey(Topic, models.SET_NULL, null=True, blank=True)
    # on_delete=models.SET_NULL, null=True, blank=True = si l'objet réference Topic est supprimé alors la valeur de la clé étrangère Room sera défini null, tjrs définir le null et blank en True pour qu'ils fonctionnent
    # .CharField = permet de stocké des chaine de caractère
    name = models.CharField(max_length=200)
    # max_length = nombre de caracère max
    description = models.TextField(null=True, blank=True)
    # .TextField = permet de stocké des chaines de caractères de type 'Text' et pas besoin de spécifié le max_length
    # blank=True = cela indique que le champ peut être vide ou null (not required)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    # .ManyToManyField() = permet de lier plusieurs instances du modèle User a une instance de Room
    # related_name = permet de définir l'attribut inversé qui permettra a partir de l'instance User d'accéder a tout les instances de Room,  il sera possible d'accéder aux instances de Room via l'attribut participants de l'instance de User
    updated = models.DateTimeField(auto_now=True)
    # .DateTimeField = qui stock la date et l'heur
    # auto_now=True = la valeur du champ sera automatiquement définie a la date et l'heure actuelles
    created = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True = définie la date et l'heur de la creation initiale de l'object

    def __str__(self):  # permet de faire une representation en chaine de caractères de l'objet de modèle dans l'interface d'administration
        return self.name

    class Meta:  # utilisée pour fournir des options suplémentaires au modèle django
        # ici est utilisé pour spécifier l'ordre par défaut des instances de la classe Room
        # trié par ordre décroissant de la date de mis a jour (updated) et en cas d'égalité, par ordre décroissant de la date de création (created)
        ordering = ['-updated', '-created']
        # - = trié par ordre décroissant


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # .Foreignkey() = permet de créer une relation de clé étrangère entre les 2 models
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # on_delete=models.CASCADE = permet de dire que si l'objet réference Room est supprimé alors tout les Message associé a ce Room seront également supprimé
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50] # [0:50] = retourne les 50 premiers caractères de l'attribut 'body'
