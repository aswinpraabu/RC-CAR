#ifndef SENSORS_H
#define SENSORS_H



#define STATUS_LED LED_BUILTIN
#define TURN_POT_PIN PA0 // potentiometer pin for Turn Angle input
#define THROTTLE_POT_PIN PA1 // potentiometer pin for Throttle input


#define RFM69_CS    PA3  //
//#define RFM69_CS    PIN_SPI_SS  //
#define RFM69_INT   PA2  //
#define RFM69_RST   PA11  // "A"

#define RF_SPI_CS 
#define RF_IRQ PA2



struct SensorsData {
    int8_t turn_angle; // turn angle -90 to +90 degrees
    float_t throttle; // throttle -50 to 100 %      
};

extern SensorsData sensors_data;

void toggle_status_led(uint8_t counts, uint16_t delayms);
void toggle_pin(uint8_t counts, uint16_t delayms, uint32_t pin);
void sensors_init();
void sensors_task_005ms();
void update_turn_angle();
void update_throttle();


#endif /* SENSORS_H */