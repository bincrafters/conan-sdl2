#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class SDL2Conan(ConanFile):
    name = "sdl2"
    version = "2.0.7"
    url = "https://github.com/bincrafters/conan-libname"
    description = "Simple DirectMedia Layer is a cross-platform development library designed to provide low level " \
                  "access to audio, keyboard, mouse, joystick, and graphics hardware via OpenGL and Direct3D"
    license = "hhttps://hg.libsdl.org/SDL/file/5c8fc26757d7/COPYING.txt"
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def build_requirements(self):
        self.build_requires("ninja_installer/[>=1.8.2]@bincrafters/stable")

    def requirements(self):
        self.requires.add("libiconv/[>=1.15]@bincrafters/stable")

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        source_url = "https://www.libsdl.org/release/SDL2-%s.tar.gz" % self.version
        tools.get(source_url)
        extracted_dir = "SDL2-" + self.version
        os.rename(extracted_dir, "sources")

    def build(self):
        cmake = CMake(self, generator='Ninja')
        cmake.definitions['SDL_SHARED'] = self.options.shared
        cmake.definitions['SDL_STATIC'] = not self.options.shared
        cmake.configure(source_dir="sources")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="COPYING.txt", src="sources")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs.append(os.path.join('include', 'SDL2'))
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(['dl', 'rt', 'pthread'])
        elif self.settings.os == "Macos":
            frameworks = ['Cocoa', 'Carbon', 'IOKit', 'CoreVideo', 'CoreAudio', 'AudioToolbox', 'ForceFeedback']
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
