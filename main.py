from os import startfile

import pyzbar.pyzbar as pyzbar
import pywifi
import cv2
from pywifi import const
from time import sleep


def connect_wifi(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    sleep(2)
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.key = password
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    iface.remove_all_network_profiles()
    profile_new = iface.add_network_profile(profile)
    iface.connect(profile_new)
    sleep(2)
    if iface.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False


def openbrowser():
    startfile("http://192.168.0.1/index.html")


def read_qr_code():
    cap = cv2.VideoCapture(1)
    cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera Feed", 640, 480)
    while True:
        ret, frame = cap.read()
        cv2.imshow("Camera Feed", frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        decoded = pyzbar.decode(gray)
        for code in decoded:
            data = code.data.decode('utf-8')
            print("QR Code Data:", data)
            if data.startswith("WIFI:S:"):
                data = data[7:]
                parts = data.split(";")
                ssid = parts[0][0:]
                password = parts[2][2:]
                print("SSID:", ssid)
                print("Password:", password)
            else:
                print("Invalid QR code")
                return
            if connect_wifi(ssid, password):
                print("Connected to WiFi network:", ssid)
                openbrowser()
                cap.release()
                cv2.destroyAllWindows()
                return
            else:
                print("Failed to connect to WiFi network:", ssid)
                return
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break


read_qr_code()
