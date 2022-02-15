from django.urls import path, include
from rest_framework.routers import DefaultRouter
from veiculo.api.veiculo import VeiculoViewSet
from .views import index
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'veiculo', VeiculoViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", index),
    path('', include(router.urls)),
] 