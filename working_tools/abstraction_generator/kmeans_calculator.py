from sklearn.cluster import KMeans
import numpy as np

from tree_elements.info_set import InfoSet


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
                            values_for_coordinates.append(float(utility_second_cycle) / 1000000)
            # the single coordinate has dimension equal to the number of actions that the player can do
            # dim[values] = dim[actions]
            # then we append the coordinate to the coordinate list
            utilities_coordinates_list.append(values_for_coordinates)
            # append the node of the corresponding coordinate just found to the nodes list in the same order
            node_ordered_list.append(current_node)

    # here we create a structure (type: list of lists) to simulate a dictionary and guarantee a deterministic order
    # between the elements
    # example:
    # infoset_dictionary = [['/C:J?', [[ActionNode, [-1.0, -2.0]], [ActionNode, [-1.0, -2.0]], ...],
    #                       ['/C:Q?', [[ActionNode, [-1.0, -2.0]], [ActionNode, [-1.0, -2.0]], ...],
    #                       ['/C:K?', [[ActionNode, [+1.0, +1.0]], [ActionNode, [+1.0, +1.0]], ...]]
    infosets_dictionary = list()
    # cycle through the cluster_table, which is indexed by (action, utility) and returns a list of nodes for each key
    for node_list in cluster_table.values():
        # cycle the node list
        for current_node in node_list:
            # create list of two values = node object, utilities coordinates
            couple_node_coordinates = [None, None]
            # save current node in the tuple
            couple_node_coordinates[0] = current_node
            # retrieve coordinates of the current node
            desired_utilities_coordinates = utilities_coordinates_list[node_ordered_list.index(current_node)]
            # save coordinates in the tuple
            couple_node_coordinates[1] = desired_utilities_coordinates

            # create a list of the infosets currently present in the infosets_dictionary
            # this list follows the order of appearance of the infoset in the dictionary and ensures that the
            # insertions below are done in the same order
            infosets_names = list()
            for infoset in infosets_dictionary:
                infosets_names.append(infoset[0])

            # if the current node in the cluster_table is part of an infoset NOT present in the infoset_dictionary
            if current_node.infoset.name not in infosets_names:
                # create an infoset_vector containing:
                #  - the name of the infoset
                #  - a list of tuples (Node, [utilities coordinates])
                infoset_vector = [current_node.infoset.name, list()]
                infoset_vector[1].append(couple_node_coordinates)
                # append the vector of the new infoset to the dictionary
                infosets_dictionary.append(infoset_vector)
            # else append the the tuple (Node, [utilities coordinates]) to the index corresponding to the position
            # of the infoset in the infoset_dictionary
            else:
                # the index is retrieved using the position of the infoset's name in the infosets_names vector
                infosets_dictionary[infosets_names.index(current_node.infoset.name)][1].append(couple_node_coordinates)

    # initialization of centroids structure = dictionary indexed by infoset object and storing the values
    # of the cluster coordinates
    centroids_dictionary = {}

    for infoset in infosets_dictionary:
        # initialization of action_utilities list where we store the utilities of the single infoset
        tuple_list = infoset[1]
        tuple_node_utilities = tuple_list[0]
        actions_utilities = np.array([tuple_node_utilities[1]])
        # storing the cluster coordinates in the centroids dictionary
        centroids_dictionary[infoset[0]] = actions_utilities

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
    infosets_names = list()

    # create a dictionary containing a new infoset for each cluster obtained from the K-means algorithm:
    # this infoset will contain the union of some old infosets
    # example of a new infoset: /C:J?+/C:Q?

    # the dictionary is indexed by a number in the set [0, number_of_clusters), according to the labels
    # returned by the K-means algorithm
    # example of labels returned by K-means: [0 0 1] --> the first two infosets are merged into one new infoset
    # placed at index 0 in the grouped_infosets dictionary
    for i in range(0, number_of_clusters):
        grouped_infosets[i] = InfoSet()
        infosets_names.append('')

    # cycle to assign the old infosets to the grouped_infosets dictionary

    # initialize an index to keep track of the position in the kmeans.labels_ vector
    infoset_position = 0
    # cycle the kmeans.labels_ vector
    for cluster_index in kmeans.labels_:
        # cycle the list of tuples (Node, [utility1, utility2]) in the infosets_dictionary corresponding to
        # the infoset that we are cycling in the kmeans.labels_ vector
        for node_and_utilities in infosets_dictionary[infoset_position][1]:
            # join the history of the node (type: list) into a string separated by '/'
            node_name = '/' + '/'.join(map(str, node_and_utilities[0].history))
            # add the node (first element in the node_and_utilities vector) to the info_nodes
            # dictionary of the new grouped infoset
            # the index in the grouped infosets depends on the cluster_index returned by kmeans.labels_
            # example: kmeans.labels_ = [0 0 1] and the current cluster_index = 0 --> we assign the node to
            # the grouped_infoset[0]
            grouped_infosets[cluster_index].info_nodes[node_name] = node_and_utilities[0]
        # update the infoset position to keep track of the index in the kmeans.labels_ vector
        infoset_position += 1

    # generate a name to the new grouped infosets
    # the convention that we chose was to concatenate the names of the infosets with a '+' as a separator
    # example: old infosets names = {'/C:J?', '/C:Q?'} --> new name = '/C:J?+/C:Q?'
    # cycle again the kmeans.labels_ vector, keeping track of the position with the infoset_position index
    infoset_position = 0
    for cluster_index in kmeans.labels_:
        # add a '+' in the name, if the string that we are building already contains an infoset's name
        if infosets_names[cluster_index] != '':
            infosets_names[cluster_index] += '+'
        # add the name of the infoset (contained in infosets_dictionary[infoset_position][0]) to the string
        # that we are building
        infosets_names[cluster_index] += infosets_dictionary[infoset_position][0]
        # update the infoset position to keep track of the index in the kmeans.labels_ vector
        infoset_position += 1

    # cycle to assign the names to the new infosets
    index = 0
    for infoset_key in sorted(grouped_infosets.keys()):
        grouped_infosets[infoset_key].name = infosets_names[index]
        index += 1

    # return the new grouped_infosets
    return grouped_infosets
