#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class SDL2Conan(ConanFile):
    name = "sdl2"
    version = "2.0.8"
    description = "Access to audio, keyboard, mouse, joystick, and graphics hardware via OpenGL and Direct3D"
    url = "https://github.com/bincrafters/conan-sdl2"
    license = "LGPL-2.1"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = ['cmake']
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "directx": [True, False],
               "alsa": [True, False],
               "jack": [True, False],
               "pulse": [True, False],
               "nas": [True, False],
               "esd": [True, False],
               "arts": [True, False],
               "x11": [True, False],
               "xcursor": [True, False],
               "xinerama": [True, False],
               "xinput": [True, False],
               "xrandr": [True, False],
               "xscrnsaver": [True, False],
               "xshape": [True, False],
               "xvm": [True, False],
               "wayland": [True, False],
               "mir": [True, False],
               "directfb": [True, False],
               "iconv": [True, False]}
    default_options = ("shared=False",
                       "fPIC=True",
                       "directx=True",
                       "alsa=True",
                       "jack=True",
                       "pulse=True",
                       "nas=True",
                       "esd=True",
                       "arts=False",
                       "x11=True",
                       "xcursor=True",
                       "xinerama=True",
                       "xinput=True",
                       "xrandr=True",
                       "xscrnsaver=True",
                       "xshape=True",
                       "xvm=True",
                       "wayland=False",
                       "mir=False",
                       "directfb=False",
                       "iconv=False")

    def requirements(self):
        if self.options.iconv:
            self.requires.add("libiconv/1.15@bincrafters/stable")

    def system_requirements(self):
        if self.settings.os == "Linux" and tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
                if self.settings.arch == "x86":
                    arch_suffix = ':i386'
                else:
                    arch_suffix = ':amd64'
                packages = ['pkg-config%s' % arch_suffix]
                packages.append('mesa-common-dev%s' % arch_suffix)
                packages.append('libegl1-mesa-dev%s' % arch_suffix)
                packages.append('libgbm-dev%s' % arch_suffix)
                packages.append('libdrm-dev%s' % arch_suffix)
                if self.options.alsa:
                    packages.append('libasound2-dev%s' % arch_suffix)
                if self.options.jack:
                    packages.append('libjack-dev%s' % arch_suffix)
                if self.options.pulse:
                    packages.append('libpulse-dev%s' % arch_suffix)
                if self.options.nas:
                    packages.append('libaudio-dev%s' % arch_suffix)
                if self.options.esd:
                    packages.append('libesd0-dev%s' % arch_suffix)
                if self.options.arts:
                    packages.append('artsc0-dev%s' % arch_suffix)
                if self.options.x11:
                    packages.extend(['libx11-dev%s' % arch_suffix,
                                     'libxext-dev%s' % arch_suffix])
                if self.options.xcursor:
                    packages.append('libxcursor-dev%s' % arch_suffix)
                if self.options.xinerama:
                    packages.append('libxinerama-dev%s' % arch_suffix)
                if self.options.xinput:
                    packages.append('libxi-dev%s' % arch_suffix)
                if self.options.xrandr:
                    packages.append('libxrandr-dev%s' % arch_suffix)
                if self.options.xscrnsaver:
                    packages.append('libxss-dev%s' % arch_suffix)
                if self.options.xvm:
                    packages.append('libxxf86vm-dev%s' % arch_suffix)
                if self.options.wayland:
                    packages.extend(['libwayland-dev%s' % arch_suffix,
                                     'libxkbcommon-dev%s' % arch_suffix,
                                     'wayland-protocols'])
                if self.options.mir:
                    packages.extend(['libmirclient-dev%s' % arch_suffix,
                                     'libxkbcommon-dev%s' % arch_suffix])
                if self.options.directfb:
                    packages.append('libdirectfb-dev%s' % arch_suffix)
                for package in packages:
                    installer.install(package)

    def config_options(self):
        if self.settings.os != "Linux":
            self.options.remove("alsa")
            self.options.remove("jack")
            self.options.remove("pulse")
            self.options.remove("nas")
            self.options.remove("esd")
            self.options.remove("arts")
            self.options.remove("x11")
            self.options.remove("xcursor")
            self.options.remove("xinerama")
            self.options.remove("xinput")
            self.options.remove("xrandr")
            self.options.remove("xscrnsaver")
            self.options.remove("xshape")
            self.options.remove("xvm")
            self.options.remove('mir')
            self.options.remove('wayland')
            self.options.remove('directfb')
        if self.settings.os != "Windows":
            self.options.remove("directx")

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC

    def source(self):
        source_url = "https://www.libsdl.org/release/SDL2-%s.tar.gz" % self.version
        tools.get(source_url)
        extracted_dir = "SDL2-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        if self.settings.compiler == 'Visual Studio':
            with tools.vcvars(self.settings, filter_known_paths=False):
                self.build_cmake()
        else:
            self.build_cmake()

    def build_cmake(self):
        tools.replace_in_file(
                os.path.join(self.source_subfolder, 'CMakeLists.txt'),
                'install(FILES ${SDL2_BINARY_DIR}/libSDL2.${SOEXT} DESTINATION "lib${LIB_SUFFIX}")',
                '')

        cmake = CMake(self)
        if self.settings.compiler != 'Visual Studio':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        if self.settings.compiler == 'Visual Studio' and not self.options.shared:
            cmake.definitions['HAVE_LIBC'] = True
        cmake.definitions['SDL_SHARED'] = self.options.shared
        cmake.definitions['SDL_STATIC'] = not self.options.shared
        if self.settings.os == "Linux":
            cmake.definitions['ALSA'] = self.options.alsa
            cmake.definitions['JACK'] = self.options.jack
            cmake.definitions['PULSEAUDIO'] = self.options.pulse
            cmake.definitions['NAS'] = self.options.nas
            cmake.definitions['VIDEO_X11'] = self.options.x11
            cmake.definitions['VIDEO_X11_XCURSOR'] = self.options.xcursor
            cmake.definitions['VIDEO_X11_XINERAMA'] = self.options.xinerama
            cmake.definitions['VIDEO_X11_XINPUT'] = self.options.xinput
            cmake.definitions['VIDEO_X11_XRANDR'] = self.options.xrandr
            cmake.definitions['VIDEO_X11_XSCRNSAVER'] = self.options.xscrnsaver
            cmake.definitions['VIDEO_X11_XSHAPE'] = self.options.xshape
            cmake.definitions['VIDEO_X11_XVM'] = self.options.xvm
            cmake.definitions['VIDEO_MIR'] = self.options.mir
            cmake.definitions['VIDEO_WAYLAND'] = self.options.wayland
            cmake.definitions['VIDEO_DIRECTFB'] = self.options.directfb
        elif self.settings.os == "Windows":
            cmake.definitions["DIRECTX"] = self.options.directx

        cmake.configure(build_dir='build')
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="COPYING.txt", dst="license", src=self.source_subfolder)

    def add_libraries_from_pc(self, library):
        pkg_config = tools.PkgConfig(library, static=not self.options.shared)
        libs = [lib[2:] for lib in pkg_config.libs_only_l]  # cut -l prefix
        lib_paths = [lib[2:] for lib in pkg_config.libs_only_L]  # cut -L prefix
        self.cpp_info.libs.extend(libs)
        self.cpp_info.libdirs.extend(lib_paths)
        self.cpp_info.sharedlinkflags.extend(pkg_config.libs_only_other)
        self.cpp_info.exelinkflags.extend(pkg_config.libs_only_other)

    def package_info(self):
        sdl2_config = 'sdl2-config.exe' if self.settings.os == 'Windows' else 'sdl2-config'
        sdl2_config = os.path.join(self.package_folder, 'bin', sdl2_config)
        self.output.info('Creating SDL2_CONFIG environment variable: %s' % sdl2_config)
        self.env_info.SDL2_CONFIG = sdl2_config
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs.append(os.path.join('include', 'SDL2'))
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(['dl', 'rt', 'pthread'])
            if self.options.alsa:
                self.add_libraries_from_pc('alsa')
            if self.options.jack:
                self.add_libraries_from_pc('jack')
            if self.options.pulse:
                self.add_libraries_from_pc('libpulse')
            if self.options.nas:
                self.cpp_info.libs.append('audio')
            if self.options.esd:
                self.add_libraries_from_pc('esound')
            if self.options.directfb:
                self.add_libraries_from_pc('directfb')
        elif self.settings.os == "Macos":
            frameworks = ['Cocoa', 'Carbon', 'IOKit', 'CoreVideo', 'CoreAudio', 'AudioToolbox', 'ForceFeedback']
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
            if not self.options.iconv:
                self.cpp_info.libs.append('iconv')
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        elif self.settings.os == "Windows":
            self.cpp_info.libs.extend(['imm32', 'winmm', 'version'])
