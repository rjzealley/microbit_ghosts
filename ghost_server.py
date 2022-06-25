"""
ghost_server
Genrates random white ghost LEDs
Waits for radio input from multiple chasers
Adds chaser to array and moves left/right
Catch ghost by moving to same LED while ghost is lit
Message format: name,'start',R,G,B - creates chaser identified by name
(R,G,B = RGB colour combination)
Message format: name,'left'
Message format: name,'right'
"""

# Import microbit libraries
from microbit import *

# import random number library
from random import randint

# Import radio library
import radio

# Import music library
# import music

# Import NeoPixel libraries
import neopixel

# Setup the Neopixel strip on pin0 with a length of 32 LEDs (8 x 4)
# These will be numbered 0 to 23
pixels = 32
np = neopixel.NeoPixel(pin0, pixels)

# Start by clearing the display
np.clear()

# The radio won't work unless it's switched on.
radio.on()

max_ghosts = 5
ghosts = []
chasers = []


# Classes
# A Ghost is a white pixel that appears for a random time (1 to 5 seconds)
# Statuses
class Ghost:
    def __init__(self):
        self.pos = randint(0, pixels - 1)
        self.start = running_time()
        self.life = randint(1, 5) * 1000
        self.status = 1
        # print("Make ghost at:" + str(self.pos) + " for " + str(self.life ))


class Chaser:
    def __init__(self, name, colour):
        self.name = name
        self.pos = 0
        self.colour = colour
        self.score = 0
        self.move = ""


# Start with empty list of ghosts and chasers
def initialise():
    game_start = running_time()
    ghosts = []
    chasers = []
    np.clear()
    return


def process_ghosts(gs):
    new_ghosts = []

    # Ensure there is at least one ghost at all times
    if len(gs) == 0 or (len(gs) < max_ghosts and randint(0, 4)) == 1:
        g = Ghost()
        np[g.pos] = (16, 16, 16)
        new_ghosts.append(g)

    for g in gs:
        # Check still alive
        if running_time() < g.start + g.life and g.status == 1:
            # Show it
            np[g.pos] = (16, 16, 16)
            # Keep in new list
            new_ghosts.append(g)
        else:
            # Ignore it so dropped from list
            # print("Kill ghost at:" + str(g.pos))
            # Turn off LED
            np[g.pos] = (0, 0, 0)

    # Show total no of ghosts
    # display.show(str(len(gs)))

    return new_ghosts


def process_chasers(cs, gs):
    for c in cs:
        # Hide
        np[c.pos] = (0, 0, 0)

        # Check if moved
        if c.move == 'left':
            if c.pos > 0:
                c.pos -= 1
            else:
                c.pos = pixels - 1
        elif c.move == 'right':
            if c.pos < (pixels - 1):
                c.pos += 1
            else:
                c.pos = 0

        # Check for a ghost
        for g in gs:
            # Kill if moved and on same pixel and not already dead
            if c.move != '' and g.pos == c.pos and g.status == 1:
                # Increase score
                c.score += 1
                # display.show(str(c.score))
                radio.send(c.name + ",score," + str(c.score))

                # Show kill as chaser colour * 4
                np[g.pos] = tuple(i * 8 for i in c.colour)

                # Set to die when next processed
                g.status = 0
                # print("Killed ghost at " + str(g.pos))
            else:
                # Show in new position
                np[c.pos] = c.colour

        # Cancel any move
        c.move = ""

    return


def process_message(msg, cs):
    # Get values
    bits = msg.strip().split(",")

    # Must be at least 2 bits to command
    if len(bits) >= 2:

        # Get chaser name and action
        name = bits[0]
        action = bits[1]

        # Check for valid action
        for c in cs:
            if c.name == name:
                if action in ('left', 'right'):
                    c.move = action
                break
        else:
            c = None

        if c is None and action == 'start':
            chasers.append(Chaser(name, (int(bits[2]), int(bits[3]), int(bits[4]))))

    return


# Start game
initialise()

# Temporary, single player
# chasers.append(Chaser("temp", (0, 0, 16)))

display.show(Image.HAPPY)

# Event loop, listens for incoming message
while True:

    """ Button A left, b right
    if button_a.is_pressed():
        chasers[0].move = "left"
    elif button_b.is_pressed():
        chasers[0].move = "right"""

    # Process ghosts
    ghosts = process_ghosts(ghosts)

    # Process chasers
    process_chasers(chasers, ghosts)

    # Read any incoming messages.
    msg = radio.receive()
    if msg is not None:
        # print(str(msg))
        process_message(str(msg), chasers)

    # Show pixels
    np.show()

    # Slow things down
    sleep(250)
    # print("tick")