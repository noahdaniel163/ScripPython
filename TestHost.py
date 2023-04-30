import smtplib
import subprocess

def send_email(subject, body):
    sender_email = "coytathichdapda445368@gmail.com"
    sender_password = "kmzvddfytrnzfprc"
    receiver_email = "thanhbinh0316@gmail.com"

    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)
#host = "Google.com"
host = "adpusan.co.kr"

response = subprocess.Popen(["ping", "-c", "1", host], stdout=subprocess.PIPE).stdout.read().decode('utf-8')

if "1 received" in response:
    send_email("Ping result", f"{host} is up and running! Ping result: {response}")
else:
    send_email("Ping result", f"{host} is down! Ping result: {response}")
