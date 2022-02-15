#django imports
from django.urls import path, include

#3rd imports
from rest_framework.routers import DefaultRouter

#my imports
from veiculo.api.veiculo import VeiculoViewSet
from veiculo.api.marca import MarcaViewSet
from .views import index

router = DefaultRouter()
router.register(r'veiculo', VeiculoViewSet)
router.register(r'marca', MarcaViewSet) 
 
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", index),
    path('', include(router.urls)),
] 