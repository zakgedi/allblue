# allblue
Project Overview

My project starts with a command line interface object. After the command line is parsed, player 1 and player 2 are created as human, random, or greedy player object. The command line interface method creates a board object, a game object, an optional game history object.

1)	The player objects take advantage of the Template design pattern. The player class has two steps when executing a move/strategy. As step 1, it has a function that enumerates all possible moves for a given player and another function that makes a move based on a specific strategy. The random player inherits from the player class and overrides the make_move() method in order to implement a random approach to picking a move. Similarly, the greedy player inherits from the general player class, and overrides the make_move method with its own greedy strategy. 
2)	Moves use a Command design pattern in order to take advantage of the ability to defer the execution of a command. If a given move is valid, a simple move or jump move object is created. Both classes have similar functions, but the jump class has an extra attribute to track the number of pieces captured by a given move. Like the Command pattern requires the simple and jump objects have execute methods that ultimately class the move_piece() command in the piece class. 
3)	In order to find the best move to take or find a random move, move objects are stored using the Iterator design pattern. This pattern makes iterating through a list of moves, finding a random move or finding the move with the maximum number of pieces easier. The pieces class finds all the legal moves of a given piece and returns a simple move iterable object and a jump move iterable object. After all moves have been enumerated the player object executes the move object as a result of their specific strategy. 
4)	The state of the game was stored before any action was taken. This storage is made possible through the Memento design pattern. A deep copy of a game object is created and a static game memento is created. At each turn a memento is added to a stack (known as the undo stack) allowing the user to undo by popping mementos off of the undo stack. 

The game takes advantage of encapsulation. Therefore, the code can be further updated for any game by adding new players that inherit from the player class but update the make_move() method. The command line interface class will call make_move on the player regardless of which player it is. Different pieces can inherit from the piece class and override the move_piece class and make their own methods to find legal moves. Therefore, adapting the code to work for another game is a matter of creating new objects that inherit from what is currently available and overriding some methods. Encapsulation means that the rest of the code will interact with the objects just as normal.


** Setting up your backend **
Run the following code to set up your virtual enviroment:
```
python3 -m venv env 
source env/bin/activate 
```
You can check that you've set up the virtual enviroment with: 
```
echo $VIRTUAL_ENV
```

Then we will install all the necessary packages:
```
install package pip install -e .
```

Then we can run our backend:
```
export FLASK_ENV=development 
export FLASK_APP=jumble 
flask run --host 0.0.0.0 --port 8000
```
