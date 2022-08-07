#docker-compose -w /api_yamdb up -d --build;
docker-compose --project-directory ./infra up -d --build
sleep 1
docker-compose --project-directory ./infra exec web python manage.py migrate;

sleep 1
docker-compose --project-directory ./infra exec web python manage.py createsuperuser --noinput --email admin@admin.ru --username admin

sleep 1
docker-compose --project-directory ./infra exec web python manage.py collectstatic --no-input;
#admin@admin.ru
#BaX-xDs-JpD-q5Q