import random

# Parameter definition
pipe_length = 2000
initial_impedance = 50  # water in pipe, no PIG inside the pipe
pig_impedance = 10 # intial guess of the PIG impedance.
pig_position = random.randint(0, pipe_length-1)  # intial pos, place at random, since there are no reference position of the start pos

# Pipe initilization, 
pipe = [initial_impedance for _ in range(pipe_length)]

# Function to update impedance when PIG is at a certain position
def update_impedance(pipe, pig_position, pig_impedance):
    pipe[pig_position] += pig_impedance

# impedance measurement
def measure_impedance(pipe):
    return pipe[-1]

# Simulate PIG movement through the pipe
for step in range(pipe_length):
    # PIG reset position
    pipe[pig_position] = initial_impedance

    pig_position = (pig_position + 1) % pipe_length
    update_impedance(pipe, pig_position, pig_impedance)
    measured_impedance = measure_impedance(pipe)
    print(f"Step {step+1}: PIG at position {pig_position}, Measured Impedance = {measured_impedance} Ohms")

