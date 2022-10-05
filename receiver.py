import pigpio
import time
from convertUtility import bytesToMessage
from chatProcessor import processChat
import constants

CLOCKSPEED = 0.01

BIT_STUFF_RUN_LENGTH = 6

switch_time = None

def switch_callback(a, b, c):
    global switch_time
    switch_time = time.time()

def sleepCorrection():
    if switch_time is None:
        time.sleep(CLOCKSPEED)
    else:
        difference = time.time() - switch_time
        if difference <= CLOCKSPEED:
            time.sleep(CLOCKSPEED + (CLOCKSPEED / 2 - difference))
        else:
            time.sleep(CLOCKSPEED)

def listen(pi, GPIO_RECEIVER_NUMBER):
    start = "0101001001110111"

    stop = "0101100101110111"

    state = "readingStart"

    buffer = ""

    message_buffer = ""

    runValue = None

    runLength = 0

    while True:
        bit = str(pi.read(GPIO_RECEIVER_NUMBER))

        if (runLength == BIT_STUFF_RUN_LENGTH):
            runLength = 1
            runValue = bit
            sleepCorrection()
            continue

        runLength = (runLength + 1) if (bit == runValue) else 1

        runValue = bit

        if state == "readingStart":
            if len(buffer) >= len(start):
                buffer = buffer[1:]

            buffer += bit

            if buffer == start:
                buffer = ""
                state = "readingMessage"

        elif state == "readingMessage":
            message_buffer += bit

            if len(buffer) >= len(stop):
                buffer = buffer[1:]

            buffer += bit

            if buffer == stop:
                buffer = ""
                state = "readingStart"

                message_buffer = message_buffer[:-1 * len(stop)]
                processChat(message_buffer)
                message_buffer = ""
        sleepCorrection()

def listenForData(port):

    GPIO_RECEIVER_NUMBER = constants.GPIO_RECEIVER_NUMBER(port)

    pi = pigpio.pi()

    pi.callback(GPIO_RECEIVER_NUMBER, pigpio.EITHER_EDGE, switch_callback)

    listen(pi, GPIO_RECEIVER_NUMBER)
