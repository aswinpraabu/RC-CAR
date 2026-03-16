#include "RFM69.h"
#include "pin_config.h"
#include "pico/stdlib.h"
#include "hardware/sync.h"


volatile uint32_t core0_interrupts = 0; // variable to save and restore interrupts state RFM69 moduled

