.PHONY: test gui-test docs package desktop-build api

test:
	docker compose run --rm test

gui-test:
	docker compose run --rm gui-test

docs:
	docker compose run --rm docs

package:
	docker compose run --rm package

desktop-build:
	docker compose run --rm desktop-build

api:
	docker compose up api
