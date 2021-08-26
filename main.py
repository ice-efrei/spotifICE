"""
Spotifice
A program for raspberry pi to activate music from spotify when something is detected by the HC-SR04 sensor.
"""
from time import sleep, time
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from USERNAME import USERNAME

scope = 'user-modify-playback-state user-read-playback-state app-remote-control user-read-currently-playing ' \
        'streaming ugc-image-upload '

initial_playlist = 'spotify:playlist:0vvXsWCC9xrXsKd4FyS8kM'

GPIO_TRIGGER = 18
GPIO_ECHO = 24

TARGET_DEVICE = 'Redmi Note 7'


def distance():
    """
    do a ping with a HC-SR04 sensor
    (source : https://raspberrypi-tutorials.fr/utilisation-dun-capteur-de-distance-raspberry-pi-capteur-ultrasonique-hc-sr04/)
    :return: distance of the pinged object
    """
    GPIO.output(GPIO_TRIGGER, True)
    sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time()
    StopTime = time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time()
    # --- while ---

    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time()
    # --- while ---

    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s) and divide by 2, because there and back
    return (TimeElapsed * 34300) / 2
# --- distance ---


def standby():
    """
    block the program in a infinite loop until something pass below <insert distance>cm of the HC-SR04 sensor
    :return: True when something is detected
    """

    while distance() > 4:
        sleep(0.5)
    # --- distance ---

    return True
# --- standby ---


if __name__ == "__main__":
    # GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)

    # set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    print("--- start ---")

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(username=USERNAME, scope=scope))

    device = None
    for i in sp.devices()['devices']:
        if i['id'] == TARGET_DEVICE:
            device = i['id']
        # --- if ---
    # --- for ---

    standby()

    sp.start_playback(device_id=device, context_uri=initial_playlist)

    print("--- end ---")
# --- main ---
