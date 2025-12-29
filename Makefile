.PHONY: setup generate serve clean all

VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

all: generate serve

setup:
	@echo "Setting up virtual environment and installing dependencies..."
	python3 -m venv $(VENV_DIR)
	$(PIP) install -r requirements.txt

generate:
	@echo "Generating static site..."
	$(PYTHON) generate_site.py

serve:
	@echo "Serving site locally at http://localhost:8000 (Ctrl+C to stop)..."
	python -m http.server --directory docs 8000

clean:
	@echo "Cleaning generated files and virtual environment..."
	rm -rf docs $(VENV_DIR)
