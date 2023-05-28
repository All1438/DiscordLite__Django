from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')), #include('chemain_fichier') permet d'iclure le fichier ici(liaison)
    path('api/', include('base.api.urls'))
    # path('', TemplateView.as_view(template_name='index.html'))
        # TemplateView.as_view() = pour afficher une vue basé sur un modèle, affiche directement 'index.html' si il existe
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
# indique a django d'ajouter une nouvelle route qui pointe vers les fichiers media(MEDIA_URL) et de servir ces fichiers en utilisant le chemain absolu spécifié(MEDIA_ROOT)
# Après avoir mis les code MEDIA_URL et MEDIA_ROOT il faut tjrs ajouter ce ligne de code 
