import networkx as nx
import matplotlib.pyplot as plt
import random
import sys
import os

# global debug variable invoked through CLI to determine whether to print
# debug outputs, and save each state as a graph
debug = False

def read_input(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    # read number of nodes and edges
    num_nodes, num_edges = map(int, lines[0].split())

    # read edges
    edges = []
    for line in lines[1:num_edges + 1]:
        source, target, length = map(int, line.split())
        extra_nodes = length - 1
        new_nodes = range(num_nodes + 1, num_nodes + extra_nodes + 1)
        edges.extend([(source, new_nodes[0])])
        edges.extend([(new_nodes[i], new_nodes[i + 1]) for i in range(extra_nodes - 1)])
        edges.extend([(new_nodes[-1], target)])
        num_nodes += extra_nodes


    # read fail, stop, and start nodes
    fails = list(map(int, lines[num_edges + 2].split()))[1:]
    stops = list(map(int, lines[num_edges + 3].split()))[1:]
    start = int(lines[num_edges + 4].split()[1])

    return num_nodes, num_edges, edges, fails, stops, start

def draw_graph(num_nodes, edges, fails, stops, start, wanderer_location, filename):
    # create a graph
    G = nx.Graph()

    # add nodes
    G.add_nodes_from(range(1, num_nodes + 1))

    # add edges
    G.add_edges_from(edges)

    # draw the graph
    pos = nx.spring_layout(G, seed=1)  # set the seed, so that all graphs look the same
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=300, edge_color='black', linewidths=1, font_size=10)

    # highlight fail, stop, and start nodes as big and colorful
    nx.draw_networkx_nodes(G, pos, nodelist=fails, node_color='red', node_size=1500)
    nx.draw_networkx_nodes(G, pos, nodelist=stops, node_color='green', node_size=1500)
    nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color='skyblue', node_size=1500)

    # make the wanderer location gray so you can better see where he is going
    nx.draw_networkx_nodes(G, pos, nodelist=[wanderer_location], node_color='gray', node_size=300)

    # save the plot as a PNG file
    plt.savefig(filename)

def make_a_random_move(num_nodes, edges, fails, stops, start, wanderer_location):
    # find all edges that contain the wanderer's current location
    relevant_edges = []
    for edge in edges:
        if edge[0] == wanderer_location or edge[1] == wanderer_location:
            relevant_edges.append(edge)

    # extract the other node of each relevant edge as a possible move
    possible_moves = []
    for edge in relevant_edges:
        if edge[0] == wanderer_location:
            possible_moves.append(edge[1])
        elif edge[1] == wanderer_location:
            possible_moves.append(edge[0])

    # choose one move at random
    chosen_move = random.choice(possible_moves)

    # debug prints
    if debug:
        print(f" ")
        print(f" ")
        print(f" ")
        print(f"wanderer is at {wanderer_location}")
        print(f"Relevant edges: {relevant_edges}")
        print(f"wanderer can go to {possible_moves}")
        print(f"wanderer went to {chosen_move}")

    return chosen_move

if __name__ == "__main__":

    # check for command-line invoked debug mode
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        debug = True

    num_nodes, _, edges, fails, stops, start = read_input("input.txt")

    if debug:
        # remove all files from "paths/" directory, so that if the current random walk
        # takes shorter amount of moves than the previous to finish, there wont be
        # old files with higher number left over
        for filename in os.listdir("paths"):
            os.remove(os.path.join("paths", filename))

        print(f"all edges: {edges}")

    wanderer_location = start
    graph_name = 0
    while wanderer_location not in stops and wanderer_location not in fails:
        if debug:
            draw_graph(num_nodes, edges, fails, stops, start, wanderer_location, f"paths/{graph_name}.png")
        chosen_move = make_a_random_move(num_nodes, edges, fails, stops, start, wanderer_location)
        wanderer_location = chosen_move # remember to assign the wanderer his new location
        graph_name += 1

    if debug:
        draw_graph(num_nodes, edges, fails, stops, start, wanderer_location, f"paths/{graph_name}.png")

    # since the loop stopped, this means that the wanderer is either in a STOP or a FAIL
    if wanderer_location in stops:
        print("Wanderer successfully stopped")
    elif wanderer_location in fails:
        print("Wanderer has failed")
