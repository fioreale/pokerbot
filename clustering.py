from sklearn.cluster import KMeans
import numpy as np


def k_means(table, clusters):
    utilities = []
    nodes = []
    actions = []

    for action, utility in table.keys():
        if action not in actions:
            actions.append(action)

    for node_list in table.values():
        for node in node_list:
            values = []
            for action_of_the_coordinate in actions:
                for (action, utility), node_list_second in table.items():
                    if action == action_of_the_coordinate:
                        if node in node_list_second:
                            values.append(float(utility)/1000000)
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
        centroids[infoset] = kmeans.cluster_centers_

    centroids_values = []
    print(centroids.values())
    for value in centroids.values():
        centroids_values.append((float(value[0][0]), float(value[0][1])))
    kmeans_input = np.asarray(centroids_values)
    print(kmeans_input)
    kmeans = KMeans(n_clusters=clusters, random_state=0).fit(kmeans_input)
    print(kmeans.cluster_centers_)
    return kmeans.cluster_centers_
