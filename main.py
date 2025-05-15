from machine import Pin, time_pulse_us
import time
import esp32
import ota_server
import _thread

led = Pin(33, Pin.OUT)
button = Pin(14, Pin.IN)
trig = Pin(26, Pin.OUT)    
echo = Pin(25, Pin.IN)

def start_ota():
    ota_server.start_ota_server()

_thread.start_new_thread(start_ota, ()) #OTA Server muss in neuem Thread gestartet werden da sonst der Hauptprozess blockiert wird


while True:
    if button.value() == 1:
        led.on()
    else:
        led.off()

    
    
    