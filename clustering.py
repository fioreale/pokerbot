from sklearn.cluster import KMeans
import numpy as np

from tree_elements.infoStructure import InfoStructure
from utilities import clustering_table_creation


def k_means(table, clusters):
    utilities = []
    nodes = []

    for (action, utility), node_list in table.items():
        for node in node_list:
            values = []
            for (action, utility), node_list in table.items():
                if node in node_list:
                    values.append(utility)
            utilities.append(values)
            nodes.append(node)

    infosets = {}
    for node_list in table.values():
        for node in node_list:
            tuple_node_utilities = [None, None]
            tuple_node_utilities[0] = node
            tuple_node_utilities[1] = utilities[nodes.index(node)]
            if node.infoSet.name not in infosets.keys():
                infosets[node.infoSet.name] = []
                infosets[node.infoSet.name].append(tuple_node_utilities)
            else:
                infosets[node.infoSet.name].append(tuple_node_utilities)

    centroids = {}
    for infoset in infosets.keys():
        actions_utilities = []
        for tuple in infosets[infoset]:
            actions_utilities.append(tuple[1])
        kmeans_input = np.asarray(actions_utilities)
        kmeans = KMeans(n_clusters=1, random_state=0).fit(kmeans_input)
        centroids[infoset.name] = kmeans.cluster_centers_

    kmeans_input = np.asarray(centroids.values())
    kmeans = KMeans(n_clusters=clusters, random_state=0).fit(kmeans_input)

    return kmeans.cluster_centers_
