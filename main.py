import sys
from Board import Board
from Game import Game, GameHistory
from Player import Player, Player, Random_Player, Greedy_Player, OutOfBoundsError, JumpAvailableError, NotYourPieceError, EmptySpaceError, PieceIsStuckError, InvalidOptionIndex
from Piece import Peasant, WHITE, BLACK

class CheckersCLI:

    def __init__(self, history=False):
        self.history = history

    def run(self, cmd_line):

        # create board
        current_board = Board()

        # create game
        player1, player2 = self.parse_players(cmd_line)
        current_game = Game(current_board, player1, player2)

        # create game history
        if self.history:
            game_history = GameHistory(current_game)

        while(True):

            # print board from board class
            current_game.current_board.print_board()

            # print turn and color from game class
            current_game.print_turn()

            if self.history:                

                command = input("undo, redo, or next\n>")

                if command == "undo":
                    current_game = game_history.undo(current_game)
                    current_board = current_game.current_board
                    continue
                elif command == "redo":
                    current_game = game_history.redo(current_game)
                    current_board = current_game.current_board
                    continue
                elif command == "next":
                    game_history.redo_stack = []
                else:
                    print("That is an invalid command")
                    continue

            # add game state to undo stack
            if self.history:
                game_history.save(current_game)

            # check if the game has ended in a victory or draw
            if current_game.is_game_over(current_board):
                break

            while(True):

                try:
                    # increment game counter
                    current_game.game_counter+=1

                    # current player makes a move
                    current_game.current_player.make_a_move(self, current_game, current_game.current_board, current_game.other_player)
                    
                    # change turns
                    temp = current_game.current_player
                    current_game.current_player = current_game.other_player
                    current_game.other_player = temp

                    # increment number of turns made
                    current_game.number_of_turns+=1
                    break
                
                except OutOfBoundsError:
                    print("That piece cannot move")
                except JumpAvailableError:
                    print("That piece cannot move")
                except NotYourPieceError:
                    print("That is not your piece")  
                except EmptySpaceError:
                    print("No piece at that location")
                except PieceIsStuckError:
                    print("That piece cannot move")
            
    def display_options(self, coord, moves):

        # find valid moves - create move_options dict of move objects
        move_options = {}
        dict_index = 0

        # create options dict
        for move in moves:
            if move.old_coord == coord:
                if str(dict_index) not in move_options.keys():
                    move_options[str(dict_index)] = move
                    dict_index+=1

        # print move_options dict
        for index, move in move_options.items():
            print(index + ": " + str(move))

        # return move_options dict
        return move_options 

    def parse_players(self, cmd_line):

        player1 = Player(WHITE)
        player2 = Player(BLACK)
        
        if len(cmd_line) > 1:
            if cmd_line[1] == "human":
                player1 = Player(WHITE)
            
            elif cmd_line[1] == "greedy":
                player1 = Greedy_Player(WHITE)

            elif cmd_line[1] == "random":
                player1 = Random_Player(WHITE)

            if cmd_line[2] == "human":
                player2 = Player(BLACK)
                
            elif cmd_line[2] == "greedy":
                player2 = Greedy_Player(BLACK)

            elif cmd_line[2] == "random":
                player2 = Random_Player(BLACK)

        return player1, player2
        
if __name__ == "__main__":

    history = True if len(sys.argv) == 4 and sys.argv[3] == "on" else False

    # while(True):
    CheckersCLI(history).run(sys.argv)

