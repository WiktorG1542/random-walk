import random
import sys
import os

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
        # print(f"len(new_nodes): {len(new_nodes)}")
        if len(new_nodes)==0:
            edges.extend([(source, target)])
        else:
            edges.extend([(source, new_nodes[0])])
            edges.extend([(new_nodes[i], new_nodes[i + 1]) for i in range(extra_nodes - 1)])
            edges.extend([(new_nodes[-1], target)])

        num_nodes += extra_nodes

    # read fail, stop, and start nodes
    fails = list(map(int, lines[num_edges + 2].split()))[1:]
    stops = list(map(int, lines[num_edges + 3].split()))[1:]
    start = int(lines[num_edges + 4].split()[1])

    return num_nodes, num_edges, edges, fails, stops, start

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

    return chosen_move

if __name__ == "__main__":
    num_of_tests = None

    if len(sys.argv) > 1:
        try:
            num_of_tests = int(sys.argv[1])
        except ValueError:
            pass

    num_nodes, _, edges, fails, stops, _ = read_input("input.txt")


    myoutput = []  # Initialize a list to store (node number, success probability) pairs

    for start in range(1, num_nodes + 1):
        num_of_fails = 0
        num_of_stops = 0

        for _ in range(num_of_tests):
            wanderer_location = start

            while wanderer_location not in stops and wanderer_location not in fails:
                chosen_move = make_a_random_move(num_nodes, edges, fails, stops, start, wanderer_location)
                wanderer_location = chosen_move

            if wanderer_location in stops:
                num_of_stops += 1
            elif wanderer_location in fails:
                num_of_fails += 1

        success_probability = num_of_stops / num_of_tests * 100
        print(f"{start}\t - {success_probability:.2f}%")
        # myoutput.append((start, success_probability))  # Append (node number, success probability) pair

    # # Sort the myoutput list in descending order of success probability
    # myoutput.sort(key=lambda x: x[1], reverse=True)

    # # Print the sorted output
    # for node, success_probability in myoutput:
    #     print(f"{node}\t - {success_probability:.2f}%")

