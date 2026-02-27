cmake_minimum_required(VERSION 3.31)

if(POLICY CMP0091)
    cmake_policy(SET CMP0091 NEW)
endif()

project(ctp_bridge_native VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON CACHE BOOL "Export compile_commands.json" FORCE)

option(CTP_STRICT_LINK "Fail configure when Thost native libs are missing" OFF)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)

execute_process(
    COMMAND "${Python3_EXECUTABLE}" -m pybind11 --cmakedir
    OUTPUT_VARIABLE _pybind11_cmake_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE
    COMMAND_ERROR_IS_FATAL ANY
)
set(pybind11_DIR "${_pybind11_cmake_dir}" CACHE PATH "pybind11 CMake config dir")
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(ctp_bridge_native src/py_module.cpp)

target_compile_features(ctp_bridge_native PRIVATE cxx_std_23)
set_target_properties(ctp_bridge_native PROPERTIES
    CXX_EXTENSIONS OFF
)

if(MSVC)
    target_compile_options(ctp_bridge_native PRIVATE /std:c++latest /utf-8 /bigobj /EHsc)
endif()

if(WIN32)
    set(THOST_API_DIR "${CMAKE_CURRENT_SOURCE_DIR}/api/win")
elseif(UNIX)
    set(THOST_API_DIR "${CMAKE_CURRENT_SOURCE_DIR}/api/linux")
else()
    message(FATAL_ERROR "Unsupported platform for Thost API")
endif()

target_include_directories(ctp_bridge_native PRIVATE
    "$<BUILD_INTERFACE:${THOST_API_DIR}>"
)

if(WIN32)
    set(THOST_TRADER_LIB "${THOST_API_DIR}/thosttraderapi_se.lib")
    set(THOST_MD_LIB "${THOST_API_DIR}/thostmduserapi_se.lib")
    if(EXISTS "${THOST_TRADER_LIB}" AND EXISTS "${THOST_MD_LIB}")
        target_link_libraries(ctp_bridge_native PRIVATE
            "${THOST_TRADER_LIB}"
            "${THOST_MD_LIB}"
        )
    elseif(CTP_STRICT_LINK)
        message(FATAL_ERROR "Thost .lib files not found under ${THOST_API_DIR}")
    else()
        message(WARNING "Thost .lib files not found under ${THOST_API_DIR}, build will use header-only skeleton.")
    endif()
endif()

if(UNIX)
    set(THOST_TRADER_SO "${THOST_API_DIR}/thosttraderapi_se.so")
    set(THOST_MD_SO "${THOST_API_DIR}/thostmduserapi_se.so")
    if(EXISTS "${THOST_TRADER_SO}" AND EXISTS "${THOST_MD_SO}")
        # 使用 -l:filename 兼容非 lib*.so 命名，并通过 target_link_libraries 保证库顺序正确
        target_link_directories(ctp_bridge_native PRIVATE "${THOST_API_DIR}")
        target_link_libraries(ctp_bridge_native PRIVATE
            "-l:thosttraderapi_se.so"
            "-l:thostmduserapi_se.so"
        )
        set_target_properties(ctp_bridge_native PROPERTIES
            BUILD_RPATH "${THOST_API_DIR}"
            INSTALL_RPATH "$ORIGIN/native/ctp_bridge/api/linux;$ORIGIN"
        )
    elseif(CTP_STRICT_LINK)
        message(FATAL_ERROR "Thost .so files not found under ${THOST_API_DIR}")
    else()
        message(WARNING "Thost .so files not found under ${THOST_API_DIR}, build will use header-only skeleton.")
    endif()
endif()
