import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.graph = nx.Graph()

        # PUNTO 2
        self.best_path = []
        self.max_score = float("-inf")
        self.recursion_count = 0

    def get_years(self):
        return DAO.get_all_years()

    def get_states(self, year):
        return DAO.get_states(year)

    def build_graph(self, year, state):
        print("Build graph called")
        self.graph.clear()
        nodes = DAO.get_nodes(year, state)
        self.graph.add_nodes_from(nodes)
        print(f"{self.graph.number_of_nodes()}")

        for a in nodes:
            for b in nodes:
                if a.id < b.id and a.distance_HV(b) < 100:
                    self.graph.add_edge(a, b)

    def print_graph(self):
        _txt = f"Il grafo ha {self.graph.number_of_nodes()} nodi e {self.graph.number_of_edges()} archi"
        print(_txt)
        return _txt

    def conn_components(self):
        n = nx.number_connected_components(self.graph)
        largest_cc = max(nx.connected_components(self.graph), key=len)
        sorted_sightings = sorted(largest_cc, key=lambda sighting: sighting.datetime)
        txt = f"Il numero di componenti connesse è {n} e la componente connessa di dimensione maggiore è:\n"
        for n in sorted_sightings:
            txt += f"{n.city}: {n.datetime}\n"
        print(txt)
        return txt

        ########PUNTO 2##########

    def find_path(self):
        self.max_score = 0
        self.best_path = []
        self.recursion_count = 0

        for n in self.graph.nodes():
            self.recursive(n, [],  [n])

        printable_path = self.printablepath(self.best_path)

        return self.max_score, printable_path

    def recursive(self, last_node, partial, visited):
        self.recursion_count += 1
        if (self.recursion_count % 100 == 0):
            print(f"---------------------{self.recursion_count}--------------------")
        print(f"Calling recursion on node {last_node.id}")  # DEBUG
        # uscita preventiva dalla ricorsione (es cerca cammino di tot archi e noi abbiamo un parziale più lungo di tot
        archiammissibili = self.getArchiAmmissibili(last_node, visited)
        print(f"Archi ammissibili: {archiammissibili}")  # DEBUG

        if not archiammissibili:
            print(f"Exiting from {self.print_easy(visited)}")  # DEBUG
            tot_score = self.compute_score(partial)
            print(f"Tot score: {tot_score}\n")  # DEBUG
            if tot_score > self.max_score:
                self.max_score = tot_score
                self.best_path = copy.deepcopy(partial)
        else:
            for edge in archiammissibili:
                partial.append(edge)
                visited.append(edge[1])
                self.recursive(edge[1], partial, visited)
                partial.pop()
                visited.pop()

    def getArchiAmmissibili(self, last_node, visited):
        output = []
        archi_vicini = self.graph.edges(last_node, data=True)
        for edge in archi_vicini:
            next_node = edge[1]
            res = ""
            if next_node.duration > last_node.duration and next_node not in visited:
                res += f"Duration limit ok. "  # DEBUG
                if not self.max_month_sightings(visited, last_node):
                    res += f"Max month limit ok"  # DEBUG
                    output.append(edge)

        return output

    def max_month_sightings(self, visited, next_node):
        if len(visited) >= 3:
            count = 0
            for n in visited:
                if n.datetime.month == next_node.datetime.month:
                    count += 1
            if count > 2:
                print(f"MAX MONTH LIMIT REACHED\n")  # DEBUG
                return True
        return False

    def compute_score(self, partial):
        tot_score = 0
        for edge in partial:
            a = edge[0]
            b = edge[1]
            if (a.datetime).month == (b.datetime).month:
                tot_score += 200
            else:
                tot_score += 100
        return tot_score

    def printablepath(self, path):
        result = []
        for edge in path:
            a = edge[0].id
            b = edge[1].id
            result.append(
                f"{a}->{b}")
        return result

    def print_easy(self, visited):
        result = ""
        for elem in visited:
            result += f"{elem.id}   "
        return result