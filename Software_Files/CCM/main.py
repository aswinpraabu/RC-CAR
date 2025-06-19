from CCM_Submodules import global_data
from CCM_Submodules import hw_drivers
from CCM_Submodules import rf_comms

from time import sleep_ms, ticks_ms, ticks_diff

# CCM = Car Control Module
# this module is responsible for controlling the car's hardware components

def initialize():
	pass

def task_005ms():
	pass

def task_010ms():
	pass

def task_100ms():
	pass


if __name__ == "__main__":
	initialize()
	timer_ref_005ms = timer_ref_010ms = timer_ref_100ms = ticks_ms()

	while True:
		if ticks_diff(ticks_ms(), timer_ref_005ms) >= 5:
			timer_ref_005ms = ticks_ms() # Reset the 5ms timer reference
			task_005ms()
		if ticks_diff(ticks_ms(), timer_ref_010ms) >= 10:
			timer_ref_010ms = ticks_ms() # Reset the 10ms timer reference
			task_010ms()
		if ticks_diff(ticks_ms(), timer_ref_100ms) >= 100:
			timer_ref_100ms = ticks_ms() # Reset the 100ms timer reference
			task_100ms()		