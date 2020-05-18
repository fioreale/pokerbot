def apply_strategies_to_nodes(abstraction_set, strategy_table):
    # iterate over the abstracted infosets
    for abstracted_infoset in abstraction_set:
        # store the strategies dictionary of the abstracted infoset
        strategies_of_infoset = strategy_table[abstracted_infoset.name]
        # iterate over all the nodes of the abstracted infosets
        for node in abstracted_infoset.info_nodes.values():
            # iterate over all the actions of the node
            for action in node.actions:
                # store the corresponding probability to the list of strategies of the node
                node.strategies_probabilities.append(strategies_of_infoset[action])
