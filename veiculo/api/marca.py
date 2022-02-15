#django imports

#3rd imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status as StatusCode

#my imports 
from veiculo.serializers.serializers import MarcaSerializer
from veiculo.models import Marca


class MarcaViewSet(viewsets.ViewSet):
    queryset = Marca.objects
    serializer_class= MarcaSerializer
    
    def list(self, request):
        veiculos = self.queryset.all()
        serializer = self.serializer_class(veiculos, many=True)
        return Response(serializer.data, status=StatusCode.HTTP_200_OK)