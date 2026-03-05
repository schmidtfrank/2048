from fastapi import FastAPI
from game import Game2048


app = FastAPI()

GameInstance = Game2048()

@app.get("/")
async def root():
    return {"welcome":"please view github for support on api usage"}

@app.get("/new")
async def new_game():
    global GameInstance
    GameInstance.new_game()

    return {"board":GameInstance.board}

@app.get("/move/{movement}")
async def move(movement:str):
    global GameInstance
    if movement == 'd':
        GameInstance.move_right()
    elif movement == 'a':
        GameInstance.move_left()
    elif movement == 'w':
        #TODO
        pass
    elif movement == 's':
        #TODO
        pass

    #choose to ignore invalid moves instead of throwing error
    return {"board":GameInstance.board}