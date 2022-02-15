
### Dependências

- Python
- Django
- Django-Rest
- Docker
- Pip


## Passos para executar a aplicação.
Caso esteja utilizando windows troque o python3 por python.

- Execute o seguinte comando:
- sudo docker run -p 3306:3306 --name db_tinnova -e MYSQL_ROOT_PASSWORD=db_tinnova -d mysql:latest
- Conecte-se ao banco de dados utilizando os dados do arquivo .env e crie uma instância chamada db_tinnova, após isso copie o conteúdo do arquivo chamado dump e insira no banco.
- Entre na pasta do projeto.
- Execute o comando python3 -m venv venv
- No caso do linux, ative a venv com source venv/bin/activate
- No caso do windows, ative a venv com venv/Scripts/Activate
- Execute o comando pip install -r requirements.txt
- Execute o comando python manage.py makemigrations
- Execute o comando python manage.py migrate
- Execute o comando python3 manage.py runserver

## End-Points - Veículo :
- End-Point

	> /veiculo/

- Verbo HTTP
	> GET

- Entrada
	 by_pk opcional e termo opcional.
	 
- Saída

        {
			"id": 51,
			"veiculo": "123",
			"marca": "CHEVROLET",
			"ano": 23123,
			"descricao": "222",
			"vendido": false
		}

- End-Point

	> /veiculo/

- Verbo HTTP
	> GET

- Entrada
	 pk obrigatório
	 
- Saída

        {
			"id": 51,
			"veiculo": "123",
			"marca": "CHEVROLET",
			"ano": 23123,
			"descricao": "222",
			"vendido": false
		}


- End-Point

	> /veiculo/

- Verbo HTTP
	> DELETE

- Entrada
	 Pk obrigatório.
	 
- Saída
    	
		{
        	"veiculo.Veiculo": 1
    	}

- End-Point

	> /veiculo/pk/

- Verbo HTTP
	> PÙT E PATCH

- Entrada
	 Pk obrigatório.
	 
- Saída
	
		{
			"message": "Updated",
			"id": "52" 
		}


## Comandos para executar os testes.
	 python3 manage.py test veiculo.tests.TestVeiculo
	 python manage.py test veiculo.tests.VeiculoTest.test_delete_return_200
	 python manage.py test veiculo.tests.VeiculoTest.test_post_sem_marca_retorna_400 
	
## Um pouco sobre a aplicação.
A aplicação foi feita utilizando Python, Django, Django-Rest, Docker e UnitTest.

## Observações
- Algumas da tarefas eu não tive tempo para concluir.
- Os exercício estão em um arquivo chamado exercício.py
- 
