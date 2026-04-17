# makefile for Sphinx documentation

SPHINXOPTS ?= -j auto
SPHINXBUILD ?= sphinx-build
SPHINXGENERATE ?= sphinx-apidoc
MODULEPATH = ../yandex_music
SOURCEDIR = source
BUILDDIR = build
TEMPLATEDIR = source/templates

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

gen:
	@$(SPHINXGENERATE) -f -e -M -P -o "$(SOURCEDIR)" -t "$(TEMPLATEDIR)" "$(MODULEPATH)" $(O)
	@python generate_client_docs.py

.PHONY: gen Makefile

# html → dirhtml: локальная сборка совпадает с production (.readthedocs.yaml: builder: dirhtml).
html:
	@$(SPHINXBUILD) -M dirhtml "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: html

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)