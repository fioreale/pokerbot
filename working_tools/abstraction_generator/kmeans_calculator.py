from sklearn.cluster import KMeans
import numpy as np

from tree_elements.info_set import InfoSet
from working_tools.abstraction_generator import tree_navigator


def k_means(cluster_table, number_of_clusters):

    kmeans_results_dict = {}

    # iterate over the cluster table history groups
    for history_group_name, history_group_dict in cluster_table.items():
        # build numpy array of centroids coordinates
        kmeans_input = []
        for infoset in history_group_dict.values():
            for value in infoset:
                kmeans_input = np.append(kmeans_input, value)
        # compute the K-Means of the centroids of the infoset clusters
        kmeans_input = kmeans_input.reshape(len(history_group_dict.keys()), -1)
        kmeans_results_dict[history_group_name] = KMeans(n_clusters=number_of_clusters, random_state=0).fit(kmeans_input)
        for infoset in history_group_dict.keys():
            print(infoset.name, end=' ')
        print(str(kmeans_results_dict[history_group_name].labels_))

    # return the new kmeans clusters
    return kmeans_results_dict
