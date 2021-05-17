import requests
from datetime import datetime, timedelta
from time import sleep
import smtplib, ssl

port = 465
smtp_server = "smtp.gmail.com"
sender_email = "abc@gmail.com"
receiver_email = sender_email 
password = "password"

message = """\
Subject: Vaccination center found

pincode : {}
date : {}
name : {}
address : {}
"""

pincodes = ['411033','411017']
date_no = 3
today_date = datetime.now()
un_date=[]
fo_date = []

for i in range(date_no):
    un_date = un_date + [today_date + timedelta(days=i)]

for i in un_date:
    fo_date = fo_date + [i.strftime("%d-%m-%Y")]

while True :
    shown = 0
    for pincode in pincodes:
        for date in fo_date:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

            cowin_res = requests.get(URL, headers=header)

            if cowin_res.status_code == 200 :
                result = cowin_res.json()
                for res in result["centers"]:
                    for session in res["session"]:
                        if session["available_capacity"] > 2 :
                            print("pincode : " + pincode)
                            print("date : " + date)
                            print("center name : " + res["name"])
                            message = message.format(pincode,date,res["name"],res["address"])
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                server.login(sender_email, password)
                                server.sendmail(sender_email, receiver_email, message)
                            shown = shown + 1

            else : print("error occurred, error code : " + str(cowin_res.status_code))
    
    if shown == 0 :
        print("No available slots")

    check_dt = datetime.now() + timedelta(seconds=5)

    if datetime.now() < check_dt : 
        sleep(5)
