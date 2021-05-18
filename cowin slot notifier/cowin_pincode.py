import requests
from fake_useragent import UserAgent
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
"""
add_val = """

Pincode : {}   
Date : {}
Name : {}
Address : {}
Capacity : {}"""


res_pin = []
res_date = []
res_name = []
res_add = []
res_cap = []

def format_msg(count):
    ret_msg = """"""
    for i in range(0,count):
        ret_msg = ret_msg + add_val.format(res_pin[i],res_date[i],res_name[i],res_add[i],res_cap[i])
    return  message + ret_msg

def exist(name,ex_Date):
    if name in res_name:
        i = res_name.index(name)
        if res_date[i] == ex_Date:
            return True
    return False
    
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
            temp_user_agent = UserAgent()
            header = {'User-Agent': temp_user_agent.random}

            cowin_res = requests.get(URL, headers=header)

            if cowin_res.status_code == 200 :
                result = cowin_res.json()
                for res in result["centers"]:
                    for session in res["sessions"]:
                        if session["available_capacity"] > 0 and exist(res["name"],date) == False:
                            print("pincode : " + pincode)
                            print("date : " + date)
                            print("center name : " + res["name"])
                            res_pin = res_pin + [res["pincode"]]
                            res_date = res_date + [date]
                            res_name = res_name + [res["name"]]
                            res_add = res_add + [res["address"]]
                            res_cap = res_cap + [session["available_capacity"]]
                            shown = shown + 1
                            shown = shown + 1

            else : print("error occurred, error code : " + str(cowin_res.status_code))
    
    if shown == 0 and old_res != result:
        print("No available slots")
    elif old_res != result : 
        old_res = result
        new_msg = format_msg(shown)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, new_msg)
    else : print("No new slots found")
    sleep(5)

