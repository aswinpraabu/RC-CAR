#include "RFM69.h"
#include "pin_config.h"
#include "pico/stdlib.h"
#include "hardware/sync.h"


volatile uint32_t core0_interrupts = 0; // variable to save and restore interrupts state RFM69 moduled

volatile bool RFM69_timer_expired = false; // variable to signal timeout expiration to RFM69 module

// internal function
int64_t _RFM69_timer_callback(alarm_id_t id, __unused void *user_data);