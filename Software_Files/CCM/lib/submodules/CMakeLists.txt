add_library(rfm69 ./RFM69/RFM69.c)

target_link_libraries(rfm69 pico_stdlib)

target_include_directories(rfm69 PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/RFM69)