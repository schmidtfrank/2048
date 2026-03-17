from game import Game2048
import pytest


def test_move_up():
    GameInstance = Game2048()
    GameInstance.allow_tile_replace = False

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

def test_move_down():
    GameInstance = Game2048()
    GameInstance.allow_tile_replace = False

    GameInstance.board = [
        [0,0,0,0],
        [0,2,0,2],
        [0,0,0,0],
        [0,0,0,0]
    ]
    GameInstance.move_down()
    actual_board = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,2,0,2]
    ]
    assert GameInstance.board == actual_board

    GameInstance.board = [
        [0,0,0,0],
        [0,2,0,0],
        [0,2,0,0],
        [0,0,0,0]
    ]
    GameInstance.move_down()
    actual_board = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,4,0,0]
    ]
    assert GameInstance.board == actual_board

    GameInstance.board = [
        [0,2,0,0],
        [0,2,0,0],
        [0,2,0,0],
        [0,0,0,0]
    ]
    GameInstance.move_down()
    actual_board = [
        [0,0,0,0],
        [0,0,0,0],
        [0,2,0,0],
        [0,4,0,0]
    ]
    assert GameInstance.board == actual_board

    GameInstance.board = [
        [4,8,0,0],
        [0,2,16,2],
        [0,0,0,0],
        [0,0,0,16]
    ]
    GameInstance.move_down()
    actual_board = [
        [0,0,0,0],
        [0,0,0,0],
        [0,8,0,2],
        [4,2,16,16]
    ]
    assert GameInstance.board == actual_board