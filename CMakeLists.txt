cmake_minimum_required(VERSION 3.8)
project(BlankApp)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

configure_file(module.g.cpp "${CMAKE_BINARY_DIR}/Generated Files/module.g.cpp" COPYONLY)
configure_file(packages.config "${CMAKE_BINARY_DIR}/packages.config" COPYONLY)

set(SOURCE_FILES
  App.cpp
  MainPage.cpp
  pch.cpp
  "${CMAKE_BINARY_DIR}/Generated Files/module.g.cpp"
  )

set(HEADER_FILES
  App.h
  MainPage.h
  pch.h
  )

set(XAML_FILES
  App.xaml
  MainPage.xaml
  )

set(IDL_FILES
  App.idl
  MainPage.idl
  )

set(ASSET_FILES
    Assets/LockScreenLogo.scale-200.png
    Assets/SplashScreen.scale-200.png
    Assets/Square44x44Logo.scale-200.png
    Assets/Square44x44Logo.targetsize-24_altform-unplated.png
    Assets/Square150x150Logo.scale-200.png
    Assets/StoreLogo.png
    Assets/Wide310x150Logo.scale-200.png
    )

set(CONTENT_FILES
    Package.appxmanifest
    )

set(RESOURCE_FILES
  ${CONTENT_FILES} ${ASSET_FILES}
  "${CMAKE_BINARY_DIR}/packages.config"
  BlankApp_TemporaryKey.pfx)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

set_property(SOURCE ${CONTENT_FILES} PROPERTY VS_DEPLOYMENT_CONTENT 1)
set_property(SOURCE ${ASSET_FILES} PROPERTY VS_DEPLOYMENT_CONTENT 1)
set_property(SOURCE ${ASSET_FILES} PROPERTY VS_DEPLOYMENT_LOCATION "Assets")

set_property(SOURCE "App.xaml" PROPERTY VS_XAML_TYPE "ApplicationDefinition")

add_executable(BlankApp WIN32 ${SOURCE_FILES} ${HEADER_FILES} ${RESOURCE_FILES} ${XAML_FILES} ${IDL_FILES})

set_source_files_properties(pch.cpp PROPERTIES COMPILE_FLAGS "/Ycpch.h")
set_target_properties(BlankApp PROPERTIES COMPILE_FLAGS "/Yupch.h")

#### CUSTOM CMAKE STEPS
set_source_files_properties(App.h PROPERTIES OBJECT_DEPENDS "App.xaml")
set_source_files_properties(MainPage.h PROPERTIES OBJECT_DEPENDS "MainPage.xaml")
set_target_properties(BlankApp PROPERTIES VS_CPPWINRT true)
#### END CUSTOM CMAKE STEPS

set_target_properties(BlankApp PROPERTIES VS_GLOBAL_ROOTNAMESPACE BlankApp)
set_target_properties(BlankApp PROPERTIES CXX_STANDARD 17)

SET(CPPWINRT_REQUIRED_COMPILER_FLAGS "/std:c++latest /await")
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CPPWINRT_REQUIRED_COMPILER_FLAGS}")

set_property(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT BlankApp)

add_custom_command(TARGET BlankApp
  PRE_BUILD
  COMMAND ../tools/nuget.exe restore ${CMAKE_BINARY_DIR}/BlankApp.sln
)