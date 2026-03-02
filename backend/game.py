import random 

class Game2048:
    def __init__(self):
        self.score = 0
        self.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]
    
    #debugging purposes
    def print_board(self):
        for i in range(4):
            print(self.board[i])
    
    def new_game(self):
        self.score = 0
        
        for x in range(4):
            for y in range(4):
                self.board[x][y] = 0
        
        for i in range(2):
            x = random.randint(0,3)
            y = random.randint(0,3)

            if self.board[x][y] != 0:
                i -= 1
            else:
                self.board[x][y] = 2
    
    def move_right(self):
        pass


GameInstance = Game2048()

GameInstance.new_game()

GameInstance.print_board()