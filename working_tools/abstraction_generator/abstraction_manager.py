from working_tools.abstraction_generator import tree_navigator
from working_tools.abstraction_generator import clustering_manager
from working_tools.abstraction_generator import kmeans_calculator
from tree_elements.action_node import ActionNode


# initializes the cluster table. Graphic example: 'Abstraction Generation - slides.pdf' slide 7/67
# cluster table is a dictionary indexed by action and utility that where each value is a list of nodes
# Example: {[('c', '2.00000') : [<object ActionNode>, <object ActionNode>, <object ActionNode>]]}

def create_abstraction(tree, clusters):
    height = tree_navigator.find_tree_height(tree, 0)
    infosets_abstraction = list()
    for i in range(0, height):
        infosets_abstraction.append(list())

        current_tree_level = tree_navigator.get_tree_level(tree, i)

        filtered_level = []
        for node in current_tree_level:
            if isinstance(node, ActionNode):
                filtered_level += [node]

        if len(filtered_level) > 0:
            organized_level = tree_navigator.split_node_list(filtered_level)

            for node_list in organized_level:
                cluster_table = clustering_manager.create_clustering_table_new(node_list)
                # prints the cluster table using matplotlib
                # clustering_manager.print_cluster_table(cluster_table)

                # computes the K-Means estimation of the node clusters,given some node clusters
                # placed in the space of utilities
                # it computes some centroids of the most likely clusters of node clusters
                kmeans = kmeans_calculator.k_means(cluster_table, clusters)
                infosets_abstraction[i].extend(kmeans)

    return infosets_abstraction


def infoset_finder(abstraction, node):
    for level in abstraction:
        for infoset in level:
            if node in infoset.info_nodes.values():
                return infoset
