# makefile for Yandex Music project

ruff:
	ruff . --fix

ruff_format:
	ruff format .

gen_async:
	python generate_async_version.py

gen_alias:
	python generate_camel_case_aliases.py

gen:
	make gen_async && make gen_alias

g:
	make gen

all:
	make g && make ruff && make ruff_format

a:
	make all
