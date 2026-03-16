
#include "rf_comms.h"


// module interface, platform specific
void noInterrupts()                // function to disable interrupts
{
    core0_interrupts = save_and_disable_interrupts();
}
void interrupts()                  // function to enable interrupts
{
    restore_interrupts(core0_interrupts);
}
// function to control the GPIO tied to RFM69 chip select (parameter HIGH or LOW)
void RFM69_SetCSPin(bool value)
{
    gpio_put(RFM69_CS_PIN, !value); // Active LOW
}
// function to read GPIO connected to RFM69 DIO0 (RFM69 interrupt signalling)
bool RFM69_ReadDIO0Pin(void)
{
    return gpio_get(RFM69_DIO0_PIN);
}
uint8_t SPI_transfer8(uint8_t data)     // function to transfer 1byte on SPI with readback
{
    uint8_t result;
    spi_write_read_blocking(spi0, &data, &result, 1);
    return result;
}

void RFM69_SPI_init(void) 
{
    // Initialize SPI for RFM69 communication
    spi_init(spi0, 1000*1000); // Initialize SPI at 1MHz
    gpio_set_function(RFM69_SCK_PIN, GPIO_FUNC_SPI);
    gpio_set_function(RFM69_MOSI_PIN, GPIO_FUNC_SPI);
    gpio_set_function(RFM69_MISO_PIN, GPIO_FUNC_SPI);
    gpio_init(RFM69_CS_PIN);
    gpio_set_dir(RFM69_CS_PIN, GPIO_OUT);
    gpio_put(RFM69_CS_PIN, true); // Set CS high (inactive)

    //bi_decl(bi_4pins_with_func(RFM69_MISO_PIN, RFM69_MOSI_PIN, RFM69_SCK_PIN, RFM69_CS_PIN, GPIO_FUNC_SPI));

}

// function to print to serial port a string
void Serialprint(char* printf_str)
{
    printf("%s\n", printf_str);
}

void Timeout_SetTimeout1(uint16_t timeout_ms) // function for timeout handling, sets a timeout, parameter is in milliseconds (ms)
{
    RFM69_timer_expired = false;
    add_alarm_in_ms(timeout_ms,_RFM69_timer_callback, NULL, false);
}
bool Timeout_IsTimeout1(void)      // function for timeout handling, checks if previously set timeout expired
{
    return RFM69_timer_expired;
}

int64_t _RFM69_timer_callback(alarm_id_t id, __unused void *user_data) 
{
    RFM69_timer_expired = true;
    return 0;
}


void rf_comms_init(void)
{
    RFM69_SPI_init();
    // Additional initialization code for RFM69 can be added here
}