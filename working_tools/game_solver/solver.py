from working_tools.game_solver.external_sampling import external_sampling
from tqdm import tqdm


def solver(abstraction, time_horizon, num_of_players, root):
    regret_table = {}
    strategy_table = {}
    sigma_table = {}
    for infoset in abstraction:
        actions = list(infoset.info_nodes.values())[0].actions
        regret_actions = {}
        strategy_actions = {}
        sigma_actions = {}
        for action in actions:
            regret_actions[action] = 0
            strategy_actions[action] = 0
            sigma_actions[action] = 1 / len(actions)
        regret_table[infoset.name] = regret_actions
        strategy_table[infoset.name] = strategy_actions
        sigma_table[infoset.name] = sigma_actions

    utilities = []

    regrets_history = []

    description = 'time elapsed:'
    for t in tqdm(range(time_horizon), desc=description, unit="t"):
        for player in range(1, num_of_players + 1):
            utilities.append(external_sampling(abstraction,
                                               str(player),
                                               regret_table,
                                               strategy_table,
                                               sigma_table,
                                               root,
                                               1))
        total_timestep_regret = 0
        for infoset in regret_table.keys():
            for action in regret_table[infoset].keys():
                total_timestep_regret += regret_table[infoset][action]

        regrets_history.append(total_timestep_regret / (t+1))

    return regrets_history, strategy_table
