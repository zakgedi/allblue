from hashlib import new
import sys
import hw4_provided as hw4
from Move import Jump_Move, Simple_Move
from Move_collection import Move_Collection
WHITE, BLACK = 1, 2

class Piece:
    def __init__(self, color):
        self.color = color
        self.direction = -1 if self.color == WHITE else 1

    def is_move_valid(self, board, row, col):

        # if new coord is out of range
        if row > 7 or row < 0 or col > 7 or col < 0:
            return False

        # if new coord in not empty
        elif board.spaces[row][col].piece != None:
            return False

        return True

    def is_jump_valid(self, board, row, col, row_adjustment, col_adjustment, captured_path=[], backwards=False):

        # if neighbor is in range
        if row > 7 or row < 0 or col > 7 or col < 0:
            return False 
        
        # if neighbor exists
        elif board.spaces[row][col].piece == None:
            return False
        
        # if neighbor is opponent
        elif self.color == board.spaces[row][col].piece.color:
            return False

        # if neighbor has already been captured, don't jump
        if captured_path:
            for old_coord in captured_path:
                if row == old_coord[0] and col == old_coord[1]:
                    return False

        next_row = row - row_adjustment if backwards else row + row_adjustment
        next_col = col + col_adjustment

        # if new coord is out of range
        if next_row > 7 or next_row < 0 or next_col > 7 or next_col < 0:
            return False 

        # new coord is empty
        elif board.spaces[next_row][next_col].piece != None:
            return False

        return True

    def move_piece(self, board, old_coord, new_coord):
        spaces = board.spaces
        
        # old coordinates
        old_row = old_coord[0]
        old_col = old_coord[1]

        # new coordinates
        new_row = new_coord[0]
        new_col = new_coord[1]

        # if new row is king row, turn peasont into king
        if self.color == WHITE and new_row == 0:
            spaces[old_row][old_col].piece = King(self.color)
        elif self.color == BLACK and new_row == 7:
            spaces[old_row][old_col].piece = King(self.color)

        # swap empty space and piece positions
        spaces[new_row][new_col].piece = spaces[old_row][old_col].piece
        spaces[old_row][old_col].piece = None

    def recursive_helper(self, board, next_row, next_col, row_adjustment, col_adjustment, final_destinations, captured, captured_path, backwards=False):

        # change coord
        new_coord = (next_row - row_adjustment, next_col + col_adjustment) if backwards else (next_row + row_adjustment, next_col + col_adjustment) 
        captured_coord = (next_row, next_col)

        # add to captured
        captured_path.append(captured_coord)

        # recurse on right
        final_destinations, captured_path = self.get_jump_moves(board, new_coord, final_destinations, captured, captured_path)
        
        # pop last piece off
        captured_path = captured_path[:-1]

        return final_destinations, captured_path
    
class Peasant(Piece):
    def __repr__(self):
        return str(u'⚆') if self.color == WHITE else str(u'⚈')

    def get_legal_moves(self, board, old_coord):

        row = old_coord[0]
        col = old_coord[1]

        simple_moves = Move_Collection()
        
        # left move forward
        if self.is_move_valid(board, row + self.direction, col - 1):
            new_coord = (row + self.direction, col - 1)
            new_move = Simple_Move(self, old_coord, new_coord)
            simple_moves.add_move(new_move)

        # right move forward
        if self.is_move_valid(board, row + self.direction, col + 1):
            new_coord = (row + self.direction, col + 1)
            new_move = Simple_Move(self, old_coord, new_coord)
            simple_moves.add_move(new_move)
        

        jump_moves = Move_Collection()

        final_destinations = []
        captured = []
        captured_path = []

        # find list of destinations and captured pieces
        self.get_jump_moves(board, old_coord, final_destinations, captured, captured_path)

        # look though destinations and captured
        for i in range(len(final_destinations)):
            if old_coord != final_destinations[i]:
                # create jump command objects
                new_jump_move = Jump_Move(self, old_coord, final_destinations[i], captured[i])
                jump_moves.add_move(new_jump_move)

        # return two iterators
        return simple_moves, jump_moves

    def get_jump_moves(self, board, old_coord, final_destinations, captured, captured_path=[]):

        row_adjustment = self.direction
        next_row = old_coord[0] + row_adjustment
        right_col = old_coord[1] + 1

        # king row reached stop jumping
        if self.color == WHITE and old_coord[0] == 0 or self.color == BLACK and old_coord[0] == 7:
            final_destinations.append(old_coord) 
            if len(captured_path) != 0:
                captured.append(captured_path)
            return final_destinations, captured_path

        # check if left forward is valid jump
        col_adjustment = -1
        left_col = old_coord[1] + col_adjustment
        if self.is_jump_valid(board, next_row, left_col, row_adjustment, col_adjustment):
            final_destinations, captured_path = self.recursive_helper(board, next_row, left_col, row_adjustment, col_adjustment, final_destinations, captured, captured_path)

        # check if right forward is valid jump
        col_adjustment = 1
        right_col = old_coord[1] + col_adjustment
        if self.is_jump_valid(board, next_row, right_col, row_adjustment, col_adjustment):
            final_destinations, captured_path = self.recursive_helper(board, next_row, right_col, row_adjustment, col_adjustment, final_destinations, captured, captured_path)

        # return last coords and captured
        if not self.is_jump_valid(board, next_row, left_col, row_adjustment, -1) and not self.is_jump_valid(board, next_row, right_col, row_adjustment, 1):
            final_destinations.append(old_coord)
                
            if len(captured_path) != 0:
                captured.append(captured_path)

            return final_destinations, captured_path
        
        return final_destinations, captured_path


class King(Piece):
    def __repr__(self):
        return str(u'⚇') if self.color == WHITE else str(u'⚉')

    def get_legal_moves(self, board, old_coord):

        row = old_coord[0]
        col = old_coord[1]
        
        simple_moves = Move_Collection()

        # left move forward
        if self.is_move_valid(board, row + self.direction, col - 1):
            new_coord = (row + self.direction, col - 1)
            new_move = Simple_Move(self, old_coord, new_coord)
            simple_moves.add_move(new_move)

        # right move forward
        if self.is_move_valid(board, row + self.direction, col + 1):
            new_coord = (row + self.direction, col + 1)
            new_move = Simple_Move(self, old_coord, new_coord)
            simple_moves.add_move(new_move)

        # left move backward
        if self.is_move_valid(board, row - self.direction, col - 1):
            new_coord = (row - self.direction, col - 1)
            new_move = Simple_Move(self, old_coord, new_coord)
            simple_moves.add_move(new_move)

        # right move backward
        if self.is_move_valid(board, row - self.direction, col + 1):
            new_coord = (row - self.direction, col + 1)
            new_move = Simple_Move(self, old_coord, new_coord)
            simple_moves.add_move(new_move)
        
        jump_moves = Move_Collection()
        final_destinations = []
        captured = []
        captured_path = []

        # find list of destinations and captured pieces
        # print("Here: ", hw4.convert_matrix_coord(old_coord))
        self.get_jump_moves(board, old_coord, final_destinations, captured, captured_path)

        # look though destinations and captured
        for i in range(len(final_destinations)):
            if old_coord != final_destinations[i]:
                # create jump command objects
                new_jump_move = Jump_Move(self, old_coord, final_destinations[i], captured[i])
                jump_moves.add_move(new_jump_move)

        # return two iterators
        return simple_moves, jump_moves

    def get_jump_moves(self, board, old_coord, final_destinations, captured, captured_path=[]):

        row_adjustment = self.direction
        forward_row = old_coord[0] + row_adjustment
        backward_row = old_coord[0] - row_adjustment

        # check if left forward is valid jump
        col_adjustment = -1
        left_col = old_coord[1] + col_adjustment
        left_forward_valid = self.is_jump_valid(board, forward_row, left_col, row_adjustment, col_adjustment, captured_path)
        if left_forward_valid:
            # print("Up Left: ", hw4.convert_matrix_coord((forward_row, left_col)), captured_path)
            final_destinations, captured_path = self.recursive_helper(board, forward_row, left_col, row_adjustment, col_adjustment, final_destinations, captured, captured_path)

        # check if right forward is valid jump
        col_adjustment = 1
        right_col = old_coord[1] + col_adjustment
        right_forward_valid = self.is_jump_valid(board, forward_row, right_col, row_adjustment, col_adjustment, captured_path)
        if right_forward_valid:
            # print("Up Right: ", hw4.convert_matrix_coord((forward_row, right_col)), captured_path)
            final_destinations, captured_path = self.recursive_helper(board, forward_row, right_col, row_adjustment, col_adjustment, final_destinations, captured, captured_path)

        # check if left backwards is valid jump
        col_adjustment = -1
        left_col = old_coord[1] + col_adjustment
        left_backward_valid = self.is_jump_valid(board, backward_row, left_col, row_adjustment, col_adjustment, captured_path, backwards=True)
        if left_backward_valid:
            # print("Down Left: ", hw4.convert_matrix_coord((backward_row, left_col)), captured_path)
            final_destinations, captured_path = self.recursive_helper(board, backward_row, left_col, row_adjustment, col_adjustment, final_destinations, captured, captured_path, backwards=True)

        # check if right backwards is valid jump
        col_adjustment = 1
        right_col = old_coord[1] + col_adjustment
        right_backward_valid = self.is_jump_valid(board, backward_row, right_col, row_adjustment, col_adjustment, captured_path, backwards=True)
        if right_backward_valid:
            # print("Down Right: ", hw4.convert_matrix_coord((backward_row, right_col)), captured_path)
            final_destinations, captured_path = self.recursive_helper(board, backward_row, right_col, row_adjustment, col_adjustment, final_destinations, captured, captured_path, backwards=True)

        # Base Case - return last coords and captured
        if not left_forward_valid and not right_forward_valid and not left_backward_valid and not right_backward_valid:
            final_destinations.append(old_coord)  
            if len(captured_path) != 0:
                captured.append(captured_path)
            return final_destinations, captured_path
        
        return final_destinations, captured_path
