.DEFAULT_GOAL := help
PKG = pyne2001
TESTS_DIR = pyne2001/tests

# NOTE: To avoid putting binaries into the distribution,
# we delete them and rebuild them afterwards
dist: ## Build source distribution
	make clean
	find . -type f -name "NE2001" -delete
	find . -type f -name "libNE2001.a" -delete
	python setup.py sdist
	make all -C ${PKG}/NE2001/src

# NOTE: -e installs in "Development Mode"
# See: https://packaging.python.org/tutorials/installing-packages/
install: ## Install the package in development mode
	pip install -e .

# NOTE: remove the .egg-info directory
uninstall: ## Uninstall the package
	pip uninstall ${PKG}
	rm -rf ${PKG}.egg-info

# GLORIOUS hack to autogenerate Makefile help
# This simply parses the double hashtags that follow each Makefile command
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Print this help message
	@echo "Makefile help for ${PKG}"
	@echo "=========================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

clean: ## Remove all python cache and build files
	find . -type f -name "*.o" -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/
	rm -rf dist/
	rm -rf ${PKG}.egg-info/

upload_test: ## Upload the distribution source to the TEST PyPI
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: ## Upload the distribution source to the REAL PyPI
	twine upload dist/*

tests: ## Run unit tests
	python -m unittest discover ${TESTS_DIR}

.PHONY: dist install uninstall help clean tests
