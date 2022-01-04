# This project uses an Adafruit Neokey Trinkey to enter keyboard input to keep
# Final Fantasy IXV from activating the automatic log out. Pushing the button on
# the Trinkey should start regular keyboard entry. Pushing it again should stop
# the keyboard entry.
#
# This version does not have very accurate time values. When the frequency
# is set to 10 minutes, the actual intervals run roughly 7 seconds too long.
# This is because I'm making assumptions regarding the delay and execution
# time that are slightly off. I'm currently adding wait times when I probably
# should be running a global timer.
#
# The LED color is set in the statements that resemble:
# pixel.fill((0, 75, 0))
# The three comma separated values control the color and brightness of the LED
# In order, the values are for Red, Green, and Blue. The higher the number
# brighter the particular color is. (0, 0, 0) is completely off.
# (255, 255, 255) is the brightest white light available.
import time
import board
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from digitalio import DigitalInOut, Pull


print("NeoKey Trinkey FFXIV 'Away' Typer")

# some default variables to get us started
firstrun = True
secs = 0
mins = 0
total_minutes = 0
# This number is the frequency of the regular message in minutes.
freq = 10
# I'm setting the default to free company chat, but this could be an emote or any command really
# don't add a / to it becasue the code will do that for you.
base_cmd = 'fc'
# This is the first text that will type when you initially hit the button to go away.
intro_txt = "This is not where I am. So, I will be away."
# This text is what will be typed at regular intervals. {h} will be replaced with the current away hours
# at execution time and {m} will be replaced with the current away minutes at time of execution.
reg_txt = "It has been {h} hours and {m} minutes since I last was where I was."

# create the pixel and turn it off
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
pixel.fill((0,0,0))

time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

# create the switch, add a pullup, start it with not being pressed
button = DigitalInOut(board.SWITCH)
button.switch_to_input(pull=Pull.DOWN)
button_state = False

while True:
    if button.value and not button_state:
        for i in range(1,5):
            pixel.fill((0, 100, 0))
            time.sleep(0.1)
            pixel.fill((0, 0, 0))
            time.sleep(0.1)
        pixel.fill((0, 100, 0))
        print("Button pressed and now we begin...")
        print("After entering an initial command, a regular command will be entered every %s minutes" % (freq))
        time.sleep(0.1)
        button_state = True

    if button.value and button_state:
        for i in range(1,5):
            pixel.fill((0, 0, 0))
            time.sleep(0.1)
            pixel.fill((0, 100, 0))
            time.sleep(0.1)
        pixel.fill((0, 0, 0))
        print("Button pressed again and now we stop.")
        time.sleep(0.1)
        firstrun = True
        secs = 0
        mins = 0
        total_minutes = 0
        button_state = False
    if button_state:
        #pixel.fill((0,196,0))
        if firstrun == True:
            # Change the color of the LED while the device is typing
            pixel.fill((100,0,100))
            keyboard_layout.write('/')  # this will enter command mode in FFXIV
            time.sleep(0.6) # give the interface time to register the slash and change modes
            secs += 6 # keep the time right
            # This loop enter a single character at a time very slowly because my initial tests with a Playstation 4
            # indicated the device was typing the characters too quickly for the console.
            loop_secs = 0
            for c in base_cmd + ' ' + intro_txt:
                keyboard_layout.write(c)  # some kind of command like fc or ls or an emote
                time.sleep(0.1) # slight delay
                loop_secs += 1 # keep the time right
            secs += loop_secs # keep the time right
            keyboard_layout.write("\n")  # hit the enter key
            time.sleep(0.1) # slight delay
            secs += 1 # keep the time right
            # Change the LED color back to the running color
            pixel.fill((0,100,0))
            firstrun = False
        if mins == freq:
            # Change the color of the LED while the device is typing
            pixel.fill((100,0,100))
            chat_txt = reg_txt.format(h = (total_minutes//60),m = (total_minutes%60))
            keyboard_layout.write('/')  # this will enter command mode in FFXIV
            time.sleep(0.6) # give the interface time to register the slash and change modes
            loop_secs = 0
            # This loop enter a single character at a time very slowly because my initial tests with a Playstation 4
            # indicated the device was typing the characters too quickly for the console.
            for c in base_cmd + ' ' + chat_txt:
                keyboard_layout.write(c)  # some kind of command like fc or ls or an emote
                time.sleep(0.1) # slight delay
                loop_secs += 1 # keep the time right
            secs += loop_secs # keep the time right            keyboard_layout.write(chat_txt)  # some kind of command like fc or ls or an emote
            keyboard_layout.write("\n")  # hit the enter key
            time.sleep(0.1) # slight delay
            secs += 1 # keep the time right
            secs = 0
            mins = 0
            # Change the LED color back to the running color
            pixel.fill((0,100,0))
        time.sleep(0.1)
        secs += 1
        if secs == 600:
            mins += 1
            total_minutes += 1
            secs = 0
            print("%s Minutes have passed in this loop. %s hours and %s minutes have passed overall." % (mins,total_minutes//60,total_minutes%60))
