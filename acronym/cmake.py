def dr_check(debug, release):
    return """if (CMAKE_BUILD_TYPE EQUAL "DEBUG")\n    {}\nelse()\n    {}\nendif()\n""".format(debug, release)

class Cmake():
    def __init__(self, name, c3po=True, targets={},
                 debug_flags=[f for f in "-masm=intel -Wall -Wextra -Wno-unknown-pragmas -g -O0 -fsanitize=address -fno-omit-frame-pointer".split()],
                 release_flags=[f for f in "-masm=intel -Wall -Wextra -Wno-unknown-pragmas -Ofast -s -fno-ident -march=native -flto -DNDEBUG".split()],
                 debug_defines=[], release_defines=['NDEBUG']):
        self.name = '_'.join(name.split())
        self.c3po = c3po
        self.targets = targets
        self.debug_flags = debug_flags
        self.release_flags = release_flags
        self.debug_defines = debug_defines
        self.release_defines = release_defines

    def add_target(self, name, **kwargs):
        self.targets[name] = Target(name, c3po=self.c3po, **kwargs)
        return self.targets[name]

    def __str__(self):
        return '''(
{}
targets: [
    {}
]
c3po: {}
dflags: {}
rflags: {}
ddefs: {}
rdefs: {}
)'''.format(
    self.name,
    ',\n'.join("\n    ".join(str(self.targets[t]).split('\n')) for t in self.targets),
    self.c3po,
    self.debug_flags,
    self.release_flags,
    self.debug_defines,
    self.release_defines)

    def compile(self):
        cmakelines = ["""#autogenerated by ACRONYM
#changes should be done through the utility to avoid overwrites

cmake_minimum_required(VERSION 3.9.0)
project({0})

#default to release
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "" FORCE)
endif()

#clear defaults
set(CMAKE_C_FLAGS_DEBUG "{1}")
set(CMAKE_C_FLAGS_RELEASE "{2}")

#set some standards
set(CMAKE_C_STANDARD 11)
add_definitions(-D_POSIX_C_SOURCE=200809L -D_DEFAULT_SOURCE)

#ensure IPO and LTO is avalible
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_LINK_WHAT_YOU_USE ON)
include(CheckIPOSupported)
check_ipo_supported(RESULT ipo_supported OUTPUT error)
if(ipo_supported)
    set(CMAKE_INTERPROCEDURAL_OPTIMIZATION_RELEASE ON)
else()
    message(STATUS "IPO / LTO not supported: <${{error}}>")
endif()

#update/pull git submodules
find_package(Git QUIET)
if(GIT_FOUND AND EXISTS "${{PROJECT_SOURCE_DIR}}/.git")
# Update submodules as needed
    option(GIT_SUBMODULE "Check submodules during build" ON)
    if(GIT_SUBMODULE)
        message(STATUS "Submodule update")
        execute_process(COMMAND ${{GIT_EXECUTABLE}} submodule update --init --recursive
                        WORKING_DIRECTORY ${{CMAKE_CURRENT_SOURCE_DIR}}
                        RESULT_VARIABLE GIT_SUBMOD_RESULT)
        if(NOT GIT_SUBMOD_RESULT EQUAL "0")
            message(FATAL_ERROR "git submodule update --init failed with ${{GIT_SUBMOD_RESULT}}, please checkout submodules")
        endif()
    endif()
endif()
""".format(self.name, ' '.join(self.debug_flags), ' '.join(self.release_flags))]

        if self.debug_defines:
            cmakelines.append("set(DEBUG_DEFINES {})".format(' '.join(self.debug_defines)))

        if self.release_defines:
            cmakelines.append("set(RELEASE_DEFINES {})".format(' '.join(self.release_defines)))

        cmakelines.append(dr_check("add_definitions(${DEBUG_DEFINES})",
                                    "add_definitions(${RELEASE_DEFINES})"))

        for target in self.targets:
            cmakelines.append("")
            cmakelines.append(self.targets[target].compile())

        cmakelines.append("")
        return '\n'.join(cmakelines)


class Target():
    def __init__(self, name,  c3po=True, files=[], libraries=[], includes=[], debug_flags=[], debug_defines=[], release_flags=[], release_defines=[]):
        self.name = '_'.join(name.split())
        self.c3po = c3po
        self.files = files
        self.libraries= libraries
        self.includes = includes
        self.debug_flags = debug_flags
        self.release_flags = release_flags
        self.debug_defines = debug_defines
        self.release_defines = release_defines

    def __str__(self):
        return '''(
>{}<
c3po: {}
files: {}
libs: {}
inc: {}
dflags: {}
rflags: {}
ddefs: {}
rdefs: {}
)'''.format(
    self.name,
    self.c3po,
    self.files,
    self.libraries,
    self.includes,
    self.debug_flags,
    self.release_flags,
    self.debug_defines,
    self.release_defines)

    def compile(self):
        targetlines = ["#{} specific configuration".format(self.name)]

        if not self.files:
            targetlines.append("#no files in target, skipped")
            return "\n".join(targetlines)

        targetlines.append("set({}_SOURCES\n    {})".format(self.name, '\n    '.join("\"{}\"".format(file) for file in self.files)))

        targetlines.append("add_executable({0} ${{{0}_SOURCES}})".format(self.name))

        if self.c3po:
            targetlines.append("add_executable({0}d ${{{0}_SOURCES}})".format(self.name))
            targetlines.append('add_custom_target(gen_{0} ALL COMMAND python3 "${{PROJECT_SOURCE_DIR}}/c3po.py" "build" "-s" "${{PROJECT_SOURCE_DIR}}/src" "-o" "${{PROJECT_SOURCE_DIR}}/gen")'.format(self.name))
            targetlines.append("add_dependencies(gen_{0} {0}d)".format(self.name))
            targetlines.append("add_dependencies({0} gen_{0})".format(self.name))
            targetlines.append('add_custom_target(post_{0} ALL COMMAND python3 ${{PROJECT_SOURCE_DIR}}/c3po.py "post" "-s" "${{PROJECT_BINARY_DIR}}/{0}")'.format(self.name))
            targetlines.append("add_dependencies(post_{0} {0})".format(self.name))

        if self.debug_flags:
            targetlines.append("set({}_DEBUG {})".format(self.name, ' '.join(self.debug_flags)))

        if self.release_flags:
            targetlines.append("set({}_RELEASE {})".format(self.name, ' '.join(self.release_flags)))

        if self.debug_defines:
            targetlines.append("set({}_DEBUG_DEFINES {})".format(self.name, ' '.join(self.debug_defines)))

        if self.release_defines:
            targetlines.append("set({}_RELEASE_DEFINES {})".format(self.name, ' '.join(self.release_defines)))

        if self.includes:
            targetlines.append("target_include_directories({} PUBLIC {})".format(self.name, ' '.join(include for include in self.includes)))

        if self.libraries:
            targetlines.append("target_link_libraries({} PRIVATE {})".format(self.name, ' '.join(library for library in self.libraries)))

        targetlines.append(dr_check("target_compile_options({0} PRIVATE ${{{0}_DEBUG}})".format(self.name),
                                    "target_compile_options({0} PRIVATE ${{{0}_RELEASE}})".format(self.name)))

        targetlines.append(dr_check("target_compile_definitions({0} PRIVATE ${{{0}_DEBUG_DEFINES}})".format(self.name),
                                    "target_compile_definitions({0} PRIVATE ${{{0}_RELEASE_DEFINES}})".format(self.name)))

        return "\n".join(targetlines)
