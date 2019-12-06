from sense_hat import SenseHat
import time
import datetime
import socket
import time
import sys
import json
import requests
from pytz import timezone
import serial
import re
import urllib.request


port_num = 12345
server_ip = "192.168.0.110"
url = ""

def socket_connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, port_num))
    print("connect")
    return  sock

def json_senservalue(sense, con, url):
    humidity      = sense.get_humidity()
    temp          = sense.get_temperature_from_humidity()
    pressure      = sense.get_pressure()
    moisture_data = re.findall(r'[0-9]+', con.readline().decode('utf-8'))
    now_time      = datetime.datetime.now(timezone("Asia/Tokyo")).strftime("%Y%m%d %H:%M:%S")

    send_mes      = {'datetime':now_time, 'humidity':humidity, 'temp':temp, 'press':pressure, 'moisture':moisture_data[0]}
    
    #requests post
    headers = {'Content-Type': 'application/json',}
    req = urllib.request.Request(url, json.dumps(send_mes).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()

    #send_mes_str = json.dumps(send_mes).encode("UTF-8")
    return now_time, humidity, temp, pressure, moisture_data[0]
    #return send_mes_str, now_time, humidity, temp, pressure, moisture_data[0]

def main():
#    sock = socket_connect()
    sense = SenseHat()
    sense.clear()
    con = serial.Serial('/dev/ttyACM0', 9600)

    while True:
        now_time, humidity, temp, pressure, moisture_data = json_senservalue(sense, con, url)
        #send_mes_str, now_time, humidity, temp, pressure, moisture_data = json_senservalue(sense, con)
        #sock.send(send_mes_str)

        print(now_time)
        print("Humidity   : {0}".format(humidity))
        print("Temparature: {0}".format(temp))
        print("Pressure   : {0}".format(pressure))
        print("Moisture   : {0}".format(moisture_data))

        print("\n")
        time.sleep(1)


if __name__ == "__main__":
    main()
