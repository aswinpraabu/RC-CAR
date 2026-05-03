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
    // Placeholder for motor control logic
}

void power_control(void)
{
    // Placeholder for power control logic
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
