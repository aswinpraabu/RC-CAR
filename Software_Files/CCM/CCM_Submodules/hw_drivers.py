from CCM_Submodules.global_data import hw_drivers_data, rf_comms_data, controls_data
from CCM_Submodules.global_data import POWER_MODES
from machine import SPI, Pin,PWM

# region RFM69
# Define pin numbers for RFM69 module
RFM69_MOSI_PIN = 19
RFM69_MISO_PIN = 16
RFM69_SCK_PIN = 18
RFM69_CS_PIN = 17
RFM69_RESET_PIN = 20
a = PWM(Pin(RFM69_MOSI_PIN), freq=1000000)  # Example PWM initialization, adjust as needed
a.duty_ns()

# endregion
SERVO_PIN = 21
LED2_LOC_RCM_PIN = 25

MOTOR_FWD_PIN = 15
MOTOR_REV_PIN = 14

POWER_ON_PIN_NUM = 13
POWER_ON_PIN = Pin(POWER_ON_PIN_NUM, Pin.OUT)
POWER_ON_PIN.value(1)  # Set high to power on the system

LED2 = Pin(LED2_LOC_RCM_PIN, Pin.OUT)
LED2.value(0)  # Turn off LED initially

class Servo:
    def __init__(self):
        pass

    def configure_pin(self, pin):

        # Initialize the parameters for the SG90 servo motor
        self.pin = Pin(pin, Pin.OUT)
        self.angle = 0  # Initialize angle to 0 degrees
        self.min_angle = -90.0  # Minimum angle
        self.max_angle = 90.0 # Maximum angle
        self.min_duty_ns = 1.0e6 # (1ms) Minimum duty cycle in nanoseconds
        self.max_duty_ns = 2.0e6 # (2ms)Maximum duty cycle in nanoseconds
        self.freq = 50

        self.min_duty_offset_ms = -0.5344 # Offset for minimum duty cycle
        self.max_duty_offset_ms = 0.57 # Offset for maximum duty cycle
        self.min_duty_ns += int(self.min_duty_offset_ms * 1e6)  # Convert ms to ns
        self.max_duty_ns += int(self.max_duty_offset_ms * 1e6)  # Convert ms to ns
        
        self.pwm = PWM(self.pin, freq=self.freq)


    def set_angle(self, angle):
        self.angle = angle
        
        duty_ns = self._angle_to_duty_ns(angle)
        self.pwm.duty_ns(duty_ns)

    def _angle_to_duty_ns(self, angle: float) -> int:
        '''
        Convert angle to duty cycle in ns
        '''
        duty_ns:int = 0
        if angle < self.min_angle or angle > self.max_angle:
            print(f"Angle must be between {self.min_angle} and {self.max_angle} degrees")
            duty_ns = int(( self.max_duty_ns + self.min_duty_ns)/2)
        else:    
            factor = (self.max_duty_ns - self.min_duty_ns)/(self.max_angle - self.min_angle)
            duty_ns = int((angle - self.min_angle) * factor + self.min_duty_ns)
        #print(f"Setting servo angle to {angle} degrees, duty_ns: {duty_ns}")
        return duty_ns

class DC_Motor:
    def __init__(self):
        pass
    def configure_pin(self, forward_pin_num, reverse_pin_num):
        # Initialize the parameters for the DC motor
        self.forward_pin = Pin(forward_pin_num, Pin.OUT)
        self.reverse_pin = Pin(reverse_pin_num, Pin.OUT)

        self.frequency = 1000  # Frequency for PWM
        self.forward_pwm = PWM(self.forward_pin, freq=self.frequency)
        self.reverse_pwm = PWM(self.reverse_pin, freq=self.frequency)
        self.forward_pwm.duty_ns(0)  # Initialize duty cycle to 0
        self.reverse_pwm.duty_ns(0)  # Initialize duty cycle to 0

        self.power = 0 #Positive power for forward, negative for reverse
        self.min_power = -100  # Minimum power
        self.max_power = 100  # Maximum power
    def set_power(self, power):
        # Set the power of the motor
        duty_ns = self._power_to_duty_ns(power)

        if power > 0:
            self.forward_pwm.duty_ns(duty_ns)
            self.reverse_pwm.duty_ns(0)
        elif power < 0:
            self.forward_pwm.duty_ns(0)
            self.reverse_pwm.duty_ns(int(duty_ns*0.5)) # Reverse motor at half power
        
        
    def _power_to_duty_ns(self, power: float) -> int:
        '''
        Convert power to duty cycle in ns. Period is 1/freqency = 1/1000 = 1ms = 1000000ns
        '''
        duty_ns:int = 0
        is_in_range = self.min_power <= power <= self.max_power
        if not is_in_range:
            print(f"power must be between {self.min_power} and {self.max_power}")
            duty_ns = 0
        else:    
            duty_ns = int((abs(power) * 1000)) # percent to ns
        return duty_ns
    

steering_servo = Servo()
propulsion_motor = DC_Motor()

def initialize():
    print("Initializing hardware drivers...")
    hw_drivers_data.rfm69_SPI = SPI(
                                    0,
                                    baudrate=500_000,
                                    polarity=0,
                                    phase=0,
                                    bits=8,
                                    firstbit=SPI.MSB,
                                    sck=Pin(RFM69_SCK_PIN),# type: ignore
                                    mosi=Pin(RFM69_MOSI_PIN),# type: ignore
                                    miso=Pin(RFM69_MISO_PIN)# type: ignore
                                    )
    hw_drivers_data.rfm69_CS = Pin(RFM69_CS_PIN, Pin.OUT)
    hw_drivers_data.rfm69_RESET = Pin(RFM69_RESET_PIN, Pin.OUT)

    steering_servo.configure_pin(SERVO_PIN)
    propulsion_motor.configure_pin(MOTOR_FWD_PIN, MOTOR_REV_PIN)

def led_control():
    LED2.value(controls_data.led2_loc_rcm)

def motor_control():

    steering_servo.set_angle(controls_data.car_turn_angle)
    propulsion_motor.set_power(controls_data.car_throttle)

def power_control():
    if controls_data.power_mode == POWER_MODES.Shutdown:
        POWER_ON_PIN.value(0)

def hw_drivers_diagnostics():
    #TODO [RC-78,RC-77]: Add diagnostics for battery voltage
    #TODO:Add diagnostics for current sensors
    pass


def task_005ms():
    '''
    This function is called every 5ms to update the servo position based on the received data.
    '''
    motor_control()

def task_100ms():
    led_control()
