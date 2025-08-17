from CCM_Submodules.global_data import hw_drivers_data, rf_comms_data
from CCM_Libraries.micropython_rfm69 import *
from time import ticks_ms, ticks_diff

CCM_RF_ADDR = 0x11
RCM_RF_ADDR = 0x22
RADIO_FREQ_MHZ = 433
rfm69:RFM69 = None # type: ignore
rfm69_init = False
msg_0x0A_last_rx_time = 0 # Time of last successful reception of Propulsion Control message

class signal_class():
    name = ""
    factor = 1.0
    offset = 0.0
    min = 0.0
    max = 0.0
    default = 0.0
    start_bit = 0
    length = 0
    cycle_time = 0  # in milli seconds, used for periodic signals. -1 means not periodic
    def __init__(self,signal_name, signal_factor,signal_offset, signal_min, signal_max, signal_default, signal_start_bit, signal_length):
        self.name = signal_name
        self.factor = signal_factor
        self.offset = signal_offset
        self.min = signal_min
        self.max = signal_max
        self.default = signal_default
        self.start_bit = signal_start_bit
        self.length = signal_length

class message_class():
    msg_id = 0x00
    msg_len = 0
    signals = []
    def __init__(self, message_id, message_length, message_signals:list[signal_class]):
        self.msg_id = message_id
        self.msg_len = message_length
        self.signals = message_signals

    def add_signal(self, new_signal:signal_class):
        #self.signals.append(new_signal)
        pass
    def remove_signal(self, signal_name:str):
        #self.signals = [signal for signal in self.signals if signal.name != signal_name]
        pass
    def validate(self):
        return True
        # Check that signals do not overlap and fit within message length
        bit_map = [0] * (self.msg_len * 8)
        for signal in self.signals:
            for i in range(signal.start_bit, signal.start_bit + signal.length):
                if i >= len(bit_map) or bit_map[i] == 1:
                    return False
                bit_map[i] = 1
        return True



# Set to store valid message IDs
# format: (MSG_ID, MSG_LEN)
valid_msg_set = set()

def initialize():
    print("Initializing RFM69 radio communications...")

    global rfm69
    global msg_0x0A_last_rx_time
    global rfm69_init
    try:
        # Initialize RFM radio
        rfm69_SPI, rfm69_CS, rfm69_RESET = hw_drivers_data.get_rfm69_info()
        rfm69 = RFM69(rfm69_SPI, rfm69_CS, rfm69_RESET, RADIO_FREQ_MHZ)
        rfm69.high_power = True  # Only for RFM69HW!
        rfm69.node = CCM_RF_ADDR
        rfm69.destination = RCM_RF_ADDR
        rfm69_init = True
        print("RFM69 radio initialized successfully.")
    except Exception as e:
        rfm69_init = False
        print("Error initializing RFM69 radio: {0}".format(e))

    #TODO: initialize this set in another file. That file should also contain the message decoding functions
    valid_msg_set.add((0x0A, 3))  # Propulsion Control message

    msg_0x0A_last_rx_time = ticks_ms() 
    
def rf_receive():
    t1 = ticks_ms()

    # 5ms timeout for receiving packets
    # timeout > 5ms does not increase RX success rate
    if not rfm69_init:
        #print("RFM69 not initialized. Cannot receive packets.")
        rf_comms_data.rx_validity = False
        return rf_comms_data.rx_validity
    packet = rfm69.receive(timeout=5, keep_listening=True)
    
    if packet is not None:
        packet_arbitration(packet)

        # Update global data
        #rf_comms_data.rx_turn_angle = turn_angle
        #rf_comms_data.rx_throttle = throttle
        #rf_comms_data.rx_validity = decode_result
        
        #packet_text = str(packet, "ascii")
        #print("Received : {0} {1} {2}".format(packet[0], packet[1], packet[2]))
        
    
    else:
        #print("Received nothing! Listening again...")
        rf_comms_data.rx_validity = False

    return rf_comms_data.rx_validity
    
def packet_arbitration(packet):
    '''
    Packet format: [MSG_ID,RAW_DATA]\n
    '''
    global msg_0x0A_last_rx_time
    msg_id:int = packet[0]
    #print("Packet ID: {0}".format(msg_id))
    # Include checksum verification later
    if((msg_id, len(packet)) in valid_msg_set):
        raw_data = packet[1:]
        if msg_id == 0x0A:
            msg_0x0A_last_rx_time = ticks_ms()  # Update last received time for Propulsion Control message #DIAG
            decode_msg_0x0A_PropulsionCtrl(raw_data)
    else:
        print("Invalid packet received: {0}".format(packet))
        rf_comms_data.rx_validity = False
    


def decode_msg_0x0A_PropulsionCtrl(raw_data):
    '''
    Decodes a received packet into its components.
    Raw Data format: [TURN_ANGLE_RAW, THROTTLE_RAW]\n
    turn_angle = TURN_ANGLE_RAW - 90\n
    throttle = THROTTLE_RAW - 100\n
    **Returns**:
    -   turn_angle (int): degrees
    -   throttle (int): percentage
    -   decode_result (bool): True if packet is valid, False otherwise
    '''
    turn_angle = int(raw_data[0]) - 90
    throttle = int(raw_data[1]) - 100
    decode_result = True

    print("Received rx_turn_angle: {0}, rx_throttle: {1}, rx_validity: {2}".format(turn_angle, throttle, decode_result))

    #TODO: add range checks
    if decode_result:
        rf_comms_data.rx_turn_angle = turn_angle
        rf_comms_data.rx_throttle = throttle
        rf_comms_data.rx_validity = decode_result

        decode_result = True
    else:
        turn_angle = 0
        throttle = 0
        decode_result = False

def rf_comms_diagnostics():

    time_diff = ticks_diff(ticks_ms(), msg_0x0A_last_rx_time)
    #print("Diff: ", time_diff)
    if time_diff > 100: # 100ms timeout
        rf_comms_data.LOC_with_RCM = True
        #print("CCM has lost communication with RCM!")
    else:
        rf_comms_data.LOC_with_RCM = False
        
        

def task_005ms():
    rf_receive()


def task_010ms():
    rf_comms_diagnostics()