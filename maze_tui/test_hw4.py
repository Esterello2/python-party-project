import subprocess
from typing import Dict, List, Tuple
import sys

import pytest
import json
from maze import Maze, open_all, open_dead_ends

MAZE_NAMES = ['small', 'sample-1', 'sample-2', 'dead-ends',
              'maze-5x5-1', 'maze-5x5-2', 'maze-5x5-3',
              'maze-10x10-1', 'maze-10x10-2', 'maze-10x10-3',
              'maze-10x20-1', 'maze-10x20-2', 'maze-10x20-3',
              'maze-20x20-1', 'maze-20x20-2', 'maze-20x20-3',
              'maze-40x40',
              ]

TEST_DIR = "mazes/"
MAZE_EXT = ".maze.txt"
STR_EXT = ".str.txt"
OPENALL_EXT = ".open-all.txt"
OPENDEADENDS_EXT = ".open-dead-ends.txt"
BFS_EXT = ".bfs.txt"
SOLVED_EXT = ".solved.txt"


@pytest.mark.parametrize("maze_name", MAZE_NAMES)
def test_task1(maze_name: str) -> None:
    maze = Maze(TEST_DIR + maze_name + MAZE_EXT)
    f = open(TEST_DIR + maze_name + STR_EXT, encoding="utf-8")
    expected = f.read().strip()

    to_str = maze.to_string(set(), None).strip()
    dunder = str(maze).strip()

    assert to_str == expected
    assert dunder == expected


@pytest.mark.parametrize("maze_name", MAZE_NAMES)
def test_task2(maze_name: str) -> None:
    maze = Maze(TEST_DIR + maze_name + MAZE_EXT)
    f = open(TEST_DIR + maze_name + BFS_EXT, encoding="utf-8")
    expected = f.readline()

    bfs = maze.bfs()

    assert str(bfs) == expected


@pytest.mark.parametrize("maze_name", MAZE_NAMES)
def test_task3_open_all(maze_name: str) -> None:
    maze = Maze(TEST_DIR + maze_name + MAZE_EXT)
    expected = Maze(TEST_DIR + maze_name + OPENALL_EXT)

    maze.transform(open_all)

    maze_compare(maze, expected)


@pytest.mark.parametrize("maze_name", MAZE_NAMES)
def test_task3_open_dead_ends(maze_name: str) -> None:
    maze = Maze(TEST_DIR + maze_name + MAZE_EXT)
    expected = Maze(TEST_DIR + maze_name + OPENDEADENDS_EXT)

    maze.transform(open_dead_ends)

    maze_compare(maze, expected)


@pytest.mark.parametrize("frame", range(13))
def test_task4(frame: int) -> None:
    base = "maze-5x5-1"
    maze = Maze(TEST_DIR + base + MAZE_EXT)
    expected = open(TEST_DIR + base + f".frame{frame}.txt", encoding="utf-8").read().strip()
    f = open(TEST_DIR + base + BFS_EXT, encoding="utf-8")
    bfs_str = f.read()
    bfs_str = bfs_str.replace("(", "[").replace(")", "]")
    bfs_path = json.loads(bfs_str)
    bfs_path = list(map(tuple, bfs_path))

    to_str = maze.to_string(set(bfs_path[:frame]), bfs_path[frame]).strip()

    assert to_str == expected

@pytest.mark.parametrize("maze_name", ['small', 'sample-1', 'sample-2', 'dead-ends', "maze-40x40"])
def test_task5_solver(maze_name: str) -> None:
    maze_file = TEST_DIR + maze_name + MAZE_EXT
    f = open(TEST_DIR + maze_name + SOLVED_EXT, encoding="utf-8")
    expected = f.read().strip()

    command = [sys.executable, "tui_solver.py", maze_file]

    try:
        proc = subprocess.run(command, capture_output=True, timeout=1)
    except subprocess.TimeoutExpired:
        pytest.fail(f"Tried to run tui_solver.py with maze {maze_file}, but the program didn't exit when done.")

    stdout = proc.stdout.decode(encoding="utf-8")
    cmd_str = " ".join(command)

    if expected not in stdout:
        pytest.fail(f"Running '{cmd_str}' did not produce the expected output\n\nEXPECTED:\n\n{expected}\n\nACTUAL:\n\n{stdout}")

@pytest.fixture()
def sample1_game_strs() -> Dict[int, Dict[int, str]]:
    game_str: Dict[int, Dict[int, str]] = {}
    for i in range(4):
        game_str[i] = {}
        for j in range(4):
            frame = open(TEST_DIR + f"sample-1.game-{i}-{j}.txt", encoding="utf-8").read().strip()
            game_str[i][j] = frame

    return game_str

def game_helper(maze_name:str, game_difficulty: str, game_input: str,
                game_strs: Dict[int, Dict[int, str]],
                expect_coords: List[Tuple[int, int]],
                expect_wall: bool, expect_done: bool) -> None:

    WALL_MESSAGE = "There is a wall in the way"
    DONE_MESSAGE = "You made it out!"

    maze_file = f"mazes/{maze_name}.maze.txt"
    printable_inputs = game_input.strip().replace("\n", "-")
    bytes_input = bytes(game_input, encoding="utf-8")

    command = [sys.executable, "tui_game.py", maze_file, game_difficulty]

    try:
        proc = subprocess.run(command, input=bytes_input, capture_output=True, timeout=1)
    except subprocess.TimeoutExpired:
        pytest.fail(f"Tried to run tui_game.py the program didn't exit when done.")

    stdout = proc.stdout.decode(encoding="utf-8")

    cmd_str = " ".join(command)

    for i, j in expect_coords:
        if game_strs[i][j] not in stdout:
            pytest.fail(f"Running '{cmd_str}' (with moves {printable_inputs}) "
                        f"did not include the following in its output:\n\n{game_strs[i][j]}"
                        f"\n\nFULL OUTPUT:\n\n{stdout}")

    if expect_wall and WALL_MESSAGE not in stdout:
        pytest.fail(f"Running '{cmd_str}' (with moves {printable_inputs}) "
                    f"should've hit a wall (and printed '{WALL_MESSAGE}') but didn't."
                    f"\n\nFULL OUTPUT:\n\n{stdout}")

    if expect_wall and WALL_MESSAGE not in stdout:
        pytest.fail(f"Running '{cmd_str}' (with moves {printable_inputs}) "
                    f"should've printed '{DONE_MESSAGE}' but didn't."
                    f"\n\nFULL OUTPUT:\n\n{stdout}")

def test_task5_game_one_move(sample1_game_strs: Dict[int, Dict[int, str]]) -> None:
    game_helper("sample-1", "regular", "d\n", sample1_game_strs, [(0,0), (0,1)], False, False)

def test_task5_game_multiple_moves(sample1_game_strs: Dict[int, Dict[int, str]]) -> None:
    game_helper("sample-1", "regular", "d\nd\nd\nd\ns\na\n", sample1_game_strs,
                [(0,0), (0,1), (0,2), (0,3), (1,3), (1, 2)], False, False)

def test_task5_game_wall1(sample1_game_strs: Dict[int, Dict[int, str]]) -> None:
    game_helper("sample-1", "regular", "w\n", sample1_game_strs,
                [(0,0)], True, False)

def test_task5_game_wall2(sample1_game_strs: Dict[int, Dict[int, str]]) -> None:
    game_helper("sample-1", "regular", "d\nd\nd\nd\ns\na\na\n", sample1_game_strs,
                [(0,0), (0,1), (0,2), (0,3), (1,3), (1, 2)], False, False)

def test_task5_game_full(sample1_game_strs: Dict[int, Dict[int, str]]) -> None:
    game_helper("sample-1", "regular", "d\nd\nd\nd\ns\na\ns\na\ns\nd\nd\n", sample1_game_strs,
                [(0,0), (0,1), (0,2), (0,3), (1,3), (1, 2), (2, 2), (2, 1), (3, 1), (3, 2), (3, 3)],
                False, True)

def test_task5_game_easy() -> None:
    frame0 = open(TEST_DIR + "sample-1-easy.game-0-0.txt", encoding="utf-8").read().strip()
    frame1 = open(TEST_DIR + "sample-1-easy.game-0-1.txt", encoding="utf-8").read().strip()
    game_strs = {0: {0: frame0, 1: frame1}}
    game_helper("sample-1", "easy", "d\n", game_strs, [(0,0), (0,1)], False, False)

def test_task5_game_supereasy() -> None:
    frame0 = open(TEST_DIR + "sample-1-supereasy.game-0-0.txt", encoding="utf-8").read().strip()
    frame1 = open(TEST_DIR + "sample-1-supereasy.game-0-1.txt", encoding="utf-8").read().strip()
    game_strs = {0: {0: frame0, 1: frame1}}
    game_helper("sample-1", "super-easy", "d\n", game_strs, [(0,0), (0,1)], False, False)


def maze_compare(actual: Maze, expected: Maze) -> None:
    assert actual.nrows == expected.nrows, \
        f"Incorrect number of rows in maze (expected {expected.nrows}, got {actual.nrows})"
    assert actual.ncols == expected.ncols, \
        f"Incorrect number of columns in maze (expected {expected.ncols}, got {actual.ncols})"

    for row in range(expected.nrows):
        assert len(actual.grid[row]) == expected.ncols, \
            f"Row {row} of the maze has an incorrect number of columns (expected {expected.ncols}, got {len(actual.grid[row])})"

        for col in range(expected.ncols):
            actual_cell = actual.grid[row][col]
            expected_cell = expected.grid[row][col]

            assert actual_cell.north == expected_cell.north, \
                f"Cell ({row}, {col}) has incorrect north (expected {expected_cell.north}, got {actual_cell.north})"

            assert actual_cell.east == expected_cell.east, \
                f"Cell ({row}, {col}) has incorrect east (expected {expected_cell.east}, got {actual_cell.east})"
