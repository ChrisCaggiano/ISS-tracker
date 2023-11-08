import requests
import smtplib
import time
from datetime import datetime

MY_LAT = "YOUR LATITUDE HERE AS FLOAT"  # Your latitude
MY_LONG = "YOUR LONGITUDE HERE AS FLOAT"  # Your longitude
MY_EMAIL = "YOUR EMAIL HERE"
MY_PASSWORD = "YOUR PASSWORD HERE"


def send_email():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject: ISS CURRENTLY OVERHEAD\n\n"
                "Look Up"
        )


while True:
    time.sleep(60)
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    data = iss_response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    sun_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()
    data = sun_response.json()
    my_sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    my_sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print(my_sunrise)
    print(my_sunset)

    time_now = datetime.now().hour
    print(time_now)

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5 and (
            time_now > 20 or time_now < 3):
        send_email()

# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
