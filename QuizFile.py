# Quiz File
# Iguana vs. Snakes (epic): https://youtu.be/el4CQj-TCbA?t=83

# Do not modify the GridClassFile.py
import GridClassFile

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


if __name__ == "__main__":
    print("Initializing escape simulation")
    generate_metrics = True  # Change this to True to generate your average performance!

    my_grid = GridClassFile.GridEnvironment(size=11, num_snakes=5, do_print=True)

    my_grid.print_grid("start")

    either_exit = False
    max_steps = 100  # If the iguana hasn't found the exit by 100 steps it will get tired and be eaten
    current_steps = 0
    while not either_exit:
        iguana_move = generate_iguana_move(my_grid)
        my_grid.run_round(iguana_move, 2)

        if my_grid.iguana_escaped:
            print("The iguana has escaped! (win)")
            either_exit = True
        elif my_grid.iguana_ded:
            print("The snakes are victorious... (loss)")
            either_exit = True
        elif current_steps >= max_steps:
            print(
                "The iguana ran out of energy (>100 steps). The snakes are victorious... (loss)"
            )
            either_exit = True
        current_steps += 1

    # Metrics generation
    if generate_metrics:
        num_victories = 0
        num_losses = 0
        for i in range(10000):
            my_grid = GridClassFile.GridEnvironment(
                size=11, num_snakes=5, do_print=False
            )

            # my_grid.print_grid("start")

            either_exit = False
            current_steps = 0  # Resets
            while not either_exit:
                iguana_move = generate_iguana_move(my_grid)
                my_grid.run_round(iguana_move, 2)

                if my_grid.iguana_escaped:
                    # print("The iguana has escaped! (win)")
                    num_victories += 1
                    either_exit = True
                elif my_grid.iguana_ded:
                    # print("The snakes are victorious... (loss)")
                    num_losses += 1
                    either_exit = True
                elif current_steps >= max_steps:
                    num_losses += 1
                    either_exit = True
                current_steps += 1
        print(
            "Wins:",
            num_victories,
            "Losses:",
            num_losses,
            "Win Ratio:",
            num_victories / num_losses,
            "Win Percent:",
            round(num_victories / 10000.0 * 100, 4),
        )
