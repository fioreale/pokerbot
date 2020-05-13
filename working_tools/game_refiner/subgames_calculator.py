from working_tools.abstraction_generator.tree_navigator import get_infosets_of_tree_level


def subgame_calculator(tree, level):
    infosets_of_the_level = get_infosets_of_tree_level(tree, level)

    subgames_list = []

    for infoset in infosets_of_the_level:
        if not subgames_list:
            subgames_list.append([infoset])
        else:
            subgames_infoset_list = [infoset]
            for node in infoset.info_nodes.values():
                for child in node.children.values():
                    for node_infoset_sibling in child.infoset.info_nodes.values():
                        if node_infoset_sibling.parent.infoset not in subgames_infoset_list:
                            subgames_infoset_list.append(node_infoset_sibling.parent.infoset)

    return subgames_list
