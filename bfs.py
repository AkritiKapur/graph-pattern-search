import Queue


class Graph:

    def __init__(self, relation):
        """
        :param relation: relation is of the type [['A', 'B', 20, 0.5],['C', 'D', 80, 0.2]]
        which means A is directed to B and weight is 20, and the probability of edge AB is 0.5
        C is directed to D and weight is 80, probability of edge CD is 0.2
        """
        self.adjacency_matrix = {}
        self._get_adjacency_matrix(relation)

    def _get_adjacency_matrix(self, relation):
        """
        Gets adjacency matrix for the Graph object.
        :param relation: relation is of the type [['A', 'B', 20],['C', 'D', 80]]
        which means A is directed to B and weight is 20,
        C is directed to D and weight is 80.
        """
        for x in relation:
            if x[0] not in self.adjacency_matrix:
                self.adjacency_matrix[x[0]] = {x[1]: [x[2], x[3]]}
            else:
                self.adjacency_matrix[x[0]][x[1]] = [x[2], x[3]]
            if x[1] not in self.adjacency_matrix:
                self.adjacency_matrix[x[1]] = {}

    def breadth_first_search(self, initial_vertex, observations):
        """
            Performs breadth first search from the initial vertex to the rest of the graph
            to find the pattern of observations with the highest probability
        :param initial_vertex: vertex from where search starts.
        :param observations: pattern that needs to be matched.
        :return: list of vertices describing the path if such a path exists else `NO`.
        """

        current_list = []
        most_probable_path = []
        max_probability = 0
        current_probability = 0
        most_probable_path, _ = self._search(initial_vertex, observations, 0, current_list,
                                             most_probable_path, current_probability, max_probability)
        return most_probable_path

    def _search(self, vertex, observations, current_index, current_list, most_probable_path,
                current_probability, max_probability):
        """
        :param vertex: current vertex being examined
        :param observations: {List(observations)} pattern of observations that need to be matched
            to the edges of the graph
        :param current_index: {int} index of the observation to be matched
        :param current_list: {List(vertex)} current list of path being examined
        :param most_probable_path: {List(vertex)} most probable path till now
        :param current_probability: the current probability of the path edges currently being examined.
        :param max_probability: maximum probability of the sequence occuring till now.
        :return: most probable path and it's probability if a path is found else returns NO.
        """
        if current_index == len(observations):
            # if path is a match to the pattern of observations,
            # then compare it's probability and check if it is the most probable path.
            current_list.append(vertex)
            if current_probability > max_probability:
                max_probability = current_probability
                most_probable_path = current_list
            return most_probable_path, max_probability

        found_obs = False

        # check for all children of the current vertex if they match the observation
        # currently being examined.
        for connection, obs in self.adjacency_matrix[vertex].iteritems():
            if obs[0] == observations[current_index]:

                found_obs = True
                current_list.append(vertex)

                # update the probability of the path.
                current_probability += obs[1]
                most_probable_path, max_probability = self._search(connection, observations, current_index + 1,
                                                                   current_list, most_probable_path,
                                                                   current_probability, max_probability)

                # reinitialize variables for new paths to be discovered.
                current_probability = 0
                current_list = []

                # if the path is not a match then check for the next child.
                if max_probability == 'NO':
                    continue

        # if no match is found
        if not found_obs:
            return 'NO', 'NO'

        return most_probable_path, max_probability


if __name__  == "__main__":
    g = Graph([['A', 'B', 'o1', 0.9], ['B', 'D', 'o5', 0.8], ['C', 'D', 'o5', 1], ['D', 'E', 'o3', 0.5],
               ['A', 'C', 'o1', 0.1], ['C', 'B', 'o3', 0.5], ['B', 'A', 'o1', 0.5]])
    print g.breadth_first_search('A', ['o1', 'o9', 'o3'])
