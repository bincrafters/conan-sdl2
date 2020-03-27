from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os


class SDL2Conan(ConanFile):
    name = "sdl2"
    description = "Access to audio, keyboard, mouse, joystick, and graphics hardware via OpenGL, Direct3D and Vulkan"
    topics = ("conan", "sdl2", "audio", "keyboard", "graphics", "opengl")
    url = "https://github.com/bincrafters/conan-sdl2"
    homepage = "https://www.libsdl.org"
    license = "Zlib"
    exports_sources = ["CMakeLists.txt", "patches/*"]
    generators = ["cmake", "pkg_config"]
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "directx": [True, False],
        "alsa": ["conan", "system", "off"],
        "jack": [True, False],
        "pulse": ["conan", "system", "off"],
        "nas": [True, False],
        "esd": [True, False],
        "arts": [True, False],
        "x11": ["conan", "system", "off"],
        "xcursor": ["conan", "system", "off"],
        "xinerama": ["conan", "system", "off"],
        "xinput": ["conan", "system", "off"],
        "xrandr": ["conan", "system", "off"],
        "xscrnsaver": ["conan", "system", "off"],
        "xshape": [True, False],
        "xvm": ["conan", "system", "off"],
        "wayland": [True, False],
        "directfb": [True, False],
        "iconv": [True, False],
        "video_rpi": [True, False],
        "sdl2main": [True, False],
        "gl": ["mesa", "system"],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "directx": True,
        "alsa": "system",
        "jack": True,
        "pulse": "system",
        "nas": True,
        "esd": False,
        "arts": False,
        "x11": "system",
        "xcursor": "system",
        "xinerama": "system",
        "xinput": "system",
        "xrandr": "system",
        "xscrnsaver": "system",
        "xshape": True,
        "xvm": "system",
        "wayland": False,
        "directfb": False,
        "iconv": True,
        "video_rpi": False,
        "sdl2main": True,
        "gl": "system",
    }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _cmake = None

    def requirements(self):
        if self.options.iconv:
            self.requires.add("libiconv/1.16")

        if self.settings.os == "Linux" and tools.os_info.is_linux:
            self.requires.add("libdrm/2.4.100@bincrafters/stable")
            if not tools.which('pkg-config'):
                self.requires.add("pkg-config_installer/0.29.2@bincrafters/stable")
            if self.options.alsa == "conan":
                self.requires.add("libalsa/1.1.9")
            if self.options.x11 == "conan":
                self.requires.add("libx11/1.6.8@bincrafters/stable")
                self.requires.add("libxext/1.3.4@bincrafters/stable")
            if self.options.xcursor == "conan":
                self.requires.add("libxcursor/1.2.0@bincrafters/stable")
            if self.options.xinerama == "conan":
                self.requires.add("libxinerama/1.1.4@bincrafters/stable")
            if self.options.xinput == "conan":
                self.requires.add("libxi/1.7.10@bincrafters/stable")
            if self.options.xrandr == "conan":
                self.requires.add("libxrandr/1.5.2@bincrafters/stable")
            if self.options.xscrnsaver == "conan":
                self.requires.add("libxscrnsaver/1.2.3@bincrafters/stable")
            if self.options.xvm == "conan":
                self.requires.add("libxxf86vm/1.1.4@bincrafters/stable")
            if self.options.wayland:
                self.requires.add("xkbcommon/0.9.1@bincrafters/stable")
            if self.options.pulse == "conan":
                self.requires("pulseaudio/13.0@bincrafters/stable")
            if self.options.gl == "mesa":
                self.requires("mesa/19.3.1@bincrafters/stable")

    def system_requirements(self):
        if self.settings.os == "Linux" and tools.os_info.is_linux:
            if tools.os_info.with_apt or tools.os_info.with_yum:
                installer = tools.SystemPackageTool()

                packages = []
                packages_apt = []
                packages_yum = []

                # Note that while this builds against mesa, the actual implementation might be something else
                if self.options.gl == "system":
                    packages_apt.append('mesa-common-dev')
                    packages_yum.append('mesa-libGL-devel')

                    packages_apt.append('libegl1-mesa-dev')
                    packages_yum.append('mesa-libEGL-devel')

                packages_apt.append('libgbm-dev')
                packages_yum.append('gdm-devel')
                if self.options.alsa == "system":
                    packages_apt.append('libasound2-dev')
                    packages_yum.append('alsa-lib-devel')
                if self.options.jack:
                    packages_apt.append('libjack-dev')
                    packages_yum.append('jack-audio-connection-kit-devel')
                if self.options.pulse == "system":
                    packages_apt.append('libpulse-dev')
                    packages_yum.append('pulseaudio-libs-devel')
                if self.options.nas:
                    packages_apt.append('libaudio-dev')
                    packages_yum.append('nas-devel')
                if self.options.esd:
                    packages_apt.append('libesd0-dev')
                    packages_yum.append('esound-devel')
                if self.options.arts:
                    packages_apt.append('artsc0-dev')
                if self.options.x11 == "system":
                    packages_apt.extend(['libx11-dev',
                                         'libxext-dev'])
                    packages_yum.extend(['libX11-devel',
                                         'libXext-devel'])
                if self.options.xcursor == "system":
                    packages_apt.append('libxcursor-dev')
                    packages_yum.append('libXcursor-devel')
                if self.options.xinerama == "system":
                    packages_apt.append('libxinerama-dev')
                    packages_yum.append('libXinerama-devel')
                if self.options.xinput == "system":
                    packages_apt.append('libxi-dev')
                    packages_yum.append('libXi-devel')
                if self.options.xrandr == "system":
                    packages_apt.append('libxrandr-dev')
                    packages_yum.append('libXrandr-devel')
                if self.options.xscrnsaver == "system":
                    packages_apt.append('libxss-dev')
                    packages_yum.append('libXScrnSaver-devel')
                if self.options.xvm == "system":
                    packages_apt.append('libxxf86vm-dev')
                    packages_yum.append('libXxf86vm-devel')
                if self.options.wayland:
                    packages_apt.extend(['libwayland-dev',
                                         'wayland-protocols'])
                    packages_yum.extend(['wayland-devel',
                                         'wayland-protocols-devel'])
                if self.options.directfb:
                    packages_apt.append('libdirectfb-dev')

                if tools.os_info.with_apt:
                    packages = packages_apt
                elif tools.os_info.with_yum:
                    packages = packages_yum

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
            self.options.remove('wayland')
            self.options.remove('directfb')
            self.options.remove('video_rpi')
        if self.settings.os != "Windows":
            self.options.remove("directx")

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC
        if self.settings.os == "Macos" and not self.options.iconv:
            raise ConanInvalidConfiguration("On macOS iconv can't be disabled")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "SDL2-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

        if "patches" in self.conan_data and self.version in self.conan_data["patches"]:
            for patch in self.conan_data["patches"][self.version]:
                tools.patch(**patch)

    def build(self):
        # ensure sdl2-config is created for MinGW
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"),
                              "if(NOT WINDOWS OR CYGWIN)",
                              "if(NOT WINDOWS OR CYGWIN OR MINGW)")
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"),
                              "if(NOT (WINDOWS OR CYGWIN))",
                              "if(NOT (WINDOWS OR CYGWIN OR MINGW))")
        self._build_cmake()

    def _check_pkg_config(self, option, package_name):
        if option:
            pkg_config = tools.PkgConfig(package_name)
            if not pkg_config.provides:
                raise ConanInvalidConfiguration('package %s is not available' % package_name)

    def _check_dependencies(self):
        if self.settings.os == 'Linux':
            if self.options.gl == "system":
                self._check_pkg_config(True, 'egl')
            self._check_pkg_config(self.options.jack, 'jack')
            self._check_pkg_config(self.options.esd, 'esound')
            self._check_pkg_config(self.options.wayland, 'wayland-client')
            self._check_pkg_config(self.options.wayland, 'wayland-protocols')
            self._check_pkg_config(self.options.directfb, 'directfb')

    def _configure_cmake(self):
        if not self._cmake:
            self._check_dependencies()

            self._cmake = CMake(self)
            # FIXME: self.install_folder not defined? Neccessary?
            self._cmake.definitions['CONAN_INSTALL_FOLDER'] = self.install_folder
            if self.settings.os != 'Windows':
                if not self.options.shared:
                    self._cmake.definitions['SDL_STATIC_PIC'] = self.options.fPIC
            if self.settings.compiler == 'Visual Studio' and not self.options.shared:
                self._cmake.definitions['HAVE_LIBC'] = True
            self._cmake.definitions['SDL_SHARED'] = self.options.shared
            self._cmake.definitions['SDL_STATIC'] = not self.options.shared
            if self.settings.os == "Linux":
                # See https://github.com/bincrafters/community/issues/696
                self._cmake.definitions['SDL_VIDEO_DRIVER_X11_SUPPORTS_GENERIC_EVENTS'] = 1

                self._cmake.definitions['ALSA'] = self.options.alsa
                if self.options.alsa != "off":
                    self._cmake.definitions['HAVE_ASOUNDLIB_H'] = True
                    self._cmake.definitions['HAVE_LIBASOUND'] = True
                self._cmake.definitions['JACK'] = self.options.jack
                self._cmake.definitions['PULSEAUDIO'] = self.options.pulse
                self._cmake.definitions['NAS'] = self.options.nas
                self._cmake.definitions['VIDEO_X11'] = self.options.x11
                if self.options.x11 != "off":
                    self._cmake.definitions['HAVE_XEXT_H'] = True
                self._cmake.definitions['VIDEO_X11_XCURSOR'] = self.options.xcursor != "off"
                if self.options.xcursor != "off":
                    self._cmake.definitions['HAVE_XCURSOR_H'] = True
                self._cmake.definitions['VIDEO_X11_XINERAMA'] = self.options.xinerama != "off"
                if self.options.xinerama != "off":
                    self._cmake.definitions['HAVE_XINERAMA_H'] = True
                self._cmake.definitions['VIDEO_X11_XINPUT'] = self.options.xinput != "off"
                if self.options.xinput != "off":
                    self._cmake.definitions['HAVE_XINPUT_H'] = True
                self._cmake.definitions['VIDEO_X11_XRANDR'] = self.options.xrandr != "off"
                if self.options.xrandr != "off":
                    self._cmake.definitions['HAVE_XRANDR_H'] = True
                self._cmake.definitions['VIDEO_X11_XSCRNSAVER'] = self.options.xscrnsaver != "off"
                if self.options.xscrnsaver != "off":
                    self._cmake.definitions['HAVE_XSS_H'] = True
                self._cmake.definitions['VIDEO_X11_XSHAPE'] = self.options.xshape
                if self.options.xshape:
                    self._cmake.definitions['HAVE_XSHAPE_H'] = True
                self._cmake.definitions['VIDEO_X11_XVM'] = self.options.xvm != "off"
                if self.options.xvm != "off":
                    self._cmake.definitions['HAVE_XF86VM_H'] = True
                self._cmake.definitions['VIDEO_WAYLAND'] = self.options.wayland
                self._cmake.definitions['VIDEO_DIRECTFB'] = self.options.directfb
                self._cmake.definitions['VIDEO_RPI'] = self.options.video_rpi
                self._cmake.definitions['HAVE_VIDEO_OPENGL'] = True
                self._cmake.definitions['HAVE_VIDEO_OPENGL_EGL'] = True
            elif self.settings.os == "Windows":
                self._cmake.definitions["DIRECTX"] = self.options.directx

            self._cmake.configure(build_dir=self._build_subfolder)
        return self._cmake

    def _build_cmake(self):
        if self.settings.os == "Linux":
            if self.options.pulse == "conan":
                os.rename('libpulse.pc', 'libpulse-simple.pc')
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING.txt", dst="license", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install(build_dir=self._build_subfolder)
        tools.rmdir(os.path.join(self.package_folder, "cmake"))

    def _add_libraries_from_pc(self, library, static=None):
        if static is None:
            static = not self.options.shared
        pkg_config = tools.PkgConfig(library, static=static)
        libs = [lib[2:] for lib in pkg_config.libs_only_l]  # cut -l prefix
        lib_paths = [lib[2:] for lib in pkg_config.libs_only_L]  # cut -L prefix
        self.cpp_info.libs.extend(libs)
        self.cpp_info.libdirs.extend(lib_paths)
        self.cpp_info.sharedlinkflags.extend(pkg_config.libs_only_other)
        self.cpp_info.exelinkflags.extend(pkg_config.libs_only_other)

    def package_id(self):
        del self.info.options.sdl2main

    @staticmethod
    def _chmod_plus_x(filename):
        if os.name == 'posix':
            os.chmod(filename, os.stat(filename).st_mode | 0o111)

    def package_info(self):
        sdl2_config = os.path.join(self.package_folder, 'bin', "sdl2-config")
        self._chmod_plus_x(sdl2_config)
        self.output.info('Creating SDL2_CONFIG environment variable: %s' % sdl2_config)
        self.env_info.SDL2_CONFIG = sdl2_config
        self.output.info('Creating SDL_CONFIG environment variable: %s' % sdl2_config)
        self.env_info.SDL_CONFIG = sdl2_config
        self.cpp_info.libs = [lib for lib in tools.collect_libs(self) if '2.0' not in lib]
        if not self.options.sdl2main:
            self.cpp_info.libs = [lib for lib in self.cpp_info.libs]
        else:
            # ensure that SDL2main is linked first
            sdl2mainlib = "SDL2main"
            if self.settings.build_type == "Debug":
                sdl2mainlib = "SDL2maind"
            self.cpp_info.libs.insert(0, self.cpp_info.libs.pop(self.cpp_info.libs.index(sdl2mainlib)))
        self.cpp_info.includedirs.append(os.path.join('include', 'SDL2'))
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.extend(['dl', 'rt', 'pthread'])
            if self.options.jack:
                self._add_libraries_from_pc('jack')
            if self.options.nas:
                self.cpp_info.libs.append('audio')
            if self.options.esd:
                self._add_libraries_from_pc('esound')
            if self.options.directfb:
                self._add_libraries_from_pc('directfb')
            if self.options.video_rpi:
                self.cpp_info.libs.append('bcm_host')
                self.cpp_info.includedirs.extend(["/opt/vc/include",
                                                  "/opt/vc/include/interface/vcos/pthreads",
                                                  "/opt/vc/include/interface/vmcs_host/linux"])
                self.cpp_info.libdirs.append("/opt/vc/lib")
                self.cpp_info.sharedlinkflags.append("-Wl,-rpath,/opt/vc/lib")
                self.cpp_info.exelinkflags.append("-Wl,-rpath,/opt/vc/lib")
        elif self.settings.os == "Macos":
            self.cpp_info.frameworks.extend(['Cocoa', 'Carbon', 'IOKit', 'CoreVideo', 'CoreAudio', 'AudioToolbox', 'ForceFeedback'])
        elif self.settings.os == "Windows":
            self.cpp_info.system_libs.extend(['user32', 'gdi32', 'winmm', 'imm32', 'ole32', 'oleaut32', 'version', 'uuid', 'advapi32', 'setupapi', 'shell32'])
