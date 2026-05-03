#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/spi.h"
#include "hardware/i2c.h"
#include "hardware/timer.h"
#include "hardware/uart.h"

#include "global_data.h"
#include "hw_drivers.h"
#include "rf_comms.h"
#include "controls.h"


void initialize_system(void) {
    stdio_init_all();
    hw_drivers_init();
    rf_comms_init();
    controls_init();
}

void task_005ms(void) {
    rf_comms_task_005ms();
    hw_drivers_task_005ms();
    controls_task_005ms();
    
}
void task_010ms(void) {
    hw_drivers_task_010ms();
    controls_task_010ms();
    
}
void task_100ms(void) {
    hw_drivers_task_100ms();
}

int main() {
    initialize_system();
    absolute_time_t task_005ms_time, task_010ms_time, task_100ms_time, debug_task_time;
    task_005ms_time = task_010ms_time = task_100ms_time = debug_task_time = get_absolute_time();
    uint8_t led_state = 1;

    sleep_ms(1000); // Wait for system to stabilize

    servo_set_angle(45);

    pico_set_led(led_state);

    

    while (true) {
        if(absolute_time_diff_us(task_005ms_time, get_absolute_time()) >= 5*1000) {
            task_005ms();
            task_005ms_time = get_absolute_time();
        }
        if(absolute_time_diff_us(task_010ms_time, get_absolute_time()) >= 10*1000) {
            task_010ms();
            task_010ms_time = get_absolute_time();
        }
        if(absolute_time_diff_us(task_100ms_time, get_absolute_time()) >= 100*1000) {
            task_100ms();
            task_100ms_time = get_absolute_time();



        }
        if(absolute_time_diff_us(debug_task_time, get_absolute_time()) >= 3*1000*1000) {
            pico_set_led(led_state);
            led_state = !led_state;

            rf_comms_task_debug(); // Call debug task to print received data every 3 seconds
            hw_drivers_task_debug(); // Call debug task to print hardware status every 3 seconds

            //printf("Debug Task: Turn Angle = %d, Throttle = %d\n", global_rf_comms_data.rx_turn_angle, global_rf_comms_data.rx_throttle);
            //printf("Debug Task: Car Throttle = %d, Car Turn Angle = %d, Power Status = %d\n", global_controls_data.car_throttle, global_controls_data.car_turn_angle, global_controls_data.ccm_power_state);
            debug_task_time = get_absolute_time();
        }
    }
}