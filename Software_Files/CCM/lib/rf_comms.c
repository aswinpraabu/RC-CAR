
#include "rf_comms.h"

volatile uint32_t core0_interrupts; // variable to save and restore interrupts state RFM69 moduled

volatile bool RFM69_timer_expired; // variable to signal timeout expiration to RFM69 module
volatile uint8_t *rxdata; // buffer to hold received data from RFM69 module
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
    gpio_put(RFM69_CS_PIN, value); // Active LOW
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

void RFM69_delay_us(uint16_t us)           // function to delay for a specified number of microseconds (us)    
{
    sleep_us(us);
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

//TODO [RC-131] Move this function inside RFM69.c. And call it during initialization.

void rfm69_reset() {
    // Reset RFM69 module by toggling the reset pin
    
    gpio_put(RFM69_RESET_PIN, true); // Set reset low
    sleep_us(100); // Hold reset for 100ms
    gpio_put(RFM69_RESET_PIN, false); // Set reset high
    sleep_ms(5); // Wait for module to stabilize after reset
}

void rfm69_gpio0_interrupt_callback(uint gpio, uint32_t events) {
    if (gpio == RFM69_DIO0_PIN && (events & GPIO_IRQ_EDGE_RISE)) {
        RFM69_isr0();
    }
}

void rfm69_SPI_init(void) 
{
    // Initialize SPI for RFM69 communication
    spi_init(spi0, 5000*1000); // Initialize SPI at 5MHz
    gpio_set_function(RFM69_SCK_PIN, GPIO_FUNC_SPI);
    gpio_set_function(RFM69_MOSI_PIN, GPIO_FUNC_SPI);
    gpio_set_function(RFM69_MISO_PIN, GPIO_FUNC_SPI);
    gpio_init(RFM69_CS_PIN);
    gpio_set_dir(RFM69_CS_PIN, GPIO_OUT);
    gpio_put(RFM69_CS_PIN, true); // Set CS high (inactive)

    //bi_decl(bi_4pins_with_func(RFM69_MISO_PIN, RFM69_MOSI_PIN, RFM69_SCK_PIN, RFM69_CS_PIN, GPIO_FUNC_SPI));

}

void rfm69_device_init()
{
    gpio_init(RFM69_RESET_PIN);
    gpio_set_dir(RFM69_RESET_PIN, GPIO_OUT);
    rfm69_reset();
    // Initialize RFM69 device
    RFM69_initialize(RF69_433MHZ,CCM_NODE_ADDR,NETWORK_ID);
    RFM69_setHighPower(true);
    gpio_init(RFM69_DIO0_PIN);
    gpio_set_dir(RFM69_DIO0_PIN, GPIO_IN);
    gpio_set_pulls(RFM69_DIO0_PIN, false, true); // Enable pull-up on DIO0 pin
    gpio_set_irq_enabled_with_callback(RFM69_DIO0_PIN, GPIO_IRQ_EDGE_RISE | GPIO_IRQ_EDGE_FALL, true, &rfm69_gpio0_interrupt_callback);
    



}


void rf_comms_init(void)
{
    printf("Initializing RF Communications...\n");
    rfm69_SPI_init();
    
    rfm69_device_init();



}


void rf_comms_task_005ms(void)
{
    // Check for received packets
    if (RFM69_receiveDone()) {
        //printf("Received packet from node %d: %d\n", RFM69_getSenderID(), RFM69_getDataLen());
        rxdata = RFM69_getData();

    }
    else {
        //printf("No packet received.\n");
    }
}

void rf_comms_task_debug(void)
{
    // Debug task to print received data
    if (rxdata) {
        printf("Received data: %d, %d, %d, %d, %d, %d\n", rxdata[0], rxdata[1], rxdata[2], rxdata[3], rxdata[4], rxdata[5]);
    }
}