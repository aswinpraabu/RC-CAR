from CCM_Submodules.global_data import hw_drivers_data, rf_comms_data
from CCM_Libraries.micropython_rfm69 import *
from time import ticks_ms, ticks_diff

CCM_RF_ADDR = 0x11
RCM_RF_ADDR = 0x22
RADIO_FREQ_MHZ = 433
rfm69:RFM69 = None # type: ignore

msg_0x0A_last_rx_time = 0 # Time of last successful reception of Propulsion Control message


shutdown_cmd_last_rx_time = 0 # Time of last successful reception of Shutdown message
shutdown_request_any_received = False # Flag to indicate if any shutdown request has been received
shutdown_request_received_count = 0 # Counter for shutdown requests received
shutdown_confirmation_min_count = 5 # Minimum number of requests required to confirm shutdown request
#TODO [RC-83] define calibration variables in a separate file with a specific format

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
# format: (MSG_ID, DATA_LEN)
valid_msg_set = set()

def initialize():
    print("Initializing RFM69 radio communications...")

    global rfm69
    global msg_0x0A_last_rx_time

    # Initialize RFM radio
    rfm69_SPI, rfm69_CS, rfm69_RESET = hw_drivers_data.get_rfm69_info()
    rfm69 = RFM69(rfm69_SPI, rfm69_CS, rfm69_RESET, RADIO_FREQ_MHZ)
    rfm69.high_power = True  # Only for RFM69HW!
    rfm69.node = CCM_RF_ADDR
    rfm69.destination = RCM_RF_ADDR

    #TODO: initialize this set in another file. That file should also contain the message decoding functions
    valid_msg_set.add((0x0A, 3))  # Propulsion Control message
    valid_msg_set.add((0x0B, 1))  # Shutdown message

    msg_0x0A_last_rx_time = ticks_ms() 
    
def rf_receive():
    t1 = ticks_ms()

    # 5ms timeout for receiving packets
    # timeout > 5ms does not increase RX success rate
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
    if((msg_id, len(packet)-1) in valid_msg_set):
        raw_data = packet[1:]
        if msg_id == 0x0A:
            msg_0x0A_last_rx_time = ticks_ms()  # Update last received time for Propulsion Control message #DIAG
            decode_msg_0x0A_PropulsionCtrl(raw_data)
        elif msg_id == 0x0B:
            pass
            #decode_msg_0x0B_Shutdown(raw_data)

    else:
        print("Invalid packet received: {0}".format(packet))
        rf_comms_data.rx_validity = False
    


def decode_msg_0x0A_PropulsionCtrl(raw_data):
    '''
    Decodes a received packet into its components.
    Raw Data format: [TURN_ANGLE_RAW, THROTTLE_RAW, SHUTDOWN_CMD]\n
    turn_angle = TURN_ANGLE_RAW - 90\n
    throttle = THROTTLE_RAW - 100\n
    shutdown_flag = True if SHUTDOWN_CMD==0xAB else False\n
    **Returns**:
    -   turn_angle (int): degrees
    -   throttle (int): percentage
    -   decode_result (bool): True if packet is valid, False otherwise
    '''
    turn_angle = int(raw_data[0]) - 90
    throttle = int(raw_data[1]) - 100
    shutdown_flag = decode_Shutdown(raw_data[2])  # Decode shutdown command
    decode_result = True

    #if shutdown_flag:
    #print("Received rx_turn_angle: {0}, rx_throttle: {1}, rx_validity: {2}, shutdown: {3}".format(turn_angle, throttle, decode_result, shutdown_flag))

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

def decode_Shutdown(shutdown_raw_data):
    '''
    Decodes a received shutdown packet.
    Raw Data format: [SHUTDOWN_FLAG]\n
    shutdown_flag = True if SHUTDOWN_FLAG==0xAB\n
    **Returns**:
    -   shutdown_flag (bool): True if shutdown is requested, False otherwise
    '''
    global shutdown_cmd_last_rx_time
    global shutdown_request_any_received
    global shutdown_request_received_count

    shutdown_flag = True if shutdown_raw_data == 0xAB else False
    
    if shutdown_flag:
        #print("Received shutdown_flag: {0}".format(shutdown_flag))
        shutdown_cmd_last_rx_time = ticks_ms()  # Update last received time for Shutdown message #DIAG
        shutdown_request_any_received = True
        shutdown_request_received_count += 1
        
    return shutdown_flag

def rf_comms_diagnostics():

    time_diff = ticks_diff(ticks_ms(), msg_0x0A_last_rx_time)
    #print("Diff: ", time_diff)
    if time_diff > 100: # 100ms timeout
        rf_comms_data.LOC_with_RCM = True
        print("CCM has lost communication with RCM!")
    else:
        rf_comms_data.LOC_with_RCM = False
        
def rf_shutdown_request_handler():
    '''
    Handles shutdown requests based on received packets.
    If shutdown request is confirmed, set shutdown_request_confirmed to True.

    If shutdown request is not confirmed, reset the request after a timeout.
    '''
    global shutdown_request_received_count
    global shutdown_request_any_received

    if shutdown_request_any_received:
        time_diff = ticks_diff(ticks_ms(), shutdown_cmd_last_rx_time)
        #print("Shutdown request received. Count: {0}, time diff: {1}".format(shutdown_request_received_count, time_diff))
        if shutdown_request_received_count >= shutdown_confirmation_min_count:
            rf_comms_data.shutdown_request_confirmed = True
            #print("Shutdown request confirmed!")
        else:
            # assuming that msg_0x0B_last_rx_time is updated in decode_msg_0x0B_Shutdown
            rf_comms_data.shutdown_request_confirmed = False
            
        #TODO [RC-84] define calibration variable for timeout
        if time_diff > 100: # 100ms timeout
            #print("Time since last shutdown request: {0} ms".format(time_diff))
            #print("Shutdown request reset due to timeout. Request count: {0}".format(shutdown_request_received_count))
            shutdown_request_any_received = False
            shutdown_request_received_count = 0
    else:
        rf_comms_data.shutdown_request_confirmed = False

def task_005ms():
 # typical execution time: 5 +/-1 ms, occasionally ~12ms
    rf_receive()


def task_010ms():
    rf_comms_diagnostics()

    # Minimum time to confirm shutdown request = 50ms
    # Minimum time to reset shutdown request = 100ms
    # At 10ms interval, worst case is 60ms to confirm and 110ms to reset
    # This is acceptable for the system. Can even be extended to 20ms for more reduction in processing
    rf_shutdown_request_handler()