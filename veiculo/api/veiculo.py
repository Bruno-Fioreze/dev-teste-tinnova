#django imports
from django.shortcuts import get_object_or_404,  get_list_or_404
from django.db.models import Q
from datetime import datetime
from django.http import Http404

#3rd imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status as StatusCode
from rest_framework.decorators import action

#my imports 
from veiculo.serializers.serializers import VeiculoSerializer
from veiculo.models import Veiculo

class VeiculoViewSet(viewsets.ViewSet):
    queryset = Veiculo.objects
    serializer_class= VeiculoSerializer
    
    def list(self, request):
        """Método responsável por retornar listas.

        Args:
            termo, e by_termo (str e str):  termo e by_termo são opcionais

        Returns:
            json: lista
        """
        termo, by_termo = request.GET.get('termo', None), request.GET.get('termo', None)
        if termo == None:
            veiculos = self.queryset.all()
        elif termo.isdigit() and by_termo != None:
            veiculos = get_list_or_404(self.queryset,  ano=termo)
        else:
            veiculos = get_list_or_404(self.queryset,  marca=termo) 
        serializer = self.serializer_class(veiculos, fields={"id", "veiculo", "marca", "ano", "descricao", "vendido"}, many=True)
        return Response(serializer.data, status=StatusCode.HTTP_200_OK)

    def create(self, request):
        """Método responsáavel por Criar instância.

        Args:
            Ano e Marca (int e str): obrigatórios.

        Returns:
            json: return um json com os dados do veículo
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True) : 
            serializer.save()
            return Response(
                serializer.data, status=StatusCode.HTTP_200_OK
            )
        return Response(serializer.errors, status=StatusCode.HTTP_400_BAD_REQUEST)

    #z#def retrieve(self, request, pk=None):
    #@action(detail=True, methods=["get"])
    def retrieve(self, request, *args, **kwargs):
        """Método responsável por devolver os dados de uma instância.

        Args:
            pk (int): Obrigatório

        Returns:
            json: retorna um json com os dados.
        """
        termo = kwargs.get("pk", None)
        veiculo = get_object_or_404(self.queryset,  pk=termo)
        fields = {"veiculo", "marca", "ano", "id", "vendido", "descricao"}
        serializer = self.serializer_class(veiculo, fields=fields, many=False)
        return Response(serializer.data, status=StatusCode.HTTP_200_OK)

    def update(self, request, pk=None):
        """Método responsável por atualizar completamente a instância.

        Args:
            pk (int): Obrigatório

        Returns:
            json: Retorna um json com o id e uma mensagem
        """
        response, data = {}, {}
        if not self.queryset.filter(pk=pk).exists():
            response = {"message": "Not exists"}
            return Response(response, status=404)
        data = dict(request.data)
        data.update({"updated": datetime.now()})
        affected = self.queryset.filter(pk=pk).update(**data)
        response = {"message": "Updated", "id": pk}
        return Response(response, status=StatusCode.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        """Método responsável por atualizar parcialmente a instância.

        Args:
            pk (int): Obrigatório

        Returns:
            json: Retorna um json com o id e uma mensagem
        """
        response, data = {}, {}
        if not self.queryset.filter(pk=pk).exists():
            response = {"message": "Not found"}
            return Response(response, status=404)

        data = dict(request.data)
        data.update({"updated": datetime.now()})
        affected = self.queryset.filter(pk=pk).update(**data)
        response = {"message": "Updated", "id": pk}
        return Response(response, status=StatusCode.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Método responsável por deletar a instância.

        Args:
            pk (int): Obrigatório

        Returns:
            json: retorna um json com o pk
        """
        queryset = get_object_or_404(self.queryset, pk=pk)
        affected = queryset.delete()
        return Response(affected, status=StatusCode.HTTP_200_OK)