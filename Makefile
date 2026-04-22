.PHONY: help install build clean test run docker

# Colors for help
GREEN := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
RESET := $(shell tput -Txterm sgr0)

help: ## Show this help message
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-15s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

list-prof:
	python -m custom_browser.cli list

update_cam:
	python -m camoufox fetch

install: ## Install Python dependencies and Playwright browsers
	pip install -r build/requirements.txt
	playwright install firefox

build: ## Build the browser from source
	./build/build.sh

clean: ## Clean build artifacts
	rm -rf src/firefox-source/build/
	rm -rf src/firefox-source/obj-*/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

test: ## Run tests
	pytest tests/ -v

run: ## Start the profile manager CLI
	python -m custom_browser.cli

docker-build: ## Build Docker image
	docker build -t custom-antidetect-browser .

docker-run: ## Run in Docker container
	docker run -it --rm custom-antidetect-browser

dev: ## Setup development environment
	pip install -e .
	pip install black ruff pytest

update-camoufox: ## Update Camoufox source to latest
	cd src/firefox-source && git pull

## creating a new profile
create_profile-%:
	python -m custom_borwser.cli create --name "$*"

## launching that specific profile
launch-%:
	python -m custom_browser.cli launch $*

workrun:
	python -m custom_browser.cli launch work
