#ifndef GLOBAL_DATA_H
#define GLOBAL_DATA_H

#include "pico/stdlib.h"
#include "stdio.h"
#include "stdint.h"

struct rf_comms_data
{
    int8_t rx_throttle;
    int8_t rx_turn_angle;
    uint8_t rx_shutdown_flag;
};

extern struct rf_comms_data global_rf_comms_data;

#endif //GLOBAL_DATA_H