import logging

from working_tools.abstraction_generator import tree_navigator
from working_tools.abstraction_generator import clustering_manager
from working_tools.abstraction_generator import kmeans_calculator


# initializes the cluster table. Graphic example: 'Abstraction Generation - slides.pdf' slide 7/67

def create_abstraction(tree, compressed_tree, number_of_clusters):

    height = tree_navigator.find_tree_height(tree, 0)

    for i in range(3, height):
        print('computing cluster table level: ' + str(i))

        cluster_table, strategies_list_dictionary = clustering_manager.create_clustering_table(tree, i)

        kmeans = kmeans_calculator.k_means(cluster_table, number_of_clusters)

        print('executed level: ' + str(i))

        compressed_tree.compress_tree(kmeans, strategies_list_dictionary)

    return compressed_tree


def infoset_finder(abstraction, node):
    for level in abstraction:
        for infoset in level:
            if node in infoset.info_nodes.values():
                return infoset
