import datetime
import requests
import random
import smtplib
import urllib.request
import json
import time

from requests.api import request

url = 'https://www.cowin.gov.in/home'
api_endpoint_manipal = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=576104&date='
api_endpoint_kundapur = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=576201&date='
gmailaddress = "rohan.kumar.smtp@gmail.com"
gmailpassword = "Maryhadalittlelamb"
allProxies = ['https://116.203.190.255:80', 'https://180.151.231.166:80', 'https://14.99.187.7:80', 'https://13.233.244.234:80', 'https://103.52.210.237:80' ]

def alert(vaccineInfo):
    # print(vaccineInfo)
    mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
    mailServer.starttls()
    mailServer.login(gmailaddress , gmailpassword)
    mailServer.sendmail(gmailaddress, gmailaddress , vaccineInfo)
    mailServer.quit()
    print("Mailed available vaccine info!")

def cronjob():
    try:
        # Randomly choose a proxy
        proxies = {
            "https": random.choice(allProxies),
        }
        dateToday = datetime.datetime.now()
        dateStr = str(dateToday.day) + '-' + str(dateToday.month) + '-' + str(dateToday.year)  
        #response = requests.get(api_endpoint_manipal + dateStr, proxies=proxies)
        proxy_support = urllib.request.ProxyHandler({'https': proxies["https"]})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

        with urllib.request.urlopen(api_endpoint_manipal + dateStr) as response:
            # ... implement things such as 'html = response.read()'
            response = response.read()
            JSON = json.loads(response.decode('utf-8'))#response.json()
            print(JSON)
            if JSON:
                centers = JSON["centers"]
                for center in centers:
                    sessions = center["sessions"]
                    name = center["name"]
                    for session in sessions:
                        if session["available_capacity"] != 0 and session["min_age_limit"] == 18:
                            vaccine = session["vaccine"]
                            date = session["date"]
                            age = session["min_age_limit"]
                            print(name, vaccine, date, age, sep=' - ')
                            msgStr = name + " - " + vaccine + " - " + date
                            alert(msgStr)

    except:
        time.sleep(5000)
        cronjob()
        # dateToday = datetime.datetime.now()
        # dateStr = str(dateToday.day) + '-' + str(dateToday.month) + '-' + str(dateToday.year)  
        # response = requests.get(api_endpoint_kundapur + dateStr)
        # json = response.json()
        

        # centers = json["centers"]

        # for center in centers:
        #     sessions = center["sessions"]
        #     name = center["name"]
        #     for session in sessions:
        #         if session["available_capacity"] != 0:
        #             vaccine = session["vaccine"]
        #             date = session["date"]
        #             age = session["min_age_limit"]
        #             print(name, vaccine, date, age, sep=' - ')
        #             msgStr = name + " - " + vaccine + " - " + date
        #             alert(msgStr)



if __name__ == "__main__":
    cronjob()