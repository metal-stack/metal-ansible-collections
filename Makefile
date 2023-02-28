DEPLOYMENT_BASE_IMAGE := ghcr.io/metal-stack/metal-deployment-base
DEPLOYMENT_BASE_TAG := latest

.PHONY: test
test:
	docker pull ${DEPLOYMENT_BASE_IMAGE}:${DEPLOYMENT_BASE_TAG}
	docker run --rm -it \
		-v $(PWD):/work \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-w /work ${DEPLOYMENT_BASE_IMAGE}:${DEPLOYMENT_BASE_TAG} \
		bash -c \
		"pip install --upgrade pip mock metal_python ansible-lint molecule[docker,lint] && make unit && cd partition && molecule lint"

.PHONY: unit
unit:
	for file in $(shell find . -name "test?" -type d); do python -m unittest discover -v -p '*_test.py' -s $$(dirname $$file); done

.PHONY: molecule
molecule:
	molecule test
