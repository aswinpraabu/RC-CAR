#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/spi.h"
#include "hardware/i2c.h"
#include "hardware/timer.h"
#include "hardware/uart.h"

#include "hw_drivers.h"
#include "rf_comms.h"



void initialize_system(void) {
    stdio_init_all();
    hw_drivers_init();
}

void task_005ms(void) {
    
}
void task_010ms(void) {
    
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
        if(absolute_time_diff_us(debug_task_time, get_absolute_time()) >= 2*1000000) {
            pico_set_led(led_state);
            led_state = !led_state;

            //printf("Hello, world!\n");

            //servo_set_angle(90 * (led_state ? 1 : -1));

            debug_task_time = get_absolute_time();
        }
    }
}