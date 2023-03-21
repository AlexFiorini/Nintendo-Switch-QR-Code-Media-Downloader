import os

from cv2 import cv2


def print_hi(name):
    print(f'Hi, {name}')


def decode_qr_code(img):
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    if data not in [None, '']:
        print(data)
        return 1


def Webcam():
    webcam = cv2.VideoCapture(0)
    currentframe = 0
    detected = 0

    while not detected:
        success, frame = webcam.read()
        cv2.imshow("Output", frame)
        cv2.imwrite('Frame' + str(currentframe) + '.jpg', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        detected = decode_qr_code(frame)
        os.system('del Frame' + str(currentframe) + '.jpg')
    webcam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    Webcam()
