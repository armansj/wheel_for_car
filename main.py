import network
import socket
from machine import Pin
import utime

ssid = "Vodafone-820C"
password = "xc5dadQYrqpo2J2sd2q2"


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while wlan.isconnected() == False:
        print('Waiting for connection...')
        utime.sleep(1)

    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


rotary_pin_A = Pin(11, Pin.IN, Pin.PULL_UP)
rotary_pin_B = Pin(12, Pin.IN, Pin.PULL_UP)

button_W = Pin(15, Pin.IN, Pin.PULL_UP)
button_S = Pin(14, Pin.IN, Pin.PULL_UP)
button_L = Pin(13, Pin.IN, Pin.PULL_UP)

last_A = rotary_pin_A.value()
position = 0
previous_position = 0

# Connect to Wi-Fi
ip = connect_wifi()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (ip, 65432)
sock.bind(server_address)

sock.listen(1)
print('Waiting for a connection...')
connection, client_address = sock.accept()
print(f'Connection from {client_address}')


def send_key(key):
    try:
        connection.sendall(key.encode())
    except OSError as e:
        print(f"Error sending data: {e}")


def read_rotary():
    global last_A, position, previous_position
    current_A = rotary_pin_A.value()
    current_B = rotary_pin_B.value()

    if current_A != last_A:
        last_A = current_A
        if current_A != current_B:
            position += 1
            send_key("RIGHT_ARROW")
        else:
            position -= 1
            send_key("LEFT_ARROW")

        previous_position = position


while True:
    read_rotary()

    if not button_W.value():
        send_key("UP_ARROW")
        utime.sleep(0.2)

    if not button_S.value():
        send_key("DOWN_ARROW")
        utime.sleep(0.2)

    if not button_L.value():
        send_key("SPACE_KEY")
        utime.sleep(0.2)

    utime.sleep(0.01)

