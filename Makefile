APPS:=./api_case ./api ./tests

.PHONY: pretty lint test

pretty:
	black $(APPS)
	isort $(APPS)

lint:
	black $(APPS) --check
	isort $(APPS) --check-only
	ruff check $(APPS)

test:
	coverage run manage.py test ./tests && coverage combine && coverage report && coverage html && coverage erase
