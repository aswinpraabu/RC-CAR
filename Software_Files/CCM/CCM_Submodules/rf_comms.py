from global_data import hw_drivers_data
from CCM_Libraries.micropython_rfm69 import *

CCM_RF_ADDR = 0x11
RCM_RF_ADDR = 0x22
RADIO_FREQ_MHZ = 433
rfm69 = None


def initialize():
    global rfm69

    # Initialize RFM radio
    rfm69_SPI, rfm69_CS, rfm69_RESET = hw_drivers_data.get_rfm69_info()
    rfm69 = RFM69(rfm69_SPI, rfm69_CS, rfm69_RESET, RADIO_FREQ_MHZ)
    rfm69.high_power = True  # Only for RFM69HW!
    rfm69.node = CCM_RF_ADDR
    rfm69.destination = RCM_RF_ADDR

def task_005ms():
    # RX()
    pass

def rf_receive():
    packet = rfm69.receive(timeout=0.05, keep_listening=True)
    if packet is None:
        return None
    else:
        packet_text = packet.decode("ascii")
        
        return packet_text
    
def decode_packet(packet):
    '''
    Decodes a received packet into its components.
    Packet format: <MSG_ID><TURN_ANGLE><THROTTLE
    Example: b'\x02\x01\x05Hello\xA1\x03'
    
    Returns:
        cmd (int): Command byte
        data (str): Data string
    '''
    # Include checksum verification later
    START_BYTE = 0x02
    END_BYTE = 0x03
    
    if len(packet) < 5:
        raise ValueError("Packet too short to be valid")
    
    if packet[0] != START_BYTE or packet[-1] != END_BYTE:
        raise ValueError("Invalid start or end byte")
    
    cmd = packet[1]
    data_length = packet[2]
    
    if len(packet) != data_length + 5:
        raise ValueError("Data length mismatch")
    
    data = packet[3:3+data_length].decode('ascii')
    checksum = packet[3+data_length]
    
    # Verify checksum
    calculated_checksum = (sum(packet[1:3+data_length]) & 0xFF)
    if checksum != calculated_checksum:
        raise ValueError("Checksum mismatch")
    
    return cmd, data
