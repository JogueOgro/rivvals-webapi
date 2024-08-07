Para rodar o projeto
python run.py

Para gerar os models direto da base de dados que criamos no servidor usar a linha de comando:

pip install sqlacodegen
ou
pip install flask-sqlacodegen
em src/webapi rodar:
sqlacodegen mysql://root:d3st_4ws@rivvals-dev.cpsu0go086lf.sa-east-1.rds.amazonaws.com:3306/rivvals-dev > model/models_new.py

Criar arquivo de dependencias PIP:
pip freeze > requirements.txt

Instalar dependencias com PIP:
pip install -r requirements.txt