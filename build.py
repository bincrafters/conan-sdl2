#!/usr/bin/env python

import os
from conans import tools
from bincrafters import build_template_default


if __name__ == "__main__":

    builder = build_template_default.get_builder()

    gcc_version = os.getenv("CONAN_GCC_VERSIONS", None)
    clang_version = os.getenv("CONAN_CLANG_VERSIONS", None)
    compiler_version = gcc_version if gcc_version else clang_version
    
    if tools.os_info.is_linux and (gcc_version is in (8,9,10)  or clang_version is in (10,)):
        for shared_option in [False, True]:
            custom_options = {"sdl2:esd": False, "sdl2:wayland": True, "sdl2:x11": True, 'sdl2:shared': shared_option}
            builder.add({'arch': 'x86_64', 'build_type': 'Release', 'compiler': 'gcc',
                         'compiler.version': compiler_version}, custom_options)
            builder.add({'arch': 'x86_64', 'build_type': 'Debug', 'compiler': 'gcc',
                         'compiler.version': compiler_version}, custom_options)

    builder.run()
