# Metal Ansible Collections

This repository contains Ansible collections for deploying metal-stack.

The metal-stack primarily consists of a control plane and partitions that register at the control plane. For this reason, there are two further collections in this repository, one containing the parts relevant for the control plane deployment and another one containing roles for bootstrapping a partition. Please find more documentation in the respective sub folders:

- [Control Plane Deployment](controlplane)
- [Partition Deployment](partition)

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

Many roles require names and tags of the microservices to be set explicitly. You can, however, make use of the [setup_yaml](https://github.com/metal-stack/ansible-common/blob/master/library/setup_yaml.py) module, which fetches image release versions from the [release](https://github.com/metal-stack/releases) vector. This way, you only need to define the following data structure somewhere in your playbooks:

```yaml
setup_yaml:
  - url: https://raw.githubusercontent.com/metal-stack/releases/master/release.yaml
    meta_var: metal_stack_release
    # the metal_stack_release variable is provided through role defaults of this project
    # use release versions if you want to have stable deployment!
```

## Variables

There are global defaults for all roles of this project defined [here](defaults/main.yaml).

| Name                         | Mandatory | Description                               |
| ---------------------------- | --------- | ----------------------------------------- |
| metal_registry_auth_enabled  |           | Enables deployment of image pull secrets  |
| metal_registry_auth_user     |           | The default auth user for the registry    |
| metal_registry_auth_password |           | The password for the user of the registry |
