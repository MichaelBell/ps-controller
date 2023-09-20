cmake_minimum_required(VERSION 3.12)

# Change your executable name to something creative!
set(NAME ps-controller) # <-- Name your project/executable here!

#include(pimoroni_pico_import.cmake)
include(pico_sdk_import.cmake)

# Gooey boilerplate
project(${NAME} C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

#set(PICO_COPY_TO_RAM 1)

# Initialize the SDK
pico_sdk_init()

set(PICOSYSTEM_DIR ${CMAKE_CURRENT_LIST_DIR}/../picosystem/)
find_package(PICOSYSTEM REQUIRED)

add_compile_options(-Wall
        -Wno-format
        -Wno-unused-function
        -Wno-maybe-uninitialized
        )

# Add your source files
picosystem_executable(${NAME}
	control.cpp
)

target_link_libraries(${NAME} pico_multicore)

pixel_double(${NAME})

