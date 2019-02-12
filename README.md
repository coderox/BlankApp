# Use CMake and C++/WinRT to build UWP Xaml apps

This small sample demonstrates some of the issues that currently exists when trying to leverage CMake to generate a UWP solution built with C++/WinRT. The sample is originally based on the C++/WinRT BlankApp sample and I've tried as much as possible to not change the source files. The existing BlankApp.sln can be opened in Visual Studio 2017 or Visual Studio 2019 and will build as is.

If you want to generate a pure CMake solution (either by overwriting the current project files or in a separate directory) here is the steps required.

1. Install [CMake](https://cmake.org)

2. Clone this repo

`git clone https://github.com/coderox/BlankApp.git`

3. Change into the cloned directory and update submodules

`cd BlankApp`

`git submodules update`

4. Build a custom version of CMake
There are a couple of issues with the current CMake releases that requires manual steps, or this minor update to CMake which fixes this by adding two features. The updated CMake doesn't modify the MIDL settings for the project, and it also makes the required sources files to be dependent on appropriate files. This requires us to build CMake with CMake as follows:

`cd CMake`

`cmake .`

`cmake --build`

`cd ..`

5. Generate the solution

`mkdir output`

`cd output`

`..\CMake\bin\debug\cmake.exe -DCMAKE_SYSTEM_NAME="WindowsStore" -DCMAKE_SYSTEM_VERSION="10.0" ..`

6. Add C++/WinRT nuget package
We also need to manually add the C++/WinRT nuget package to be able to build the solution, I have tried to leverage the existing packages.config but `nuget restore` fails to integrate the required elements into the .vcxproj. Open the solution in Visual Studio 2017 or Visual Studio 2019 and add the following C++/WinRT nuget package:

Microsoft.Windows.CppWinRT

7. Build and run the solution

# Why do I need a custom CMake?
There are two issues I haven't found a way to mitigate without a custom CMake version.

The first issue is that since we are adding .IDL files in the solution, CMake will automatically add a <MIDL>...</MIDL> element in the project file and the properties included in this section will break the C++/WinRT generation. This is now being handled in the CMakeLists.txt by specifying a property on the target called VS_CPPWINRT (which is set to true). Line 65 in CMakeLists.txt

The second issue is that C++/WinRT requires the header files to be dependent upon the appropriate .xaml files, otherwise the header files will not be #included in the XamlTypeInfo.g.cpp. Hence in CMakeLists.txt I add some properties to the .h-files through leveraging the OBJECT_DEPENDS . Line 63 and 64 in CMakeLists.txt