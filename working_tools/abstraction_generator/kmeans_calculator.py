from sklearn.cluster import KMeans
import numpy as np

from tree_elements.info_set import InfoSet
from working_tools.abstraction_generator import tree_navigator


def k_means(cluster_table, number_of_clusters):

    kmeans_results_dict = {}

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
        # return the coordinates of the new centroids

    # grouped_infosets = []
    #
    # # create a vector containing a new infoset for each cluster obtained from the K-means algorithm:
    # # this infoset will contain the union of some old infosets
    # # example of a new infoset: /C:J?+/C:Q?
    #
    # # the vector has a number of elements equal to [number_of_clusters], according to the labels
    # # returned by the K-means algorithm
    # # example of labels returned by K-means: [0 0 1] --> the first two infosets are merged into one new infoset
    # # placed at index 0 in the grouped_infosets vector
    # for i in range(0, number_of_clusters):
    #     grouped_infosets.append(InfoSet())
    #
    # # cycle to assign the old infosets to the grouped_infosets vector
    #
    # # initialize an index to keep track of the position in the kmeans.labels_ vector
    # infoset_position = 0
    # # cycle the kmeans.labels_ vector
    # for cluster_index in kmeans.labels_:
    #     # retrieve the desired infoset in the cluster table accordingly to the infoset_position
    #     desired_infoset = list(cluster_table.keys())[infoset_position]
    #     # add the infoset nodes to the infoset in the grouped_infoset structure
    #     grouped_infosets[cluster_index].info_nodes.update(desired_infoset.info_nodes)
    #     # update the name of the new infoset
    #     if grouped_infosets[cluster_index].name is None:
    #         grouped_infosets[cluster_index].name = desired_infoset.name
    #     else:
    #         grouped_infosets[cluster_index].name += '+' + desired_infoset.name
    #     # update the infoset position to keep track of the index in the kmeans.labels_ vector
    #     infoset_position += 1

    # return the new grouped_infosets
    return kmeans_results_dict
