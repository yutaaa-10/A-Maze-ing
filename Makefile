PYTHON := python3
CONFIG ?= config.txt

install:
	@$(PYTHON) -m pip install flake8 mypy

build:
	@$(PYTHON) -m build

run:
	@$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	@$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict