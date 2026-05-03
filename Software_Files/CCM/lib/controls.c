#include "controls.h"

struct controls_data global_controls_data;

void controls_init(void)
{
    global_controls_data.car_throttle = 0;
    global_controls_data.car_turn_angle = 0;
    global_controls_data.led1_bat_low = false;
    global_controls_data.led2_loc_rcm = false;
    global_controls_data.ccm_power_state = CCM_POWERSTATE_RUNNING;
}

void motor_control(void)
{
    bool comms_data_check = global_rf_comms_data.rx_validity_flag;
    bool power_mode_check = global_controls_data.ccm_power_state == CCM_POWERSTATE_RUNNING;
    //bool safety_check = hw_drivers_data.battery_voltage_low_critical_diag.get_status() != DIAG_STATUS.FAIL;
    bool safety_check = true; // Placeholder for safety check, replace with actual diagnostic status check
    bool drive_enable = comms_data_check && power_mode_check && safety_check;

    if(drive_enable) {
        global_controls_data.car_throttle = global_rf_comms_data.rx_throttle;
        global_controls_data.car_turn_angle = global_rf_comms_data.rx_turn_angle;
    } else {
        global_controls_data.car_throttle = 0;
        global_controls_data.car_turn_angle = 0;
    }
}

void power_control(void)
{
    
}

void warning_lights_control(void)
{
    // Placeholder for warning lights control logic
}

void controls_task_005ms(void)
{
    motor_control();
}

void controls_task_010ms(void)
{
    // Placeholder for tasks that need to run every 10ms
}

void controls_task_100ms(void)
{
    power_control();
    warning_lights_control();
}
