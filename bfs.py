import Queue


class Graph:

    def __init__(self, relation):
        """
        :param relation: relation is of the type [['A', 'B', 20],['C', 'D', 80]]
        which means A is directed to B and weight is 20,
        C is directed to D and weight is 80.
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
                self.adjacency_matrix[x[0]] = {x[1]: x[2]}
            else:
                self.adjacency_matrix[x[0]][x[1]] = x[2]
            if x[1] not in self.adjacency_matrix:
                self.adjacency_matrix[x[1]] = {}

    def breadth_first_search(self, initial_vertex, observations):
        """
            Performs breadth first search from the initial vertex to the rest of the graph
            to find the pattern of observations
        :param initial_vertex: vertex from where search starts.
        :param observations: pattern that needs to be matched.
        :return: list of vertices describing the path if such a path exists else `NO`.
        """

        current_list = []
        return self._search(initial_vertex, observations, 0, current_list)

    def _search(self, vertex, observations, current_index, current_list):
        if current_index == len(observations):
            current_list.append(vertex)
            return current_list

        found_obs = False
        for connection, obs in self.adjacency_matrix[vertex].iteritems():
            if obs == observations[current_index]:
                found_obs = True
                current_list.append(vertex)
                result = self._search(connection, observations, current_index + 1, current_list)
                if result == 'NO':
                    current_list = []
                    continue
                return result
        if not found_obs:
            return 'NO'


if __name__  == "__main__":
    g = Graph([['A', 'B', 'o1'], ['B', 'D', 'o5'], ['C', 'D', 'o2'], ['D', 'E', 'o3'], ['A', 'C', 'o1'], ['C', 'B', 'o3'], ['B', 'A', 'o1']])
    g.breadth_first_search('A', ['o1', 'o5', 'o3'])
