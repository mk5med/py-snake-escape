# Snake Escape / Iguana escape optimisation

The original game and source code was shared with me and the original author is unknown.
This repository improves the original code and starts tracking the history for future use.

# Gameplay

You play the role of an iguana that needs to move towards a goal while avoiding snakes that hunt you.
The game is played by modifying the `generate_iguana_move` to create a algorithm that decides what the best move for the iguana based only on the game state.

The engine will run your algorithm with random test cases and will return a final win score. 
```
Note that the iguana moves first (then the snakes)
Return either "up", "down", "left", or "right"

To win, the iguana ('I') must reach the goal ('G')
The iguana will always spawn at the centre of the grid
Snakes ('S') will randomly spawn on the boundaries of the grid, as will the goal.
Snakes will always move in the direction of the iguana.
If a snake touches the iguana you lose ('X'). If the iguana touches the goal you win ('W').
```

Sample score
```
Wins: 153 Losses: 9847 Win Ratio: 0.015537727226566466 Win Percent: 1.53
```