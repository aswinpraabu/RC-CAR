
#ifndef RF_COMMS_H
#define RF_COMMS_H

// Change to 434.0 or other frequency, must match RX's freq!
#define RF69_FREQ 433.0
#define FROM_ADDRESS 0x22 // Address of this node
#define TO_ADDRESS   0x11 // Address of the node to send to





void rf_comms_init();
void rf_comms_task_005ms();
void rf_comms_task_02();
void send_data();
void tx_msg_0x0B_Shutdown();

#endif /* RF_COMMS_H */