import os
import glob
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

search_dir = '\\\\140.8.105.121\\share\\latency\\'
file_pattern = 'Time_OUT*.txt'

files = glob.glob(search_dir + file_pattern)
if files:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('coytathichdapda445368@gmail.com', 'kmzvddfytrnzfprc')

    to_email = 'thanhbinh0316@gmail.com'
    email_subject = 'TIME OUT _ ' + datetime.datetime.now().strftime('%H:%M_%d/%m/%Y')

    msg = MIMEMultipart()
    msg['From'] = 'coytathichdapda445368@gmail.com'
    msg['To'] = to_email
    msg['Subject'] = email_subject

    for file in files:
        with open(file, 'rb') as f:
            file_content = f.read()
            msg.attach(MIMEText(file_content.decode(), 'plain'))

    text = msg.as_string()
    server.sendmail('coytathichdapda445368@gmail.com', to_email, text)
    server.quit()
