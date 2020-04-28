from working_tools.abstraction_generator import tree_navigator
from working_tools.abstraction_generator import clustering_manager
from working_tools.abstraction_generator import kmeans_calculator


# initializes the cluster table. Graphic example: 'Abstraction Generation - slides.pdf' slide 7/67
# cluster table is a dictionary indexed by action and utility that where each value is a list of nodes
# Example: {[('c', '2.00000') : [<object ActionNode>, <object ActionNode>, <object ActionNode>]]}

def create_abstraction(tree, compressed_tree, number_of_clusters):

    height = tree_navigator.find_tree_height(tree, 0)

    for i in range(0, height):
        cluster_table = clustering_manager.create_clustering_table(tree, i)
        kmeans = kmeans_calculator.k_means(cluster_table, number_of_clusters)
        print('execute: ' + str(i))
        # compressed_tree.compress_tree(cluster_table, kmeans)

    return kmeans


def infoset_finder(abstraction, node):
    for level in abstraction:
        for infoset in level:
            if node in infoset.info_nodes.values():
                return infoset
