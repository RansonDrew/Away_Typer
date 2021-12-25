# This project uses an Adafruit Neokey Trinkey to enter keyboard input to keep
# Final Fantasy IXV from activating the automatic log out. Pushing the button on
# the Trinkey should start regular keyboard entry. Pushing it again should stop
# the keyboard entry.
import time
import board
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode  # pylint: disable=unused-import
from digitalio import DigitalInOut, Pull


print("NeoKey Trinkey FFXIV 'Away' Typer")

# some default variables to get us started
firstrun = True
freq = 10
secs = 0
mins = 0
total_minutes = 0
base_cmd = 'fc '

# create the pixel and turn it off
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
pixel.fill(0x0)

time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

# create the switch, add a pullup, start it with not being pressed
button = DigitalInOut(board.SWITCH)
button.switch_to_input(pull=Pull.DOWN)
button_state = False

while True:
    if button.value and not button_state:
        pixel.fill((0, 196, 0))
        print("Button pressed and now we begin...")
        print("After entering an initial command, a regular command will be entered every %s minutes" % (freq))
        time.sleep(0.1)
        button_state = True

    if button.value and button_state:
        pixel.fill(0x0)
        print("Button pressed again and now we stop.")
        time.sleep(0.1)
        firstrun = True
        secs = 0
        mins = 0
        total_minutes = 0
        button_state = False
    if button_state:
        pixel.fill((0,196,0))
        if firstrun == True:
            keyboard_layout.write('/')  # this will enter command mode in FFXIV
            time.sleep(0.6) # give the interface time to register the slash and change modes
            secs += 6 # keep the time right
            keyboard_layout.write(base_cmd)  # some kind of command like fc or ls or an emote
            time.sleep(0.1) # slight delay
            secs += 1 # keep the time right
            keyboard_layout.write("For the foreseeable future, I will be away. However, my presence will remain.\n")  # some kind of command like fc or ls or an emote
            time.sleep(0.1) # slight delay
            secs += 1 # keep the time right
            firstrun = False
        if mins == freq:
            chat_txt = "It has been {h} hours and {m} minutes since I did that thing. \n".format(h = (total_minutes//60),m = (total_minutes%60))
            keyboard_layout.write('/')  # this will enter command mode in FFXIV
            time.sleep(0.6) # give the interface time to register the slash and change modes
            keyboard_layout.write(base_cmd)  # some kind of command like fc or ls or an emote
            time.sleep(0.1) # slight delay
            keyboard_layout.write(chat_txt)  # some kind of command like fc or ls or an emote
            time.sleep(0.1) # slight delay
            secs = 0
            mins = 0
        time.sleep(0.1)
        secs += 1
        if secs == 600:
            mins += 1
            total_minutes += 1
            secs = 0
            print("%s Minutes have passed in this loop. %s hours and %s minutes have passed overall." % (mins,total_minutes//60,total_minutes%60))
