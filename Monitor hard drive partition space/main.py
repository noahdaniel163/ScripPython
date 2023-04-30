import psutil

# Get all disk partitions
partitions = psutil.disk_partitions()

# Loop through each partition
for partition in partitions:
    print(f"Device: {partition.device}")
    print(f"Mountpoint: {partition.mountpoint}")
    print(f"File system type: {partition.fstype}")
    
    # Get the usage statistics of the partition
    usage = psutil.disk_usage(partition.mountpoint)
    print(f"Total space: {usage.total}")
    print(f"Used space: {usage.used}")
    print(f"Free space: {usage.free}")
    print(f"Percentage used: {usage.percent}%\n")
