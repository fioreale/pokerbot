import operator

import game_abstraction.infosets_navigator
from game_model.info_set import InfoSet
from game_abstraction import clustering_manager, kmeans_calculator
import numpy as np
from game_abstraction.percentage_wizard import PercentageWizard


def create_abstraction(tree, player, total_number_of_infosets, percentage, wizard_coefficient):
    abstraction_set = []

    percentage_wizard = PercentageWizard(total_number_of_infosets, percentage, wizard_coefficient)

    infosets_list = game_abstraction.infosets_navigator.get_infosets_of_tree_level(tree, int(player))

    initial_level = infosets_list

    recursive_abstraction(initial_level, abstraction_set, percentage_wizard)

    return abstraction_set


def recursive_abstraction(infosets_list, abstraction_set, percentage_wizard):
    level = infosets_list[0].level

    cluster_table, strategies_list_dictionary = clustering_manager. \
        create_clustering_table(infosets_list, level)
    kmeans_dictionary_structure = kmeans_calculator.k_means(cluster_table, percentage_wizard)
    clustered_infosets = group_infosets(kmeans_dictionary_structure)
    abstraction_set.extend(clustered_infosets)
    for infoset in clustered_infosets:
        descendant_infosets = game_abstraction.infosets_navigator.get_descendants(infoset)
        if len(descendant_infosets) != 0:
            descendants_by_level = {}
            for infoset in descendant_infosets:
                if infoset.level not in descendants_by_level.keys():
                    descendants_by_level[infoset.level] = [infoset]
                else:
                    descendants_by_level[infoset.level].append(infoset)
            for level in descendants_by_level.keys():
                recursive_abstraction(descendants_by_level[level], abstraction_set, percentage_wizard)


    # print('executed level: ' + str(1))
    #
    # # CLUSTERING LEVEL 2
    # print('computing cluster table level: ' + str(2))
    # infosets_list = tree_navigator.get_infosets_of_tree_level(tree, 2)
    # cluster_table, strategies_list_dictionary = clustering_manager.create_clustering_table(infosets_list, 2)
    #
    # kmeans_dictionary_structure = kmeans_calculator.k_means(cluster_table)
    # grouped_level = group_infosets(kmeans_dictionary_structure)
    # abstraction_set.append(grouped_level)
    # print('executed level: ' + str(2))
    #
    # # CLUSTERING LEVEL 3
    # level_3_infosets = []
    # for infoset in abstraction_set[0]:
    #     descendant_infosets = []
    #     for node in infoset.info_nodes.values():
    #         descendant_infosets.extend(get_infosets_of_tree_level(node, 2))
    #     descendant_infosets = set(descendant_infosets)
    #
    #     cluster_table, strategies_list_dictionary = clustering_manager.create_clustering_table(descendant_infosets, 3)
    #     kmeans_dictionary_structure = kmeans_calculator.k_means(cluster_table)
    #     grouped_level = group_infosets(kmeans_dictionary_structure)
    #     level_3_infosets.extend(grouped_level)
    # abstraction_set.append(level_3_infosets)
    #
    # # CLUSTERING LEVEL 4
    # level_4_infosets = []
    # for infoset in abstraction_set[0]:
    #     descendant_infosets = []
    #     for node in infoset.info_nodes.values():
    #         descendant_infosets.extend(get_infosets_of_tree_level(node, 3))
    #     descendant_infosets = set(descendant_infosets)
    #
    #     cluster_table, strategies_list_dictionary = clustering_manager.create_clustering_table(descendant_infosets, 4)
    #     kmeans_dictionary_structure = kmeans_calculator.k_means(cluster_table)
    #     grouped_level = group_infosets(kmeans_dictionary_structure)
    #     level_4_infosets.extend(grouped_level)
    # abstraction_set.append(level_3_infosets)
    #
    # for infoset in abstraction_set[1]:
    #     descendant_infosets = []
    #     for node in infoset.info_nodes.values():
    #         descendant_infosets.extend(get_infosets_of_tree_level(node, 2))
    #     descendant_infosets = set(descendant_infosets)
    #
    #     cluster_table, strategies_list_dictionary = clustering_manager.create_clustering_table(descendant_infosets, 4)
    #     kmeans_dictionary_structure = kmeans_calculator.k_means(cluster_table)
    #     grouped_level = group_infosets(kmeans_dictionary_structure)
    #     level_4_infosets.extend(grouped_level)
    # abstraction_set.append(level_3_infosets)

    return abstraction_set


def group_infosets(kmeans_dictionary_structure):
    infoset_level = []
    for history_group in kmeans_dictionary_structure.values():
        infoset_ordered_list = history_group[0]
        kmeans = history_group[1]
        for kmeans_label in set(kmeans.labels_):
            same_label_infosets_indexes = np.argwhere(kmeans.labels_ == kmeans_label)
            # group all infosets with same labels
            same_label_infosets_ndarray = np.array(infoset_ordered_list)[same_label_infosets_indexes].flatten()
            same_label_infosets_list = same_label_infosets_ndarray.tolist()
            new_infoset = InfoSet()
            new_infoset.name = ''
            new_infoset.level = same_label_infosets_list[0].level
            for infoset in sorted(same_label_infosets_list, key=operator.attrgetter('name')):
                new_infoset.info_nodes.update(infoset.info_nodes)
                if new_infoset.name == '':
                    new_infoset.name = infoset.name
                else:
                    new_infoset.name += '+' + infoset.name
            infoset_level.append(new_infoset)
    return infoset_level
