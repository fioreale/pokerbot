from sklearn.cluster import KMeans
import numpy as np

from tree_elements.info_set import InfoSet


def k_means(cluster_table, number_of_clusters):

    # build numpy array of centroids coordinates
    kmeans_input = np.asarray(list(cluster_table.values()))
    # compute the K-Means of the centroids of the infoset clusters
    kmeans = KMeans(n_clusters=number_of_clusters, random_state=0).fit(kmeans_input)
    # return the coordinates of the new centroids

    grouped_infosets = []

    # create a vector containing a new infoset for each cluster obtained from the K-means algorithm:
    # this infoset will contain the union of some old infosets
    # example of a new infoset: /C:J?+/C:Q?

    # the vector has a number of elements equal to [number_of_clusters], according to the labels
    # returned by the K-means algorithm
    # example of labels returned by K-means: [0 0 1] --> the first two infosets are merged into one new infoset
    # placed at index 0 in the grouped_infosets vector
    for i in range(0, number_of_clusters):
        grouped_infosets.append(InfoSet())

    # cycle to assign the old infosets to the grouped_infosets vector

    # initialize an index to keep track of the position in the kmeans.labels_ vector
    infoset_position = 0
    # cycle the kmeans.labels_ vector
    for cluster_index in kmeans.labels_:
        desired_infoset = list(cluster_table.keys())[infoset_position]
        grouped_infosets[cluster_index].info_nodes.update(desired_infoset.info_nodes)
        if grouped_infosets[cluster_index].name is None:
            grouped_infosets[cluster_index].name=desired_infoset.name
        else:
            grouped_infosets[cluster_index].name+= '+' + desired_infoset.name
        # update the infoset position to keep track of the index in the kmeans.labels_ vector
        infoset_position += 1

    # return the new grouped_infosets
    return grouped_infosets
