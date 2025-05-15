# boot.py
import network
import time

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    for _ in range(10):
        if wlan.isconnected():
            print("Verbunden mit WLAN:", wlan.ifconfig())
            return True
        time.sleep(1)
    print("Keine WLAN-Verbindung.")
    return False

# WLAN-Daten hier eintragen:
connect_wifi("CoCoLabor2", "cocolabor12345")