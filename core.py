import sensor_module
import voltage_module
import temperature_module
import current_module
import relay_module
import actuator_module
import time


program_step_time = 0.010 # 10 ms

# how many counts for each timeperiod
counts_10ms = 0.010 / program_step_time
counts_20ms = 0.020 / program_step_time
counts_50ms = 0.050 / program_step_time







if __name__ == '__main__':
	#TODO Initialize the module objects

	#TODO load calibrations from file

	# Use to 
	run_program = True 
	
	#count the number of iterations
	program_counter = 0
	init = time.time()
	while run_program:

		if(program_counter % counts_10ms == 0):
			# 10 ms modules
			pass

		if(program_counter % counts_20ms == 0):
			# 20 ms modules
			pass
		if(program_counter % counts_50ms == 0):
			# 50 ms modules
			pass

		program_counter += 1

		# Temporarily including to end the program after 5 minutes while in development 
		#TODO remove this
		if(program_counter >= 300/program_step_time):
			run_program = False
		#print(time.time() - init)
		time.sleep(program_step_time) # sleep for 10 ms

	# clean up
		