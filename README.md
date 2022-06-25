# microbit_ghosts
A client/server game for micro:bit using Neopixel LEDs and radio messaging.

**Server**
ghost_server.py
The server micro:bit is attached to an array of Neopixel LEDs of configurable length. 
Ghosts are created randonly and appear as white-lit pixels for a few seconds. 
With radion turned on, the server listens for messages from client micro:bits.
Received messages identify the chaser (client) and a direction (left/right), moving the chaser as a colouted pixel in the LED array. 
If the chaser array position equals a ghost position while the ghost is lit, the chaser scores a point and the point is send as a mesage to the client.

**Client**
ghost_client.py
The client micro:bit uses a defined name and colour to identoify itself for the messaging and LED array.
On startup, the chser name and colour are send to the server to be added the chasers
Pressing button A sends a message containing [chaser name],"right"
Pressing button B sends a message containing [chaser name],"left"
Pressing buttons A+B shows the current score.

**Message Format**
A comma-separated string with 2 elements:
 chaser name,action (see below)
E.g. "guido,left"

**Actions**
 - start
 - right
 - left

