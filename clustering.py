from sklearn.cluster import KMeans
import numpy as np


def k_means(table, clusters):
    # utility list where we store the "coordinates" of the nodes to cluster
    utilities = []
    # nodes list where we store the nodes in the same order of the utilities list
    # in order to be able to achieve the node of the corresponding coordinates
    nodes = []
    # list of action where we save the distinct values of actions ordered to create the coordinates in the same order
    actions = []

    # cycle to create the list of ordered distinct values of actions
    for action, utility in table.keys():
        if action not in actions:
            actions.append(action)

    # here comes the deep shit written by luciano
    # cycle through the values of the dictionary which are list of nodes
    for node_list in table.values():
        # cycle through the nodes inside each list of the node lists
        for node in node_list:
            # list where to save the utilities ordered by action
            values = []
            # cycle through the ordered list of action to search the exact utility corresponding to that action
            for action_of_the_coordinate in actions:
                # cycle again through the dictionary to retrieve the utilities for the selected action
                for (action, utility), node_list_second in table.items():
                    # check if the action in the dictionary corresponds to the selected action
                    if action == action_of_the_coordinate:
                        # check if the node of the searched action corresponds to the action in the cycled dictionary
                        if node in node_list_second:
                            # then we append the utility value to the list where we save the coordinates
                            values.append(float(utility)/1000000)
            # the single coordinate has dimension equal to the number of actions that the player can do
            # dim[values] = dim[actions]
            # then we append the coordinate to the coordinate list
            utilities.append(values)
            # append the node of the corresponding coordinate just found to the nodes list in the same order
            nodes.append(node)

    # here we build a dictionary indexed for each infoset storing the list of nodes and coordinate values
    # in that infoset
    infosets = {}
    # cycle through the nodes
    for node_list in table.values():
        for node in node_list:
            # create list of two values = node object, utilities coordinates
            tuple_node_utilities = [None, None]
            tuple_node_utilities[0] = node
            tuple_node_utilities[1] = utilities[nodes.index(node)]
            # creation of a new entry in the dictionary and store the new value
            if node.infoSet.name not in infosets.keys():
                infosets[node.infoSet.name] = []
                infosets[node.infoSet.name].append(tuple_node_utilities)
            else:
                infosets[node.infoSet.name].append(tuple_node_utilities)

    # initialization of centroids structure = dictionary indexed by infoset object and storing the values
    # of the cluster coordinates
    centroids = {}
    # cycle through infosets dictionary
    for infoset in infosets.keys():
        # initialization of action_utilities list where we store the utilities of the single infoset
        actions_utilities = []
        # cycle through the dictionary to retrieve the utilities
        for tuple in infosets[infoset]:
            actions_utilities.append(tuple[1])
        # build numpy array of utilities for the infosets
        kmeans_input = np.asarray(actions_utilities)
        # call K-Means on the utilities for the single infoset
        kmeans = KMeans(n_clusters=1, random_state=0).fit(kmeans_input)
        # storing the cluster coordinates in the centroids dictionary
        centroids[infoset] = kmeans.cluster_centers_

    # list used to convert the centroids dictionary into an array
    centroids_values = []
    # cycle through the coordinates of centroids in the centroids dictionary
    for value in centroids.values():
        # conversion of values
        centroids_values.append((float(value[0][0]), float(value[0][1])))
    # build numpy array of centroids coordinates
    kmeans_input = np.asarray(centroids_values)
    # compute the K-Means of the centroids of the infoset clusters
    kmeans = KMeans(n_clusters=clusters, random_state=0).fit(kmeans_input)
    # return the coordinates of the new centroids
    return kmeans.cluster_centers_
