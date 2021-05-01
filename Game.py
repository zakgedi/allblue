from Move_collection import Move_Collection
from Board import Board
from Piece import WHITE, BLACK
import copy

class Game:
    def __init__(self, board, player, other_player, number_of_turns=1, game_counter=0):
        self.current_player = player
        self.other_player = other_player
        self.current_board = board
        self.number_of_turns = number_of_turns
        self.game_counter = game_counter

    def print_turn(self):
        print("Turn: " + str(self.number_of_turns) + ", " + str(self.current_player))

    def is_game_over(self, board):

        all_moves = Move_Collection()

        simple_moves, jump_moves = self.current_player.enumerate_all_moves(board)
        all_moves.append_collections(simple_moves, jump_moves)
        #  = simple_moves + jump_moves

        if self.current_player.pieces_remaining == 0:
            print(str(self.other_player) + " has won")
            return True
        elif len(all_moves.moves) == 0:
            print("draw: no more moves")
            return True
        elif self.game_counter >= 50:
            print("draw: nothing happened for 50 cycles")
            return True
        else:
            return False
        
class GameHistory:
    def __init__(self, game, undo_stack=[], redo_stack=[]):
        self.current_game = game
        self.undo_stack = undo_stack
        self.redo_stack = redo_stack

    def undo(self, current_game):

        if len(self.undo_stack) == 0:
            return current_game

        # push current game onto redo stack
        self.redo_stack.append(current_game)

        # get last game off stack
        last_game_state = self.undo_stack [-1]

        # shorten from undo stack
        self.undo_stack = self.undo_stack [:-1]

        # return game state
        return last_game_state

    def redo(self, current_game):

        if len(self.redo_stack) == 0:
            return current_game

        # push current game onto undo stack
        self.undo_stack.append(current_game)
        
        # retrieve most recent element
        last_game_state = self.redo_stack[-1]

        # remove from stack
        self.redo_stack = self.redo_stack[:-1]

        # return game state
        return last_game_state

    def save(self, game):
        # make copy of game
        memento = GameMemento(game)

        # push onto undo stack
        self.undo_stack.append(memento.game)

class GameMemento:
    def __init__(self, game):
        self.game = copy.deepcopy(game)
