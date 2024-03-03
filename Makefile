dev:
	./manage.py runserver

docker_build:
	docker build -t lms .

docker_start:
	docker run -d --env-file ./docker/env/.env -p 8000:8000 --rm --name lms sergeynaum/HardQode_lms

docker_stop:
	docker stop sergeynaum/HardQode_lms


