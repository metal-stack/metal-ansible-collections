DEPLOYMENT_BASE_IMAGE := ghcr.io/metal-stack/metal-deployment-base
DEPLOYMENT_BASE_TAG := latest

ifeq ($(CI),true)
  DOCKER_TTY_ARG=
  FORCE_COLORS=-e PY_COLORS=1 -e ANSIBLE_FORCE_COLOR=1
else
  DOCKER_TTY_ARG=t
endif

.PHONY: test-local
test-local:
	docker pull ${DEPLOYMENT_BASE_IMAGE}:${DEPLOYMENT_BASE_TAG}
	docker run --rm -i$(DOCKER_TTY_ARG) $(FORCE_COLORS) \
		-v $(PWD):/work \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-w /work ${DEPLOYMENT_BASE_IMAGE}:${DEPLOYMENT_BASE_TAG} \
		bash -c \
		"make test || bash"

.PHONY: test
test: install unit molecule

.PHONY: unit
unit:
	for file in $(shell find . -name "test?" -type d); do python -m unittest discover -v -p '*_test.py' -s $$(dirname $$file); done

.PHONY: molecule
molecule:
	cd partition && molecule test

.PHONY: install
install:
	pip install --upgrade pip mock metal_python ansible-lint molecule[docker,lint]
