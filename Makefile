.PHONY: install test lint typecheck format docs doctor examples clean

install:
	pdm sync -G dev -G docs

test:
	pdm run pytest

lint:
	pdm run ruff check .

format:
	pdm run ruff format .

typecheck:
	pdm run mypy src/ultilog

docs:
	pdm run mkdocs build

doctor:
	PYTHONPATH=src python -m ultilog doctor --json

examples:
	PYTHONPATH=src python examples/01_zero_config.py
	PYTHONPATH=src python examples/02_setup_dev.py
	PYTHONPATH=src python examples/03_setup_prod.py
	PYTHONPATH=src python examples/05_context_scope.py
	PYTHONPATH=src python examples/06_json_mode.py
	PYTHONPATH=src python examples/10_asgi_shape.py

clean:
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -prune -exec rm -rf {} +
	find . -type d -name '.mypy_cache' -prune -exec rm -rf {} +
	find . -type d -name '.ruff_cache' -prune -exec rm -rf {} +
