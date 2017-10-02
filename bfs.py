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
    return self._dp_search(initial_vertex, observations, 0)

def _dp_search(self, vertex, observation, current_index):

    # if the observation is a match returns the end vertice of the match.
    # for example, for observations - o1,o2,o3 and edges A, B, C, D returns D
    if current_index == len(observation):
        return [vertex]

    # if the vertex already exists in the dictionary with the observation pattern needed,
    # does not traverse the children instead returns the value.
    # exmaple : pattern = { 'A':
    if vertex in self.pattern and ','.join(observation[current_index:]) in self.pattern[vertex]:
        return self.pattern[vertex][','.join(observation[current_index:])]

    # if vertex does not exist in pattern dictionary, creates a key for vertex.
    # for example: For observation pattern: o1, o2, o3 and vertex A (initial vertex),
    # pattern = {'A': {'o1,o5,o3': ['ACDE', 'ACDF', 'ABDE', 'ABDF']},
    #            'C': {'o5,o3': ['CDE', 'CDF']},
    #            'B': {'o5,o3': ['BDE', 'BDF']},
    #            'D': {'o3': ['DE', 'DF']}}
    if vertex not in self.pattern:
        self.pattern[vertex] = {','.join(observation[current_index:]): []}

    found_obs = False
    result = 'NO'

    # recurses through the children to find the pattern.
    for connection, obs in self.adjacency_matrix[vertex].iteritems():
        if obs == observation[current_index]:
            found_obs = True
            result = self._dp_search(connection, observation, current_index+1)

            if result == 'NO':
                continue

            # creates pattern dictionary in the form described above.
            if result != 'NO':
                for r in result:
                    self.pattern[vertex][','.join(observation[current_index:])].append(vertex + r)

    # if the pattern is not found returns `No`
    if not found_obs or result == 'NO':
        return 'NO'

    return self.pattern[vertex][','.join(observation[current_index:])]

if __name__  == "__main__":
    g = Graph([['A', 'B', 'o1'], ['B', 'D', 'o5'], ['C', 'D', 'o5'], ['D', 'E', 'o3'], ['A', 'C', 'o1'],
               ['C', 'B', 'o3'], ['B', 'A', 'o1'], ['D', 'F', 'o3'], ['D', 'E', 'o3']])
    print g.breadth_first_search('A', ['o1', 'o5', 'o3'])
