"""
CMSC 14200, Spring 2023
Homework #4
"""
from typing import List, Optional, Tuple, Set, Callable, Union, Dict
import sys
from maze import Maze, open_all, open_dead_ends

def dir_dct_constr(maze: Maze, at: Tuple[int, int]) -> Dict[str,\
    Union[Tuple[int, int], None]]:
    """
    Given a maze and a location, creates a dictionary which maps
    WASD keyboard characters (w, a, s, d) to the "at" cell's neighbor
    location in a respective direction; for example, since "w" key
    corresponds to an "up", or North, direction, the north neighbor
    is the value. If there is no open neighbor, the value is None.
    
    Input:
        maze [Maze]
        at [Tuple[int, int]]
    """
    dir_dct = {"w" : maze.north(at), "d" : maze.east(at), "s" : maze.south(at),
               "a" : maze.west(at)}
    return dir_dct

def play_maze(maze: Maze, difficulty: str) -> None:
    """
    The game is played here; the maze is updated after every
    user's valid input, and takes in a difficulty mode to determine
    the transformation on a maze.
    """
    start: Tuple[int, int] = (0, 0)
    while True:
        if difficulty == "easy":
            maze.transform(open_dead_ends)
        elif difficulty == "super-easy":
            maze.transform(open_all)
        print(maze.to_string(set(), start))
        if start == (maze.nrows - 1, maze.ncols - 1) :
            print("You made it out!")
            break
        table_dirs = dir_dct_constr(maze, start)
        dirx = input("Click W, A, S, or D to navigate the maze, and select \
            ENTER.")
        if dirx in table_dirs:
            if not table_dirs[dirx]:
                print("There is a wall in the way")
            else:
                start = table_dirs[dirx]
        else:
            print("Input must only be W, A, S, or D")


if __name__ == "__main__":
    game: Maze
    game = Maze(sys.argv[1])
    play_maze(game, sys.argv[2])
