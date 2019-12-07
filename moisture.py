import datetime
import time
import json
from pytz import timezone
import serial
import re
import requests


def json_sensor_value(con, url):
    moisture_data = re.findall(r'[0-9]+', con.readline().decode('utf-8'))
    # moisture_dataでうまく値が取れなかった時の処理です．
    if len(moisture_data) == 0:
        moisture_data = ["0"]
    now_time = datetime.datetime.now(timezone("Asia/Tokyo")).strftime("%Y%m%d %H:%M:%S")

    # 送るdict(json)データです．
    send_mes = {'datetime': now_time, 'moisture': moisture_data[0]}

    # requests post
    headers = {'Content-Type': 'application/json', }
    req = requests.put(url, data=json.dumps(send_mes).encode(), headers=headers)

    return now_time, moisture_data[0]


def main():
    url = "http://61.113.176.134:9200/"
    con = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(5)

    while True:
        now_time, moisture_data = json_sensor_value(con, url)

        print(now_time)
        print("Moisture   : {0}".format(moisture_data))

        print("\n")
        time.sleep(1)


if __name__ == "__main__":
    main()
