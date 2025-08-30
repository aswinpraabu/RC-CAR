#include <Arduino.h>
#include <sensors.h>

SensorsData sensors_data;

void toggle_status_led(uint8_t counts, uint16_t delayms) {
	toggle_pin(counts, delayms, LED_BUILTIN);
}

void toggle_pin(uint8_t counts, uint16_t delayms, uint32_t pin) {
	for (uint8_t i = 0; i < counts; i++) {
	digitalWrite(pin, HIGH);
	delay(delayms);
	digitalWrite(pin, LOW);
	delay(delayms);
	}
}


void sensors_init() {
	pinMode(STATUS_LED, OUTPUT);
	digitalWrite(STATUS_LED, LOW);

	pinMode(RFM69_RST, OUTPUT);
	//pinMode(TURN_POT_PIN, INPUT);
	//pinMode(THROTTLE_POT_PIN, INPUT);
}


	
void sensors_task_005ms() {
	update_turn_angle();
	update_throttle();
}

void update_turn_angle() {
	volatile uint32_t pot_adc = analogRead(TURN_POT_PIN);
	volatile int8_t pot = (int8_t)(pot_adc*180.0 / 1023.0); // assuming 10-bit ADC
	volatile int8_t angle = pot - 90; // map 0-180 to -90 to +90
	sensors_data.turn_angle = 0;angle;
}

void update_throttle() {
	volatile uint32_t pot_adc = analogRead(THROTTLE_POT_PIN);
	float throttle_raw  = (pot_adc * 200.0 / 1023.0); // map 0-1023 to 0-100%
	throttle_raw = throttle_raw - 100.0; // map 0-100% to -50 to +50
	float throttle = abs(throttle_raw)>10? abs((throttle_raw)-10)*10/9 : 0; // map 0-50% to 0-100%
	if (throttle_raw>=0) {
		throttle = throttle; // forward 0-100%
	} else {
		throttle = -throttle; // reverse 0 to -100%
	}

	sensors_data.throttle = throttle;
}