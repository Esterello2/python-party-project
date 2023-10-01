"""
CMSC 14200, Spring 2023
Homework #4

Do not modify this file!
"""

class Cell:
    """
    Class for representing an individual cell.
    """

    north: bool
    east: bool

    def __init__(self, north: bool, east: bool):
        """
        Constructor

        Args:
            north: True if this cell is connected to a cell
                to the north. False otherwise.
            east: True if this cell is connected to a cell
                to the east. False otherwise
        """
        self.north = north
        self.east = east

    def __repr__(self) -> str:
        """
        Returns a string representation of a Cell object,
        useful for debugging.
        """
        dir_str = ""
        dir_str += "N" if self.north else ""
        dir_str += "E" if self.east else ""

        return f"Cell<{dir_str}>"
