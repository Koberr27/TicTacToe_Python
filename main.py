import random

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.mode = None
        self.player_symbol = None

    def display_board(self): #aktualny stan planszy
        print("\n   |   |   ")
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print("   |   |   \n")

    def display_help_board(self):
        print("\nPlansza z numerami pól:")
        print("\n   |   |   ")
        print(" 1 | 2 | 3 ")
        print("___|___|___")
        print("   |   |   ")
        print(" 4 | 5 | 6 ")
        print("___|___|___")
        print("   |   |   ")
        print(" 7 | 8 | 9 ")
        print("   |   |   \n")

    def check_win(self, mark):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  #poziom
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  #pion
            [0, 4, 8], [2, 4, 6]              #ukos
        ]
        #sprawdza czy są 3 pod rząd
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] == mark:
                return True
        return False

    def check_tie(self): #jeżeli wszystkie zajęte to koniec gry
        return ' ' not in self.board

    def get_player_move(self):
        while True:
            try:
                move = int(input(f"Gracz {self.current_player}, podaj numer pola (1-9): ")) - 1
                if move >= 0 and move <= 8 and self.board[move] == ' ':
                    return move
                else:
                    print("Źle! Spróbuj ponownie.")
            except ValueError:
                print("Podaj liczbę od 1 do 9")

    def easy_bot_move(self): #łatwy wybiera losowe pole
        available_moves = [i for i, spot in enumerate(self.board) if spot == ' ']
        return random.choice(available_moves)

    def hard_bot_move(self): #trudny sprawdza dokładniej jak wygrać
        player_symbol = 'X' if self.player_symbol == 'O' else 'O'
        
        #sprawdza czy nie brakuje 1 ruchu do wygranej
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.player_symbol
                if self.check_win(self.player_symbol):
                    self.board[i] = ' '  #cofa test
                    return i
                self.board[i] = ' '
        
        for i in range(9): #sprawdza jak zablokować przeciwnika
            if self.board[i] == ' ':
                self.board[i] = player_symbol
                if self.check_win(player_symbol):
                    self.board[i] = ' '
                    return i
                self.board[i] = ' '
        
        #celuje w środek jeżeli jest pusty
        if self.board[4] == ' ':
            return 4
        
        #jeżeli jest zajęty to krańce
        corners = [0, 2, 6, 8]
        random.shuffle(corners)
        for corner in corners:
            if self.board[corner] == ' ':
                return corner
        
        #jak nie to losowe pole
        available_moves = [i for i, spot in enumerate(self.board) if spot == ' ']
        return random.choice(available_moves)

    def choose_mode(self):
        print("Wybierz tryb gry:")
        print("1 - Gracz vs Gracz")
        print("2 - Gracz vs Bot [łatwy]")
        print("3 - Gracz vs Bot [trudny]")
        
        while True:
            try:
                choice = int(input("Twój wybór (1-3): "))
                if choice in [1, 2, 3]:
                    return choice
                else:
                    print("Proszę wybrać 1, 2 lub 3!")
            except ValueError:
                print("Proszę podać liczbę!")

    def choose_symbol(self): #wybór
        while True:
            symbol = input("Wybierz symbol (X lub O): ").upper()
            if symbol in ['X', 'O']:
                return symbol
            print("Nieprawidłowy symbol! Wybierz X lub O.")

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            return True
        return False

    def switch_player(self): #zmienia gracza
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def reset_game(self):
        self.board = [' '] * 9
        self.current_player = 'X'

    def play_game(self):
        print("------------> Witaj użytkowniku... <------------")
        
        self.mode = self.choose_mode()
        self.player_symbol = self.choose_symbol()
        
        print("\n------------> Gra start <------------")
        
        while True:
            self.display_help_board()
            self.display_board()
            
            if self.mode == 1:
                move = self.get_player_move()
            else:
                if self.current_player == self.player_symbol:
                    move = self.get_player_move()
                else:
                    if self.mode == 2:
                        move = self.easy_bot_move()
                    else:
                        move = self.hard_bot_move()
                    print(f"Bot wybiera pole {move + 1}")
            
            self.make_move(move)
            
            if self.check_win(self.current_player): #sprawdza czy kto wygrał
                self.display_board()
                if self.mode == 1:
                    print(f"Gracz {self.current_player} wygrywa!")
                else:
                    if self.current_player == self.player_symbol:
                        print("------------> Wygrałeś! <------------")
                    else:
                        print("------------> Przegrałeś! <------------")
                break
            
            if self.check_tie():
                self.display_board()
                print("------------> Remis <------------")
                break
            
            self.switch_player()
        
        play_again = input("\nJeszcze raz? [T/N]: ").upper()
        if play_again == 'T':
            self.reset_game()
            self.play_game()
        else:
            print("Dzięki za grę")

if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()
