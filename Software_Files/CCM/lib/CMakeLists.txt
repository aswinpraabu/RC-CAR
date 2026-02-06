add_library(hw_drivers hw_drivers.c)
add_library(rf_comms rf_comms.c)
add_library(ina260 ina260_sensor.c)

target_link_libraries(hw_drivers pico_stdlib pico_cyw43_arch_none hardware_pwm ina260)
target_link_libraries(rf_comms pico_stdlib)
target_link_libraries(ina260 pico_stdlib hardware_i2c)

target_include_directories(hw_drivers PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_include_directories(rf_comms PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_include_directories(ina260 PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})