//#include <Arduino.h>

#include <RH_RF69.h>
#include <RHReliableDatagram.h>

#include "sensors.h"
#include "rf_comms.h"


void setup() {
	// put your setup code here, to run once:
	sensors_init();
	toggle_status_led(3,300);
	rf_comms_init();

	//toggle_status_led(5,1000);
}

uint32_t loop_start = millis();
uint32_t loop_start2 = millis();
void loop() {
	
	uint32_t now_time = millis();
	uint32_t diff = abs(int(now_time - loop_start)) ;
	uint32_t diff2 = abs(int(now_time - loop_start2)) ;
	if (diff >= 5){
		sensors_task_005ms();
		rf_comms_task_005ms();
		loop_start = millis();
	}
	else if (diff2 >= 5000)
	{
		rf_comms_task_02();
		loop_start2 = millis();
	}
	
	

	/*
	volatile uint32_t now_time = millis();
	volatile uint32_t now_time_m = getCurrentMillis();
	volatile uint32_t now_time_u = micros();
	sensors_task_005ms();
	rf_comms_task_005ms();
	*/
	delay(1);
}
