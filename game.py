import hashlib
import hmac
import secrets
from tabulate import tabulate 
import random

class KeyGenerator:
    def generate_key():
        return secrets.token_hex(32) 

class HMACGenerator:
    def generate_hmac(key, message):
        return hmac.new(key.encode(), message.encode(), hashlib.sha3_256).hexdigest()

class Rules:
    def __init__(self, moves):
        self.moves = moves
        self.num_moves = len(moves)

    def determine_winner(self, user_move, computer_move):
        user_index = self.moves.index(user_move)
        comp_index = self.moves.index(computer_move)

        half = self.num_moves // 2
        if user_index == comp_index:
            return "Draw"
        elif (comp_index - user_index) % self.num_moves <= half:
            return "You lose!"
        else:
            return "You win!"

    def generate_help_table(self):
        headers = ["v PC\\User >"] + self.moves
        table = []

        for i, move in enumerate(self.moves):
            row = [move]
            for j in range(self.num_moves):
                if i == j:
                    row.append("Draw")
                elif (j - i) % self.num_moves <= self.num_moves // 2:
                    row.append("Win")
                else:
                    row.append("Lose")
            table.append(row)

        return tabulate(table, headers, tablefmt="grid")

class Game:
    def __init__(self, num_moves):
        self.moves = ["rock", "paper", "scissors"] + [f"{i+4}th move" for i in range(num_moves - 3)]
        self.rules = Rules(self.moves)
        self.key = KeyGenerator.generate_key()
        self.computer_move = random.choice(self.moves)
        self.hmac = HMACGenerator.generate_hmac(self.key, self.computer_move)

    def play(self):
        print(f"HMAC: {self.hmac}")
        while True:
            print("\nAvailable moves:")
            for i, move in enumerate(self.moves, 1):
                print(f"{i} - {move}")
            print("0 - exit")
            print("? - help")

            choice = input("Enter your move: ")
            if choice == "0":
                print("Exiting game. Goodbye!")
                break
            elif choice == "?":
                print(self.rules.generate_help_table())
            else:
                try:
                    user_choice = int(choice)
                    if 1 <= user_choice <= len(self.moves):
                        user_move = self.moves[user_choice - 1]
                        result = self.rules.determine_winner(user_move, self.computer_move)
                        print(f"Your move: {user_move}")
                        print(f"Computer move: {self.computer_move}")
                        print(result)
                        print(f"HMAC key: {self.key}")
                        break
                    else:
                        print("Invalid choice. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

def main():
    try:

      while (True):
        num_moves = int(input("Enter an odd number of moves (>= 3): "))
        if num_moves < 3 or num_moves % 2 == 0:
            print("Error: Please enter an odd number greater than or equal to 3.")
        else:
            game = Game(num_moves)
            game.play()
            break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()
