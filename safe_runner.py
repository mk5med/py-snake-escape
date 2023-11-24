import GridClassFile
from QuizFile import generate_iguana_move
import copy


def run_action(action, grid: GridClassFile.GridEnvironment):
    """
    Ensures that action is called with a copy of `grid`.
    This protects the game from algorithms that modify the grid and influence game results
    """
    return action(copy.deepcopy(grid))


def run_simulation(*, action, grid: GridClassFile.GridEnvironment, max_steps: int):
    current_steps = 0

    # Flag to stop the loop
    # This is triggered when:
    # 1) The iguana escaped
    # 2) The iguana died
    # 3) The iguana exceeded its maximum movements
    either_exit = False

    while not either_exit:
        iguana_move = run_action(action, grid)
        grid.run_round(iguana_move, 2)

        if grid.iguana_escaped:
            print("The iguana has escaped! (win)")
            either_exit = True
        elif grid.iguana_ded:
            print("The snakes are victorious... (loss)")
            either_exit = True
        elif current_steps >= max_steps:
            print(
                "The iguana ran out of energy (>100 steps). The snakes are victorious... (loss)"
            )
            either_exit = True
        current_steps += 1


def generate_metrics(*, action, samples: int = 10000, max_steps: int):
    # Metrics generation
    num_victories = 0
    num_losses = 0
    for i in range(samples):
        grid = GridClassFile.GridEnvironment(size=11, num_snakes=5, do_print=False)

        # my_grid.print_grid("start")

        either_exit = False
        current_steps = 0  # Resets
        while not either_exit:
            iguana_move = run_action(action, grid)
            grid.run_round(iguana_move, 2)

            if grid.iguana_escaped:
                # print("The iguana has escaped! (win)")
                num_victories += 1
                either_exit = True
            elif grid.iguana_ded:
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


def main(action, *, should_generate_metrics=True, max_steps=100):
    """
    @param action A pure function that generates a string action. Allowed values: `up, down, left, right`
    @param should_generate_metrics: bool = True Change this to True to generate your average performance!
    @param max_steps: int = 100 The maximum number of steps an Iguana will take before it gets tired and is eaten
    """
    print("Initializing escape simulation")

    my_grid = GridClassFile.GridEnvironment(size=11, num_snakes=5, do_print=True)

    # Print the initial grid
    my_grid.print_grid("start")

    run_simulation(action=action, grid=my_grid, max_steps=max_steps)

    if should_generate_metrics:
        generate_metrics(action=action, max_steps=max_steps)


if __name__ == "__main__":
    main(generate_iguana_move)
