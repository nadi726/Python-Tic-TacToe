from random import randint
from itertools import cycle, chain


class Board:
    def __init__(self):
        self._board = [["-"]*3 for i in range(3)]

    def place_symbol(self, symbol, tile):
        """Try to place the player inside the tile
        Returns True if successful and None otherwise
        """
        row, colmn = tile
        if self._board[row][colmn] == "-":
            self._board[row][colmn] = symbol
            return True

    def check_win(self):
        """Checks all possible winning combinations,
        Returns True for a win and False otherwise.
        """
        # Store all checks here
        checks = set()

        # Add rows
        for row in self._board:
            checks.add(tuple(row))

        # Add columns
        colmns = zip(self._board[0], self._board[1], self._board[2])
        for colmn in colmns:
            checks.add(tuple(colmn))

        # Add diagonals
        diag1 = (self._board[0][0], self._board[1][1], self._board[2][2])
        diag2 = (self._board[0][2], self._board[1][1], self._board[2][0])
        checks.update((diag1, diag2))

        # Check every option for a win
        return any(len(set(lst)) == 1 and lst[0] != "-" for lst in checks)

    def is_full(self):
        return "-" not in set(chain(*self._board))

    def __str__(self):
        return '\n'.join(' '.join(row) for row in self._board)


class Player:
    def __init__(self, is_human, symbol, name):
        self.is_human = is_human
        self.symbol = symbol
        self.name = name
        self.score = 0

def get_player_input(choices, text=''):
    while True:
        inpt = input(text)
        # Once the input is valid, break from the function and return it.
        if inpt in choices:
            return inpt
        print(f"Enter one of the following: {', '.join(choices)}")


def main():
    print("Welcome to tic tac toe!")
    print("type the appropiate number to choose a game option:")
    print("1.player vs player\n2.player vs computer\n3.computer vs computer")
    choice = get_player_input(('1', '2', '3'),)
    if choice == '1':
        player1_name = input("Choose a Name for player 1: ")
        player2_name = input("Choose a Name for player 2: ")
        player1_is_human = True
        player2_is_human = True
    elif choice == '2':
        player1_name = input("Choose a name: ")
        player2_name = "Computer"
        player1_is_human = True
        player2_is_human = False
    elif choice == '3':
        player1_name = "Computer 1"
        player2_name = "Computer 2"
        player1_is_human = False
        player2_is_human = False

    player1 = Player(player1_is_human, "X", player1_name)
    player2 = Player(player2_is_human, "O", player2_name)
    players = [player1, player2]
    board = Board()
    # For player row and colmn input
    options = ('1', '2', '3')

    for player in cycle(players):
        print(board)
        print(f"It's {player.name}'s turn")

        # The actual turn of the player
        while True:
            if player.is_human:
                row = int(get_player_input(options, "Enter row number(1-3): ")) - 1
                colmn = int(get_player_input(options, "Enter column number(1-3): ")) - 1
            else:
                row, colmn = randint(0, 2), randint(0, 2)

            result = board.place_symbol(player.symbol, (row, colmn))
            # Result is invalid
            if result is None:
                if player.is_human:
                    print("Enter in a non-full tile")
                continue
            # Result is valid
            else:
                break

        win = board.check_win()
        if win or board.is_full():
            print(board)
            if win:
                print(f"player {player.name} won")
                player.score += 1
                print(f"current scores:\nPlayer {players[0].name}: {players[0].score}")
                print(f"Player {players[1].name}: {players[1].score}")
            elif board.is_full():
                print("It's a draw!")

            again = input("Another game?(y/n)")
            if again == "y":
                # Initialize board and start a new game with the losing player
                # as the first one to go
                board = Board()
                continue
            # Finish execution
            return


if __name__ == '__main__':
    main()
