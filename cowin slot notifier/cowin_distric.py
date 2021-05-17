import requests
from requests.models import Response
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

District : {}   
Date : {}
Name : {}
Address : {}
Capacity : {}"""


res_dist = []
res_date = []
res_name = []
res_add = []
res_cap = []

def format_msg(count):
    ret_msg = """"""
    for i in range(0,count):
        ret_msg = ret_msg + add_val.format(res_dist[i],res_date[i],res_name[i],res_add[i],res_cap[i])
    return  message + ret_msg

districts = ['363']
date_no = 3
today_date = datetime.now()
un_date=[]
fo_date = []
old_res = {}


for i in range(date_no):
    un_date = un_date + [today_date + timedelta(days=i)]

for i in un_date:
    fo_date = fo_date + [i.strftime("%d-%m-%Y")]

while True :
    shown = 0
    for district in districts:
        for date in fo_date:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(district, date)
            temp_user_agent = UserAgent()
            header = {'User-Agent': temp_user_agent.random}

            cowin_res = requests.get(URL, headers=header)

            if cowin_res.status_code == 200 :
                result = cowin_res.json()
                for res in result["centers"]:
                    for session in res["sessions"]:
                        if session["available_capacity"] > 0 :
                            print("district : " + res["district_name"])
                            print("date : " + date)
                            print("center name : " + res["name"])
                            res_dist = res_dist + [res["district_name"]]
                            res_date = res_date + [date]
                            res_name = res_name + [res["name"]]
                            res_add = res_add + [res["address"]]
                            res_cap = res_cap + [session["available_capacity"]]
                            shown = shown + 1
            else : print("error occurred, error code : " + str(cowin_res.status_code))
    
    if shown == 0 :
        print("No available slots")
    elif old_res != result : 
        old_res = result
        new_msg = format_msg(shown)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, new_msg)
    sleep(5)

