# Alugo



![Alugo logo](/statics/images/alugo_home.jpeg)
![Alugo logo](/statics/images/alugo_products.jpeg)


Configuração/Setup

    1 - Em uma pasta, clone o projeto/ In a folder, clone the project: git clone <link do repositório> 

    2 - Crie um ambiente virtual/ Create a virtual environtment: - virtualenv env

    3 - Ative o ambiente virtual/ Activate VirtualENV - ubuntu : source env/bin/activate || windows : . .\env\Scripts\activate

    4 - Rode o requirements-dev.txt/ Run requirements-dev.txt: - pip install -r requirements-dev.txt

    5 - Rode/run: python manage.py makemigrations

    6 - Rode/run: python manage.py migrate

    7 - Para criar um usuario admin/ To create admin user: python manage.py createsuperuser      

    8 - Rode a aplicação/ Run the Application - python manage.py runserver

    
Rodar os Testes unitários/ Run unit tests

    python manage.py test home

    python manage.py test address

    python manage.py test products
