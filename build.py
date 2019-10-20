#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import tools
from bincrafters import build_template_default

def add_build_requires(builds):
    return map(add_required_installers, builds)

def add_required_installers(build):
    installers = ['ninja_installer/1.9.0@bincrafters/stable']
    build.build_requires.update({"*" : installers})
    return build

if __name__ == "__main__":

    builder = build_template_default.get_builder()

    if tools.os_info.is_linux and os.getenv("CONAN_GCC_VERSIONS") == 8:
        for shared_option in [False, True]:
            custom_options = {"sdl2:esd": False, "sdl2:wayland": True, "sdl2:x11": True, 'sdl2:shared': shared_option}
            builder.add({'arch': 'x86_64', 'build_type': 'Release', 'compiler': 'gcc', 'compiler.version': 8}, custom_options)
            builder.add({'arch': 'x86_64', 'build_type': 'Debug', 'compiler': 'gcc', 'compiler.version': 8}, custom_options)

    builder.items = add_build_requires(builder.items)

    builder.run()
