"""
CMSC 14200, Spring 2023
Homework #4
"""
from typing import List, Optional, Tuple, Set, Callable
import sys
from cell import Cell
from maze import Maze

class TuiSolver():
    """
    This class implements a TUI that takes a maze file, and prints out the
    solved maze using the BFS solver to provide the appropriate path
    """

    maze: Maze

    def __init__(self) -> None:
        self.maze = Maze(sys.argv[1])

    def __str__(self) -> str:
        path = self.maze.bfs()
        set_path: Set[Tuple[int, int]] = set(path)
        return self.maze.to_string(set_path, None)

if __name__ == "__main__":
    solver = TuiSolver()
    print(solver)
