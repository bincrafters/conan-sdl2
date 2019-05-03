[![Download](https://api.bintray.com/packages/bincrafters/public-conan/sdl2%3Abincrafters/images/download.svg) ](https://bintray.com/bincrafters/public-conan/sdl2%3Abincrafters/_latestVersion)
[![Build Status Travis](https://travis-ci.com/bincrafters/conan-sdl2.svg?branch=stable%2F2.0.9)](https://travis-ci.com/bincrafters/conan-sdl2)
[![Build Status AppVeyor](https://ci.appveyor.com/api/projects/status/github/bincrafters/conan-sdl2?branch=stable%2F2.0.9&svg=true)](https://ci.appveyor.com/project/bincrafters/conan-sdl2)

## Conan package recipe for [*sdl2*](https://www.libsdl.org)

Access to audio, keyboard, mouse, joystick, and graphics hardware via OpenGL and Direct3D

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/bincrafters/public-conan/sdl2%3Abincrafters).


## Issues

If you wish to report an issue or make a request for a Bincrafters package, please do so here:

[Bincrafters Community Issues](https://github.com/bincrafters/community/issues)


## For Users

### Basic setup

    $ conan install sdl2/2.0.9@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    sdl2/2.0.9@bincrafters/stable

    [generators]
    cmake

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.


## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create . bincrafters/stable


### Available Options
| Option        | Default | Possible Values  |
| ------------- |:----------------- |:------------:|
| shared      | False |  [True, False] |
| fPIC      | True |  [True, False] |
| directx      | True |  [True, False] |
| alsa      | True |  [True, False] |
| jack      | True |  [True, False] |
| pulse      | True |  [True, False] |
| nas      | True |  [True, False] |
| esd      | False |  [True, False] |
| arts      | False |  [True, False] |
| x11      | True |  [True, False] |
| xcursor      | True |  [True, False] |
| xinerama      | True |  [True, False] |
| xinput      | True |  [True, False] |
| xrandr      | True |  [True, False] |
| xscrnsaver      | True |  [True, False] |
| xshape      | True |  [True, False] |
| xvm      | True |  [True, False] |
| wayland      | False |  [True, False] |
| mir      | False |  [True, False] |
| directfb      | False |  [True, False] |
| iconv      | False |  [True, False] |
| sdl2main      | True |  [True, False] |


## Add Remote

    $ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"


## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package sdl2.
It does *not* in any way apply or is related to the actual software being packaged.

[MIT](https://github.com/bincrafters/conan-sdl2/blob/stable/2.0.9/LICENSE.md)
