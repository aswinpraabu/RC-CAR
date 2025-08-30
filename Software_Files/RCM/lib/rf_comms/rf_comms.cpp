#include <RH_RF69.h>
#include <RHReliableDatagram.h>
#include <rf_comms.h>
#include <sensors.h>


uint16_t packetnum = 0;

uint8_t data[] = "Hello World!";
// Dont put this on the stack:
uint8_t msg_buf[RH_RF69_MAX_MESSAGE_LEN];

// Singleton instance of the radio driver
RH_RF69 rf69(RFM69_CS, RFM69_INT);

// Class to manage message delivery and receipt, using the driver declared above
//RHReliableDatagram manager(rf69, FROM_ADDRESS);

bool send_shutdown = false;
uint8_t shutdown_tx_count = 0;
uint8_t shutdown_cmd = 0x99;

void rf_comms_init(){
    
    
    // manual reset
	toggle_pin(1,10,RFM69_RST);
    
    if (!rf69.init())
	{
		//Serial.println("RFM69 radio init failed");
        toggle_status_led(10,1000);
		while (1)
        {
            toggle_status_led(10,1000);
        }
	}

	//Serial.println("RFM69 radio init OK!");
	//toggle_status_led(2,500);

    // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM (for low power module)
	// No encryption
	if (!rf69.setFrequency(RF69_FREQ))
	{
		//Serial.println("setFrequency failed");
		toggle_status_led(10,100);
	}
	toggle_status_led(3,50);

    // If you are using a high power RF69 eg RFM69HW, you *must* set a Tx power with the
	// ishighpowermodule flag set like this:
	rf69.setTxPower(20, true); // range from 14-20 for power, 2nd arg must be true for 69HCW
	
    //volatile  int tempC = rf69.temperatureRead(); // Read the temperature (is in C);
	//volatile int16_t a = tempC;
	
    rf69.setThisAddress(FROM_ADDRESS); // Set our address
	rf69.setHeaderTo(TO_ADDRESS); // Set the address we are sending to

}

void rf_comms_task_005ms()
{
    send_data();
	tx_msg_0x0B_Shutdown();
}

void rf_comms_task_02()
{
	// This function can be used to handle other RF tasks, such as receiving messages
	// or handling specific commands.
	// For now, we will just send a shutdown message.

	//send_shutdown = true;
	//toggle_status_led(1,50);
}



/**
 * @brief   format: [MSG_ID, TURN_ANGLE_RAW, THROTTLE_RAW]
 * 
 *          turn_angle = TURN_ANGLE_RAW - 90 
 * 
 *          throttle = THROTTLE_RAW 
 * 
 */
void send_data() {



	uint8_t msg_len = 4;
	//buf[0] = pot_adc & 0xFF; // Low byte of ADC value
	//buf[1] = (pot_adc >> 8) & 0xFF; // High byte of ADC value

	msg_buf[0] = 0x0A; // Message ID
	msg_buf[1] = (uint8_t) (sensors_data.turn_angle + 90); // map -90 to +90 to 0-180
	msg_buf[2] = (uint8_t) (sensors_data.throttle + 100); 
	msg_buf[3] = shutdown_cmd; 
	
	packetnum++; // Increment the packet number

	if (rf69.send(msg_buf, msg_len)) {
		//Serial.print("Sending: ");
		//Serial.println((char*)data);
		//toggle_status_led(3,30); //blink LED once, 100ms between blinks
	} else {
		//Serial.println("Send failed");
		toggle_status_led(1,100);
	}


}

volatile uint8_t shutdown_tx_max_count = 10;
void tx_msg_0x0B_Shutdown() {

	if (send_shutdown) 
	{
		shutdown_cmd = 0xAB; // Shutdown command
		shutdown_tx_count++;
		if (shutdown_tx_count >= shutdown_tx_max_count) {
			// Reset the shutdown flag after sending 10 shutdown messages
			shutdown_cmd = 0x99; // Reset command
			send_shutdown = false;
			shutdown_tx_count = 0;
			//toggle_status_led(2,30);
			//Serial.println("Shutdown messages sent, resetting flag");
		}
	}
}