#ifndef RF_COMMS_H
#define RF_COMMS_H

#include "RFM69.h"
#include "pin_config.h"
#include "pico/stdlib.h"
#include "hardware/sync.h"
#include "hardware/spi.h"

#define CCM_NODE_ADDR 0x11
#define RCM_NODE_ADDR 0x22
#define NETWORK_ID 0xAA2D



// internal function
int64_t _RFM69_timer_callback(alarm_id_t id, __unused void *user_data);

void rfm69_SPI_init(void);
void rfm69_device_init(void);
void rfm69_gpio0_interupt_callback(uint gpio, uint32_t events);

void rf_comms_init(void);
void rf_comms_task_005ms(void);
void rf_comms_task_010ms(void);
void rf_comms_task_100ms(void);

#endif // RF_COMMS_H