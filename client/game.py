import requests

list_commands=["exit", "buy", "sell", "logout", "server items", "help", "my items"]
class Game(object):    
    def __init__(self):
        self.game_state = "LOGIN"
        self.is_logged = False
        self.server_items = {}
    def login_user(self, login):
        answer = requests.get("http://127.0.0.1:5000/login", headers={'username':login})
        data = answer.json()
        if 'error' in data:
            print(data['error'])
            return False
        self.game_state = "START"
        self.is_logged = True
        self.credit = data['credit']
        self.login = data['username']
        self.user_items = data['items']
        if not self.login:
            return False
        print("Hello "+self.login)
        print("You items: ")
        self.show_my_items()
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
                    self.end_game()
                elif cmd == 'sell':
                    self.sell_item()
                elif cmd == "buy":
                    self.buy_item()
                elif cmd == "server items":
                    self.show_server_items()
                elif cmd == "my items":
                    self.show_my_items()
            except KeyboardInterrupt:  
                self.end_game()
                
    def end_game(self):
        print("Goodbye "+self.login)
        self.logout()
        self.game_state = "END_GAME"

    def buy_item(self):
        self.show_server_items()
        item = raw_input("Enter number of item which you want to buy: ")
        try:
            buy_item = int(item)
            if buy_item >= len(self.server_items):
                print("Error number!")
                return
        except ValueError:
            print("Wrong item number! ")

        print("Try to buy: " + str(self.server_items[buy_item][0][1]))
        answer = requests.get("http://127.0.0.1:5000/buy",
                              params={'item': self.server_items[buy_item][0][1]},
                              headers={'username': self.login})
        data = answer.json()
        if 'error' in data:
            print(str(data['error']))
        else:
            print ("Congratulation! You buy " + str(self.server_items[buy_item][0][1]))
            self.credit = data['credit']
            self.user_items = data['items']
    
    def sell_item(self):
        self.show_my_items()
        item_number = raw_input("Enter number of item which you want to sell: ")
        try:
            sell_item = int(item_number)
            if sell_item > len(self.user_items):
                print("Error number!")
                return
        except ValueError:
            print("Wrong item number!")
            return
        item_sell = self.user_items[sell_item][0]
        print("Try to sell: " + str(item_sell))
        answer = requests.get("http://127.0.0.1:5000/sell",
                                  params={'item': item_sell},
                                  headers={'username': self.login})
        data = answer.json()
        if 'error' in data:
            print(str(data['error']))
        else:
            print ("Congratulation! You sell " + str(item_sell))
        self.credit = data['credit']
        self.user_items = data['items']


    def logout(self):
        answer = requests.get("http://127.0.0.1:5000/logout", headers={'username': self.login})
        pass
    def show_server_items(self):
        answer = requests.get("http://127.0.0.1:5000/get_items",
                              headers={'username': self.login})
        data = answer.json()['items']
        self.server_items = data
        print ("Name      price")
        index=0
        for item in data:
            print(str(index)+". "+str(item[0][1]) + "    "+ str(item[1][1]))
            index+=1

    def show_my_items(self):
        index = 0
        print ("    Name      price")
        for item in self.user_items:
            print(" "+str(index)+". "+str(item[0]) + "   "+str(item[1]))
            index+=1
        print ("You have a " + str(self.credit)+" credit.")

def main():
    game = Game()
    login = raw_input("Enter You login: ")
    if game.login_user(login):
        game.start()

if __name__ == '__main__':
    while 1:
        main()

