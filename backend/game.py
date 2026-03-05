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
    
    def new_tile(self):

        valid_tiles = []
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == 0:
                    valid_tiles.append((y,x))
        
        new_idx = random.randint(0,len(valid_tiles)-1)

        self.board[valid_tiles[new_idx][0]][valid_tiles[new_idx][1]] = 2
    def move_right(self):
        #self.board[y][x] works like intuition
        y = 0
        while y <= 3:
            x = 3
            while x >= 0:
                if self.board[y][x] == 0:
                    #need to see if there is any number in this row to put in our position
                    i = x-1
                    while i >= 0:
                        #found a match!
                        if self.board[y][i] != 0:
                            self.board[y][x] = self.board[y][i]
                            self.board[y][i] = 0
                            x += 1
                            break
                        i -= 1
                elif self.board[y][x] != 0:
                    #we need to check if something will merge into us here
                    i = x-1
                    while i >= 0:
                        if self.board[y][i] == self.board[y][x]:
                            self.board[y][x] *= 2
                            self.score += self.board[y][x]
                            self.board[y][i] = 0
                            break
                        i -= 1
                x -= 1
            y += 1
        
        self.new_tile()
    


GameInstance = Game2048()

GameInstance.new_game()

GameInstance.print_board()
