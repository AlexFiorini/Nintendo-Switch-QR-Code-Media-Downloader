import pyzbar.pyzbar as pyzbar
import pywifi
import cv2
from pywifi import const
from time import sleep
import json
import os
import urllib.request

url = "http://192.168.0.1/"
url_json = url + "data.json"
url_file = url + "img/"


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
    with urllib.request.urlopen(url_json) as response:
        data = json.loads(response.read())

    filetype = data["FileType"]
    if filetype == "photo":
        image_names = data["FileNames"]
        if not os.path.exists("img"):
            os.makedirs("img")

        for image_name in image_names:
            image_url = url_file + image_name
            save_path = os.path.join("img", image_name)
            urllib.request.urlretrieve(image_url, save_path)
    elif filetype == "movie":
        video_name = data["FileNames"][0]
        if not os.path.exists("video"):
            os.makedirs("video")

        video_url = url_file + video_name
        save_path = os.path.join("video", video_name)
        urllib.request.urlretrieve(video_url, save_path)
    else:
        raise Exception("Invalid file type")
    print("Download complete")


def read_qr_code():
    cap = cv2.VideoCapture(cv2.CAP_DSHOW)
    cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera Feed", 640, 480)
    while True:
        ret, frame = cap.read()
        cv2.imshow("Camera Feed", frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        decoded = pyzbar.decode(gray)
        for code in decoded:
            data = code.data.decode('utf-8')

            if data.startswith("WIFI:S:"):
                data = data[7:]
                parts = data.split(";")
                ssid = parts[0][0:]
                password = parts[2][2:]
            else:
                raise Exception("Invalid QR code")

            if connect_wifi(ssid, password):
                print("Connected to WiFi network:", ssid)
                openbrowser()
                cap.release()
                cv2.destroyAllWindows()
                return
            else:
                raise Exception("Failed to connect to WiFi network:", ssid)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break


def main():
    read_qr_code()


if __name__ == "__main__":
    main()
