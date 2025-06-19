from global_data import hw_drivers_data, rf_comms_data
from CCM_Libraries.micropython_rfm69 import *


CCM_RF_ADDR = 0x11
RCM_RF_ADDR = 0x22
RADIO_FREQ_MHZ = 433
rfm69 = RFM69(None, None, None, None)  # Placeholder, will be initialized in initialize()


def initialize():
    global rfm69

    # Initialize RFM radio
    rfm69_SPI, rfm69_CS, rfm69_RESET = hw_drivers_data.get_rfm69_info()
    rfm69:RFM69 = RFM69(rfm69_SPI, rfm69_CS, rfm69_RESET, RADIO_FREQ_MHZ)
    rfm69.high_power = True  # Only for RFM69HW!
    rfm69.node = CCM_RF_ADDR
    rfm69.destination = RCM_RF_ADDR

def task_005ms():
    # RX()
    pass

def rf_receive():
    packet = rfm69.receive(timeout=0.05, keep_listening=True)
    if packet is not None:
        turn_angle, throttle, decode_result = decode_packet(packet)
        # Update global data
        rf_comms_data.rx_turn_angle = turn_angle
        rf_comms_data.rx_throttle = throttle
        rf_comms_data.rx_validity = decode_result
    else:
        rf_comms_data.rx_validity = False

    return rf_comms_data.rx_validity
    
def decode_packet(packet):
    '''
    Decodes a received packet into its components.
    Packet format: [MSG_ID, TURN_ANGLE_RAW, THROTTLE_RAW]\n
    turn_angle = TURN_ANGLE_RAW - 90\n
    throttle = THROTTLE_RAW\n
    **Returns**:
    -   turn_angle (int): degrees
    -   throttle (int): percentage
    -   decode_result (bool): True if packet is valid, False otherwise
    '''
    # Include checksum verification later
    MSG_LEN = 3
    
    if len(packet) == MSG_LEN:
        turn_angle = int(packet[0]) - 90
        throttle = int(packet[1])
        decode_result = True
    else:
        turn_angle = 0
        throttle = 0
        decode_result = False
    
    return turn_angle, throttle, decode_result
