import random

from tree_elements.terminal_node import  TerminalNode
from tree_elements.nature_node import NatureNode

def external_sampling(abstraction, history, player, regret_table, cumulative_table, root)
    node = root.node_finder(history)


    if type(node) is TerminalNode:
        return node.utilities[player]

    n_actions = len(node.actions) - 1
    if type(node) is NatureNode:
        sampled_action_chance = node.actions[random.randint(0,n_actions)]
        return external_sampling(abstraction, history + str('P' + player + ':' + sampled_action_chance), player, regret_table, cumulative_table, root)

    infoset = []  # TODO information set to find within abstraction

    # from strategy = {}
    strategy[infoset] = RegretMatching(regret_table[infoset])

    if node.player == player:
        u_sigma = 0
        utilities_per_action = {}

        # initialization
        for a in node.actions:
            utilities_per_action[a] = 0

        for a in node.actions:
            utilities_per_action[a] = external_sampling(abstraction,history + str('P' + player + ':' + a), player, regret_table, cumulative_table, root)
            u_sigma += strategy[infoset, a] * utilities_per_action[a]

        for a in node.actions:
            r_tilde[infoset, a] = utilities_per_action[a] - u_sigma
            regret_table[a] += r_tilde[infoset, a]

        return u_sigma

    else:
        sampled_action_player = node.actions[random.randint(0, n_actions)]
        utility = external_sampling(abstraction, history + str('P' + player + ':' + sampled_action_player), player, regret_table, cumulative_table, root)

        for a in node.actions:
            cumulative_table[infoset, a] += strategy[infoset, a]
        return utility