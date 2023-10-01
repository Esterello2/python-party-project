"""
CMSC 14200, Spring 2023
Homework #4

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from typing import List, Optional, Tuple, Set, Callable, Union, Dict
from cell import Cell

# Characters for representing mazes as strings
WALL_CHARS = {
    "H_WALL": "─", "V_WALL": "│", "HV_WALL": "┼",
    "NW_CORNER": "┌", "NE_CORNER": "┐", "SW_CORNER": "└", "SE_CORNER": "┘",
    "VE_WALL": "├", "VW_WALL": "┤", "HS_WALL": "┬", "HN_WALL": "┴",
    "N_WALL": "╵", "E_WALL": "╶", "S_WALL": "╷", "W_WALL": "╴"
}

CURSOR = "•"
PATH = "·"

# Notice how box drawing character are always a combination
# of four possible lines starting at the center and going
# north, east, south, or west. For example:
#
#   north and east: "└"
#   east, west, and south: "┬"
#   west only: "╴"
#
# The following dictionary maps a tuple with four boolean
# values (corresponding to north, east, south, west) to
# the corresponding box drawing character. This dictionary
# should make it easier to select the appropriate character
# in various situations.
#
# (the name of the variable relates to the fact that we can
# also think of these directions as hands on a clock pointing
# to 12, 3, 6, or 9)
CLOCK_CHARS = {
    (False, False, False, False): " ",
    (False, False, False, True): WALL_CHARS["W_WALL"],
    (False, False, True, False): WALL_CHARS["S_WALL"],
    (False, False, True, True): WALL_CHARS["NE_CORNER"],
    (False, True, False, False): WALL_CHARS["E_WALL"],
    (False, True, False, True): WALL_CHARS["H_WALL"],
    (False, True, True, False): WALL_CHARS["NW_CORNER"],
    (False, True, True, True): WALL_CHARS["HS_WALL"],
    (True, False, False, False): WALL_CHARS["N_WALL"],
    (True, False, False, True): WALL_CHARS["SE_CORNER"],
    (True, False, True, False): WALL_CHARS["V_WALL"],
    (True, False, True, True): WALL_CHARS["VW_WALL"],
    (True, True, False, False): WALL_CHARS["SW_CORNER"],
    (True, True, False, True): WALL_CHARS["HN_WALL"],
    (True, True, True, False): WALL_CHARS["VE_WALL"],
    (True, True, True, True): WALL_CHARS["HV_WALL"]
}


class Maze:
    """
    A class for representing mazes
    """

    grid: List[List[Cell]]

    def __init__(self, filename: str):
        """
        Constructor

        Args:
            filename: File containing specification of a maze
        """
        with open(filename, encoding="utf-8") as f:
            lines = f.readlines()
        self.grid = []
        for line in lines:
            row = []
            for cell in line.split(","):
                row.append(Cell("N" in cell, "E" in cell))
            self.grid.append(row)

        # Make sure contents of grid are consistent
        assert all(len(row) == len(self.grid[0]) for row in self.grid), \
            f"Rows in {filename} don't all have the same length"
        assert not any(c.north for c in self.grid[0]), \
            f"Top row of {filename} includes cells with north set to True"
        assert not any(row[self.ncols-1].east for row in self.grid), \
            f"Rightmost column of {filename} includes " \
            f"cells with east set to True"

    @property
    def nrows(self) -> int:
        """
        Returns the number of rows in the maze
        """
        return len(self.grid)

    @property
    def ncols(self) -> int:
        """
        Returns the number of columns in the maze
        """
        return len(self.grid[0])

    def cell(self, at: Tuple[int, int]) -> Optional[Cell]:
        """
        Returns the cell (if any) at a given coordinate

        Args:
            at: Tuple with (row, col) coordinates

        Returns: Cell object at that location. If the location
            is outside the bounds of the maze, returns None.

        """
        row, col = at
        if not ((0 <= row < len(self.grid)) and (0 <= col < len(self.grid[0]))):
            return None

        return self.grid[row][col]

    def north(self, at: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Returns the coordinates of the cell (if any) to the north of a cell.

        Args:
            at: Tuple with (row, col) coordinates

        Returns: If there exists a cell to the north of the cell
            at the given coordinates, *and* the two cells are
            connected, return the coordinates of the cell to the north.
            Otherwise, return None.
        """
        i, j = at
        if self.grid[i][j].north:
            return (i - 1, j)
        return None

    def east(self, at: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Returns the coordinates of the cell (if any) to the east of a cell.

        Args:
            at: Tuple with (row, col) coordinates

        Returns: If there exists a cell to the east of the cell
            at the given coordinates, *and* the two cells are
            connected, return the coordinates of the cell to the east.
            Otherwise, return None.
        """
        i, j = at
        if self.grid[i][j].east:
            return (i, j + 1)
        return None

    def south(self, at: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Returns the coordinates of the cell (if any) to the south of a cell.

        Args:
            at: Tuple with (row, col) coordinates

        Returns: If there exists a cell to the south of the cell
            at the given coordinates, *and* the two cells are
            connected, return the coordinates of the cell to the south.
            Otherwise, return None.
        """
        i, j = at
        if i + 1 >= len(self.grid):
            return None
        if self.grid[i + 1][j].north:
            return (i + 1, j)
        return None

    def west(self, at: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Returns the coordinates of the cell (if any) to the west of a cell.

        Args:
            at: Tuple with (row, col) coordinates

        Returns: If there exists a cell to the west of the cell
            at the given coordinates, *and* the two cells are
            connected, return the coordinates of the cell to the west.
            Otherwise, return None.
        """
        i, j = at
        if j == 0:
            return None
        if self.grid[i][j - 1].east:
            return (i, j - 1)
        return None

    def to_string(self, path: Set[Tuple[int, int]],
                  at: Optional[Tuple[int, int]]) -> str:
        """
        Returns a string representation of the maze

        Args:
            path: Set of locations to highlight with
                the path character
            at: Location to highlight with the cursor
                character

        Returns: String representation
        """
        side1 = (self.nrows * 2) + 1
        side2 = (self.ncols * 2) + 1

        result = self.list_string(path, at)

        walls = [WALL_CHARS["H_WALL"], WALL_CHARS["V_WALL"]]
        for r in range(side1):
            for c in range(side2):
                if result[r][c] is None:
                    bools = [False, False, False, False]
                    if 0 <= r - 1 and result[r-1][c] in walls:
                        bools[0] = True
                    if c + 1 < side2 and result[r][c+1] in walls:
                        bools[1] = True
                    if r + 1 < side1 and result[r+1][c] in walls:
                        bools[2] = True
                    if 0 <= c - 1 and result[r][c-1] in walls:
                        bools[3] = True
                    tup = (bools[0], bools[1], bools[2], bools[3])
                    result[r][c] = CLOCK_CHARS[tup]
        string: str = "\n".join("".join(cell or " " for cell in row) for row \
            in result)
        return string

    def list_string(self, path: Set[Tuple[int, int]],
                at: Optional[Tuple[int, int]]) -> List[List[Union[str, None]]]:
        """
        Creates an implementation of a maze in a list of lists manner
        
        Args:
            path: Set of locations to highlight with
                the path character
            at: Location to highlight with the cursor
                character

        Returns: a list of lists string representation
        """
        side1 = (self.nrows * 2) + 1
        side2 = (self.ncols * 2) + 1
        result: List[List[Union[str, None]]] = [[None]*side2 for _ in \
            range(side1)]

        for r in range(self.nrows):
            for c in range(self.ncols):
                x, y = ((r*2) + 1, (c*2) + 1)
                cell = self.grid[r][c]

                if cell.north:
                    result[x-1][y] = " "
                else:
                    result[x - 1][y] = WALL_CHARS["H_WALL"]
                if cell.east:
                    result[x][y+1] = " "
                else:
                    result[x][y+1] = WALL_CHARS["V_WALL"]
                if ((r+1) < self.nrows and self.grid[r+1][c].north) or (c == \
                    self.ncols - 1 and r == self.nrows - 1):
                    result[x+1][y] = " "
                else:
                    result[x+1][y] = WALL_CHARS["H_WALL"]
                if (0 <= (c-1) and self.grid[r][c-1].east) or (c == 0 and r == \
                    0):
                    result[x][y-1] = " "
                else:
                    result[x][y-1] = WALL_CHARS["V_WALL"]

                result[x][y] = " "

                self.check_at_and_path((x, y, r, c), path, at, result)

        result[0][0] = WALL_CHARS["H_WALL"]
        result[side1-1][side2-1] = WALL_CHARS["V_WALL"]
        return result

    def check_at_and_path(self, tup: Tuple[int, int, int, int], \
            path: Set[Tuple[int, int]], at: Optional[Tuple[int, int]], \
            lst: List[List[Union[str, None]]]) -> None:
        """
        This function changes the provided list to contain the at and/or path
        functionality
        
        Args:
            tup1: contains all necessary coordinates
            path: Set of locations to highlight with
                the path character
            at: Location to highlight with the cursor
                character
            lst: list of grid shown to player

        Returns: Nothing
        """
        x, y, r, c = tup
        if at:
            if (r, c) == at:
                lst[x][y] = CURSOR
        if path:
            if (r, c) in path and (r, c) != at:
                lst[x][y] = PATH

    def __str__(self) -> str:
        """
        Returns a string representation with no path or cursor highlighted
        """
        return self.to_string(set(), None)

    def bfs(self) -> List[Tuple[int, int]]:
        """
        Does a BFS traversal starting at (0,0) and returns
        the shortest path to the bottom-right cell of the maze.

        Returns: List of coordinates of the cells that would be
            visited on the shortest path, starting at (0,0).
            The list must include (0,0) and the bottom-left coordinate.
        """
        start = (0, 0)
        q = [start]
        visited = []
        loc_dict = {start: (0, 0)}
        path : List[Tuple[int, int]] = []
        while q:
            curr = q.pop(0)
            if curr not in visited and curr != start:
                visited.append(curr)
            if curr == (self.nrows - 1, self.ncols - 1):
                key = curr
                while key != (0, 0):
                    path.append(loc_dict[key])
                    key = loc_dict[key]
                path.reverse()
                path.append(curr)
            for pos in (self.north(curr), self.east(curr), self.south(curr),\
                self.west(curr)):
                if pos is not None and (pos not in visited):
                    loc_dict[pos] = curr
                    q.append(pos)
        return path

    def transform(
            self,
            transformer: Callable[["Maze", Tuple[int, int]], None]
            ) -> None:
        """
        Transforms the maze by applying a function to every cell of the maze.

        Args:
            transformer: Function that takes a Maze object and a tuple
                (representing the coordinates a cell) and transforms
                that cell is some way (does not return anything)

        Returns: Nothing
        """
        for i in range(self.nrows):
            for j in range(self.ncols):
                transformer(self, (i, j))


def open_all(maze: Maze, loc: Tuple[int, int]) -> None:
    """
    Takes a cell and connects it to the cells (if any)
    to the north, east, south, west (i.e., it "opens all the
    doors" of a cell)

    Args:
        maze: Maze object
        loc: Location (row, col) on the maze

    Returns: Nothing
    """
    x, y = loc
    if x == 0 and y == maze.ncols - 1:
        maze.grid[x][y].north = False
        maze.grid[x][y].east = False
    elif x == 0:
        maze.grid[x][y].east = True
    elif y == maze.ncols - 1:
        maze.grid[x][y].north = True
    else:
        maze.grid[x][y].north = True
        maze.grid[x][y].east = True

def open_dead_ends(maze: Maze, loc: Tuple[int, int]) -> None:
    """
    Takes a cell and, if it is a dead end (once in the cell,
    there you can only leave the cell by going back in the
    direction you came in), it creates a connection to
    the cell (if any) in the opposite direction to the existing
    connection.

    Args:
        maze: Maze object
        loc: Location (row, col) on the maze

    Returns: Nothing
    """
    x , y = loc
    counter = 0
    target_dir = ""
    tracker = dct_tracker(maze, loc)
    for val in tracker.values():
        if val:
            counter += 1
    if counter == 1:
        for dirx, stat in tracker.items():
            if stat:
                target_dir = dirx
        if target_dir == "N" and x < maze.nrows - 1:
            a, b = (x + 1, y)
            maze.grid[a][b].north = True
        if target_dir == "W" and y < maze.ncols - 1:
            maze.grid[x][y].east = True
        if target_dir == "E" and y > 0:
            a, b = (x, y - 1)
            maze.grid[a][b].east = True
        if target_dir == "S" and x > 0:
            maze.grid[x][y].north = True

def dct_tracker(maze: Maze, loc: Tuple[int, int]) -> Dict[str, bool]:
    """
    Given a location on a maze, a dictionary is returned mapping
    each of the four cardinal directions (N, E, S, W) to a bool value,
    True if there is a connecting Cell in a respective direction,
    False if there is None.
    
    Input:
        maze [Maze]: a Maze object
        loc [tuple[int]]: a tuple-pair of integers
        
    Output:
        dict[str: bool]
    """
    tracker= {}
    if not maze.north(loc):
        tracker["N"] = False
    else:
        tracker["N"] = True
    if not maze.south(loc):
        tracker["S"] = False
    else:
        tracker["S"] = True
    if not maze.east(loc):
        tracker["E"] = False
    else:
        tracker["E"] = True
    if not maze.west(loc):
        tracker["W"] = False
    else:
        tracker["W"] = True
    return tracker
