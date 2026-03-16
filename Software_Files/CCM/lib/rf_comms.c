
#include "rf_comms.h"


// module interface, platform specific
void noInterrupts();                // function to disable interrupts
void interrupts();                  // function to enable interrupts
// function to control the GPIO tied to RFM69 chip select (parameter HIGH or LOW)
void RFM69_SetCSPin(bool value)
{
    gpio_put(RFM69_CS_PIN, !value); // Active LOW
}
bool RFM69_ReadDIO0Pin(void);       // function to read GPIO connected to RFM69 DIO0 (RFM69 interrupt signalling)
bool RFM69_ReadDIO0Pin(void)
{
    return gpio_get(RFM69_DIO0_PIN);
}
uint8_t SPI_transfer8(uint8_t);     // function to transfer 1byte on SPI with readback

// function to print to serial port a string
void Serialprint(char* printf_str)
{
    printf("%s\n", printf_str);
}

bool Timeout_IsTimeout1(void);      // function for timeout handling, checks if previously set timeout expired
void Timeout_SetTimeout1(uint16_t); // function for timeout handling, sets a timeout, parameter is in milliseconds (ms)