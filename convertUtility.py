def messageToBytes(message):
    encodedString = ''.join(format(ord(i), '08b') for i in message)
    return encodedString

def bytesToMessage(byte):

    return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(byte)]*8))

