Para gerar os models direto da base de dados que criamos no servidor usar a linha de comando:

Instalar dependencias com PIP:
pip install -r requirements.txt

pip install flask-sqlacodegen
em src/webapi rodar:
sqlacodegen mysql://root:root@localhost:3306/rivvals > model/models_new.py