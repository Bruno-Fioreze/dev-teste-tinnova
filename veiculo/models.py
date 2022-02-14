from xml.parsers.expat import model
from django.db import models
from django.utils.timezone import now

class Veiculo(models.Model):
    id = models.AutoField(primary_key=True)
    veiculo = models.CharField(max_length=120, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=False, null=False)
    ano = models.IntegerField(blank=False, null=False)
    descricao = models.TextField(blank=True, null=True)
    vendido = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(editable=False, default=now, blank=True)
    updated = models.DateTimeField(blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.created = datetime.now()
    #     self.updated = datetime.now()
    #     return super(Veiculo, self).save(*args, **kwargs)
    
    
class Marca(models.Model): 
    id = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=100)