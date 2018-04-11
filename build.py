#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default

def add_build_requires(builds):
    return map(add_required_installers, builds)

def add_required_installers(build):
    installers = ['ninja_installer/1.8.2@bincrafters/stable']
    build.build_requires.update({"*" : installers})
    return build

if __name__ == "__main__":

    builder = build_template_default.get_builder()

    builder.items = add_build_requires(builder.items)

    builder.run()
