#include "hw_drivers.h"


/**
 * @brief Initialize the servo motor by configuring the PWM hardware and setting the initial position.
 * @note
 * `SERVO_PWM_CLK_HZ` - This is the frequency of the clock driving the PWM hardware. 

 * `SERVO_FREQ` - This is the frequency of the actual PWM signal sent to the servo. A common value for hobby servos is 50Hz (20ms period).
 * 
 * `SYS_CLK_HZ` - This is the frequency of the system clock. 
 * 
 * To achieve a specific PWM frequency, we need to set the PWM clock divider and the wrap value appropriately.
 * 
 * The pwm clock will count up at a rate of `SERVO_PWM_CLK_HZ`, and reset to 0 after it reaches the wrap value set by `pwm_set_wrap`. 
 * To achieve a PWM signal of frequency `SERVO_FREQ`, we need the period of the PWM signal (in seconds) to be the inverse of `SERVO_FREQ`,
 * which means the number of clock cycles in one period should be `SERVO_PWM_CLK_HZ / SERVO_FREQ`. 
 * Therefore, we set the wrap value to `SERVO_PWM_CLK_HZ / SERVO_FREQ - 1` (subtracting 1 because the count starts at 0).
 * 
 * The system clock is divided down with `pwm_set_clkdiv`
 * The PWM Period is set with `pwm_set_wrap`. The period clock cycles
 * The duty cycle is set with `pwm_set_gpio_level`, which sets the number of clock cycles the signal is high for.
 * 
 */
void servo_init(void) {
    // Initialize PWM for servo control
    pwm_config config = pwm_get_default_config();
    uint8_t slice_num = pwm_gpio_to_slice_num(SERVO_PIN);
    uint8_t channel = pwm_gpio_to_channel(SERVO_PIN);

    gpio_set_function(SERVO_PIN, GPIO_FUNC_PWM);
    
    /*
        * Divider calculated from:
        * Final clock frequency = system clock frequency / divider
        * 
    */
    pwm_set_clkdiv(slice_num, SYS_CLK_HZ / SERVO_PWM_CLK_HZ);

    pwm_set_wrap(slice_num, SERVO_PWM_CLK_HZ / SERVO_FREQ - 1); // Set wrap value based on frequency

    servo_set_angle(0); // Set to neutral position
    pwm_set_enabled(slice_num, true);
    
}

void servo_set_angle(int8_t angle) {
    // Constrain angle to valid range
    if (angle < SERVO_MIN_ANGLE) angle = SERVO_MIN_ANGLE;
    if (angle > SERVO_MAX_ANGLE) angle = SERVO_MAX_ANGLE;

    float duty_ms = SERVO_MIN_DUTY_MS + ((angle - SERVO_MIN_ANGLE) / (SERVO_MAX_ANGLE - SERVO_MIN_ANGLE)) * (SERVO_MAX_DUTY_MS - SERVO_MIN_DUTY_MS);
    
    uint32_t duty_cycle = (uint32_t)((duty_ms / 1e3) * (SERVO_PWM_CLK_HZ)); // Convert milliseconds to clock cycles

    pwm_set_gpio_level(SERVO_PIN, duty_cycle);
    //printf("Servo angle set to %d degrees (duty cycle: %u, duty_ms: %f)\n", angle, duty_cycle, duty_ms);
}

#pragma region DC_Motor

/**
 * @brief Initialize GPIO pins for DC motor control and set up PWM for motor speed control.
 * 
 */
void dc_motor_init(void) {
    // Initialize GPIO for DC motor control
    uint8_t motor_fwd_pin_slice_num = pwm_gpio_to_slice_num(MOTOR_FWD_PIN);
    uint8_t motor_rev_pin_slice_num = pwm_gpio_to_slice_num(MOTOR_REV_PIN);

    gpio_set_function(MOTOR_FWD_PIN, GPIO_FUNC_PWM);
    gpio_set_function(MOTOR_REV_PIN, GPIO_FUNC_PWM);

    pwm_set_clkdiv(motor_fwd_pin_slice_num, SYS_CLK_HZ / MOTOR_PWM_CLK_HZ);
    pwm_set_clkdiv(motor_rev_pin_slice_num, SYS_CLK_HZ / MOTOR_PWM_CLK_HZ);

    pwm_set_wrap(motor_fwd_pin_slice_num, MOTOR_PWM_CLK_HZ / MOTOR_PWM_FREQ - 1); // Set wrap value based on frequency
    pwm_set_wrap(motor_rev_pin_slice_num, MOTOR_PWM_CLK_HZ / MOTOR_PWM_FREQ - 1); // Set wrap value based on frequency

    dc_motor_set_power(0); // Set to neutral position
    
    pwm_set_enabled(motor_fwd_pin_slice_num, true);
    pwm_set_enabled(motor_rev_pin_slice_num, true);
}


/**
 * @brief drive the motor based on power percentage
 * @param power Power level as a percentage (-100 to 100)
 * Positive power values correspond to forward motion, negative values correspond to reverse motion.
 */
void dc_motor_set_power(int8_t power) {
    // Constrain power to valid range
    if (power < -100) power = -100;
    if (power > 100) power = 100;

    if (power > 0) {
        pwm_set_gpio_level(MOTOR_FWD_PIN, _dc_motor_power_to_duty_cycle(power));
        pwm_set_gpio_level(MOTOR_REV_PIN, 0);
    } else if (power < 0) {
        pwm_set_gpio_level(MOTOR_FWD_PIN, 0);
        pwm_set_gpio_level(MOTOR_REV_PIN, _dc_motor_power_to_duty_cycle(power));
    } else {
        pwm_set_gpio_level(MOTOR_FWD_PIN, 0);
        pwm_set_gpio_level(MOTOR_REV_PIN, 0);
    }
}


/**
* @brief Convert power percentage to duty cycle, applying a deadzone to ensure minimum power is delivered to overcome motor stiction.
* @param power Power level as a percentage (-100 to 100)
* @return Duty cycle value
*/
uint32_t _dc_motor_power_to_duty_cycle(int8_t power) {

    float scale_factor = (100.0 - MOTOR_MIN_ABS_POWER) / 100.0; // Scale factor to apply deadzone
    float scaled_power = abs(power)*scale_factor + MOTOR_MIN_ABS_POWER; // Apply deadzone

    uint32_t duty_cycle = (uint32_t)((scaled_power / 100.0) * (MOTOR_PWM_CLK_HZ / MOTOR_PWM_FREQ)); // Convert percentage to clock cycles

    return duty_cycle;
}


void motor_control_task(void) {
    dc_motor_set_power(global_controls_data.car_throttle);
    servo_set_angle(global_controls_data.car_turn_angle);

}
#pragma endregion DC_Motor


// Perform initialisation
int pico_led_init(void) {
  // For Pico W devices we need to initialise the driver etc
    return cyw43_arch_init();

}

// Turn the led on or off
void pico_set_led(bool led_on) {
    // Ask the wifi "driver" to set the GPIO on or off
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, led_on);
}

#pragma region INA260_REGION
/* Platform specific functions for INA260*/

// All register sizes in INA260 are 2 bytes (16 bits)
void _INA260_writeRegister(uint8_t reg, uint16_t value) {
    // Write to register code
    int ret;
    uint8_t txdata[3];
    txdata[0] = reg;
    txdata[1] = (value >> 8) & 0xFF;
    txdata[2] = value & 0xFF;
    ret = i2c_write_blocking(i2c0, INA260_I2CADDR_DEFAULT, txdata, 3, false);
}
uint16_t _INA260_readRegister(uint8_t reg) {
    // Read from register code
    int ret;
    uint8_t rxdata[2];
    ret = i2c_write_blocking(i2c0, INA260_I2CADDR_DEFAULT, &reg, 1, true);
    ret = i2c_read_blocking(i2c0, INA260_I2CADDR_DEFAULT, rxdata, 2, false);
    return (rxdata[0] << 8) | rxdata[1];
}

void INA260_init(uint8_t i2caddr) {
    // Initialization code for INA260 sensor
    i2c_init(i2c0, 400000); // Initialize I2C at 400kHz
    gpio_set_function(I2C_SDA_PIN, GPIO_FUNC_I2C);
    gpio_set_function(I2C_SCL_PIN, GPIO_FUNC_I2C);
    gpio_pull_up(I2C_SDA_PIN);
    gpio_pull_up(I2C_SCL_PIN);
    printf("INA260 initialized at I2C address 0x%02X\n", i2caddr);

    INA260_setConfigRegisterPhys(INA260_AVERAGING_4,
                                INA260_CONVERSIONTIME_8244_US,
                                INA260_CONVERSIONTIME_1100_US,
                                INA260_MODE_CURRENT_AND_VOLTAGE_CONTINUOUS);
    
}
#pragma endregion INA260_REGION

void gpio_inits(){
    gpio_init(POWER_ON_PIN_NUM);
    gpio_set_dir(POWER_ON_PIN_NUM,GPIO_OUT);
    gpio_put(POWER_ON_PIN_NUM,true);

}

void hw_drivers_init(void) {
    gpio_inits();
    int rc = pico_led_init();
    hard_assert(rc == PICO_OK);
    servo_init();
    INA260_init(INA260_ADDR);
    dc_motor_init();

}

void hw_drivers_task_005ms(void) {
    // 5ms periodic tasks
    motor_control_task();
}

void hw_drivers_task_010ms(void) {
    // 10ms periodic tasks
}

void hw_drivers_task_100ms(void) {
    // 100ms periodic tasks
    //uint16_t dummy = _INA260_readRegister(INA260_REG_MFG_UID); // Dummy read to keep I2C active
    uint16_t voltage = INA260_readBusVoltage_mV();
    int16_t current = INA260_readCurrent_mA();
    //printf("INA260 Voltage: %u mV, Current: %d mA\n", voltage, current);
}

void hw_drivers_task_debug(void) {
    // Debug task to print hardware status
    uint16_t voltage = INA260_readBusVoltage_mV();
    int16_t current = INA260_readCurrent_mA();
    //printf("Debug Task: Battery Voltage = %u mV, Battery Current = %d mA\n", voltage, current);
    //printf("Debug Task: Car Throttle = %d, Car Turn Angle = %d, Power Status = %d\n", global_controls_data.car_throttle, global_controls_data.car_turn_angle, global_controls_data.ccm_power_state);
}