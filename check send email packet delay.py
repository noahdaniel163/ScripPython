import subprocess
import os
import datetime

# Define the target website to ping
target = "adpusan.co.kr"
#target = "amazon.com"
#target = "1.1.1.1"
# Run ping command and capture the STDOUT
process = subprocess.Popen(["ping", "-n", "5", target], stdout=subprocess.PIPE)
output = process.stdout.read().decode()

# If connection is successful
if "time=" in output:
    # Extract the time value from the output
    time_value = int(output.split("time=")[1].split("ms")[0].strip())

    # Create the filename based on the latency threshold
    now = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    if time_value < 100:
        filename = f"Low_latency_{now}.txt"
    else:
        filename = f"High_latency_{now}.txt"

    # Define the path to the shared folder and create the file
    shared_folder = r"\\140.8.105.121\share\latency"
    filepath = os.path.join(shared_folder, filename)
    
    # Write ping result to the file
    with open(filepath, "w") as file:
        file.write(f"Latency test\n{output}")

# If connection is unsuccessful
else:
    # Create the filename based on the current time
    now = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    filename = f"Time_OUT_{now}.txt"

    # Define the path to the shared folder and create the file
    shared_folder = r"\\140.8.105.121\share\latency"
    filepath = os.path.join(shared_folder, filename)

    # Write ping result to the file
    with open(filepath, "w") as file:
        file.write(f"Connection timed out\n{output}")
