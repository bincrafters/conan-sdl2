from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os


class SDL2Conan(ConanFile):
    name = "sdl2"
    version = "2.0.10"
    description = "Access to audio, keyboard, mouse, joystick, and graphics hardware via OpenGL and Direct3D"
    topics = ("conan", "sdl2", "audio", "keyboard", "graphics", "opengl")
    url = "https://github.com/bincrafters/conan-sdl2"
    homepage = "https://www.libsdl.org"
    license = "Zlib"
    exports_sources = ["CMakeLists.txt", "patches/*"]
    generators = ["cmake", "pkg_config"]
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
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
        "directfb": [True, False],
        "iconv": [True, False],
        "video_rpi": [True, False],
        "sdl2main": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "directx": True,
        "alsa": True,
        "jack": True,
        "pulse": True,
        "nas": True,
        "esd": False,
        "arts": False,
        "x11": True,
        "xcursor": True,
        "xinerama": True,
        "xinput": True,
        "xrandr": True,
        "xscrnsaver": True,
        "xshape": True,
        "xvm": True,
        "wayland": False,
        "directfb": False,
        "iconv": False,
        "video_rpi": False,
        "sdl2main": True
    }

    def requirements(self):
        if self.options.iconv:
            self.requires.add("libiconv/1.15")

        if self.settings.os == "Linux" and tools.os_info.is_linux:
            self.requires.add("libdrm/2.4.100@bincrafters/stable")
            if not tools.which('pkg-config'):
                self.requires.add("pkg-config_installer/0.29.2@bincrafters/stable")
            if self.options.alsa:
                self.requires.add("libalsa/1.1.9")
            if self.options.x11:
                self.requires.add("libx11/1.6.8@bincrafters/stable")
                self.requires.add("libxext/1.3.4@bincrafters/stable")
            if self.options.xcursor:
                self.requires.add("libxcursor/1.2.0@bincrafters/stable")
            if self.options.xinerama:
                self.requires.add("libxinerama/1.1.4@bincrafters/stable")
            if self.options.xinput:
                self.requires.add("libxi/1.7.10@bincrafters/stable")
            if self.options.xrandr:
                self.requires.add("libxrandr/1.5.2@bincrafters/stable")
            if self.options.xscrnsaver:
                self.requires.add("libxscrnsaver/1.2.3@bincrafters/stable")
            if self.options.xvm:
                self.requires.add("libxxf86vm/1.1.4@bincrafters/stable")
            if self.options.wayland:
                self.requires.add("xkbcommon/0.9.1@bincrafters/stable")

    def system_requirements(self):
        if self.settings.os == "Linux" and tools.os_info.is_linux:
            if tools.os_info.with_apt or tools.os_info.with_yum:
                installer = tools.SystemPackageTool()

                packages = []
                packages_apt = []
                packages_yum = []
                packages_apt.append('mesa-common-dev')
                packages_yum.append('mesa-libGL-devel')

                packages_apt.append('libegl1-mesa-dev')
                packages_yum.append('mesa-libEGL-devel')

                packages_apt.append('libgbm-dev')
                packages_yum.append('gdm-devel')

                if self.options.jack:
                    packages_apt.append('libjack-dev')
                    packages_yum.append('jack-audio-connection-kit-devel')
                if self.options.pulse:
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

    def source(self):
        source_url = "https://www.libsdl.org/release/SDL2-%s.tar.gz" % self.version
        tools.get(source_url, sha256="b4656c13a1f0d0023ae2f4a9cf08ec92fffb464e0f24238337784159b8b91d57")
        extracted_dir = "SDL2-" + self.version
        os.rename(extracted_dir, self._source_subfolder)
        tools.patch(base_path=self._source_subfolder, patch_file=os.path.join("patches", "cmake.patch"))
        # Workaround for linker error with VS2019, see https://bugzilla.libsdl.org/show_bug.cgi?id=4759
        if self.settings.compiler == 'Visual Studio' and self.settings.compiler.version == 16:
            tools.patch(base_path=self._source_subfolder, patch_file=os.path.join("patches", "SDL_string.patch"))

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
            self._check_pkg_config(True, 'egl')
            self._check_pkg_config(self.options.jack, 'jack')
            self._check_pkg_config(self.options.pulse, 'libpulse')
            self._check_pkg_config(self.options.esd, 'esound')
            self._check_pkg_config(self.options.wayland, 'wayland-client')
            self._check_pkg_config(self.options.wayland, 'wayland-protocols')
            self._check_pkg_config(self.options.directfb, 'directfb')

    def _configure_cmake(self):
        self._check_dependencies()

        cmake = CMake(self)
        # FIXME: self.install_folder not defined? Neccessary?
        cmake.definitions['CONAN_INSTALL_FOLDER'] = self.install_folder
        if self.settings.os != 'Windows':
            if not self.options.shared:
                cmake.definitions['SDL_STATIC_PIC'] = self.options.fPIC
        if self.settings.compiler == 'Visual Studio' and not self.options.shared:
            cmake.definitions['HAVE_LIBC'] = True
        cmake.definitions['SDL_SHARED'] = self.options.shared
        cmake.definitions['SDL_STATIC'] = not self.options.shared
        if self.settings.os == "Linux":
            # See https://github.com/bincrafters/community/issues/696
            cmake.definitions['SDL_VIDEO_DRIVER_X11_SUPPORTS_GENERIC_EVENTS'] = 1

            cmake.definitions['ALSA'] = self.options.alsa
            if self.options.alsa:
                cmake.definitions['HAVE_ASOUNDLIB_H'] = True
                cmake.definitions['HAVE_LIBASOUND'] = True
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
            cmake.definitions['VIDEO_WAYLAND'] = self.options.wayland
            cmake.definitions['VIDEO_DIRECTFB'] = self.options.directfb
            cmake.definitions['VIDEO_RPI'] = self.options.video_rpi
        elif self.settings.os == "Windows":
            cmake.definitions["DIRECTX"] = self.options.directx

        cmake.configure(build_dir=self._build_subfolder)
        return cmake

    def _build_cmake(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING.txt", dst="license", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install(build_dir=self._build_subfolder)

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
        # ensure that libSDL2main is linked first
        self.cpp_info.libs.reverse()
        if not self.options.sdl2main:
            self.cpp_info.libs = [lib for lib in self.cpp_info.libs if 'main' not in lib]
        self.cpp_info.includedirs.append(os.path.join('include', 'SDL2'))
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.extend(['dl', 'rt', 'pthread'])
            if self.options.jack:
                self._add_libraries_from_pc('jack')
            if self.options.pulse:
                self._add_libraries_from_pc('libpulse', False)
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
            if not self.options.iconv:
                self.cpp_info.libs.append('iconv')
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        elif self.settings.os == "Windows":
            self.cpp_info.system_libs.extend(['user32', 'gdi32', 'winmm', 'imm32', 'ole32', 'oleaut32', 'version', 'uuid', 'advapi32', 'setupapi', 'shell32'])
