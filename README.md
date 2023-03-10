# Metal Ansible Collections

This repository contains Ansible collections for deploying metal-stack.

The metal-stack primarily consists of a control plane and partitions that register at the control plane. For this reason, there are two further collections in this repository, one containing the parts relevant for the control plane deployment and another one containing roles for bootstrapping a partition. Please find more documentation in the respective sub folders:

- [metalstack.controlplane](controlplane)
- [metalstack.partition](partition)

Furthermore, there is a place where common roles / modules / plugins are located. It's inside the following collection:

- [metalstack.common](common)

## Usage

It's convenient to use ansible-galaxy in order to use this project.

For your deployment project, set up a `requirements.yml`:

```yaml
collections:
  - name: https://github.com/metal-stack/metal-ansible-collections
    version: main # use release versions if you want to have stable deployment!
    type: git

# you can find release versions here: https://github.com/metal-stack/releases
```

You can then download the collections with the following command:

```bash
ansible-galaxy install -r requirements.yml
```

An example for how to use this project can be found in the [mini-lab](https://github.com/metal-stack/mini-lab) project.

## Resolving Image Versions

Many roles require names and tags of the microservices to be set explicitly. You can, however, make use of the [setup_yaml](common/plugins/modules/setup_yaml.py) action plugin, which fetches image release versions from the [release](https://github.com/metal-stack/releases) vector. This way, you only need to define the following data structure somewhere in your playbooks:

```yaml
setup_yaml:
  - url: https://raw.githubusercontent.com/metal-stack/releases/master/release.yaml
    meta_var: metal_stack_release
    # the metal_stack_release variable is provided through role defaults of this project
    # use release versions if you want to have stable deployment!
```
