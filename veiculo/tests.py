from django.test import Client
from .models import Veiculo
import unittest
import json

class TestVeiculo(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        
    def test_get_retorna_200(self):
        response = self.client.get("/veiculo/")
        self.assertEqual(response.status_code, 200)
        
    def test_post_retorna_200(self):
        data = {
            "marca":"FORD",
            "descricao": "esté um veículo de teste",
            "veiculo": "Fiesta",
            "ano": 2020,
            "vendido": True
        }
        response = self.client.post("/veiculo/", data)
        
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        id = data_return["id"]
        veiculo = Veiculo.objects.filter(pk=id)
        veiculo.delete()
        self.assertEqual(response.status_code, 200)
    
    def test_post_sem_ano_retorna_400(self):
       
        
        data = {
            "marca":"FORD",
            "descricao": "esté um veículo de teste",
            "veiculo": "Fiesta",
            "ano": '',
            "vendido": True
        }
        response = self.client.post("/veiculo/", data)
        self.assertEqual(response.status_code, 400)
    
    def test_post_sem_marca_retorna_400(self):
        data = {
            "marca":"",
            "descricao": "esté um veículo de teste",
            "veiculo": "Fiesta",
            "ano": 2020,
            "vendido": True
        }
        response = self.client.post("/veiculo/", data)
        self.assertEqual(response.status_code, 400)
        
    
    def test_put_return_200(self):
        data = {
            "marca":"FORD",
            "descricao": "esté um veículo de teste",
            "veiculo": "Fiesta",
            "ano": 2020,
            "vendido": True
        }
        response = self.client.post("/veiculo/", data)
        
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        id = data_return["id"]
        
        response = self.client.patch(f"/veiculo/{id}/", data, content_type='application/json')
        
        veiculo = Veiculo.objects.filter(pk=id)
        veiculo.delete()
        
        self.assertEqual(response.status_code, 200)
        
    def test_patch_return_200(self):
        data = {
            "marca":"FORD",
            "descricao": "esté um veículo de teste",
            "veiculo": "Fiesta",
            "ano": 2020,
        }
        response = self.client.post("/veiculo/", data)
        
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        id = data_return["id"]
        
        response = self.client.patch(f"/veiculo/{id}/", data, content_type='application/json')
        
        veiculo = Veiculo.objects.filter(pk=id)
        veiculo.delete()
        
        self.assertEqual(response.status_code, 200)
        
    def test_patch_return_404(self):
        data = {
            "marca":"FORD",
            "descricao": "esté um veículo de teste",
            "veiculo": "Fiesta",
            "ano": 2020,
        }
        response = self.client.patch(f"/veiculo/{99999999999999}/", data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_put_return_404(self):
        data = {
            "marca":"FORD",
            "descricao": "esté um veículo de teste",
            "veiculo": "Fiesta",
            "ano": 2020,
            "vendido": True
        }
        response = self.client.put(f"/veiculo/{99999999999999}/", data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        
    def test_delete_return_404(self):
        response = self.client.delete(f"/veiculo/{99999999999999}/", content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_delete_return_200(self):
        data = {
            "marca":"FORD",
            "descricao": "esté um veículo de teste",
            "veiculo": "Fiesta",
            "ano": 2020,
        }
        response = self.client.post("/veiculo/", data)
        
        data_return = response.content.decode("utf8")
        data_return = json.loads( data_return )
        id = data_return["id"]
        response = self.client.delete(f"/veiculo/{id}/")
        
        veiculo = Veiculo.objects.filter(pk=id)
        veiculo.delete()
        self.assertEqual(response.status_code, 200)