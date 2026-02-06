#include "ina260_sensor.h"






void INA260_setAlertLimit(uint16_t limit) {
    // Set alert limit code
    _INA260_writeRegister(INA260_REG_ALERT_LIMIT, limit);

}
void INA260_setConfigRegisterRaw(uint16_t config) {
    // Set configuration register code
    _INA260_writeRegister(INA260_REG_CONFIG, config);
}

void INA260_setConfigRegisterPhys(uint8_t averaging, uint8_t busConvTime, uint8_t currentConvTime, uint8_t mode) {
    // Set configuration register using physical parameters
    uint16_t config = 0;
    config |= (averaging << 9) & INA260_CONFIG_AVERAGING_MASK;
    config |= (busConvTime << 6) & INA260_CONFIG_BUSVOLTAGE_CT_MASK;
    config |= (currentConvTime << 3) & INA260_CONFIG_CURRENT_CT_MASK;
    config |= mode & INA260_CONFIG_MODE_MASK;
    _INA260_writeRegister(INA260_REG_CONFIG, config);
}

void INA260_setCurrentConversionTime(uint8_t time) {
    // Set current conversion time code
    uint16_t config = _INA260_readRegister(INA260_REG_CONFIG);
    config &= ~INA260_CONFIG_CURRENT_CT_MASK;
    config |= (time << 3) & INA260_CONFIG_CURRENT_CT_MASK;
    _INA260_writeRegister(INA260_REG_CONFIG, config);
}
void INA260_setBusVoltageConversionTime(uint8_t time) {
    // Set bus voltage conversion time code
    uint16_t config = _INA260_readRegister(INA260_REG_CONFIG);
    config &= ~INA260_CONFIG_BUSVOLTAGE_CT_MASK;
    config |= (time << 6) & INA260_CONFIG_BUSVOLTAGE_CT_MASK;
    _INA260_writeRegister(INA260_REG_CONFIG, config);
}
void INA260_setAveragingMode(uint8_t mode) {
    // Set averaging mode code
    uint16_t config = _INA260_readRegister(INA260_REG_CONFIG);
    config &= ~INA260_CONFIG_AVERAGING_MASK;
    config |= (mode << 9) & INA260_CONFIG_AVERAGING_MASK;
    _INA260_writeRegister(INA260_REG_CONFIG, config);
}
void INA260_setMode(uint8_t mode) {
    // Set operating mode code
    uint16_t config = _INA260_readRegister(INA260_REG_CONFIG);
    config &= ~INA260_CONFIG_MODE_MASK;
    config |= mode & INA260_CONFIG_MODE_MASK;
    _INA260_writeRegister(INA260_REG_CONFIG, config);
}

int16_t INA260_readCurrent_mA(void) {
    // Read current in mA code
    // Conversion factor is 1.25mA per bit
    // 2s complement for negative values
    uint16_t raw = _INA260_readRegister(INA260_REG_CURRENT);
    int16_t value = (int16_t)raw * 1.25; // Convert to mA
    return value;
}
uint16_t INA260_readBusVoltage_mV(void) {
    // Read bus voltage in mV code
    // Conversion factor is 1.25mA per bit
    uint16_t raw = _INA260_readRegister(INA260_REG_BUSVOLTAGE);
    return raw * 1.25;
}
