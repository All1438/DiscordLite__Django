# from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET']) # est un decorators(utiliser avec function) qui indique que cette vue accepte uniquement les requêtes HTTP de type GET
# @api_view(['PUT']) n'accépter que les requêtes HTTP de type PUT. utilisé pour mettre a jour une ressource existant
# @api_view(['DELETE']) et de faire une retourne a une réponse que le message a été supprimer
def getRoutes(request):
    routes = [
        'GET /api', # qui correspond à la racine de l'api
        'GET /api/rooms', # qui renvoye tout les salles dans getRooms
        'GET /api/rooms/:id' # qui renvoye une salle spécifique en fonction de son identifiant id dans getRoom
    ]
    return Response(routes)
   #  return JsonResponse(routes, safe=False) # JsonResponse() = est une Response HTTP qui renvoye de Json
    # safe=False = signifie que les données peut être n'importe quelle objet séréalisable en JSON, si True (les données doit être de type chaine, nombre, liste, dictionnaire) 
    # Response() = renvoye une reponse JSON contenant la liste de route
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all() #  recupère tout les instances de la classe Room
    serializer = RoomSerializer(rooms, many=True)
    # many=True = permet de dire que le serializer doit traiter plusieurs objects a la fois
    return Response(serializer.data) # .data = permet d'accéder aux données sérialisées

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False) # traiter un seul objects a la fois
    return Response(serializer.data)  