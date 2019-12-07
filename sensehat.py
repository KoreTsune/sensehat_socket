from sense_hat import SenseHat
import datetime
import time
import json
from pytz import timezone
import urllib.request


def json_sensor_value(sense, url):
    humidity = sense.get_humidity()
    temp = sense.get_temperature_from_humidity()
    pressure = sense.get_pressure()
    now_time = datetime.datetime.now(timezone("Asia/Tokyo")).strftime("%Y%m%d %H:%M:%S")

    # 送るdict(json)データです．
    send_mes = {'datetime': now_time, 'humidity': humidity, 'temp': temp, 'press': pressure}

    # requests post
    headers = {'Content-Type': 'application/json', }
    req = urllib.request.Request(url, json.dumps(send_mes).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()

    return now_time, humidity, temp, pressure


def main():
    sense = SenseHat()
    url = ""
    sense.clear()
    time.sleep(5)

    while True:
        now_time, humidity, temp, pressure = json_sensor_value(sense, url)

        print(now_time)
        print("Humidity   : {0}".format(humidity))
        print("Temparature: {0}".format(temp))
        print("Pressure   : {0}".format(pressure))

        print("\n")
        time.sleep(1)


if __name__ == "__main__":
    main()
