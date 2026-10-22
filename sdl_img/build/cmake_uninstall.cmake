if (NOT EXISTS "E:/Livter_Game/Game/sdl_img/build/install_manifest.txt")
    message(FATAL_ERROR "Cannot find install manifest: \"E:/Livter_Game/Game/sdl_img/build/install_manifest.txt\"")
endif()

file(READ "E:/Livter_Game/Game/sdl_img/build/install_manifest.txt" files)
string(REGEX REPLACE "\n" ";" files "${files}")
foreach(file ${files})
    message(STATUS "Uninstalling \"$ENV{DESTDIR}${file}\"")
    execute_process(
        COMMAND E:/Cpp_compiler/w64devkit/bin/cmake.exe -E remove "$ENV{DESTDIR}${file}"
        OUTPUT_VARIABLE rm_out
        RESULT_VARIABLE rm_retval
    )
    if(NOT ${rm_retval} EQUAL 0)
        message(FATAL_ERROR "Problem when removing \"$ENV{DESTDIR}${file}\"")
    endif (NOT ${rm_retval} EQUAL 0)
endforeach()
