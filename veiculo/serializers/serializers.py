#3rd imports
from rest_framework import serializers

#my imports
from veiculo.models import Veiculo
from .dynamicFields import DynamicFieldsModelSerializer

class VeiculoSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    
    def validate(self, data):
        #if data["ano"] == None:
        #    raise serializers.ValidationError({"ano": "Deposits greater than 2000 are not allowed"})
        return data
    
    class Meta:
        model = Veiculo
        fields = "__all__"