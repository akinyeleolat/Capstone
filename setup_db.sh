echo 'CREATING TABLES...'
python manage.py db upgrade

echo 'SEEDING TABLES...'
python manage.py seed