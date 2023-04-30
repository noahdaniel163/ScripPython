import psutil

def get_disk_partitions():
    partitions = psutil.disk_partitions()
    return partitions

def get_partition_usage(partition):
    usage = psutil.disk_usage(partition.mountpoint)
    return usage
