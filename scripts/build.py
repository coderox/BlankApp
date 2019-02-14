import subprocess
import cppwinrt

# move into the correct directory
# subprocess.call(["cd","output"])

# generate project with cmake
subprocess.call(["../CMake/bin/debug/cmake.exe","-DCMAKE_SYSTEM_NAME='WindowsStore'","-DCMAKE_SYSTEM_VERSION='10.0'", ".."])

# restore nuget package
subprocess.call(["../tools/nuget.exe","restore"])

# inject cppwinrt nuget xml into .vcxproj
cppwinrt.inject_nuget_xml("./BlankApp.vcxproj", "1.0.190211.5")

# build project with cmake
subprocess.call(["cmake","--build","."])