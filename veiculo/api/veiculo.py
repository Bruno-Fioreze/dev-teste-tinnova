#django imports
from django.shortcuts import get_object_or_404,  get_list_or_404
from django.db.models import Q
from datetime import datetime

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
        veiculos = self.queryset.all()
        serializer = self.serializer_class(veiculos, many=True)
        return Response(serializer.data, status=StatusCode.HTTP_200_OK)

    def create(self, request):
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
        termo, by_pk, is_many = kwargs.get("pk", None), request.GET.get("by_pk", None),  True
        fields = {"veiculo", "marca", "ano", "id"}
        if by_pk:
            veiculo = get_object_or_404(self.queryset,  pk=termo)
            is_many = False 
            fields = {"veiculo", "marca", "ano", "id", "vendido", "descricao"}
        elif termo.isdigit() and by_pk == None:
            veiculo = get_list_or_404(self.queryset,  ano=termo)
        else:
            veiculo = get_list_or_404(self.queryset,  marca=termo)
        serializer = self.serializer_class(veiculo, fields=fields, many=is_many)
        return Response(serializer.data, status=StatusCode.HTTP_200_OK)

    def update(self, request, pk=None):
        response, data = {}, {}
        if not self.queryset.filter(pk=pk).exists():
            response = {"message": "Not exists"}
            return Response(response, status=StatusCode.HTTP_404_NOT_FOUND)
        data = dict(request.data)
        data.update({"updated": datetime.now()})
        affected = self.queryset.filter(pk=pk).update(**data)
        response = {"message": "Updated", "id": pk}
        return Response(response, status=StatusCode.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        response, data = {}, {}
        if not self.queryset.filter(pk=pk).exists():
            response = {"message": "Not found"}
            return Response(response, status=StatusCode.HTTP_404_NOT_FOUND)

        data = dict(request.data)
        data.update({"updated": datetime.now()})
        affected = self.queryset.filter(pk=pk).update(**data)
        response = {"message": "Updated", "id": pk}
        return Response(response, status=StatusCode.HTTP_200_OK)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(self.queryset, pk=pk)
        affected = queryset.delete()
        return Response(affected, status=StatusCode.HTTP_200_OK)