import hw4_provided as hw4

class Move:
    def __init__(self, piece, old_coord, new_coord):
        self.piece = piece
        self.old_coord = old_coord
        self.new_coord = new_coord
        
class Simple_Move(Move):

    def __repr__(self):
        old_coord = hw4.convert_matrix_coord(self.old_coord)
        new_coord = hw4.convert_matrix_coord(self.new_coord)
        return str("simple move" + ": " + str(old_coord) + "->" + str(new_coord))

    def execute(self, board, other_player, current_game):
        self.piece.move_piece(board, self.old_coord, self.new_coord)

class Jump_Move(Move):
    def __init__(self, piece, old_coord, new_coord, pieces_captured):
        self.piece = piece
        self.old_coord = old_coord
        self.new_coord = new_coord
        self.pieces_captured = pieces_captured

    def __repr__(self):
        old_coord = hw4.convert_matrix_coord(self.old_coord)
        new_coord = hw4.convert_matrix_coord(self.new_coord)

        # convert matrix coords to lettered coords
        captured_coord = []
        for captured in self.pieces_captured:
            str_coord = hw4.convert_matrix_coord(captured)
            captured_coord.append(str_coord)

        captured_coord = ", ".join(captured_coord)
        return str("jump move" + ": " + str(old_coord) + "->" + str(new_coord) + ", capturing [" + str(captured_coord) + "]")

    def execute(self, board, other_player, current_game):
        self.piece.move_piece(board, self.old_coord, self.new_coord)
        # remove any captured pieces
        if self.pieces_captured:
            board.remove_pieces(self.pieces_captured, other_player, current_game)