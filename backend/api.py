from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from game import Game2048


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)

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
        GameInstance.move_up()
    elif movement == 's':
        GameInstance.move_down()

    #choose to ignore invalid moves instead of throwing error
    return {"board":GameInstance.board,"game_over":GameInstance.game_over}

@app.get("/score")
async def get_score():
    global GameInstance
    return {"score" : GameInstance.score}