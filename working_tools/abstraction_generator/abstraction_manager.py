import operator

import working_tools.abstraction_generator.infosets_navigator
from tree_elements.info_set import InfoSet
from working_tools.abstraction_generator import clustering_manager
from working_tools.abstraction_generator import kmeans_calculator
from working_tools.abstraction_generator.percentage_wizard import PercentageWizard
import numpy as np


def create_abstraction(tree, player, infosets_length, abstraction_percentage):
    abstraction_set = []

    percentage_wizard = PercentageWizard(infosets_length, abstraction_percentage)

    infosets_list = working_tools.abstraction_generator.infosets_navigator.get_infosets_of_tree_level(tree, int(player))

    initial_level = infosets_list

    recursive_abstraction(initial_level, abstraction_set, percentage_wizard)

    return abstraction_set


def recursive_abstraction(infosets_list, abstraction_set, percentage_wizard):
    level = infosets_list[0].level

    cluster_table, strategies_list_dictionary = clustering_manager. \
        create_clustering_table(infosets_list, level)
    kmeans_dictionary_structure = kmeans_calculator.k_means(cluster_table, percentage_wizard.clusterization_start())
    clustered_infosets = group_infosets(kmeans_dictionary_structure)
    percentage_wizard.parsed_infosets += len(clustered_infosets)
    abstraction_set.extend(clustered_infosets)
    for infoset in clustered_infosets:
        descendant_infosets = working_tools.abstraction_generator.infosets_navigator.get_descendants(infoset)
        if len(descendant_infosets) != 0:
            descendants_by_level = {}
            for infoset_descendant in descendant_infosets:
                if infoset_descendant.level not in descendants_by_level.keys():
                    descendants_by_level[infoset_descendant.level] = [infoset_descendant]
                else:
                    descendants_by_level[infoset_descendant.level].append(infoset_descendant)
            for level in descendants_by_level.keys():
                recursive_abstraction(descendants_by_level[level], abstraction_set, percentage_wizard)

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
