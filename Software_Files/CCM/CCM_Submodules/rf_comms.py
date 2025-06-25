from CCM_Submodules.global_data import hw_drivers_data, rf_comms_data
from CCM_Libraries.micropython_rfm69 import *
from time import ticks_ms, ticks_diff

CCM_RF_ADDR = 0x11
RCM_RF_ADDR = 0x22
RADIO_FREQ_MHZ = 433
rfm69:RFM69 = None # type: ignore


def initialize():
    print("Initializing RFM69 radio communications...")

    global rfm69

    # Initialize RFM radio
    rfm69_SPI, rfm69_CS, rfm69_RESET = hw_drivers_data.get_rfm69_info()
    rfm69 = RFM69(rfm69_SPI, rfm69_CS, rfm69_RESET, RADIO_FREQ_MHZ)
    rfm69.high_power = True  # Only for RFM69HW!
    rfm69.node = CCM_RF_ADDR
    rfm69.destination = RCM_RF_ADDR
    
def rf_receive():
    t1 = ticks_ms()

    # 5ms timeout for receiving packets
    # timeout > 5ms does not increase RX success rate
    packet = rfm69.receive(timeout=5, keep_listening=True)
    
    if packet is not None:
        turn_angle, throttle, decode_result = decode_packet(packet)

        # Update global data
        rf_comms_data.rx_turn_angle = turn_angle
        rf_comms_data.rx_throttle = throttle
        rf_comms_data.rx_validity = decode_result
        
        #packet_text = str(packet, "ascii")
        print("Received rx_turn_angle: {0}, rx_throttle: {1}, rx_validity: {2}, diff: {3}".format(turn_angle, throttle, decode_result,ticks_diff(ticks_ms(), t1)))
    
    else:
        #print("Received nothing! Listening again...")
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
        turn_angle = int(packet[1]) - 90
        throttle = int(packet[2])
        decode_result = True
    else:
        turn_angle = 0
        throttle = 0
        decode_result = False
    
    return turn_angle, throttle, decode_result


def task_005ms():
    rf_receive()