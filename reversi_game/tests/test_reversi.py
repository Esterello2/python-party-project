from typing import List, Tuple
from enum import Enum
import pytest
from reversi import Reversi, Piece, Board, PieceColor

def helper_apply(rev: Reversi, moves: List[Tuple[int, int]]) -> Reversi:
    """
    This helper function takes in a game of Reversi, and applies the list of
    moves provided
    
    Args:
        rev (Reversi): a game of Reversi
        moves (List[Tuple[int, int]]): moves to apply

    Returns:
        Reversi: the game of Reversi with the applied moves
    """
    for move in moves:
        assert rev.legal_move(move) == True
        rev.apply_move(move)
    
    return rev

def helper_available(rev: Reversi, moves: List[Tuple[int, int]]) -> None:
    """
    This function checks that for the given turn in reversi, the available_moves
    are all in the list moves.

    Args:
        rev (Reversi): a game of Reversi
        moves (List[Tuple[int, int]]): list of expected available moves

    Returns: None
    """
    for move in rev.available_moves:
        assert rev.legal_move(move) == True
        assert move in moves

def test_create_size_1():
    """
    Test whether we can correctly create a (non-Othello) 4x4 game
    """
    rev = Reversi(side = 4, players = 2, othello = False)
    grid = rev.grid
    assert len(grid) == 4
    
    for r, row in enumerate(grid):
        assert len(row) == 4
        for c, value in enumerate(row):
            assert value is None, f"Expected grid[{r}][{c}] to be None but got \
                {value}"
    
    assert rev.size == 4
    assert rev.num_players == 2
    assert not rev.done
    assert rev.outcome == []
    assert rev.turn == 1

def test_create_size_2():
    """
    Test whether we can correctly create a (non-Othello) 6x6 game
    """
    rev = Reversi(side = 6, players = 2, othello = False)
    grid = rev.grid
    assert len(grid) == 6
    
    for r, row in enumerate(grid):
        assert len(row) == 6
        for c, value in enumerate(row):
            assert value is None, f"Expected grid[{r}][{c}] to be None but got \
                {value}"
    
    assert rev.size == 6
    assert rev.num_players == 2
    assert not rev.done
    assert rev.outcome == []
    assert rev.turn == 1
    
def test_create_size_3():
    """
    Test whether we can correctly create a (non-Othello) 8x8 game
    """
    rev = Reversi(side = 8, players = 2, othello = False)
    grid = rev.grid
    assert len(grid) == 8
    
    for r, row in enumerate(grid):
        assert len(row) == 8
        for c, value in enumerate(row):
            assert value is None, f"Expected grid[{r}][{c}] to be None but got \
                {value}"
    
    assert rev.size == 8
    assert rev.num_players == 2
    assert not rev.done
    assert rev.outcome == []
    assert rev.turn == 1

def test_create_size_4():
    """
    Raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        rev = Reversi(side = 0, players = 2, othello = False)

def test_create_size_5():
    """
    Raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        rev = Reversi(side = 2, players = 2, othello = False)

def test_create_size_6():
    """
    Raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        rev = Reversi(side = 3, players = 2, othello = False)

def test_create_size_7():
    """
    Raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        rev = Reversi(side = 5, players = 2, othello = False)

def test_create_othello_size_1():
    """
    Test whether we can correctly create an 6x6 Othello game
    """
    rev = Reversi(side=6, players=2, othello=True)
    grid = rev.grid
    assert len(grid) == 6

    othello_pos = [(2, 2, 2), (3, 2, 1), (2, 3, 1), (3, 3, 2)]

    for r, row in enumerate(grid):
        assert len(row) == 6
        for c, value in enumerate(row):
            if r in (2, 3) and c in (2, 3):
                continue
            assert value is None, f"Expected grid[{r}][{c}] to be None but got \
                {value}"

    for r, c, player in othello_pos:
        piece = grid[r][c]
        assert (piece == player), f"Expected grid[{r}][{c}] to be \
            {player} but got {grid[r][c]}"

    assert rev.size == 6
    assert rev.num_players == 2
    assert not rev.done
    assert rev.outcome == []
    assert rev.turn == 1

def test_create_othello_size_2():
    """
    Raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        rev = Reversi(side = 0, players = 2, othello = True)

def test_create_othello_size_3():
    """
    Raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        rev = Reversi(side = 3, players = 2, othello = True)

def test_create_othello_size_4():
    """
    Raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        rev = Reversi(side = 7, players = 2, othello = True)

def test_othello_8x8_1():
    """
    Test whether we can correctly create an 8x8 Othello game and apply_move
    functions
    """
    rev = Reversi(side = 8, players = 2, othello = True)
    grid = rev.grid
    assert len(grid) == 8
    
    assert rev.legal_move((3, 2)) == True
    
    apply = rev.apply_move((3, 2))
    assert apply == None
    
    assert rev.piece_at((3, 2)) == 1
    assert rev.piece_at((3, 3)) == 1
    
    assert rev.size == 8
    assert rev.num_players == 2
    
    assert not rev.done
    assert rev.outcome == []
    assert rev.turn == 2

def test_othello_8x8_2():
    """
    Test whether we can correctly create an 8x8 Othello game and apply_move
    functions
    """
    rev = Reversi(side = 8, players = 2, othello = True)
    grid = rev.grid
    assert len(grid) == 8
    
    assert rev.legal_move((3, 2)) == True
    
    apply = rev.apply_move((3, 2))
    assert apply == None
    
    assert rev.piece_at((3, 2)) == 1
    assert rev.piece_at((3, 3)) == 1
    assert rev.turn == 2

    assert rev.legal_move((4, 2)) == True

    apply = rev.apply_move((4, 2))
    assert apply == None

    assert rev.piece_at((4, 2)) == 2
    assert rev.piece_at((4, 3)) == 2

    assert rev.size == 8
    assert rev.num_players == 2
    
    assert not rev.done
    assert rev.outcome == []
    assert rev.turn == 1

def test_othello_8x8_3():
    """
    Test whether we can correctly create an 8x8 Othello game and apply_move
    functions
    """
    rev = Reversi(side = 8, players = 2, othello = True)
    grid = rev.grid
    assert len(grid) == 8
    
    assert rev.legal_move((5, 4)) == True
    
    apply = rev.apply_move((5, 4))
    assert apply == None
    
    assert rev.piece_at((5, 4)) == 1
    assert rev.piece_at((4, 4)) == 1
    assert rev.turn == 2

    assert rev.legal_move((3, 5)) == True

    apply = rev.apply_move((3, 5))
    assert apply == None

    assert rev.piece_at((3, 5)) == 2
    assert rev.piece_at((3, 4)) == 2
    assert rev.turn == 1
    
    assert rev.legal_move((2, 5)) == True
    
    apply = rev.apply_move((2, 5))
    assert apply == None
    
    assert rev.piece_at((2, 5)) == 1
    assert rev.piece_at((3, 4)) == 1

    assert rev.size == 8
    assert rev.num_players == 2
    
    assert not rev.done
    assert rev.outcome == []
    assert rev.turn == 2

def test_create_othello_8x8_4():
    """
    Raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        rev = Reversi(side = 8, players = 2, othello = True)
        rev.apply_move((4, 3))

def test_create_othello_8x8_5():
    """
    Raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        rev = Reversi(side = 8, players = 2, othello = True)
        rev.apply_move((2, 3))
        rev.apply_move((2, 3))

def test_create_othello_8x8_6():
    """
    Raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        rev = Reversi(side = 8, players = 2, othello = True)
        rev.apply_move((2, 3))
        rev.apply_move((1, 3))

def test_create_othello_8x8_7():
    """
    tests available moves in 8x8 othello game
    """
    rev = Reversi(side=8, players=2, othello=True)
    
    expected = {(2, 3), (3, 2), (4, 5), (5, 4)}

    assert set(rev.available_moves) == expected

def test_create_othello_8x8_8():
    """
    tests available moves in an 8x8 othello game
    """
    rev = Reversi(side=8, players=2, othello=True)
    
    expected = {(2, 3), (3, 2), (5, 4), (4, 5)}

    assert set(rev.available_moves) == expected

def test_create_othello_8x8_9():
    """
    tests for othello sizesize
    """
    rev = Reversi(side=8, players=2, othello=True)
    grid = rev.grid

    assert len(grid) == 8

    othello_pos = [(3, 3, 2), (3, 4, 1), (4, 3, 1), (4, 4, 2)]

    for r, row in enumerate(grid):
        assert len(row) == 8
        for c, value in enumerate(row):
            if r in (4, 3) and c in (4, 3):
                continue
            assert value is None, f"Expected grid[{r}][{c}] to be None but got \
                {value}"

    for r, c, player in othello_pos:
        assert (
            grid[r][c] == player
        ), f"Expected grid[{r}][{c}] to be {player} but got {grid[r][c]}"

    assert rev.size == 8
    assert rev.num_players == 2
    
    assert not rev.done
    assert rev.outcome == []
    assert rev.turn == 1

def test_othello_finished_1():
    """
    Finishes a game of reversi
    """
    rev = Reversi(side=4, players=2, othello=True)
    lst = [(0,1), (0,0), (1,0), (0,2), (0,3), (3,1), (3, 2), (3,3), (2,3),
           (1,3), (2,0), (3,0)]
    rev = helper_apply(rev, lst)

    assert rev.done == True
    
    expected = set()
    assert set(rev.available_moves) == expected
    assert rev.outcome == [2]

def test_6x6_othello_1():
    """
    Constructs a 6x6 Othello game and tests size
    """
    rev = Reversi(side = 6, players = 2, othello = True)
    grid = rev.grid
    
    assert len(grid) == 6
    assert rev.size == 6
    assert not rev.done
    assert rev.outcome == []

def test_6x6_othello_2():
    """
    Constructs a 6x6 Othello game and tests num_players
    """
    rev = Reversi(side = 6, players = 2, othello = True)
    grid = rev.grid
    
    assert len(grid) == 6
    assert rev.num_players == 2
    assert not rev.done
    assert rev.outcome == []

def test_6x6_othello_3():
    """
    Constructs a 6x6 Othello game and tests turn
    """
    rev = Reversi(side = 6, players = 2, othello = True)
    grid = rev.grid
    
    assert len(grid) == 6
    assert rev.turn == 1
    assert not rev.done
    assert rev.outcome == []

def test_6x6_othello_4():
    """
    Constructs a 6x6 Othello game and tests piece_at
    """
    rev = Reversi(side = 6, players = 2, othello = True)
    grid = rev.grid
    
    assert len(grid) == 6
    assert rev.piece_at((2, 2)) == 2
    assert rev.piece_at((2, 3)) == 1
    assert not rev.done
    assert rev.outcome == []

def test_6x6_othello_5():
    """
    Constructs a 6x6 Othello game and tests legal_move
    """
    rev = Reversi(side = 6, players = 2, othello = True)
    grid = rev.grid
    
    assert len(grid) == 6
    assert rev.legal_move((4, 3)) == True
    assert rev.legal_move((0, 2)) == False
    assert not rev.done
    assert rev.outcome == []

def test_6x6_othello_6():
    """
    Constructs a 6x6 Othello game and tests available_moves
    """
    rev = Reversi(side = 6, players = 2, othello = True)
    grid = rev.grid
    
    assert len(grid) == 6
    for move in rev.available_moves:
        assert move in [(1, 2), (2, 1), (4, 3), (3, 4)]   
    assert not rev.done
    assert rev.outcome == []

def test_20x20_othello_1():
    """
    Constructs a 20x20 Othello game and tests size
    """
    rev = Reversi(side = 20, players = 2, othello = True)
    grid = rev.grid
    
    assert len(grid) == 20
    assert rev.size == 20
    assert not rev.done
    assert rev.outcome == []

def test_20x20_othello_2():
    """
    Constructs a 20x20 Othello game and tests num_players
    """
    rev = Reversi(side = 20, players = 2, othello = True)
    grid = rev.grid
    
    assert len(grid) == 20
    assert rev.num_players == 2
    assert not rev.done
    assert rev.outcome == []

def test_20x20_othello_3():
    """
    Constructs a 20x20 Othello game and tests turn
    """
    rev = Reversi(side = 20, players = 2, othello = True)
    grid = rev.grid
    
    assert len(grid) == 20
    assert rev.turn == 1
    assert rev.turn != 2
    assert rev.outcome == []

def test_20x20_othello_4():
    """
    Constructs a 20x20 Othello game and tests piece_at
    """
    rev = Reversi(side = 20, players = 2, othello = True)
    grid = rev.grid
    
    assert len(grid) == 20
    assert rev.piece_at((10, 9)) == 1
    assert rev.piece_at((9, 9)) == 2
    assert rev.piece_at((9, 9)) != 1
    assert rev.piece_at((18, 17)) != 2
    assert not rev.done
    assert rev.outcome == []

def test_20x20_othello_5():
    """
    Constructs a 20x20 Othello game and tests legal_move
    """
    rev = Reversi(side = 20, players = 2, othello = True)
    grid = rev.grid
    
    assert len(grid) == 20
    assert rev.legal_move((10, 11)) == True
    assert rev.legal_move((10, 10)) == False
    assert rev.legal_move((8, 8)) == False
    assert rev.legal_move((18, 18)) == False
    assert not rev.done
    assert rev.outcome == []

def test_20x20_othello_6():
    """
    Constructs a 20x20 Othello game and tests available_moves
    """
    rev = Reversi(side = 20, players = 2, othello = True)
    grid = rev.grid
    
    assert len(grid) == 20
    for move in rev.available_moves:
        assert move in [(9, 8), (8, 9), (11, 10), (10, 11)]   
    for move in rev.available_moves:
        assert move not in [(9, 11), (11, 9), (11, 11)]

    assert not rev.done
    assert rev.outcome == []

def test_8x8_nonothello_1():
    """
    Constructs an 8x8 non-othello 2 player game and verifies legal_move and
    available_moves only allow moves in the center square
    """
    rev = Reversi(side = 8, players = 2, othello = False)
    assert len(rev.grid) == 8
    
    for move in rev.available_moves:
        assert move in [(4, 3), (3, 4), (3, 3), (4, 4)]
        assert rev.legal_move(move) == True
    for move in rev.available_moves:
        assert move not in [(5, 5), (4, 6), (5, 4)]
        assert rev.legal_move(move) == True
    
    assert not rev.done
    assert rev.outcome == []

def test_8x8_nonothello_2():
    """
    Constructs an 8x8 non-othello 2 player game with pieces in the center square
    and verifies legal_move and available_move results consistent with the
    center square being filled in
    """
    rev = Reversi(side = 8, players = 2, othello = False)
    assert len(rev.grid) == 8
    new_grid = [[None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, 2, 1, None, None, None],
                [None, None, None, 1, 2, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None]]
    rev.load_game(1, new_grid)
    for move in rev.available_moves:
        assert move in [(3, 2), (2, 3), (5, 4), (4, 5)]
        assert rev.legal_move(move) == True
    
    assert not rev.done
    assert rev.outcome == []

def test_9x9_nonothello_1():
    """
    Construct a 9x9 non-othello 3 player game, and verify legal_move and
    available_moves only allow moves in the center square
    """
    rev = Reversi(side = 9, players = 3, othello = False)
    assert len(rev.grid) == 9
    
    helper_available(rev, [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), \
        (5, 3), (5, 4), (5, 5)])
    rev.apply_move((4, 4))
    helper_available(rev, [(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), \
        (5, 4), (5, 5)])
    rev.apply_move((3, 3))
    helper_available(rev, [(3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), \
        (5, 5)])
    
    assert not rev.done
    assert rev.outcome == []

def test_9x9_nonothello_2():
    """
    Constructs a 9x9 non-othello 3 player game with pieces in the center square,
    and verifies legal_move and available_moves results consistent with the
    center square being filled in
    """
    rev = Reversi(side = 9, players = 3, othello = False)
    assert len(rev.grid) == 9
    new_grid = [[None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None],
                [None, None, None, 1, 2, 3, None, None, None],
                [None, None, None, 1, 2, 3, None, None, None],
                [None, None, None, 1, 2, 3, None, None, None],
                [None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None, None]]
    rev.load_game(1, new_grid)

    # checks available_moves and legal_move
    helper_available(rev, [(4, 2), (5, 2), (6, 3), (6, 4), (2, 4), (2, 5),\
        (3, 6), (4, 6), (6, 2), (2, 6), (5, 6), (6, 5), (6, 6)])
    
    assert not rev.done
    assert rev.outcome == []

def test_5x5_nonothello_1():
    """
    Constructs a 5x5 non-othello 3 player game, and calls apply_move to result
    in the game ending, then verifies that the grid contains the expected,
    verifies done and outcome returns values consistent with a game that has
    ended
    """
    rev = Reversi(side = 5, players = 3, othello = False)
    grid = rev.grid
    assert len(grid) == 5
    
    helper_apply(rev, [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2), (1, 3),\
        (2, 3), (3, 3), (4, 1), (0, 4), (0, 3), (4, 4), (4, 0), (3, 4), (4, 2),\
            (1, 0), (0, 1), (0, 0), (0, 2), (1, 4), (2, 4), (4, 3), (3, 0), \
                (2, 0)])
    lst1 = [(0,0), (2, 0), (1, 1), (2, 1), (2, 2), (3, 4), (1, 0), \
        (2, 4), (4, 4)]
    lst2 = [(4, 0), (3, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3), \
        (4, 3), (0, 4), (4, 1), (3, 2), (4, 2) ]
    lst3 = [(3, 0), (0, 1), (1, 2), (1, 4)]
 
    for r, row  in enumerate(grid):
        for c, _ in enumerate(row):
            p = grid[r][c]
            if (r, c) in lst1:
                assert p == 1
            elif (r, c) in lst2:
                assert p == 2
            elif (r, c) in lst3:
                assert p == 3
            else:
                raise ValueError("Position isn't defined to a player")

    assert rev.done
    assert rev.outcome == [2]

# for the following tests
g = [[None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None],
     [None, None, None, 1, 2, None, None, None],
     [None, None, 2, 2, 2, None, None, None],
     [None, None, 2, 1, 1, 1, None, None],
     [None, None, 2, None, None, None, None, None],
     [None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None]]
lst2 = [(3, 2), (4, 2), (5, 2), (3, 3), (2, 4), (3, 4)]
lst1 = [(2, 3), (4, 3), (4, 4), (4, 5)]

def test_8x8_othello_1():
    """
    Constructs an 8x8 othello board and uses load_game to load a grid with 6
    pieces, and verifies the state of the game
    """
    rev = Reversi(side = 8, players = 2, othello = True)
    grid = rev.grid
    assert len(grid) == 8
    rev.load_game(1, g)
    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            p = grid[r][c]
            if p is None and ((r, c) not in lst1 and (r, c) not in lst2):
                continue
            elif (r, c) in lst1:
                assert p == 1
            elif (r, c) in lst2:
                assert p == 2
    assert rev.turn == 1
    assert not rev.done
    assert rev.outcome == []

def test_8x8_othello_2():
    """
    Constructs an 8x8 othello board, and in load_game, raises a ValueError if
    the value of the turn is inconsistent with _players attribute
    """
    with pytest.raises(ValueError):
        rev = Reversi(side = 8, players = 2, othello = True)
        rev.load_game(3, g)

def test_8x8_othello_3():
    """
    Constructs an 8x8 othello board, and in load_game, raises a ValueError if
    the size of the grid is inconsistent with _side attribute
    """
    with pytest.raises(ValueError):
        rev = Reversi(side = 8, players = 2, othello = True)
        h = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 1, 1, 1, 1, 1, 1]]
        rev.load_game(1, h)

def test_8x8_othello_4():
    """
    Constructs an 8x8 othello board, and in load_game, raises a ValueError if
    any value in the grid is inconsistent with _players attribute
    """
    with pytest.raises(ValueError):
        rev = Reversi(side = 8, players = 2, othello = True)
        h = g
        h[0].append((None))
        rev.load_game(1, h)

def test_skip():
    """
    Constructs a 4x4 Othello game that has a turn skipping in apply_move
    """
    rev = Reversi(side = 4, players = 2, othello = True)
    helper_apply(rev, [(3, 2), (3, 1), (3, 0), (3, 3), (2, 3), (1, 3), (0, 3),\
        (0, 1), (0, 2), (2, 0), (0, 0), (1, 0)])
    assert rev.done
    assert rev.outcome == [1]

def test_simulate_moves_1():
    """
    Test simulating a move that doesn't end the game
    """
    reversi = Reversi(side=8, players=2, othello=True)

    grid_orig = reversi.grid
    future_reversi = reversi.simulate_moves([(3, 2)])

    legal = {(2, 3), (3, 2), (4, 5), (5, 4)}

    # Check that the original game state has been preserved
    assert reversi.grid == grid_orig
    assert reversi.turn == 1
    assert set(reversi.available_moves) == legal
    assert not reversi.done
    assert reversi.outcome == []

    # Check that the returned object corresponds to the
    # state after making the move.
    legal.remove((3, 2))
    legal = {(4, 2), (2, 4), (2, 2)}
    assert future_reversi.grid != grid_orig
    assert future_reversi.turn == 2
    assert set(future_reversi.available_moves) == legal
    assert not future_reversi.done
    assert future_reversi.outcome == []

def test_simulate_move_2():
    """
    Test simulating a move that results in Player 1 winning
    """
    reversi = Reversi(side=4, players=2, othello=True)
    
    grid_orig = reversi.grid

    future_reversi = reversi.simulate_moves([(3, 2), (3, 1), (3, 0), (3, 3),
        (2, 3), (1, 3), (0, 3), (0, 1), (0, 2), (2, 0), (1, 0), (0, 0)])

    legal = {(1, 0), (0, 1), (3, 2), (2, 3)}

    # Check that the original game state has been preserved
    assert reversi.grid == grid_orig
    assert reversi.turn == 1
    assert set(reversi.available_moves) == legal
    assert not reversi.done
    assert reversi.outcome == []

    # Check that the returned values correspond to the
    # state after making the move.
    assert future_reversi.grid != grid_orig
    assert future_reversi.done
    assert future_reversi.outcome == [1]

def test_simulate_move_3():
    """
    Test simulating a move that results in a tie
    """
    reversi = Reversi(side=5, players=3, othello=False)
    new_grid = [[1, 1, 1, 2, None], [1, 1, 1, 1, 1], [3, 3, 3, 3, 3],
                [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]]
    reversi.load_game(1, new_grid)
    grid_orig = reversi.grid

    future_reversi = reversi.simulate_moves([(0, 4)])                           
    legal = {(0, 4)}

    # Check that the original game state has been preserved
    assert reversi.grid == grid_orig
    assert reversi.turn == 1
    assert set(reversi.available_moves) == legal
    assert not reversi.done
    assert reversi.outcome == []

    # Check that the returned values correspond to the
    # state after making the move.
    assert future_reversi.grid != grid_orig
    assert future_reversi.done
    assert sorted(future_reversi.outcome) == [1, 2]

def test_simulate_moves_4():
    """
    Test that calling simulate_moves with an invalid position
    raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        reversi = Reversi(side=7, players=2, othello=True)
        future_reversi = reversi.simulate_moves([(-1, -1)])

    with pytest.raises(ValueError):
        reversi = Reversi(side=7, players=2, othello=True)
        future_reversi = reversi.simulate_moves([(8, 8)])

def test_simulate_moves_5():
    """
    Constructs a board and checks that in simulate_moves, it passes more than
    one move in the moves paramater
    """
    reversi = Reversi(side=4, players=2, othello=True)
    grid_orig = reversi.grid

    future_reversi = reversi.simulate_moves([(3, 2), (3, 1), (3, 0), (3, 3)])

    legal = {(1, 0), (0, 1), (3, 2), (2, 3)}

    # Check that the original game state has been preserved
    assert reversi.grid == grid_orig
    assert reversi.turn == 1
    assert set(reversi.available_moves) == legal
    assert not reversi.done
    assert reversi.outcome == []

    # Check that the returned values correspond to the
    # state after making the move.
    assert future_reversi.grid != grid_orig
    assert not future_reversi.done
    assert future_reversi.outcome == []

def test_simulate_moves_6():
    """
    Constructs a board and checks that in simulate_moves, it passes more than
    one move in the moves paramater, and moves are made before simulate_moves
    """
    reversi = Reversi(side=4, players=2, othello=True)
    grid_orig = reversi.grid

    helper_apply(reversi, [(3, 2), (3, 1)])
    future_reversi = reversi.simulate_moves([(3, 0), (3, 3)])

    legal = {(0, 0), (1, 0), (2, 0), (3, 0)}

    # Check that the original game state has been preserved
    assert reversi.grid == grid_orig
    assert reversi.turn == 1
    assert set(reversi.available_moves) == legal
    assert not reversi.done
    assert reversi.outcome == []

    # Check that the returned values correspond to the
    # state after making the move.
    assert future_reversi.grid != grid_orig
    assert not future_reversi.done
    assert future_reversi.outcome == []

def test_simulate_moves_7():
    """
    Constructs a board and checks that in simulate_moves, it passes more than
    one move in the moves paramater, and moves are made before simulate_moves
    """
    reversi = Reversi(side=6, players=2, othello=True)
    grid_orig = reversi.grid

    helper_apply(reversi, [(2, 1), (1, 1)])
    future_reversi = reversi.simulate_moves([(1, 2), (1, 3), (0, 4), (3, 1)])

    legal = {(0, 1), (1, 2), (3, 4), (4, 3)}

    # Check that the original game state has been preserved
    assert reversi.grid == grid_orig
    assert reversi.turn == 1
    assert set(reversi.available_moves) == legal
    assert not reversi.done
    assert reversi.outcome == []

    # Check that the returned values correspond to the
    # state after making the move.
    assert future_reversi.grid != grid_orig
    assert not future_reversi.done
    assert future_reversi.outcome == []

def test_full_board_1():
    '''
    Constructs an 8x8 two-player game that ends with a full board, and just one
    player as the winner
    '''
    rev = Reversi(side=8, players=2, othello=True)
    new_grid = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1], [None, 2, 2, 2, 2, 2, 2, 2]]
    rev.load_game(1, new_grid)
    
    avail = {(7,0)}
    assert set(rev.available_moves) == avail
    assert rev.legal_move((7,0))
    assert not rev.done
    rev.apply_move((7, 0))
    
    assert rev.done
    assert rev.outcome == [1]

def test_full_board_2():
    '''
    Constructs an 8x8 two-player game that ends with a full board, and with the
    two players tying.
    '''
    rev = Reversi(side=8, players=2, othello=False)
    new_grid = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],
                [None, 1, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2]]
    rev.load_game(2, new_grid)
    
    avail = {(4,0)}
    assert set(rev.available_moves) == avail
    assert rev.legal_move((4,0))
    assert not rev.done
    rev.apply_move((4, 0))
    
    assert rev.done
    assert sorted(rev.outcome) == [1,2]

def test_full_board_3():
    '''
    Constructs a 7x7 three-player game that ends with a full board, and just one
    player as the winner.
    '''
    rev = Reversi(side=7, players=3, othello=False)
    new_grid = [[1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1],
                [1, None, 2, 3, 3, 2, 1], [2, 2, 2, 2, 2, 2, 2],
                [3, 3, 3, 3, 3, 3, 3]]
    rev.load_game(1, new_grid)
    
    avail = {(4,1)}
    assert set(rev.available_moves) == avail
    assert rev.legal_move((4,1))
    assert not rev.done
    rev.apply_move((4, 1))
    
    assert rev.done
    assert rev.outcome == [1]

def test_full_board_4():
    '''
    Constructs a 7x7 three-player game that ends with a full board, and two of
    the players tying (i.e., not a three-way tie)
    '''
    rev = Reversi(side=7, players=3, othello=False)
    new_grid = [[3, 3, 3, 3, 3, 3, 3], [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1],
                [2, 2, 3, None, 2, 2, 2], [3, 3, 3, 3, 3, 3, 3],
                [3, 3, 3, 3, 3, 3, 3]]
    rev.load_game(2, new_grid)
    
    avail = {(4,3)}
    assert set(rev.available_moves) == avail
    assert rev.legal_move((4,3))
    assert not rev.done
    rev.apply_move((4, 3))
    
    assert rev.done
    assert sorted(rev.outcome) == [1, 3]

def test_full_board_5():
    '''
    Constructs an 8x8 two-player game where, before the board is full, both
    players end up having no available moves (with one of them winning at that
    point in the game)
    '''
    rev = Reversi(side=8, players=2, othello=True)
    new_grid = [[1, 2, 1, 1, 1, 1, 2, None], [2, 2, 1, 1, 1, 1, 2, 1],
                [1, 2, 1, 1, 1, 1, 2, 1], [1, 2, 2, 1, 1, 2, 2, 1],
                [2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2], [2, None, 2, 2, 2, 2, None, 2]]
    rev.load_game(2, new_grid)
    
    avail = {(0,7)}
    assert set(rev.available_moves) == avail
    assert rev.legal_move((0,7))
    assert not rev.done
    rev.apply_move((0, 7))
    
    assert rev.done
    assert rev.outcome == [2]