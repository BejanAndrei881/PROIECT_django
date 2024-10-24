from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

# app_name = 'retete'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('adauga-reteta/', views.adauga_reteta, name='adauga_reteta'),
    path('vizualizare-retete/', views.vizualizare_retete, name='vizualizare_retete'),
    path('reteta-salvata/', views.retete_salvate, name='reteta_salvata'),
    path('salveaza-reteta/<int:recipe_id>/', views.salveaza_reteta, name='salveaza_reteta'),
    path('retete-salvate/sterge/<int:saved_recipe_id>/', views.sterge_reteta, name='sterge_reteta'),
    path('sterge-reteta-privata/<int:id>/', views.sterge_reteta_privata, name='sterge_reteta_privata'),
    path('retetele-mele/', views.retetele_salvate_si_mele, name='retetele_mele'),
    path('reteta/<int:pk>/', views.detalii_reteta, name='detali_reteta'),
    path('editeaza_reteta/<int:recipe_id>/', views.edita_reteta, name='edita_reteta'),
    path('register/', views.register, name='register'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
