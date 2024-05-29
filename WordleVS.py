# first of all import the socket library
import socket
import requests
import random
# region Check for updates
# get version
# If you need to CLOSE the port, do so with this command in your command line: 
# netstat -ano | findstr :40676
# taskkill /PID <PID> /F

version = '0.0.1'
versionURL = "https://raw.githubusercontent.com/DumbsDev/wordleUpdates/main/version.txt"
versionCheck = requests.get(versionURL)
neededVersion = ''
print(f'You are on verision {version} of Wordle Versus (CMD Edition). Checking for updates...')
for i in range(len(versionCheck.text)-1):
    neededVersion += versionCheck.text[i]
if (version == neededVersion):
    print('You are on the current version of Wordle Versus (CMD Edition)!')
else:
    print(f'You are using version {version} of Wordle Versus (CMD Edition) and the current usable version is {neededVersion}.')
    print(f'Please update to the current version of Wordle Versus (CMD Edition) at' + 'https://dumbsdev.itch.io/wordle-vs-cmd')
    # stop the program
    exit()
#endregion

# close all sockets before starting
try:
    socket.socket().shutdown(socket.SHUT_RDWR)
    socket.socket().close()
    print("Sockets closed.")
except:
    print("No sockets to close.")
#socket.socket().shutdown(socket.SHUT_RDWR)
pType = input("Would you like to host a server or join a server? (Host/Join): ").lower()

#region create a temporary save file
file1 = open('tempSave.dat', 'w')
file1.write('0')
file1.write('0')
file1.close()

def playTime(pType):
    if (pType == "host" or pType == "h"):
            #region Create the server
        # next create a socket object
        s = socket.socket()
        print ("Socket successfully created")
        
        # reserve a port on your computer in our
        # case it is 40674 but it can be anything
        port = 40676
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Next bind to the port
        # we have not typed any ip in the ip field
        # instead we have inputted an empty string
        # this makes the server listen to requests
        # coming from other computers on the network
        s.bind(('', port))
        print ("socket binded to %s" %(port))
        
        # put the socket into listening mode
        s.listen(2)    
        print("socket is listening")
        #endregion
            #region Set the word
        def SetWord():
            word = input("Enter a 5 letter word to be guessed: ")
            if ('1' in word or '2' in word or '3' in word or '4' in word or '5' in word or '6' in word or '7' in word or '8' in word or '9' in word or '0' in word):
                print("Please enter a valid word with no numbers.")
                return SetWord()
            elif (len(word) != 5):
                print("Please enter a 5 letter word.")
                return SetWord()
            elif (word.isalnum() == False):
                print("Please enter a valid word with no special characters.")
                return SetWord()
            else:
                return word.lower()
        word = SetWord()
        #endregion
            #region The game
            # a forever loop until we interrupt it or an error occurs
        while True:
            # Establish connection with client.
            c, addr = s.accept()
            print('Got connection from player from', addr)

            c.send(b'Please enter a 5 letter word: ')
            def game(guesses = 0):
                # guessRaw = ''
                guessRaw = str(c.recv(1024))
                if guessRaw == "b''":
                    guessRaw = str(c.recv(1024))
                    print(guessRaw)
                    print('GuessRaw is empty!!')
                print(guesses)
                guess = ''
                for i in range(5):
                    print("i:", i, "| i+2:", i+2)
                    print('gi:',guessRaw[i+2])
                    print('guess:', guess)
                    print('guessRaw:', guessRaw)
                    guess += guessRaw[i+2]
                    print('guess final:', guess)
                if (str(guess) == (word)):
                    c.send(b'You got it, the word was ' + bytes(word, 'utf-8') + b'!')
                    file1 = open('tempSave.dat', 'w')
                    file1.write(str(guesses+1))
                    file1.close()
                    c.close()
                    exit()
                else:
                    right_letters = ''
                    for i in range(5):
                        if (word[i] == guess[i]):
                            right_letters += word[i]
                        else:
                            right_letters += '?'
                    wrong_spots = ''
                    for i in range(5):
                        if (word[i] in guess):
                            wrong_spots += word[i]
                        else:
                            wrong_spots += ''
                    print('right_letters:', right_letters)
                    print('wrong_spots:', wrong_spots)
                    guesses += 1
                    try:
                        print("Sending 'you're wrong' message.")
                        c.send(b"You didn't get it. You are on guess #" + 
                               bytes(str(guesses), 'utf-8') + 
                               b". The letters you got right are: " + 
                               bytes(str(right_letters), 'utf-8') + 
                               b" characters you got in the string (both wrong and correct spot): " + 
                               bytes(str(''.join(random.sample(wrong_spots, len(wrong_spots)))), 'utf-8')
                               )
                        print("message sent.")
                    except:
                        # close the server
                        print("An error occured in sending the correct/incorrect letters. Closing the server.")
                        c.close()
                        exit()
                    # restart the function
                    return game(guesses)
            game()
            # break
        #endregion
    elif (pType == "join" or pType == "j"):
                #region Attempt to join the server
            # Create a socket object
            s = socket.socket()
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)

            # Define the port on which you want to connect
            port = 40676
            ip = input("Enter the IP address of the host: ")
            if (ip == "Local" or ip == "local" or ip == "localhost" or ip == "Localhost" or ip == "myip" or ip == "my ip"):
                ip = IPAddr
            try:
                s.connect((ip, port))
                print("Connected to server!")
            #error handling
            except ConnectionRefusedError:
                print(f"Could not connect to server on IP and Socket {socket}!")
                exit()
            except TimeoutError:
                print(f"Connection to server on IP and Socket {socket} timed out!")
                exit()
            #endregion
                #region Set the word
            def SetWord():
                word = input("Enter a 5 letter word to be guessed: ")
                if ('1' in word or '2' in word or '3' in word or '4' in word or '5' in word or '6' in word or '7' in word or '8' in word or '9' in word or '0' in word):
                    print("Please enter a valid word with no numbers.")
                    return SetWord()
                elif (len(word) != 5):
                    print("Please enter a 5 letter word.")
                    return SetWord()
                elif (word.isalnum() == False):
                    print("Please enter a valid word with no special characters.")
                    return SetWord()
                else:
                    return word.lower()
            word = SetWord()
            #endregion
                #region The game
            
            # receive data from the server
            entera = str(s.recv(1024))
            def guessGame():
                guess = input(entera)
                if ('1' in guess or '2' in guess or '3' in guess or '4' in guess or '5' in guess or '6' in guess or '7' in guess or '8' in guess or '9' in guess or '0' in guess):
                    print("Please enter a valid word with no numbers.")
                    return guessGame()
                elif (len(guess) != 5):
                    print("Please enter a 5 letter word.")
                    return guessGame()
                elif (guess.isalnum() == False):
                    print("Please enter a valid word with no special characters.")
                    return guessGame()
                else:
                    return guess
            
            def sendIt():
                guess = guessGame()
                s.send(bytes(guess.lower(), 'utf-8'))
                res = str(s.recv(4096))
                print('outcome:', res)
                if (res == "b'You got it, the word was " + guess.lower() + "!'"):
                    s.close() # close the connection
                else: 
                    if(res != "b'You got it!'"):
                        sendIt()
            sendIt()
            s.close()
                
            #endregion
    elif(pType == "exit" or pType == "e" or pType == "stop" or pType == "quit" or pType == "q"):
        exit()
    
    else:
        print("Please enter a valid option.")
        # restart
        return playTime(input("Would you like to host a server or join a server? (Host/Join): ").lower())
playTime(pType)