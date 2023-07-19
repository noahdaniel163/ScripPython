import random
import csv

def generate_random_time():
    hours = random.randint(8, 17)
    minutes = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
    return f"{hours:02d}:{minutes:02d}"

def generate_close_time(start_time):
    start_hour, start_minute = map(int, start_time.split(":"))
    available_minutes = [i for i in range(0, 60, 5)]
    close_minute = random.choice(available_minutes)
    
    if close_minute < start_minute:
        close_hour = start_hour + 1
    else:
        close_hour = start_hour
    
    return f"{close_hour:02d}:{close_minute:02d}"

def generate_start_close_times():
    start_time = generate_random_time()

    if start_time < "08:30" or (start_time > "11:30" and start_time < "13:00") or start_time > "17:30":
        return generate_start_close_times()

    call_time = start_time
    close_time = generate_close_time(start_time)

    if (start_time >= "08:30" and close_time < "08:30") or (start_time >= "13:00" and close_time < "13:00"):
        return generate_start_close_times()

    if close_time < call_time or close_time > "23:55":
        return generate_start_close_times()

    return start_time, close_time

# Tạo danh sách 30 cặp thời gian Start Time và Close Time
data = []
for _ in range(30):
    start_time, close_time = generate_start_close_times()
    data.append([start_time, close_time])

# Lưu vào file CSV trên ổ đĩa E:
filename = "E:/time_data.csv"
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)
    
print("Đã lưu dữ liệu vào file", filename)
