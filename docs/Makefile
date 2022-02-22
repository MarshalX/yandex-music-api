# makefile for Sphinx documentation

SPHINXOPTS ?=
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
	@$(SPHINXGENERATE) -f -e -M -o "$(SOURCEDIR)" -t "$(TEMPLATEDIR)" "$(MODULEPATH)" $(O)

.PHONY: gen Makefile

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)