#ifndef CONTROLS_H
#define CONTROLS_H

#include "pico/stdlib.h"
#include "stdint.h"

#include "global_data.h"

void controls_init(void);
void motor_control(void);
void power_control(void);
void warning_lights_control(void);


void controls_task_005ms(void);
void controls_task_010ms(void);
void controls_task_100ms(void);

#endif //CONTROLS_H