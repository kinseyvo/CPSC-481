from games import *


class GameOfNim(Game):
    """Play Game of Nim with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a list with number of objects in each row."""

    def __init__(self, board):
        # gives us access to board's methods
        self.board = board
        moves = []
        for i in range(len(board)):
            for j in range(1, board[i] + 1):
                moves.append((i, j))
        self.initial = GameState(to_move='MAX', utility=0, board=board, moves=moves)

    def result(self, state, move):
        """ Have a method result(state, move) that returns the new state reached from the given state and the given move.
        Assume the move is a valid move. Note that the state for a multiplayer game also includes the player whose turn it is to play"""

        # (1,2) means remove 2 objects from row with index 1
        # board=[7, 5, 3, 1], valid move: (0,1)
        row, remove_object = move
        new_board = state.board.copy()
        new_board[row] -= remove_object
        # now the new state should be [6, 5, 3, 1]

        if state.to_move == 'MAX':
            new_player = 'MIN'
        else:
            new_player = 'MAX'

        moves = []
        for i in range(len(new_board)):
            for j in range(1, new_board[i] + 1):
                moves.append((i, j))

        # return new_board
        return GameState(to_move=new_player, utility=self.new_utility(new_board, new_player), board=new_board, moves=moves)

    def actions(self, state):
        """Legal moves are at least one object, all from the same row."""
        return state.moves

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'MAX' else -state.utility

    def new_utility(self, board, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        if all(s == 0 for s in board):
            player_name = "MAX"
            if player == player_name:
                return 1
            else:
                return -1
        else:
            return 0

    def terminal_test(self, state):
        """A state is terminal if there are no objects left"""
        """Return True if this is a final state for the game."""
        return all(s == 0 for s in state.board)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        board = state.board
        print("board: ", board)

if __name__ == "__main__":
    nim = GameOfNim(board=[0, 5, 3, 1]) # Creating the game instance
    #nim = GameOfNim(board=[7, 5, 3, 1]) # a much larger tree to search
    print(nim.initial.board) # must be [0, 5, 3, 1]
    print(nim.initial.moves) # must be [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2,1), (2, 2), (2, 3), (3, 1)]
    print(nim.result(nim.initial, (1,3) ))
    utility = nim.play_game(alpha_beta_player, query_player) # computer moves first
    if (utility < 0):
        print("MIN won the game")
    else:
        print("MAX won the game")