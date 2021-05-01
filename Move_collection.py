import random

with open('seed.txt', 'r') as f:
    seed = f.read()
    random.seed(int(seed))

class Move_Collection:
    def __init__(self):
        self.moves = []

    def __iter__(self):
        """
        The __iter__() method returns the iterator object itself, by default we
        return the iterator in ascending order.
        """

        return Move_Iterator(self.moves)

    def add_move(self, move):
        self.moves.append(move)

    def append_collections(self, other_collection, another_collection=[]):
        self.moves = self.moves + other_collection.moves
        if another_collection:
            self.moves = self.moves + another_collection.moves

    def get_max(self):
    
        max_jumps = []
        if self.moves:
            max_cap = 0
            for jump in self.moves:
                if len(jump.pieces_captured) > max_cap:
                    max_jumps = []
                    max_jumps.append(jump)
                    max_cap = len(jump.pieces_captured)
                elif len(jump.pieces_captured) == max_cap:
                    max_jumps.append(jump)

            move = random.choice(max_jumps)

            # assert greedy jump was picked
            for jump in self.moves:
                assert len(move.pieces_captured) >= len(jump.pieces_captured)

        return move

    def get_random(self):
        move = random.choice(self.moves)
        return move

    def is_empty(self):
        return self.moves == []

class Move_Iterator:
    def __init__(self, moves):
        self.moves = moves
        self.position = 0

    def __next__(self):
        try:
            value = self.moves[self.position]
            self.position+=1
        except IndexError:
            raise StopIteration()

        return value