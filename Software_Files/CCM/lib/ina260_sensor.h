#ifndef INA260_SENSOR_H
#define INA260_SENSOR_H

#include "pico/stdlib.h"
#include "stdio.h"
#include "pin_config.h"
#include "hardware/i2c.h"

#define INA260_I2CADDR_DEFAULT 0x40 ///< INA260 default i2c address
#define INA260_REG_CONFIG 0x00      ///< Configuration register
#define INA260_REG_CURRENT 0x01 ///< Current measurement register (signed) in mA
#define INA260_REG_BUSVOLTAGE 0x02 ///< Bus voltage measurement register in mV
#define INA260_REG_POWER 0x03      ///< Power calculation register in mW
#define INA260_REG_MASK_ENABLE 0x06 ///< Interrupt/Alert setting and checking register
#define INA260_REG_ALERT_LIMIT 0x07 ///< Alert limit value register
#define INA260_REG_MFG_UID 0xFE     ///< Manufacturer ID Register
#define INA260_REG_DIE_UID 0xFF     ///< Die ID and Revision Register

/// Configuration Register Masks
#define INA260_CONFIG_RESET_MASK 0x8000        ///< Reset Bit
#define INA260_CONFIG_AVERAGING_MASK 0x0E00 ///< Averaging Mode Mask
#define INA260_CONFIG_BUSVOLTAGE_CT_MASK 0x01C0 ///< Bus Voltage Conversion Time Mask
#define INA260_CONFIG_CURRENT_CT_MASK 0x0038    ///< Current Conversion Time Mask
#define INA260_CONFIG_MODE_MASK 0x0007          ///< Operating Mode Mask

// Averaging Modes
typedef enum {
    INA260_AVERAGING_1 = 0x00,
    INA260_AVERAGING_4 = 0x01,
    INA260_AVERAGING_16 = 0x02,
    INA260_AVERAGING_64 = 0x03,
    INA260_AVERAGING_128 = 0x04,
    INA260_AVERAGING_256 = 0x05,
    INA260_AVERAGING_512 = 0x06,
    INA260_AVERAGING_1024 = 0x07
} ina260_averaging_mode;

// Conversion Times
typedef enum {
    INA260_CONVERSIONTIME_140_US = 0x00,
    INA260_CONVERSIONTIME_204_US = 0x01,
    INA260_CONVERSIONTIME_332_US = 0x02,
    INA260_CONVERSIONTIME_588_US = 0x03,
    INA260_CONVERSIONTIME_1100_US = 0x04,
    INA260_CONVERSIONTIME_2116_US = 0x05,
    INA260_CONVERSIONTIME_4156_US = 0x06,
    INA260_CONVERSIONTIME_8244_US = 0x07
} ina260_conversion_time;

// Operating Modes
typedef enum {
    INA260_MODE_POWERDOWN = 0x00,
    INA260_MODE_CURRENT_TRIGGERED = 0x01,
    INA260_MODE_VOLTAGE_TRIGGERED = 0x02,
    INA260_MODE_CURRENT_AND_VOLTAGE_TRIGGERED = 0x03,
    INA260_MODE_CURRENT_CONTINUOUS = 0x05,
    INA260_MODE_VOLTAGE_CONTINUOUS = 0x06,
    INA260_MODE_CURRENT_AND_VOLTAGE_CONTINUOUS = 0x07
} ina260_mode;






void INA260_setAlertLimit(uint16_t limit);
void INA260_setConfigRegisterRaw(uint16_t config);
void INA260_setConfigRegisterPhys(uint8_t averaging, uint8_t busConvTime, uint8_t currentConvTime, uint8_t mode);
void INA260_setCurrentConversionTime(uint8_t time);
void INA260_setBusVoltageConversionTime(uint8_t time);
void INA260_setAveragingMode(uint8_t mode);
void INA260_setMode(uint8_t mode);


/* Platform specific functions for INA260*/
extern void _INA260_writeRegister(uint8_t reg, uint16_t value);
extern uint16_t _INA260_readRegister(uint8_t reg);



int16_t INA260_readCurrent_mA(void);
uint16_t INA260_readBusVoltage_mV(void);



#endif // INA260_SENSOR_H