. ./setup.sh
export ENV='test'

export FLASK_DEBUG=False

echo 'DROPPING TABLES... (if any)'
python manage.py db downgrade

echo 'CREATING TABLES...'
python manage.py db upgrade

echo 'SEEDING TABLES...'
python manage.py seed

echo 'RUNNING TEST...'
python test_app.py