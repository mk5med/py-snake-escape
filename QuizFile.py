# Do not modify the GridClassFile.py
import GridClassFile

# Iguana vs. Snakes (epic): https://youtu.be/el4CQj-TCbA?t=83

# The only thing you should need to modify is this function below!
# Given a grid state, decide on the best move for the iguana (the iguana will take 2 steps in that direction)
# Note that the iguana moves first (then the snakes)
# Return either "up", "down", "left", or "right"

# To win, the iguana ('I') must reach the goal ('G')
# The iguana will always spawn at the centre of the grid
# Snakes ('S') will randomly spawn on the boundaries of the grid, as will the goal.
# Snakes will always move in the direction of the iguana.
# If a snake touches the iguana you lose ('X'). If the iguana touches the goal you win ('W').


def generate_iguana_move(my_grid_environment: GridClassFile.GridEnvironment):
    # Hints: you may find the following useful:

    # my_grid_environment.snake_positions gives a list of all snake positions [x, y]
    snake_positions = my_grid_environment.snake_positions
    # print(snake_positions)
    # my_grid_environment.goal gives the goal position [x, y]
    goal = my_grid_environment.goal
    # print(goal)
    # my_grid_environment.iguana_pos gives the iguana position [x, y]
    iguana_pos = my_grid_environment.iguana_pos
    # print(iguana_pos)

    return "up"  # TODO: Replace this with some more winning decision!
