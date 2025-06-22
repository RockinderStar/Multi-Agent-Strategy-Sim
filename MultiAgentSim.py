import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Simulation settings
GRID_SIZE = 5
TOTAL_TURNS = 10
NUM_GAMES = 50

# Learning parameters
switch_threshold = 0.5
learning_rate = 0.1

# Failure probabilities
failure_chance_normal = 0.2  # Chance to fail when using normal strategy
failure_chance_counter = 0.1  # Chance to fail when using counter strategy

# Tracking results
results = {
    'Game': [],
    'Success': [],
    'Switch Threshold': []
}

def play_game(switch_chance):
    team_a_pos = 0
    team_b_pos = GRID_SIZE - 1
    team_b_strategy = "normal"

    for turn in range(1, TOTAL_TURNS + 1):
        # Team A randomised movement (could move 1 or 2 steps forward)
        team_a_pos += np.random.choice([1, 2])

        # Team B decides whether to switch strategy
        if np.random.rand() < switch_chance:
            team_b_strategy = "counter"
        else:
            team_b_strategy = "normal"

        # Team B movement
        if team_b_strategy == "normal":
            team_b_pos -= 1
        else:
            team_b_pos -= np.random.choice([0, 2])

        # Check for engagement
        if team_a_pos >= team_b_pos:
            # Simulate possible failure even when teams engage
            if team_b_strategy == "normal":
                if np.random.rand() < failure_chance_normal:
                    return False  # Failure despite engagement
            else:
                if np.random.rand() < failure_chance_counter:
                    return False  # Failure despite engagement

            return True  # Engagement success

    return False  # No engagement

# Run simulations
for game in range(1, NUM_GAMES + 1):
    success = play_game(switch_threshold)

    # Update learning based on success
    if success:
        switch_threshold += learning_rate * (1 - switch_threshold)
    else:
        switch_threshold -= learning_rate * switch_threshold

    switch_threshold = max(0, min(1, switch_threshold))  # Keep in valid range

    # Save game results
    results['Game'].append(game)
    results['Success'].append(1 if success else 0)
    results['Switch Threshold'].append(switch_threshold)

    print(f"Game {game}: {'Success' if success else 'Failure'} | Switch Threshold: {switch_threshold:.2f}")

# Convert results to DataFrame
df = pd.DataFrame(results)

# Calculate cumulative success rate
df['Cumulative Success Rate'] = df['Success'].cumsum() / df['Game']

# Plot the results
plt.figure(figsize=(12, 6))
plt.plot(df['Game'], df['Cumulative Success Rate'], label='Cumulative Success Rate', marker='o')
plt.plot(df['Game'], df['Switch Threshold'], label='Switch Threshold', linestyle='--')
plt.xlabel('Game Number')
plt.ylabel('Rate / Threshold')
plt.title('Learning Progress with Introduced Failures')
plt.legend()
plt.grid(True)
plt.show()

