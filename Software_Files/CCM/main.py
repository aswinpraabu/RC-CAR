#from CCM_Submodules import global_data,actuators
from CCM_Submodules import hw_drivers
from CCM_Submodules import rf_comms
from CCM_Submodules import controls

from time import sleep_ms, ticks_ms, ticks_diff

# CCM = Car Control Module
# this module is responsible for controlling the car's hardware components

def initialize():

	hw_drivers.initialize()  # Initialize hardware drivers
	rf_comms.initialize()  # Initialize radio communications
	

def task_005ms():
	#print("Running Main 5ms task...")
	rf_comms.task_005ms()
	controls.task_005ms()
	hw_drivers.task_005ms()


def task_010ms():
	rf_comms.task_010ms()
	controls.task_010ms()
	

def task_100ms():
	controls.task_100ms()
	hw_drivers.task_100ms()


if __name__ == "__main__":
	initialize()
	timer_ref_005ms = timer_ref_010ms = timer_ref_100ms = ticks_ms()

	while True:
		#print("Main loop running... {0}ms".format(ticks_diff(ticks_ms(), timer_ref_005ms)))
		if ticks_diff(ticks_ms(), timer_ref_005ms) >= 5:
			#print("5ms task executed")
			timer_ref_005ms = ticks_ms() # Reset the 5ms timer reference
			task_005ms()
			#print("5ms task time: {0}ms".format(ticks_diff(ticks_ms(), timer_ref_005ms)))
		if ticks_diff(ticks_ms(), timer_ref_010ms) >= 10:
			timer_ref_010ms = ticks_ms() # Reset the 10ms timer reference
			task_010ms()
		if ticks_diff(ticks_ms(), timer_ref_100ms) >= 100:
			timer_ref_100ms = ticks_ms() # Reset the 100ms timer reference
			task_100ms()		