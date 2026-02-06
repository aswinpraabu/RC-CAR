#include "hw_drivers.h"


void servo_init(void) {
    // Initialize PWM for servo control
    pwm_config config = pwm_get_default_config();
    uint8_t slice_num = pwm_gpio_to_slice_num(SERVO_PIN);
    uint8_t channel = pwm_gpio_to_channel(SERVO_PIN);

    gpio_set_function(SERVO_PIN, GPIO_FUNC_PWM);
    
    pwm_set_clkdiv(slice_num, SYS_CLK_HZ / SERVO_PWM_CLK_HZ);
    pwm_set_wrap(slice_num, SERVO_PWM_CLK_HZ / SERVO_FREQ - 1); // Set wrap value based on frequency

    servo_set_angle(0); // Set to neutral position
    pwm_set_enabled(slice_num, true);
    
}

void servo_set_angle(int8_t angle) {
    if (angle < SERVO_MIN_ANGLE) angle = SERVO_MIN_ANGLE;
    if (angle > SERVO_MAX_ANGLE) angle = SERVO_MAX_ANGLE;

    float duty_ms = SERVO_MIN_DUTY_MS + ((angle - SERVO_MIN_ANGLE) / (SERVO_MAX_ANGLE - SERVO_MIN_ANGLE)) * (SERVO_MAX_DUTY_MS - SERVO_MIN_DUTY_MS);
    
    uint32_t duty_cycle = (uint32_t)((duty_ms / 1e3) * (SERVO_PWM_CLK_HZ)); // Convert milliseconds to clock cycles

    pwm_set_gpio_level(SERVO_PIN, duty_cycle);
    //printf("Servo angle set to %d degrees (duty cycle: %u, duty_ms: %f)\n", angle, duty_cycle, duty_ms);
}



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


void hw_drivers_init(void) {
    int rc = pico_led_init();
    hard_assert(rc == PICO_OK);
    servo_init();
    INA260_init(INA260_ADDR);
}

void hw_drivers_task_005ms(void) {
    // 5ms periodic tasks
}

void hw_drivers_task_010ms(void) {
    // 10ms periodic tasks
}

void hw_drivers_task_100ms(void) {
    // 100ms periodic tasks
    //uint16_t dummy = _INA260_readRegister(INA260_REG_MFG_UID); // Dummy read to keep I2C active
    uint16_t voltage = INA260_readBusVoltage_mV();
    int16_t current = INA260_readCurrent_mA();
    printf("INA260 Voltage: %u mV, Current: %d mA\n", voltage, current);
}