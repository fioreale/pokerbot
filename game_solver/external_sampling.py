from game_model.terminal_node import TerminalNode
from game_model.nature_node import NatureNode
import numpy as np


def external_sampling(abstraction, player, regret_table, strategy_table, sigma_table, root, probability):
    node = root

    if type(node) is TerminalNode:
        if probability == 0:
            return 0

        if player == '1':
            return node.payoffs[0]
            # / probability
        else:
            return node.payoffs[1]
            # / probability

    n_actions = len(node.actions)
    if type(node) is NatureNode:
        random_number = np.random.choice(n_actions)
        sampled_action_chance = node.actions[random_number]
        new_probability = probability * node.signals[sampled_action_chance]
        child = node.children['C:' + sampled_action_chance]
        return external_sampling(abstraction, player, regret_table, strategy_table, sigma_table,
                                 child, new_probability)

    infoset = infoset_finder(abstraction, node)

    infoset_name = infoset.name
    sigma_table[infoset_name] = regret_matching(regret_table, sigma_table, infoset_name, node.actions)

    if node.player == str(player):
        # initialization
        utilities_per_action = {}
        utility_sigma = 0

        for a in node.actions:
            child = node.children['P' + node.player + ':' + a]
            utilities_per_action[a] = external_sampling(abstraction, player, regret_table, strategy_table, sigma_table,
                                                        child, probability)
            utility_sigma += sigma_table[infoset_name][a] * utilities_per_action[a]

        r_tilde_plus = {}
        for a in node.actions:
            r_tilde_plus[infoset_name, a] = max(0, utilities_per_action[a] - utility_sigma)
            regret_table[infoset_name][a] += r_tilde_plus[infoset_name, a]

        return utility_sigma

    else:
        sampled_action_player = node.actions[np.random.choice(n_actions)]
        new_probability = probability * sigma_table[infoset_name][sampled_action_player]
        child = node.children['P' + node.player + ':' + sampled_action_player]
        utility = external_sampling(abstraction, player, regret_table, strategy_table, sigma_table,
                                    child, new_probability)

        for a in node.actions:
            strategy_table[infoset_name][a] += sigma_table[infoset_name][a]

        return utility


def regret_matching(regret_table, sigma_table, infoset_name, actions):
    tot_regret = 0
    for key, regret in regret_table[infoset_name].items():
        regret_table[infoset_name][key] = max(0, regret)
        tot_regret += regret_table[infoset_name][key]
    for action in actions:
        if tot_regret > 0:
            sigma_table[infoset_name][action] = max(0, regret_table[infoset_name][action]) / tot_regret
        else:
            sigma_table[infoset_name][action] = 1 / len(actions)
    return sigma_table[infoset_name]


def normalize_table(strategy_table):
    for infoset_name, strategies in strategy_table.items():
        tot_strategy = 0
        for strategy in strategies.values():
            tot_strategy += strategy
        if tot_strategy != 0:
            for strategy_name, strategy in strategy_table[infoset_name].items():
                strategy_table[infoset_name][strategy_name] = strategy / tot_strategy
    return strategy_table


def infoset_finder(abstraction, node):
    for infoset in abstraction:
        if node in infoset.info_nodes.values():
            return infoset
