# MY PORTFOLIO

# Reversi Board Game

Team members:
- Esteban Arellano (GUI)
- Diana Chu (TUI)
- Riyush Thakur (Bot)
- Andrew Matute (QA)

Improvements
- Game Logic
    Completeness
        -We now pass all the tests (100/100) instead of partially.
    - Issue with grid
        -We made the attributes of the Board class become private.
    - Issue with legal_move
        -We changed the dynamic of the function. Instead of iterating through
        every location a specific player has on the board to then find possible 
        starting points to legally reach the square in question, we only iterate
        through a list of directions, which takes us from the square in question
        to potentially a friendly piece. This improves the time efficiency
        of this function. We then store these directions as the negative
        reciprocal because we are now going from "target to friendly piece"
        instead of vice-versa.
    - Issue with load_game
        -We accounted for this by keeping track of the moves of load_game and
        this updates the other attributes.
    - Issue with simulate_moves
        -We now loop over the list of moves and apply them, giving back a
        simulated game, not changing the actual game state, and not just
        applying one move.
    Code Quality
        We fixed BoardGridType back to type List[Optional[Int]]. We also
        removed the inheritance of class Board from BoardGridType.

- GUI
This component received two S's in Milestone 2
- TUI
This component received two S's in Milestone 2
- Bot
This component received two S's in Milestone 2
- QA
This component received two S's in Milestone 2

Enhancements
- added alternate library to the TUI to support more than 9 colors
- added music to the GUI (this enhancement only works on mac, not on windows)
- added start screen on the GUI
- added a player piece counter that updates on GUI; it is never recaculated
since it is stored in an attribute in the Reversi class as a dictionary,
mapping player number to counter.

# Maze Game Text User Interface
Collaboration with another programmer where a TUI maze was constructed using object-oriented 
programming, BFS and DFS algorithms, and game scripting.


