dev:
	./manage.py runserver

docker_build:
	docker build -t sergeynaum/hardqodelms .

docker_start:
	docker run -d --env-file ./docker/env/.env -p 8000:8000 --rm --name hardqodelms sergeynaum/hardqodelms

docker_stop:
	docker stop hardqodelms

tests:
	./manage.py test
