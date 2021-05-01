import sys
from Move_collection import Move_Collection
import hw4_provided as hw4
import random
from Piece import WHITE, BLACK

class Player:
    def __init__(self, color):
        self.color = color
        self.pieces_remaining = 12

    def __repr__(self):
        return "white" if self.color == WHITE else "black"

    def enumerate_all_moves(self, board):
        simple_moves = Move_Collection()
        jump_moves = Move_Collection()

        # iterate through rows
        for row in range(len(board.spaces)):

            # iterate through columns
            for col in range(len(board.spaces[row])):
                space = board.spaces[row][col]

                # if piece exists, find its legal moves
                if space.piece != None:

                    # if piece belongs to current player
                    if space.piece.color == self.color:
                        legal_simple_moves, legal_jumps = space.piece.get_legal_moves(board, (row, col))
                        simple_moves.append_collections(legal_simple_moves)
                        #  = simple_moves + legal_simple_moves
                        jump_moves.append_collections(legal_jumps)
                        #  = jump_moves + legal_jumps
        
        # return two iterators
        return simple_moves, jump_moves

    def make_a_move(self, CLI, current_game, current_board, other_player):
        # take in command line input
        coord = input("Select a piece to move\n>")

        # convert coord
        coord = hw4.convert_checker_coord(coord)

        # check errors
        if coord[0] > 7 or coord[0] < 0 or coord[1] > 7 or coord[1] < 0:
            raise OutOfBoundsError()
        if current_board.spaces[coord[0]][coord[1]].piece == None:
            raise EmptySpaceError()
        if current_board.spaces[coord[0]][coord[1]].piece.color != self.color:
            raise NotYourPieceError()

        # enumerate all moves on board
        simple_moves, jump_moves = self.enumerate_all_moves(current_board)

        # check if jump is available over simple move
        piece_has_jump_move = False
        for jumps in jump_moves:
            if coord == jumps.old_coord:
                piece_has_jump_move = True
        if not piece_has_jump_move and not jump_moves.is_empty():
            raise JumpAvailableError()

        moves = simple_moves if jump_moves.is_empty() else jump_moves

        # queue available moves
        move_options = CLI.display_options(coord, moves)

        if len(move_options) == 0:
            raise PieceIsStuckError()

        # take in the index for move
        cmd_line_move_index = input("Select a move by entering the corresponding index\n>")

        if int(cmd_line_move_index) not in range(len(move_options)):
            raise InvalidOptionIndex()

        # translate index to move object
        move_command = move_options[cmd_line_move_index]

        # execute move on selected piece
        move_command.execute(current_board, other_player, current_game)

class Random_Player(Player):
    def make_a_move(self, CLI, current_game, current_board, other_player):
        
        # enumerate all moves on board
        simple_moves, jump_moves = self.enumerate_all_moves(current_board)

        # if there is a jump move, execute it first
        if not jump_moves.is_empty():
            # move = random.choice(jump_moves)
            move = jump_moves.get_random()
            move.execute(current_board, other_player, current_game)
        elif not simple_moves.is_empty():
            # move = random.choice(simple_moves)
            move = simple_moves.get_random()
            move.execute(current_board, other_player, current_game)

class Greedy_Player(Player):
    def make_a_move(self, CLI, current_game, current_board, other_player):     
        # enumerate all moves on board
        simple_moves, jump_moves = self.enumerate_all_moves(current_board)

        # find jump that captures most pieces
        if not jump_moves.is_empty():
            move = jump_moves.get_max()
            move.execute(current_board, other_player, current_game)
        elif not simple_moves.is_empty():
            move = simple_moves.get_random()
            move.execute(current_board, other_player, current_game)

class OutOfBoundsError(Exception):
    pass

class JumpAvailableError(Exception):
    pass

class EmptySpaceError(Exception):
    pass

class NotYourPieceError(Exception):
    pass

class PieceIsStuckError(Exception):
    pass

class InvalidOptionIndex(Exception):
    pass
