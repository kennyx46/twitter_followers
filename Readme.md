cd {{ projectDir }}

virtualenv -p python3 {{ tw_env }}

source {{ tw_env}}/bin/activate

cd ./twitter_followers

pip install -r requirements.txt

//please update the settings.py with DEBUG setting, twitter keys, database info

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0.0.0.0:8000