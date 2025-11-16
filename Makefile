 .PHONY: run-docker-compose clean-notebook-outputs docker-status docker-logs

docker-status:
	docker compose ps

docker-logs:
	docker compose logs -f

run-docker-compose:
	uv sync
	docker compose up --build

clean-notebook-outputs:
	jupyter nbconvert --clear-output --inplace notebooks/*/*.ipynb

run-evals-retriever:
	uv sync
	PYTHONPATH=${PWD}/src:$$PYTHONPATH:${PWD} uv run --env-file .env python -m evals.eval_retriever