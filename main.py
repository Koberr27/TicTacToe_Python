import random

def display_board(board):
    print("\n   |   |   ")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("___|___|___")
    print("   |   |   ")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("___|___|___")
    print("   |   |   ")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("   |   |   \n")

def display_help_board():
    print("\nPlansza dla podglądu:")
    print("\n   |   |   ")
    print(" 1 | 2 | 3 ")
    print("___|___|___")
    print("   |   |   ")
    print(" 4 | 5 | 6 ")
    print("___|___|___")
    print("   |   |   ")
    print(" 7 | 8 | 9 ")
    print("   |   |   \n")

def check_win(board, mark): #sprawdza czy któryś z symboli wygrał
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  #poziom
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  #pion
        [0, 4, 8], [2, 4, 6]              #skos
    ]
    for condition in win_conditions: #jeżeli 3 kolejne w poziomie, pionie albo po skosie są tym samym symbolem = wygrana
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == mark:
            return True
    return False

def check_tie(board): #gdy brakuje pól do gry wypluwa remis
    return ' ' not in board

def get_player_move(board, player_symbol): #wybieranie pola
    while True:
        try:
            move = int(input(f"Gracz {player_symbol}, podaj numer pola [1-9]: ")) - 1
            if 0 <= move <= 8 and board[move] == ' ':
                return move
            else:
                print("Błąd. Spróbuj ponownie.")
        except ValueError:
            print("Wybierz liczbę od 1 do 9")

def easy_bot_move(board): #łatwy bot oparty na wybieraniu losowych wolnych miejsc z planszy
    available_moves = [i for i, spot in enumerate(board) if spot == ' ']
    return random.choice(available_moves)

def hard_bot_move(board, bot_symbol): #trudniejszy bot analizujący możliwe ruchy
    player_symbol = 'X' if bot_symbol == 'O' else 'O'
    
    #sprawdza możliwość wygrania
    for i in range(9):
        if board[i] == ' ':
            board[i] = bot_symbol
            if check_win(board, bot_symbol):
                board[i] = ' '
                return i
            board[i] = ' '
    
    #sprawdza możliwość wygranej gracza i uniemożliwia
    for i in range(9):
        if board[i] == ' ':
            board[i] = player_symbol
            if check_win(board, player_symbol):
                board[i] = ' '
                return i
            board[i] = ' '
    
    #jeżeli są wolne bot celuje w rogi lub centrum
    if board[4] == ' ':
        return 4
    
    corners = [0, 2, 6, 8]
    random.shuffle(corners)
    for corner in corners:
        if board[corner] == ' ':
            return corner
    
    #losowe wolne miejsce
    available_moves = [i for i, spot in enumerate(board) if spot == ' ']
    return random.choice(available_moves)

def choose_mode(): #wybieranie trybu
    print("Wybierz tryb gry:")
    print("1 - Gracz vs Gracz")
    print("2 - Gracz vs Bot [łatwy]")
    print("3 - Gracz vs Bot [trudny]")
    while True:
        try:
            choice = int(input("Twój wybór [1-3]: "))
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Wybierz 1, 2 lub 3")
        except ValueError:
            print("Błąd. Można podawać tylko liczby.")

def choose_symbol(): #wybieranie symbolyu
    while True:
        symbol = input("Wybierz symbol [X/O]: ").upper()
        if symbol in ['X', 'O']:
            return symbol
        print("Błąd. Nieprawidłowy symbol. Wybierz X lub O.")

def play_game(): #funkcja główna
    print("Witaj użytkowniku!")
    
    #wybierz tryb
    mode = choose_mode()
    #symbol
    player_symbol = choose_symbol()
    bot_symbol = 'O' if player_symbol == 'X' else 'X'
    
    #plansza
    board = [' '] * 9
    current_player = 'X' #zaczynają x'sy
    
    print("\nZaczynamy")
    
    while True:
        display_help_board()
        display_board(board)
        
        #ruch gracza
        if current_player == player_symbol:
            move = get_player_move(board, current_player)
        #ruch przeciwnika
        else:
            if mode == 2:
                move = easy_bot_move(board)
            else:
                move = hard_bot_move(board, bot_symbol)
            print(f"Przeciwnik wybrał pole {move + 1}")
            
        board[move] = current_player
        
        #jaki wynik?
        if check_win(board, current_player):
            display_board(board)
            if current_player == player_symbol:
                print("Wygrałeś!")
            else:
                print("Ha ha, przegrałeś!")
            break
        
        if check_tie(board):
            display_board(board)
            print("Remis")
            break
        
        #zmiana gracza po ruchu
        current_player = 'O' if current_player == 'X' else 'X'
    
    #gramy ponownie?
    play_again = input("\nChcesz grać ponownie? (T/N): ").upper()
    if play_again == 'T':
        play_game()
    else:
        print("Dzięki za grę!")
#uruchom gre
if __name__ == "__main__":
    play_game()