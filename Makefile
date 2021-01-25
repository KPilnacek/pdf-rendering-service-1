VERSION := 1.0.1

start-dev:
	docker-compose -f local.yml up

stop-dev:
	docker-compose -f local.yml down

django-shell:
	docker-compose -f local.yml run --rm app python manage.py shell

createsuperuser:
	docker-compose -f local.yml run --rm app python manage.py createsuperuser

migrate-db:
	docker-compose -f local.yml run --rm app python manage.py migrate --noinput

test:
	docker-compose -f local.yml run --rm app pytest

check-code-quality:
	pre-commit run --all-files
