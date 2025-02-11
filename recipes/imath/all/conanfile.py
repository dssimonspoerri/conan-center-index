from conans import ConanFile, CMake, tools
import os, functools

required_conan_version = ">=1.33.0"

class ImathConan(ConanFile):
    name = "imath"
    description = "Imath is a C++ and python library of 2D and 3D vector, matrix, and math operations for computer graphics."
    license = "BSD-3-Clause"
    homepage = "https://github.com/AcademySoftwareFoundation/Imath"
    url = "https://github.com/conan-io/conan-center-index"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    generators = "cmake", "cmake_find_package"
    exports_sources = ["CMakeLists.txt"]
    topics = ("computer-graphics", "matrix", "openexr", "3d-vector")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
    
    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            tools.check_min_cppstd(self, 11)

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  destination=self._source_subfolder, strip_root=True)

    @functools.lru_cache(1)
    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cm = self._configure_cmake()
        cm.build()

    def package(self):
        cm = self._configure_cmake()
        cm.install()

        tools.rmdir(os.path.join(self.package_folder, "cmake"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

        self.copy("LICENSE.md", src=self._source_subfolder, dst="licenses")

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "Imath"
        self.cpp_info.names["cmake_find_package_multi"] = "Imath"
        self.cpp_info.names["pkg_config"] = "Imath"

        # Imath::ImathConfig - header only library
        imath_config = self.cpp_info.components["imath_config"]
        imath_config.names["cmake_find_package"] = "ImathConfig"
        imath_config.names["cmake_find_package_multi"] = "ImathConfig"
        imath_config.names["pkg_config"] = "ImathConfig"
        imath_config.includedirs.append(os.path.join("include", "Imath"))

        # Imath::Imath - linkable library
        imath_lib = self.cpp_info.components["imath_lib"]
        imath_lib.names["cmake_find_package"] = "Imath"
        imath_lib.names["cmake_find_package_multi"] = "Imath"
        imath_lib.names["pkg_config"] = "Imath"
        imath_lib.libs = tools.collect_libs(self)
        imath_lib.requires = ["imath_config"]
