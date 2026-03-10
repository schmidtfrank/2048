import random 

class Game2048:
    def __init__(self):
        self.score = 0
        self.board = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [2,0,0,0]
        ]
        self.game_over = False
    
    #debugging purposes
    def print_board(self):
        for i in range(4):
            print(self.board[i])
    
    def new_game(self):
        self.score = 0
        self.game_over = False
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
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == 0:
                    valid_tiles.append((y,x))
        
        if len(valid_tiles) == 0:
            #whatever move was input didnt succeed in anything, so check if game is over and do not attempt to add tile.
            self.game_end()
            return

        y,x = random.choice(valid_tiles)

        self.board[y][x] = 2

        self.game_end()
    
    def game_end(self):
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == 0:
                    #there is a valid move
                    return
                if y-1 >= 0:
                    if self.board[y-1][x] == self.board[y][x]:
                        return
                if y+1 <= 3:
                    if self.board[y+1][x] == self.board[y][x]:
                        return
                if x+1 <= 3:
                    if self.board[y][x+1] == self.board[y][x]:
                        return
                if x-1 >= 0:
                    if self.board[y][x-1] == self.board[y][x]:
                        return
        self.game_over = True

    def move_right(self):
        #self.board[y][x] works like intuition
        y = 0
        moved_tile = False
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
                            moved_tile = True
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
                            moved_tile = True
                            break
                        elif self.board[y][i] != 0:
                            break
                        i -= 1
                x -= 1
            y += 1
        
        if moved_tile:
            self.new_tile()
    
    def move_left(self):
        #self.board[y][x] works like intuition
        y = 0
        moved_tile = False
        while y <= 3:
            x = 0
            while x <= 3:
                if self.board[y][x] == 0:
                    #need to see if there is any number in this row to put in our position
                    i = x+1
                    while i <= 3:
                        #found a match!
                        if self.board[y][i] != 0:
                            self.board[y][x] = self.board[y][i]
                            self.board[y][i] = 0
                            x -= 1
                            moved_tile = True
                            break
                        i += 1
                elif self.board[y][x] != 0:
                    #we need to check if something will merge into us here
                    i = x+1
                    while i <= 3:
                        if self.board[y][i] == self.board[y][x]:
                            self.board[y][x] *= 2
                            self.score += self.board[y][x]
                            self.board[y][i] = 0
                            moved_tile = True
                            break
                        elif self.board[y][i] != 0:
                            break
                        i += 1
                x += 1
            y += 1
        
        if moved_tile:
            self.new_tile()
    
    def move_down(self):
        #self.board[y][x] works like intuition
        x = 0
        moved_tile = False
        while x <= 3:
            y = 3
            while y >= 0:
                if self.board[y][x] == 0:
                    #need to see if there is any number in this row to put in our position
                    i = y-1
                    while i >= 0:
                        #found a match!
                        if self.board[i][x] != 0:
                            self.board[y][x] = self.board[i][x]
                            self.board[i][x] = 0
                            y += 1
                            moved_tile = True
                            break
                        i -= 1
                elif self.board[y][x] != 0:
                    #we need to check if something will merge into us here
                    i = y-1
                    while i >= 0:
                        if self.board[i][x] == self.board[y][x]:
                            self.board[y][x] *= 2
                            self.score += self.board[y][x]
                            self.board[i][x] = 0
                            moved_tile = True
                            break
                        elif self.board[i][x] != 0:
                            break
                        i -= 1
                y -= 1
            x += 1
        
        if moved_tile:
            self.new_tile()
    
    def move_up(self):
        #self.board[y][x] works like intuition
        x = 0
        moved_tile = False
        while x <= 3:
            y = 0
            while y <= 3:
                if self.board[y][x] == 0:
                    #need to see if there is any number in this row to put in our position
                    i = y+1
                    while i <= 3:
                        #found a match!
                        if self.board[i][x] != 0:
                            self.board[y][x] = self.board[i][x]
                            self.board[i][x] = 0
                            y -= 1
                            moved_tile = True
                            break
                        i += 1
                elif self.board[y][x] != 0:
                    #we need to check if something will merge into us here
                    i = y+1
                    while i <= 3:
                        if self.board[i][x] == self.board[y][x]:
                            self.board[y][x] *= 2
                            self.score += self.board[y][x]
                            self.board[i][x] = 0
                            moved_tile = True
                            break
                        elif self.board[i][x] != 0:
                            break
                        i += 1
                y += 1
            x += 1
        
        if moved_tile:
            self.new_tile()
    

def test_run(GameInstance):
    v = ""
    while v != 'q':
        print("---")
        v = input()
        if v == "r":
            GameInstance.move_right()
        elif v == "l":
            GameInstance.move_left()
        elif v == 'w':
            GameInstance.move_up()
        elif v == 's':
            GameInstance.move_down()
        GameInstance.print_board()

