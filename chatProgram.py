from driver import receiveAllPorts, broadcastAllPorts

username = input("Choose a username: ")
print("You may now type in chat!")
receiveAllPorts()

while True:
    message = input("")
    broadcastAllPorts(message, username)


