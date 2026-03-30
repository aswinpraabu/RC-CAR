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
    //rf_comms_init();
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
        if(absolute_time_diff_us(debug_task_time, get_absolute_time()) >= 3*1000*1000) {
            pico_set_led(led_state);
            led_state = !led_state;

            printf("Hello, world!\n");

            //servo_set_angle(90 * (led_state ? 1 : -1));
            //rf_comms_task_005ms();
            debug_task_time = get_absolute_time();
            //rf_comms_init(); // Re-initialize RF communications every 2 seconds for testing
            //uint32_t temp = 0;//RFM69_readTemperature(1); // Read frequency for testing
            //RFM69_setNetwork(0x1234); // Set network ID for testing
            //uint32_t frequency = RFM69_readReg(0x2F); // Read frequency for testing
            //RFM69_readReg(0x30); // Read frequency for testing
            //RFM69_readReg(0x14); // Read frequency for testing
            //RFM69_readReg(0x15); // Read frequency for testing

            //RFM69_readRSSI(0); // Read frequency for testing
            //RFM69_writeReg(0x24, 0x12); // Write frequency for testing
            //RFM69_readReg(0x01); // Read frequency for testing
            //printf("Temperature: %d C, Frequency: %X Hz\n", temp, frequency);
        }
    }
}