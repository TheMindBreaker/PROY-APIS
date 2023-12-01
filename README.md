# PROY-APIS

python -m venv .env  

.\.env\Scripts\activate

pip install -r requirements.txt

cd apis_pro

python manage.py makemigrations

python manage.py migrate    

python manage.py runserver