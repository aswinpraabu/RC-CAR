#ifndef HW_DRIVERS_H
#define HW_DRIVERS_H

#include "pico/stdlib.h"
#include "pin_config.h"
#include "hardware/pwm.h"
#include "ina260_sensor.h"

// Pico W devices use a GPIO on the WIFI chip for the LED,
// so when building for Pico W, CYW43_WL_GPIO_LED_PIN will be defined
#ifdef CYW43_WL_GPIO_LED_PIN
#include "pico/cyw43_arch.h"
#endif



#pragma region Servo_Definitions
#define SERVO_MIN_ANGLE -90.0  // Minimum angle
#define SERVO_MAX_ANGLE 90.0 // Maximum angle
#define SERVO_FREQ 50 // Frequency for servo PWM in Hz

#define SERVO_MIN_DUTY_OFFSET_MS -0.5344   // Offset for minimum duty cycle in milliseconds
#define SERVO_MAX_DUTY_OFFSET_MS 0.57  // Offset for maximum duty cycle in milliseconds
#define SERVO_MIN_DUTY_MS (1.0 + SERVO_MIN_DUTY_OFFSET_MS) // (1ms) Minimum duty cycle in microseconds + offset
#define SERVO_MAX_DUTY_MS (2.0 + SERVO_MAX_DUTY_OFFSET_MS) // (2ms)Maximum duty cycle in microseconds + offset

#define SERVO_PWM_CLK_HZ 1000000 // PWM clock frequency in Hz

void servo_init(void);
void servo_set_angle(int8_t angle);
void servo_angle_to_duty_ns(int8_t angle);

#pragma endregion Servo_Definitions


#define INA260_ADDR 0x40
void INA260_init(uint8_t i2caddr);

int pico_led_init(void);
void pico_set_led(bool led_on);


void hw_drivers_init(void);
void hw_drivers_task_005ms(void);
void hw_drivers_task_010ms(void);
void hw_drivers_task_100ms(void);

uint16_t read_battery_voltage_mv(void);
uint16_t read_battery_current_ma(void);

void hw_drivers_diagnostics(void);

#endif // HW_DRIVERS_H