.PHONY: build-deps

# Defaults for parameterized builds (can be overridden: make build-branch REF=foo)
REF ?= main

# MAIN BRANCH Installation and Tests

build-deps:
	pip install -r requirements/requirements.txt
