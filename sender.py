import pigpio
import time

clockspeed = 0.01

start = "0101001001110111"
stop = "0101100101110111"
wake = "10"

def send_sequence(pi, message, GPIO_TRANSMITTER_NUMBERS):
    for bit in message:
        for number in GPIO_TRANSMITTER_NUMBERS:
            pi.write(number, int(bit))
        time.sleep(clockspeed)

def add_bit_stuffing(message, n):
    # n is the length of a repeating bit sequence before adding in a stuff bit
    answer = ""
    n_buffer = " "
    for bit in message:
        if bit != n_buffer[-1]:
            n_buffer = bit
            answer += bit
        else:
            n_buffer += bit
            answer += bit
            if len(n_buffer) == n:
                answer += str(1-int(bit))
                n_buffer = str(1-int(bit))
    return answer
            
def transmit_message(message, ports):
    GPIO_TRANSMITTER_NUMBERS = [27 - 2 * (port -1) for port in ports]
    pi = pigpio.pi()
    sequence = wake + start + message + stop
    bit_stuffed_sequence = add_bit_stuffing(sequence, 6)
    send_sequence(pi, bit_stuffed_sequence, GPIO_TRANSMITTER_NUMBERS)
