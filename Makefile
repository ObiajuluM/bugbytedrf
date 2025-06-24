serve:
	python manage.py runserver

mmigrate:
	python manage.py makemigrations

migrate:
	python manage.py migrate

populate:
	python manage.py populate_db

# https://dreampuf.github.io
graph: 
	python manage.py graph_models api > models.dot
