#
# Basic makefile for general targets
#

VIRTUALENV_PATH = venv
VIRTUALENV_BIN = $(VIRTUALENV_PATH)/bin
EASY_INSTALL = $(VIRTUALENV_BIN)/easy_install
DEV_ENV = source $(VIRTUALENV_BIN)/activate ;
NOSE = $(VIRTUALENV_BIN)/nosetests --nocapture
NOSYD = $(VIRTUALENV_BIN)/nosyd -1
PIP = $(VIRTUALENV_BIN)/pip
PYTHON = $(ENV) $(VIRTUALENV_BIN)/python

.PHONY: test
test: unit-test integration-test acceptance-test

start_plugin:
	/Users/philipcristiano/gits/fairground/venv/bin/python -c 'from circus import plugins;plugins.main()' --endpoint tcp://127.0.0.1:5555 --pubsub tcp://127.0.0.1:5556 fairground.plugin.FairgroundPlugin

.PHONY: unit-test
unit-test:
	$(NOSE) tests/unit

.PHONY: integration-test
integration-test:
	$(NOSE) tests/integration

.PHONY: acceptance-test
acceptance-test:
	$(DEV_ENV) $(NOSE) tests/acceptance -v

.PHONY: unit-test-coverage
unit-test-coverage:
	$(NOSE) --with-coverage --cover-package=fairground --cover-tests --cover-erase

.PHONY: tdd
tdd:
	$(DEV_ENV) $(NOSYD) tests/unit

.PHONY: docs
docs:
	bin/sphinx-build -b html -d docs/build/doctrees docs/source docs/html

.PHONY: foreman
foreman:
	$(DEV_ENV) foreman start -f Procfile

.PHONY: develop
develop:
	$(PYTHON) setup.py develop

.PHONY: clean
clean:
	-$(PYTHON) setup.py clean
	-find . -type f -name '*.pyc' -o -name '*.tar.gz' -delete
	-rm -f nosetests.xml
	-rm -f pip-log.txt
	-rm -f .nose-stopwatch-times
	-rm -rf build dist *.egg-info

.PHONY: dist
dist: clean
	$(shell export COPYFILE_DISABLE=true)

	$(PYTHON) setup.py sdist

.PHONY: upload
upload:
	$(PYTHON) setup.py sdist upload

.PHONY: requirements
requirements:
	$(EASY_INSTALL) -U distribute
	$(PIP) install -r requirements.txt

.PHONY: osx_requirements
osx_requirements:

.PHONY: virtualenv
virtualenv:
	virtualenv --distribute $(VIRTUALENV_PATH)

