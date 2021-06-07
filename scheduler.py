import datetime
import requests
import smtplib

url = 'https://www.cowin.gov.in/home'
api_endpoint_manipal = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=576104&date=';
api_endpoint_kundapur = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=576201&date=';
gmailaddress = "rohan.kumar.smtp@gmail.com"
gmailpassword = "Maryhadalittlelamb"

def alert(vaccineInfo):
    # print(vaccineInfo)
    mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
    mailServer.starttls()
    mailServer.login(gmailaddress , gmailpassword)
    mailServer.sendmail(gmailaddress, gmailaddress , vaccineInfo)
    mailServer.quit()
    print("Mailed available vaccine info!")

def cronjob():
    dateToday = datetime.datetime.now()
    dateStr = str(dateToday.day) + '-' + str(dateToday.month) + '-' + str(dateToday.year)  
    response = requests.get(api_endpoint_manipal + dateStr)
    json = response.json()
    print(json)
    if json:
        centers = json["centers"]
        for center in centers:
            sessions = center["sessions"]
            name = center["name"]
            for session in sessions:
                if session["available_capacity"] != 0:
                    vaccine = session["vaccine"]
                    date = session["date"]
                    age = session["min_age_limit"]
                    print(name, vaccine, date, age, sep=' - ')
                    msgStr = name + " - " + vaccine + " - " + date
                    alert(msgStr)

        dateToday = datetime.datetime.now()
        dateStr = str(dateToday.day) + '-' + str(dateToday.month) + '-' + str(dateToday.year)  
        response = requests.get(api_endpoint_kundapur + dateStr)
        json = response.json()
        

        centers = json["centers"]

        for center in centers:
            sessions = center["sessions"]
            name = center["name"]
            for session in sessions:
                if session["available_capacity"] != 0:
                    vaccine = session["vaccine"]
                    date = session["date"]
                    age = session["min_age_limit"]
                    print(name, vaccine, date, age, sep=' - ')
                    msgStr = name + " - " + vaccine + " - " + date
                    alert(msgStr)



if __name__ == "__main__":
    cronjob()