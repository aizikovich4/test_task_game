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

list_commands=["exit", "buy", "sell", "logout","help"]
class Game(object):    
    def __init__(self):
        self.game_state = "LOGIN"
        self.is_logged = False
    def login_user(self,login):
       
        answer = requests.post("http://127.0.0.1:5000/login", data = {'username': 'user_login'})
        print(answer.json())
        #BORIS add handle json 
        self.is_logged = True
        self.game_state = "START"
        self.user_items=[]
        self.money = 500 #BORIS 
        self.login = login

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
        print("Goodbye ",self.login)
        self.logout()
        self.game_state="END_GAME"

    def buy_item(self):
        #BORIS request items from server
        items=[]
        print("Items:", items)
        item = raw_input("Enter number of item which you want to buy: ")        
        try:
            item = int(item)
            print("Try to buy item", item)
            #BORIS  send request            
        except ValueError:
            print("Wrong item number! Please repeat")  
    
    def sell_item(self):
        print("Your items:", self.user_items)
        item = raw_input("Enter number of item which you want to sell: ")        
        try:
            item = int(item)
            print("Try to sell item", item)
            #BORIS  send request            
        except ValueError:
            print("Wrong item number! Please repeat")    

    def logout(self):
        #BORIS send logout
        pass

def main():
    game = Game()
    user_login = raw_input("Enter You login: ")
    game.login_user(user_login)
    game.start()
    
if __name__ == '__main__':
    main()
 
