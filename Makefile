# makefile for Yandex Music project

black:
	black --config=black.toml yandex_music

black_test:
	black --config=black.toml tests

gen_async:
	python generate_async_version.py

gen_alias:
	python generate_camel_case_aliases.py

gen:
	make gen_async && make gen_alias

b:
	make black

bt:
	make black_test

g:
	make gen

all:
	make g && make b && make bt

a:
	make all
