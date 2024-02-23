# common

A collection for providing common deployment utilities for metal-stack.

<!-- TOC depthfrom:2 depthto:6 withlinks:true updateonsave:true orderedlist:false -->

- [Modules](#modules)
- [Roles](#roles)
- [Dynamic Inventories](#dynamic-inventories)
- [Filter Plugins](#filter-plugins)
- [Lookup Plugins](#lookup-plugins)
- [Usage](#usage)

<!-- /TOC -->

## Modules

The `metal_` modules use [metal-python](https://github.com/metal-stack/metal-python) for accessing the metal-api. Please make sure you use the correct version of this repository in order to be compatible with the API. You can setup metal-python during the execution of Ansible using the [metal_python role](../controlplane/roles/metal_python/).

| Module Name                                 | Description                                                  | Requirements |
| ------------------------------------------- | ------------------------------------------------------------ | ------------ |
| [metal_ip](library/metal_ip.py)             | Manages metal-stack IP entities                              | metal-python |
| [metal_firewall](library/metal_firewall.py) | Manages metal-stack firewall entities                        | metal-python |
| [metal_machine](library/metal_machine.py)   | Manages metal-stack machine entities                         | metal-python |
| [metal_network](library/metal_network.py)   | Manages metal-stack network entities                         | metal-python |
| [metal_project](library/metal_project.py)   | Manages metal-stack project entities                         | metal-python |
| [setup_yaml](library/setup_yaml.py)         | Setup plugin that resolves variables from a remote YAML file |              |

## Roles

| Role Name                                                              | Description                                                                                                           |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [gcp-auth](roles/gcp-auth)                                             | Authenticates at Google Cloud                                                                                         |
| [gcp-create](roles/gcp-create)                                         | Creates a Kubernetes cluster at Google Cloud                                                                          |
| [gcp-destroy](roles/gcp-destroy)                                       | Destroys a Kubernetes cluster at Google Cloud                                                                         |
| [helm-chart](roles/helm-chart)                                         | Deploys a helm chart to a k8s cluster                                                                                 |
| [systemd-docker-service](roles/systemd-docker-service)                 | Renders a systemd unit file that runs an application within a docker container                                        |
| [systemd-docker-service-cleanup](roles/systemd-docker-service-cleanup) | Stops a systemd unit and deletes its service definition                                                               |

## Dynamic Inventories

| Inventory Name                 | Description                       |
| ------------------------------ | --------------------------------- |
| [metal.py](inventory/metal.py) | Dynamic inventory for metal-stack |

## Filter Plugins

| Plugin Name               | Requirements                                                               | Description                                                           |
| ------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| humanfriendly             | [humanfriendly](https://github.com/xolox/python-humanfriendly)             | Converts sizes into human-friendly formats                            |
| transpile_ignition_config | [ct](https://github.com/coreos/container-linux-config-transpiler/releases) | Transforming a human-friendly Container Linux Config into a JSON file |
| metal_lb_config           |                                                                            | Generates the config map for metal-lb                                 |

## Lookup Plugins

| Inventory Name                   | Description         |
| -------------------------------- | ------------------- |
| [metal](lookup_plugins/metal.py) | Query the metal-api |

## Usage

It's convenient to use ansible-galaxy in order to use this collection. For your project, set up a `requirements.yml`:

```yaml
collections:
  - name: https://github.com/metal-stack/metal-ansible-collections
    version: main # use release versions if you want to have stable deployment!
    type: git
```

You can then download the roles with the following command:

```bash
ansible-galaxy install -r requirements.yml
```

Then reference the roles in your playbooks like this:

```yaml
- name: Deploy something
  hosts: localhost
  connection: local
  gather_facts: no
  roles:
    - name: metalstack.common.helm_chart
      vars:
        ...
```
