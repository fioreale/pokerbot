from working_tools.external_sampling import external_sampling


def solver(abstraction, time_horizon, num_of_players, root):
    regret_table = {}
    strategy_table = {}
    sigma_table = {}
    for level in abstraction:
        for infosets in level:
            for infoset in infosets.values():
                actions = list(infoset.info_nodes.values())[0].actions
                regret_actions = {}
                strategy_actions = {}
                sigma_actions = {}
                for action in actions:
                    regret_actions[action] = 0
                    strategy_actions[action] = 0
                    sigma_actions[action] = 1/len(actions)
                regret_table[infoset.name] = regret_actions
                strategy_table[infoset.name] = strategy_actions
                sigma_table[infoset.name] = sigma_actions

    utilities = []

    for t in range(time_horizon):
        for player in range(1, num_of_players + 1):
            utilities.append(external_sampling(abstraction, str(player), regret_table, strategy_table, sigma_table, root, 1))

    return utilities, strategy_table
