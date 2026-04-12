# makefile for Yandex Music project

ruff:
	ruff check . --fix

ruff_format:
	ruff format .

gen_sync:
	python generate_sync_version.py

gen_alias:
	python generate_camel_case_aliases.py

gen:
	make gen_sync && make gen_alias

g:
	make gen

all:
	make g && make ruff && make ruff_format

a:
	make all
