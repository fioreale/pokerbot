import os

from working_tools import input_file_parser
from working_tools import tree_visualizer
from working_tools import clustering_manager
from working_tools import kmeans_calculator

if __name__ == '__main__':

    # tree will be the root node of the entire tree
    # parse the file to compute the tree structure
    tree = input_file_parser.parse_tree(os.path.join(os.getcwd(), 'inputs', 'leduc5.txt'))

    # info_sets will contain the complete infostructure of the game
    # parse_infoset reads the file and returns the infostructure
    info_sets = input_file_parser.parse_infoset(os.path.join(os.getcwd(), 'inputs', 'leduc5.txt'), tree)

    # visualize the game tree
    tree_visualizer.visualize_game_tree(tree, 0)

    # visualize the infostructure of the tree
    # tree_visualizer.visualize_info_structure(tree, info_sets)

    # initializes the cluster table. Graphic example: 'Abstraction Generation - slides.pdf' slide 7/67
    # cluster table is a dictionary indexed by action and utility that where each value is a list of nodes
    # Example: {[('c', '2.00000') : [<object ActionNode>, <object ActionNode>, <object ActionNode>]]}

    cluster_table = clustering_manager.create_clustering_table(tree.children.values())
    # prints the cluster table using pyplot
    clustering_manager.print_cluster_table(cluster_table)

    # computes the K-Means estimation of the node clusters, given some node clusters placed in the space of utilities
    # it computes some centroids of the most likely clusters of node clusters
    kmeans_calculator.k_means(cluster_table, 3)
