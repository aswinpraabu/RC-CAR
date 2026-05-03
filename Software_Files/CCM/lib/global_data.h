#ifndef GLOBAL_DATA_H
#define GLOBAL_DATA_H

#include "pico/stdlib.h"
#include "stdio.h"
#include "stdint.h"

enum ccm_power_state {
    CCM_POWERSTATE_SHUTDOWN = 0,
    CCM_POWERSTATE_RUNNING = 1,
    CCM_POWERSTATE_PRE_SHUTDOWN = 2
};

struct rf_comms_data
{
    int8_t rx_throttle;
    int8_t rx_turn_angle;
    uint8_t rx_shutdown_flag;
    bool rx_validity_flag;
};

struct controls_data
{
    int8_t car_throttle;
    int8_t car_turn_angle;
    
    bool led1_bat_low;
    bool led2_loc_rcm;

    enum ccm_power_state ccm_power_state; 
};

extern struct rf_comms_data global_rf_comms_data;
extern struct controls_data global_controls_data;

#endif //GLOBAL_DATA_H