# Define variables
PYTHON = python3
VENV_DIR = .venv
PIP = $(VENV_DIR)/bin/pip
SRC_DIR = src
VERSION = $(shell cat src/__version__.py | grep VERSION | cut -d "'" -f 2)

# Phony targets (targets that don't create a file of the same name)
.PHONY: all venv install run clean

# Run commands in the same shell
.ONESHELL:

# Default target: runs the 'run' target which starts the server in local mode
all: run

# Create and activate a virtual environment
venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created. To activate it, run: source $(VENV_DIR)/bin/activate"

# Install dependencies from requirements.txt
install: venv
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

# Run the main Python script
run: venv
	@echo "Running main script..."
	$(VENV_DIR)/bin/$(PYTHON) $(SRC_DIR)/server.py

# Clean up build artifacts and the virtual environment
clean:
	@echo "Cleaning up..."
	rm -rf $(SRC_DIR)/__pycache__
	rm -rf $(VENV_DIR)

build:
	@echo "Building Docker image..."
	docker build -t airtasker-server:$(VERSION) .

run-docker:
	@echo "Running Docker image..."
	docker run -p 8000:8000 airtasker-server:$(VERSION)

push-docker: build
	@echo "Pushing Docker image to local minikube..."
	minikube image load airtasker-server:$(VERSION)
	@echo "Image loaded successfully at $(shell minikube image list | grep airtasker-server)"

deploy-chart:
	@echo "Deploying chart..."
	cd helm && helm upgrade --install airtasker-server ./airtasker-server --namespace airtasker --create-namespace --set image.tag=$(VERSION)