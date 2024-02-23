#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import yaml
from jinja2 import meta, exceptions
from ansible.utils.color import stringc
from ansible import template


class VariablesLinter:
    _magic_vars = {'inventory_hostname', 'hostvars', 'groups', 'item', 'play_hosts', 'ansible_hostname'} # how to get these dynamically?

    def __init__(self) -> None:
        t = template.Templar(loader=None)
        self._env = t.environment

        # no idea how to dynamically add all filters from all installed collections
        self._env.filters.update({"ansible.utils.next_nth_usable": None})

    def _find_in_path(self, root, patterns):
        files = []
        for pattern in patterns:
            files.extend(glob.glob(os.path.join(root, pattern), recursive=True))
        return files

    def _find_jinja_files(self, root):
        return self._find_in_path(root, ['templates/*']) # 'tasks/*'

    def _find_vars_files(self, root):
        return self._find_in_path(root, ['defaults/*.yaml', 'defaults/*.yml', 'vars/*.yaml', 'defaults/*.yml'])

    def lint(self):
        for role_path in glob.glob('./**/roles/*'):
            role_name = os.path.basename(role_path)

            print(f'Linting role "{role_name}"')

            defined_vars = set()
            used_vars = set()

            for f in self._find_vars_files(role_path):
                with open(f, 'r') as file:
                    parsed = yaml.safe_load(file)

                if not isinstance(parsed, dict):
                    raise Exception(f'vars file "{f}" does not contain a dictionary')

                for key in parsed.keys():
                    defined_vars.add(key)

            for file in self._find_jinja_files(role_path):
                try:
                    template_source = self._env.loader.get_source(self._env, file)[0]
                except exceptions.TemplateNotFound:
                    continue

                parsed_content = self._env.parse(template_source)

                try:
                    variables = meta.find_undeclared_variables(parsed_content)
                except exceptions.TemplateAssertionError as err:
                    print(stringc(f'Cannot parse template "{file}", skipping: {err}', 'yellow'))
                    continue

                used_vars = used_vars.union(variables)

            undefined_vars = used_vars.difference(defined_vars).difference(self._magic_vars)
            if undefined_vars:
                print(stringc('Found variables that are not defined in defaults or role variables:', 'red'))
                print(stringc(str(undefined_vars), 'red'))


VariablesLinter().lint()
