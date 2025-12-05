IMAGE := jdccabanga-test
REGISTRY := ghcr.io/henrardb/jdccabanga
PY := python3
ENVFILE := ./cabanga.env

run:
	set -a; . $(ENVFILE); set +a; \
	$(PY) -m jdccabanga.main

docker-build:
	sudo docker build --load -t $(IMAGE) .

docker-run:
	sudo docker run --rm --env-file $(ENVFILE) $(IMAGE)

k8s-job:
	kubectl -n jdccabanga create job test-$(shell date +%H%M%S) --from=cronjob/jdccabanga

k8s-logs:
	kubectl -n jdccabanga logs -f job/test*

clean:
	rm -rf __pycache__ .pytest_cache
