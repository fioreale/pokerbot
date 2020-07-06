from sklearn.cluster import KMeans
import numpy as np

from tree_elements.info_set import InfoSet
from working_tools.abstraction_generator import tree_navigator


def k_means(cluster_table, perform_clusterization):

    kmeans_results_dict = {}

    # iterate over the cluster table history groups
    for history_group_name, history_group_dict in cluster_table.items():
        # build numpy array of centroids coordinates
        print('number of nodes:' + str(len(history_group_dict.keys())))
        if perform_clusterization:
            # number_of_clusters = int(np.floor(len(history_group_dict.keys()) / 2))
            # test
            number_of_clusters = int(np.ceil(len(history_group_dict.keys())/2))
        else:
            number_of_clusters = len(history_group_dict.keys())
        if number_of_clusters == 0:
            number_of_clusters = 1
        kmeans_input = []
        infoset_ordered_list = list()
        for infoset, infoset_payoff_vector in history_group_dict.items():
            infoset_ordered_list.append(infoset)
            for value in infoset_payoff_vector:
                kmeans_input = np.append(kmeans_input, value)
        # compute the K-Means of the centroids of the infoset clusters
        kmeans_input = kmeans_input.reshape(len(history_group_dict.keys()), -1)
        kmeans_results = KMeans(n_clusters=number_of_clusters, random_state=0).fit(kmeans_input)
        kmeans_ordered_list_couple = [infoset_ordered_list, kmeans_results]
        kmeans_results_dict[history_group_name] = kmeans_ordered_list_couple

        # for infoset in infoset_ordered_list:
        #     print(infoset.name, end=' ')
        # print(str(kmeans_results.labels_))

    # return the new kmeans clusters
    return kmeans_results_dict
