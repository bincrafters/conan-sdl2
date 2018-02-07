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
    filtered_builds = []

    builder.items = add_build_requires(builder.items)
    for settings, options, env_vars, build_requires, reference in builder.items:
        settings["arch_build"] = settings["arch"]
        filtered_builds.append([settings, options, env_vars, build_requires])
    builder.builds = filtered_builds
    builder.run()


    builder.run()

