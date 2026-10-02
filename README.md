# ECEN 4293 Midterm - Perfect Connect Four Bot

This version extends the Lab 2 Connect Four game with a `PerfectCPUPlayer`.
The perfect player sends the current move sequence to Pascal Pons's exact
Connect Four solver at `connect4.gamesolver.org` and selects the legal column
with the highest returned score.

## Files

- `game.py` - menu and game loop
- `board.py` - 7x6 board, win checking, legal moves, and move history
- `player.py` - human, random CPU, and perfect CPU player classes
- `perfect_solver.py` - interface to the exact Connect Four solver
- `matplotdisplayLab02.py` - matplotlib graphical interface

## Run

Install matplotlib if necessary:

```bash
python -m pip install matplotlib
```

Then run:

```bash
python game.py
```

Game modes:

1. Human vs Human
2. Human vs Random CPU
3. Human vs Perfect CPU
4. Perfect CPU vs Perfect CPU

The perfect modes require an internet connection because they use the public
exact solver endpoint.

## Solver source

Pascal Pons, Connect 4 Solver:
- https://connect4.gamesolver.org/
- https://github.com/PascalPons/connect4

The solver evaluates positions under perfect play using alpha-beta search.
Positive move scores are winning moves, zero is a draw, and negative scores
are losing moves. The player selects the highest-scoring legal move.
