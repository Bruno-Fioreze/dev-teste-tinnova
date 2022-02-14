from xml.parsers.expat import model
from django.db import models

class Veiculo(models.Model):
    id = models.IntegerField(primary_key=True)
    veiculo = models.CharField(max_length=120)
    marca = models.CharField(max_length=100)
    ano = models.IntegerField(blank=False, null=False)
    descricao = models.TextField()
    vendido = models.BooleanField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    