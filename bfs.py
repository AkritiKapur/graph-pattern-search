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

        return self._dp_search(initial_vertex, observations, 0)['pattern']

    def _dp_search(self, vertex, observation, current_index):

        # if the observation is a match returns the end vertice of the match.
        # for example, for observations - o1,o2,o3 and edges A, B, C, D returns D
        if current_index == len(observation):
            return {'pattern': vertex, 'max_probability': 0}

        # if the vertex already exists in the dictionary with the observation pattern needed,
        # does not traverse the children instead returns the value.
        # for example: For observation pattern: o1, o2, o3 and vertex D ,
        # suppose two paths exist from D, DF with 0.5 and DE with 0.2 then DF is stored in the dictionary.
        # pattern = {'D': {'o3': ['pattern': 'DF', 'max_probability': 0.5]}}
        if vertex in self.pattern and ','.join(observation[current_index:]) in self.pattern[vertex]:
            return self.pattern[vertex][','.join(observation[current_index:])]

        # if vertex does not exist in pattern dictionary, creates a key for vertex.
        if vertex not in self.pattern:
            self.pattern[vertex] = {','.join(observation[current_index:]): {'pattern': '', 'max_probability': 0}}

        found_obs = False
        result = 'NO'

        # recurses through the children to find the pattern.
        for connection, obs in self.adjacency_matrix[vertex].iteritems():
            if obs[0] == observation[current_index]:
                found_obs = True
                result = self._dp_search(connection, observation, current_index+1)

                if result == 'NO':
                    continue

                current_probability = self.pattern[vertex][','.join(observation[current_index:])]['max_probability']

                # creates pattern dictionary in the form described above.
                if result != 'NO':
                    if current_probability == 0:
                        self.pattern[vertex][','.join(observation[current_index:])]['max_probability'] = obs[1]
                        self.pattern[vertex][','.join(observation[current_index:])]['pattern'] = vertex + result['pattern']
                    elif current_probability < obs[1]:
                        self.pattern[vertex][','.join(observation[current_index:])]['max_probability'] = \
                            obs[1] if result['max_probability'] == 0 else obs[1] * result['max_probability']
                        self.pattern[vertex][','.join(observation[current_index:])]['pattern'] = vertex + result['pattern']

        # if the pattern is not found returns `No`
        if not found_obs or result == 'NO':
            return 'NO'

        return self.pattern[vertex][','.join(observation[current_index:])]


if __name__  == "__main__":
    g = Graph([['A', 'B', 'o1', 0.9], ['B', 'D', 'o5', 0.8], ['C', 'D', 'o5', 1], ['D', 'E', 'o3', 0.5],
               ['A', 'C', 'o1', 0.1], ['C', 'B', 'o3', 0.5], ['B', 'A', 'o1', 0.5], ['D', 'F', 'o3', 0.2],
               ['D', 'E', 'o3', 0.5]])
    print g.breadth_first_search('A', ['o1', 'o5', 'o3'])
