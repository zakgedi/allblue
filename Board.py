import sys
from Piece import Piece, Peasant, King, WHITE, BLACK

class Board:
    def __init__(self):
        self.spaces = self.set_board()

    def set_board(self):
        # 2D array of spaces that represents a board
        spaces = []

        for row in range(8):
            row_array = []
            for col in range(8):
                if (row + col) % 2 == 0:
                    # black piece on white space
                    if row < 3:
                        new_piece = Peasant(BLACK)
                        new_space = Board_Space(WHITE, new_piece)
                    
                    # white piece on white space
                    elif row > 4:
                        new_piece = Peasant(WHITE)
                        new_space = Board_Space(WHITE, new_piece)
                    
                    # empty white space
                    else:
                        new_space = Board_Space(WHITE)
                
                else:
                    # empty black space
                    new_space = Board_Space(BLACK)

                row_array.append(new_space)

            spaces.append(row_array)

        return spaces

    def print_board(self):
        # iterate through rows
        for row in range(len(self.spaces)):
            print(row + 1, end=" ")
            
            # iterate through columns
            for col in range(len(self.spaces[row])):
                space = self.spaces[row][col]
                space.print_space()
            print()
        
        print("  a b c d e f g h")

    def remove_pieces(self, captured, other_player, current_game):
        for coord in captured:
            row = coord[0]
            col = coord[1]

            # ensure we only remove actual pieces
            assert self.spaces[row][col].piece != None
            self.spaces[row][col].piece = None
            
            # decrease num of pieces for opponent
            other_player.pieces_remaining-=1
            current_game.game_counter = 0

class Board_Space():
        def __init__(self, color, piece=None):
            self.color = color
            self.piece = piece

        def __repr__(self):
            if self.color == WHITE:
                unicode = str(u'◻')
            if self.color == BLACK:
                unicode = str(u'◼')
            return unicode

        def print_space(self):
            if self.piece == None:
                print(self, end=" ")
            else:
                print(self.piece, end=" ")