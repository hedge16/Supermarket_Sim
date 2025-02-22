cmake_minimum_required(VERSION 3.30)
project(progettoSupermercato C)

set(CMAKE_C_STANDARD 11)

add_executable(progettoSupermercato server.c queue.c
        colors.h)
