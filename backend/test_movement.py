from game import Game2048
import pytest

#create game instance
GameInstance = Game2048()
#disable auto tile replacement for series of tests
GameInstance.allow_tile_replace = False


def test_move_up():
    global GameInstance
    GameInstance.board = [
        [0,0,0,0],
        [0,2,0,0],
        [0,0,0,0],
        [0,0,0,2]
    ]
    GameInstance.move_up()
    actual_board = [
        [0,2,0,2],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]

    assert GameInstance.board == actual_board

    GameInstance.board = [
        [0,2,0,0],
        [2,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]
    GameInstance.move_up()
    actual_board = [
        [2,2,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]

    assert GameInstance.board == actual_board

    GameInstance.board = [
        [0,2,0,0],
        [0,2,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]
    GameInstance.move_up()
    actual_board = [
        [0,4,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]

    assert GameInstance.board == actual_board

    GameInstance.board = [
        [0,8,2,0],
        [0,4,0,0],
        [0,0,0,0],
        [0,4,0,0]
    ]
    GameInstance.move_up()
    actual_board = [
        [0,8,2,0],
        [0,8,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]

    assert GameInstance.board == actual_board

    GameInstance.board = [
        [0,0,0,0],
        [0,0,0,2],
        [0,0,0,2],
        [0,0,0,4]
    ]
    GameInstance.move_up()
    actual_board = [
        [0,0,0,4],
        [0,0,0,4],
        [0,0,0,0],
        [0,0,0,0]
    ]

    assert GameInstance.board == actual_board

    