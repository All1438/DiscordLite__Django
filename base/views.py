from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q
from django.contrib import messages
#from django.contrib.auth.models import User # User par defaut
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm

"""
rooms = [
    {'id': 1, 'name': "ReactJs"},
    {'id': 2, 'name': "Django"},
    {'id': 3, 'name': "PostgreSQL"}
]
"""
"""
def home(request):
    return HttpResponse("I'm the Best") #HttpResponse() = Renvoye une réponse Http
"""
def room(request, pk): #pk = la variable utiliser dans le <str: > dans urls.py pour qu'il soit utiliser dans room.html
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created') 
    # .message_set.all() = permet de recuperer tout les objets messages lié a l'objet Room correspondant à l'identifiant pk
    # .order_by() = permet de trier l'affichage par ordre
    # '-' = par ordre decroissant
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = Message.objects.create( # .create() = permet d'enregistrer le message dans la base de données 
            user=request.user, # request.user = l'utilisateur connecté qui a envoyer la message
            room=room, # la salle de discussion dans laquelle le message est envoyé
            body=request.POST.get('body') # recupère le contenue du message à partir du name
        )
        room.participants.add(request.user) # .add() = permet d'ajouter l'utilisateur connecté dans le ManyToManyField apres l'envoye
        return redirect('room', pk=room.id) # redirect avec pk
    
    context = {'room': room, 'room_messages': room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # sinon la valeur de q sera '' mais pas None
    # recupère la valeur d"un paramètre nommé 'q', dans href='?q=' et renvoye None si q n'existe pas
    # request.GET. = permet de recupérer les argument passé par en paramètre de la requète GET
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | # | = signifie OU logigique
                                Q(name__icontains=q) | # Q = permet de créer des condition complexes dans un requète 'filter()' ou 'exclude()' 
                                Q(description__icontains=q)) 
    #.filter() = pour filtrer les objets de la class Room, seulement les valeurs de la topic__name=q
    # __ = est une operateur de liaison
    # icontains = est utilisé pour rechercher des résultats et la recherche est insensible a la casse
    topics = Topic.objects.all()[0:5] #permet de recuperer tout les données dans la class Room dans models
    # topic = Room.objects.get(id=pk) # permet de recuperer seulement les données correspondant par get (seulement les 3 première id)
    # [0:5] = la boucle ou l'affichage sera limité a 5 premiers
    rooms_count = rooms.count() # .count() = permet de compter les rooms 
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'rooms_count': rooms_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context) #render(render, 'fichier a partir du template', {variable}) = permet de relier au fichier de templates

@login_required(login_url='/login') # utilisé au dessus d'une vue
# @login_required(login_url='url') signifie que seul les utilisateurs connectés peuvent accéder a cette vue. les non connecté sera redigé vers la page spécifié par login_url
def createRoom(request): # request = qui contient les information de la requête HTTP (les champs)
    form = RoomForm() # insertion des champ dans le model (initialement  vide)
    topics = Topic.objects.all()
    
    if request.method == 'POST': # permet de dire que si on envoye le Submit
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name) # .get_or_create(nom_var=parmètre) = permet de recupérer un objet Topic existant avec un certain nom (name) ou créer un s'il n'existe pas encore dans la BD
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        ) #topic_name or form
        #form = RoomForm(request.POST) # request.POST = permet de dire que les données sont envoyées au serveur
        #if form.is_valid(): # .is_valid() = si le formulaire est valide (submit)
            #room = form.save(commit=False) # .save() = enregistrer les données du formulaire
            #room.host = request.user
            #room.save()
        return redirect('home') # redirect('nom_function') = permet de rediriger l'utilisateur vers la function définie 
    
    context = {'form': form, 'topics': topics}
    return render(request,'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) #instance=room = les champs du formulaire sera pré-remplis avec les valeurs de l'instances de modèles 'room'
    topics = Topic.objects.all()
    
    if request.user != room.host: # si l'user connecté est différent de l'user dans .objects.get() alors
        return HttpResponse("You are not allowed here!!")
        
    if request.method == 'POST':
        #form = RoomForm(request.POST, instance=room)
        #if form.is_valid():
            #form.save
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.method == 'POST':
        room.delete() # delete() = supprimer les données désigner du formulaire
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': room}) # {'obj': room} = permet d'afficher le Name dans room

@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user: # si l'utilisateur connecter est different de l'utilisateur dans la Base de données
        return HttpResponse("You are not allowed here!!")
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() # .room_set.all() = permet de renvoyer tout les objets Room qui sont lié a l'objects User
    room_messages = user.message_set.all()
    topics = Topic.objects.all() # topic et user n'est pas connectè alors on le récupère comme ça
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('create-room')
    
    if request.method == 'POST':
        email = request.POST.get('email')#.lower() # request.POST.get('name') = permet de prendre la valeur du champ qui porte le name de username après submit
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email) # si la valeur a username dans le champ n'est pas egal a username existe
        except: # alors
            messages.error(request, 'User does not exist') # permet l'ajout d'un message (a afficher dans un condition)
        user = authenticate(request, email=email, password=password) # authenticate(request, ) = permet de vérifier les information d'identification d'un utilisateur par rapport a la base de données, value None si il y a une information incorrect
        if user is not None: 
            login(request, user) # login(request, ) = permet de connecté l'utilisateur a la session en cours
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')
            
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request) # logout(request) = permet de deconnecté a l'utilisateur connecté
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm() # UserCreationForm() = permet de créer un formulaire d'inscription pour les news utilisateurs
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # crée un objet utilisateur a partir du données de formulaire mais ne l'enregistre pas encore dans la base de données
            user.username = user.username.lower() # .lower = modifie le nom d'utilisateur en minuscule
            user.save() # enregistrer dans la base de données
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An Error reccured during registration')
    
    context = {'form': form}
    return render(request, 'base/login_register.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        # request.POST = permet de récupérer les données du formulaire après submit (il faut inclure l'attribut method="POST")
        # request.FILES = permet de récupérer les fichiers après submit (il faut inclure l'attribut enctype="multipart/form-data")
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    
    context = {'form': form}
    return render(request, 'base/update_user.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})

