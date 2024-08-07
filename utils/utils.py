# Import necessary libraries
import torch
import matplotlib.pyplot as plt

def coord_to_state(global_pos, num_states, Region_bound):
    """
    Convert global position coordinates to a local state index within a region.

    Parameters:
    - global_pos: A dictionary with 'pos' key containing a tuple (x, y) of the global coordinates.
    - num_states: Total number of states.
    - Region_bound: A dictionary where keys are region indices and values are bounds (x_min, y_min, x_max, y_max).

    Returns:
    - A one-hot encoded tensor representing the local state index or a zero tensor if outside of bounds.
    """
    # Extract coordinates from the global position
    global_pos = (global_pos['pos'][0], global_pos['pos'][1])
    state = None

    # Find the region based on the global coordinates
    for region, ((x_min, y_min), (x_max, y_max)) in Region_bound.items():
        if x_min <= global_pos[0] <= x_max and y_min <= global_pos[1] <= y_max:
            # Calculate local coordinates
            local_x = global_pos[0] - x_min + 1
            local_y = global_pos[1] - y_min + 1
            # Convert local coordinates to a state index
            len_x = x_max - x_min + 1  # width of the region
            state = int((local_y - 1) * len_x + (local_x - 1))
            break  # Exit loop once the region is found

    # Initialize one-hot encoded tensor
    one_hot = torch.zeros(num_states)
    if state is not None:
        one_hot[state] = 1

    return one_hot

def compression_function(state, Region_bound):
    """
    Map agent positions to regions.

    Parameters:
    - state: A dictionary with 'pos' key containing a tuple (x, y) of the global coordinates.
    - Region_bound: A dictionary where keys are region names and values are bounds (x_min, y_min, x_max, y_max).

    Returns:
    - The region name where the state is located or None if no region is found.
    """
    # Extract coordinates from the state
    state = (state['pos'][0], state['pos'][1])
    x, y = state

    # Find the region based on the coordinates
    for region_name, ((x1, y1), (x2, y2)) in Region_bound.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            return region_name

    print("Error: No region found for position", x, y)
    return None

def print_q_table(q_table):
    """
    Print the Q-table with tasks, regions, and options in a structured format.

    Args:
    - q_table (dict): The Q-table structured as {task: {region: {option: Q-value}}}.
    """
    for task, regions in q_table.items():
        print(f"Task {task}:")
        for region, options in regions.items():
            options_str = ', '.join([f"Option {opt}: {value}" for opt, value in options.items()])
            print(f"  Region {region}: {options_str}")
        print()

def plot_steps(steps, std_steps):
    """
    Plot the total steps per episode with standard deviation.

    Parameters:
    - steps: Average total steps per episode.
    - std_steps: Standard deviation of steps per episode.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(steps, label='Average Total Steps per Episode')
    plt.fill_between(range(len(steps)), steps - std_steps, steps + std_steps, alpha=0.2, label='Standard Deviation')
    plt.xlabel('Episode')
    plt.ylabel('Total Steps')
    plt.title('Total Steps Over Episodes')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_rewards(total_rewards, std_rewards):
    """
    Plot the total rewards per episode with standard deviation.

    Parameters:
    - total_rewards: Average total rewards per episode.
    - std_rewards: Standard deviation of rewards per episode.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(total_rewards, label='Average Total Rewards per Episode')
    plt.fill_between(range(len(total_rewards)), total_rewards - std_rewards, total_rewards + std_rewards, alpha=0.2, label='Standard Deviation')
    plt.xlabel('Episode')
    plt.ylabel('Total Rewards')
    plt.title('Total Rewards Over Episodes')
    plt.legend()
    plt.grid(True)
    plt.show()
