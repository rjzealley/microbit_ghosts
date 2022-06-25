# ghost_chasers
# Send messages to ghost_server to move chasers

# import microbit libraries
from microbit import *

# Import radio libraries
import radio

# Turn the radio on
radio.on()

# Set the chaser name by entering some characters 
# between the quotes, e.g. "guido"
name = ""

# Set the RGB values for the chaser colour
# Set each colour to a number between 0 and 15
# e.g. 
red = 15
green = 0
blue = 15

# Reset the score
score = 0

# Tell the server about this chaser
radio.send(name + ",start," + str(red) + "," + str(green) + "," + str(blue))

# Event loop, listens for incoming message
while True:
    # Check radio for score update
    # Read any incoming messages.
    incoming = radio.receive()
    if incoming is not None:
        bits = str(incoming).strip().split(",")
        if len(bits) >= 2:
            if bits[0] == name:
                if bits[1] == 'score':
                    score = int(bits[2])
                    
    message = ""

    # Button A left, b right
    if button_a.is_pressed() and button_b.is_pressed():
        display.scroll(str(score))
    elif button_a.was_pressed():
        message = "left"
        image = Image.ARROW_E        
    elif button_b.was_pressed():
        message = "right"
        image = Image.ARROW_W
        
    if (message != ''):
        display.show(image)
        
        # Send the message using the radio send function
        radio.send(name + "," + message)
        
        sleep(250)
        display.clear()

