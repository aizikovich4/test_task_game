import sys
import signal
import sys
import requests

def exception_handler(exception_type, exception, traceback):
    #print "%s: %s" % (exception_type.__name__, exception)
    exit()
#BORIS UNCOMMENT IN RELEASE
#sys.tracebacklimit = 0
#sys.excepthook = exception_handler /

list_commands=["exit", "buy", "sell", "logout", "help"]
class Game(object):    
    def __init__(self):
        self.game_state = "LOGIN"
        self.is_logged = False
    def login_user(self, login):
        answer = requests.get("http://127.0.0.1:5000/login", headers={'username':login})
        print(answer.json())
        data = answer.json()
        self.game_state = "START"
        self.is_logged = True
        self.user_items=[]
        self.credit = data['credit']
        self.login = data['username']
        if not self.login:
            return False
        print("Hello "+self.login+". You have a " + str(self.credit)+" credit.")
        return True

    def start(self):
        if not self.is_logged:
            return
        while self.game_state != "END_GAME":
            try:
                cmd = raw_input("Enter command: ")
                if cmd not in list_commands:
                    print("Unsupported command, input help to show available command")
                    continue
                if cmd == "help":
                    print(list_commands)
                elif cmd == 'logout' or cmd == 'exit':
                    print(cmd)
                    self.end_game()
                elif cmd == 'sell':
                    self.sell_item()
                elif cmd == "buy":
                    self.buy_item()        
            except KeyboardInterrupt:  
                self.end_game()
                
    def end_game(self):
        print("Goodbye "+self.login)
        self.logout()
        self.game_state = "END_GAME"

    def buy_item(self):
        items=[]
        print("Items:", items)
        item = raw_input("Enter number of item which you want to buy: ")        
        try:
            buy_item = int(item)
            #TODO add checking for including item in server items
            print("Try to buy item", item)
        except ValueError:
            print("Wrong item number! ")

        answer = requests.get("http://127.0.0.1:5000/buy",
                              params={'item': buy_item},
                              headers={'username': self.login})
    
    def sell_item(self):
        print("Your items:" + str(self.user_items))
        item_number = raw_input("Enter number of item which you want to sell: ")
        try:
            item = int(item_number)
        except ValueError:
            print("Wrong item number!")
            return
        print("Try to sell item", item)
        answer = requests.get("http://127.0.0.1:5000/sell",
                                  params={'item': item},
                                  headers={'username': self.login})

        print(answer)



    def logout(self):
        answer = requests.get("http://127.0.0.1:5000/logout", headers={'username': login})
        pass

def main():
    game = Game()
    login = raw_input("Enter You login: ")
    if game.login_user(login):
        game.start()
    else:
        print("You account was not found")
    
if __name__ == '__main__':
    main()
 
