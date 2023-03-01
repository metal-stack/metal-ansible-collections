ifeq ($(CI),true)
  DOCKER_TTY_ARG=
  FORCE_COLORS=-e PY_COLORS=1 -e ANSIBLE_FORCE_COLOR=1
else
  DOCKER_TTY_ARG=t
endif

.PHONY: test-in-docker
test-in-docker:
	docker build . -t metal-ansible-collections
	docker run --rm -i$(DOCKER_TTY_ARG) $(FORCE_COLORS) \
		-v $(PWD):/work \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-w /work \
		metal-ansible-collections \
		bash -c \
		"make test"

.PHONY: test
test: lint unit

.PHONY: unit
unit:
	for file in $(shell find . -name "test?" -type d); do python -m unittest discover -v -p '*_test.py' -s $$(dirname $$file); done

.PHONY: lint
lint:
	flake8
	yamllint .
	ansible-galaxy collection install . && ansible-lint

.PHONY: install
install:
	pip install --upgrade pip mock metal_python ansible-lint yamllint flake8
