# makefile for Yandex Music project

RUN ?= uv run

ruff:
	$(RUN) ruff check . --fix

pyrefly:
	$(RUN) pyrefly check

ruff_format:
	$(RUN) ruff format .

gen_sync:
	$(RUN) python generate_sync_version.py

gen_alias:
	$(RUN) python generate_camel_case_aliases.py

test:
	$(RUN) pytest

gen:
	make gen_sync && make gen_alias

g:
	make gen

all:
	make g && make ruff && make ruff_format

a:
	make all
