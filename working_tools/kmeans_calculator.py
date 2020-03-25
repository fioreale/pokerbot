from sklearn.cluster import KMeans
import numpy as np

from tree_elements.infoset import InfoSet


def k_means(cluster_table, number_of_clusters):
    # utility list where we store the "coordinates" of the nodes to cluster
    utilities_coordinates_list = []
    # nodes list where we store the nodes in the same order of the utilities list
    # in order to be able to achieve the node of the corresponding coordinates
    node_ordered_list = []
    # list of action where we save the distinct values of actions ordered to create the coordinates in the same order
    distinct_actions_order = []

    # cycle to create the list of ordered distinct values of actions
    for action, utility in cluster_table.keys():
        if action not in distinct_actions_order:
            distinct_actions_order.append(action)

    # here comes the deep shit written by luciano
    # cycle through the values of the dictionary which are list of nodes
    for node_list in cluster_table.values():
        # cycle through the nodes inside each list of the node lists
        for current_node in node_list:
            # list where to save the utilities ordered by action
            values_for_coordinates = []
            # cycle through the ordered list of action to search the exact utility corresponding to that action
            for single_action_from_order in distinct_actions_order:
                # cycle again through the dictionary to retrieve the utilities for the selected action
                for (action_second_cycle, utility_second_cycle), node_list_second_cycle in cluster_table.items():
                    # check if the action in the dictionary corresponds to the selected action
                    if action_second_cycle == single_action_from_order:
                        # check if the node of the searched action corresponds to the action in the cycled dictionary
                        if current_node in node_list_second_cycle:
                            # then we append the utility value to the list where we save the coordinates
                            values_for_coordinates.append(float(utility_second_cycle)/1000000)
            # the single coordinate has dimension equal to the number of actions that the player can do
            # dim[values] = dim[actions]
            # then we append the coordinate to the coordinate list
            utilities_coordinates_list.append(values_for_coordinates)
            # append the node of the corresponding coordinate just found to the nodes list in the same order
            node_ordered_list.append(current_node)

    # here we build a dictionary indexed for each infoset storing the list of nodes and coordinate values
    # in that infoset
    infosets_dictionary = {}
    # cycle through the nodes
    for node_list in cluster_table.values():
        for current_node in node_list:
            # create list of two values = node object, utilities coordinates
            couple_node_coordinates = [None, None]
            # save current node in the tuple
            couple_node_coordinates[0] = current_node
            # retrieve coordinates of the current node
            desired_utilities_coordinates = utilities_coordinates_list[node_ordered_list.index(current_node)]
            # save coordinates in the tuple
            couple_node_coordinates[1] = desired_utilities_coordinates
            # creation of a new entry in the dictionary and store the new value
            if current_node.infoset.name not in infosets_dictionary.keys():
                infosets_dictionary[current_node.infoset.name] = []
                infosets_dictionary[current_node.infoset.name].append(couple_node_coordinates)
            else:
                infosets_dictionary[current_node.infoset.name].append(couple_node_coordinates)

    # initialization of centroids structure = dictionary indexed by infoset object and storing the values
    # of the cluster coordinates
    centroids_dictionary = {}
    # cycle through infosets dictionary
    for infoset in infosets_dictionary.keys():
        # initialization of action_utilities list where we store the utilities of the single infoset
        actions_utilities = []
        # cycle through the dictionary to retrieve the utilities
        for node_coordinates_couple in infosets_dictionary[infoset]:
            actions_utilities.append(node_coordinates_couple[1])
        # build numpy array of utilities for the infosets
        kmeans_input = np.asarray(actions_utilities)
        # call K-Means on the utilities for the single infoset
        kmeans = KMeans(n_clusters=1, random_state=0).fit(kmeans_input)
        # storing the cluster coordinates in the centroids dictionary
        centroids_dictionary[infoset] = kmeans.cluster_centers_

    # list used to convert the centroids dictionary into an array
    centroids_values = []
    # cycle through the coordinates of centroids in the centroids dictionary
    for value in centroids_dictionary.values():
        # conversion of values
        centroids_values.append((float(value[0][0]), float(value[0][1])))
    # build numpy array of centroids coordinates
    kmeans_input = np.asarray(centroids_values)
    # compute the K-Means of the centroids of the infoset clusters
    kmeans = KMeans(n_clusters=number_of_clusters, random_state=0).fit(kmeans_input)
    # return the coordinates of the new centroids

    grouped_infosets = {}
    infosets_names = []

    for i in range(0, number_of_clusters):
        grouped_infosets[i] = InfoSet()
        infosets_names.append([])


    infoset_position = 0
    for cluster_index in kmeans.labels_:
        for node_and_utilities in infosets_dictionary[list(infosets_dictionary.keys())[infoset_position]]:
            node_name = '/' + '/'.join(map(str, node_and_utilities[0].history))
            grouped_infosets[cluster_index].info_nodes[node_name] = node_and_utilities[0]
        infoset_position += 1

    infoset_position = 0

    for cluster_index in kmeans.labels_:
        infosets_names[cluster_index] += list(infosets_dictionary.keys())[infoset_position]
        infoset_position += 1

    index = 0
    for new_infoset in grouped_infosets.values():
        new_infoset.name = infosets_names[index]
        index += 1

    print('dati')
    for infoset in grouped_infosets.values():
        print(infoset.info_nodes)
        print(infoset.name)

    return kmeans.cluster_centers_
