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
        self.pattern = {}

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
        :return: list of list of vertices describing the path if such a path exists else `NO`.
        """
        paths = []
        current_list = []
        return self._search(initial_vertex, observations, 0, current_list, paths)

    def _search(self, vertex, observations, current_index, current_list, paths):
        """
        :param vertex: current vertex being examined
        :param observations: {List(observations)} pattern of observations that need to be matched
            to the edges of the graph
        :param current_index: {int} index of the observation to be matched
        :param current_list: {List(vertex)} current list of path being examined
        :param paths: {List(paths)} stores all the paths that match the observation pattern
        :return: List of paths that match the pattern if there are paths else 'NO'.
        """

        # if the path being examined is a match add it to the `paths` list.
        if current_index == len(observations):
            current_list.append(vertex)
            paths.append(current_list)

            """
            memoization to store pattern for each vertex so that the next time this vertex is examined,
            we can come to know the observation pattern ahead of it and if it is a match,
            the vertex and it's children are not examined again.
            :example: if path [A, B, C, D] matches observation say [o1, o2, o3], then it is stored in the form,
            pattern = {
                'A': [[o1,o2,o3], [B, C, D]]
                'B': [[o2,o3], [C, D]]
                'C': [[o3], [D]]
            }
            """
            for i in range(0, len(observations)):
                self.pattern[current_list[i]] = [observations[i:], current_list[i:]]

            return current_list

        """
            checks if the current vertex is present in the pattern dict, if it is present and the observation pattern 
            till now + observation pattern that is stored for the vertex is a match to the pattern provided,  
            then adds it to 'path'
            :example: continuing from the example above, if vertex C is being examined,
            the observation till now is [o1,o2] and the path till now is,
            [A, D] then, we check in the pattern dict, and find that [o1,o2] + [o3] is a match to our pattern.
        """
        if vertex in self.pattern and observations[0: current_index] + self.pattern[vertex][0] == observations:
            current_list = current_list + self.pattern[vertex][1]
            paths.append(current_list)
            return current_list

        found_obs = False

        # recurses through the children to match pattern
        for connection, obs in self.adjacency_matrix[vertex].iteritems():
            if obs == observations[current_index]:
                found_obs = True
                current_list.append(vertex)
                result = self._search(connection, observations, current_index + 1, current_list, paths)
                current_list = []

                # if no pattern is found continues for children.
                if result == 'NO':
                    continue

        # if the pattern is not found returns `No`
        if not found_obs:
            return 'NO'

        return paths


if __name__  == "__main__":
    g = Graph([['A', 'B', 'o1'], ['B', 'D', 'o5'], ['C', 'D', 'o5'], ['D', 'E', 'o3'], ['A', 'C', 'o1'], ['C', 'B', 'o3'], ['B', 'A', 'o1']])
    print g.breadth_first_search('A', ['o1', 'o5', 'o3'])
