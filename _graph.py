from collections import defaultdict


class Graph:

    def __init__(self):
        self._graph_dict= defaultdict(list)

    def add_edge(self, n1, n2, w=0):
        self._graph_dict[n1].append((w, n2))

    def find_loops(self):
        nodes = unvisted_starting_nodes = self._graph_dict.keys()
        loops = set()
        for n in nodes:
            visited = set()
            current_path = tuple()
            try:
                self._find_loops(n, n, current_path, loops, visited)
            except ValueError:
                pass
        return loops

    def _find_loops(self, start_node, current_node, current_path, loops, visited):
        wconnections = self._graph_dict[current_node]
        try:
            w, node = [(w, n) for w, n in wconnections if n == start_node][0]
            current_path += (current_node, w, node),
            loops.add(current_path)
            raise ValueError
        except IndexError:
            pass
        for weight, next_node in wconnections:
            if next_node not in visited:
                visited.add(current_node)
                current_path += (current_node, weight, next_node),
                self._find_loops(start_node, next_node, current_path, loops, visited)
        # raise ValueError



if __name__ == "__main__":
    g = Graph()
    g.add_edge('a', 'b')
    g.add_edge('b', 'c')
    g.add_edge('c', 'a')
    g.add_edge('c', 'd')
    g.add_edge('d', 'e')
    g.add_edge('e', 'c')
    for i in g.find_loops():
        print(i)


