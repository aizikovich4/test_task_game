import sys
import signal
import sys

def signal_handler(signal, frame):
    print('End game!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

list_commands=["login", "buy item", "sell item", "logout","help"]


LOGIN = "LOGIN"
game_state = LOGIN


user_login = raw_input("Enter You login: ")
#send request to login


while game_state != "END_GAME":
    try:
        cmd = raw_input("Enter command: ")
        if cmd not in list_commands:
            print("Unsupported command, input help to show available command")
            continue
        if cmd == "help":
            print(list_commands)
        elif cmd == 'logout':
            print("logout")
            game_state="END_GAME"
        elif cmd == 'sell item':
            print("sell item")
        elif cmd == "buy item":
            print("buy item")        
    except KeyboardInterrupt:  
        print( "logout, end game")
        #send logout
