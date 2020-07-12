from game_solver.external_sampling import external_sampling
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
    previous_cumulative_regret = 0
    regrets_history = []
    previous_regret_table = []

    for t in tqdm(range(0, time_horizon), desc='Game solver, processed time steps', unit='t'):
        for player in range(1, num_of_players + 1):
            utilities.append(external_sampling(abstraction,
                                               str(player),
                                               regret_table,
                                               strategy_table,
                                               sigma_table,
                                               root,
                                               1))
        maximum_regret = 0

        # if t > 0:
        #     for infoset in regret_table.keys():
        #         for action in regret_table[infoset].keys():
        #             regret_difference = regret_table[infoset][action] - previous_regret_table[infoset][action]
        #             if regret_difference > maximum_regret:
        #                 maximum_regret = regret_difference
        #
        # previous_regret_table = copy.deepcopy(regret_table)
        #
        # regrets_history.append(maximum_regret)

        total_timestep_regret = 0
        for infoset in regret_table.keys():
            for action in regret_table[infoset].keys():
                total_timestep_regret += regret_table[infoset][action]

        # difference_cumulative_regrets = total_timestep_regret - previous_cumulative_regret
        # average_timestep_difference_regret = difference_cumulative_regrets / len(regret_table.keys())
        #
        # previous_cumulative_regret = total_timestep_regret

        regrets_history.append(total_timestep_regret)

    return regrets_history, strategy_table
