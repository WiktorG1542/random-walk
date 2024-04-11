def createMatrix(num_nodes, edges, stops, fails):
    total_connections = {}
    for source, target in edges:
        if source not in total_connections:
            total_connections[source] = set()
        if target not in total_connections:
            total_connections[target] = set()
        total_connections[source].add(target)
        total_connections[target].add(source)

    A = [[1 if i == j else 0 for j in range(num_nodes)] for i in range(num_nodes)]

    for i in range(num_nodes):
        node = i + 1
        if node in stops or node in fails:
            A[i] = [0] * num_nodes
            A[i][i] = 1
        else:
            connections = total_connections.get(node, set())
            m = len(connections)
            for j in connections:
                A[i][j - 1] = -1.0 / m

    return A

def create_vector_b(num_nodes, stops):
    b = [0] * num_nodes
    for stop in stops:
        # Adjust for 1-based indexing by subtracting 1
        b[stop-1] = 1
    return b

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

def eliminacjaGaussaBezWyboru(A, b):
    n = len(A)

    # Eliminacja w przód
    for i in range(n):
        # Sprawdź, czy element na przekątnej jest zerem
        #print(f'i = {i}')
        if A[i][i] == 0:
            raise ZeroDivisionError("Diagonal element is zero.")

        for j in range(i + 1, n):
            #print(f'j = {j}')
            ratio = A[j][i] / A[i][i] # Oblicz współczynnik mnożenia
            #print(f'A[{j}][{i}] = {A[j][i]}, A[{i}][{i}] = {A[i][i]}, ratio = {ratio}')

            for k in range(n):
                A[j][k] -= ratio * A[i][k] # Zaktualizuj elementy w wierszu
                #print(f'nowy A[{j}][{k}] = {A[j][k]}')

            # Zaktualizuj wektor b
            b[j] -= ratio * b[i]
            #print(f'nowy b[{j}] = {b[j]}')

    # Backward substitution
    x = [0 for _ in range(n)]
    #print(f'x = {x}')
    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        #print(f'x[{i}] = {x[i]}')
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
        x[i] = x[i] / A[i][i]
        x[i] = round(x[i], 10)  # rounding to 10 decimal places

    return x

def gauss_elimination_with_partial_pivoting(A, b):
    n = len(A)

    # Forward elimination with partial pivoting
    for i in range(n):
        # Find the maximum element for partial pivoting
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if A[max_row][i] == 0:
            raise ValueError("Matrix is singular.")

        # Swap the maximum row with the current row
        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]

        # Perform the elimination
        for j in range(i+1, n):
            ratio = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= ratio * A[i][k]
            b[j] -= ratio * b[i]

    # Backward substitution
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = b[i]
        for j in range(i+1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
        x[i] = round(x[i], 10) # rounding to 10 decimal places

    return x

def gauss_seidel(A, b, tolerance=1e-10, max_iterations=1000):
    """
    Gauss-Seidel iterative method for solving linear equations.

    Args:
    A: Coefficient matrix
    b: Right-hand side vector
    tolerance: Tolerance for the convergence of the algorithm
    max_iterations: Maximum number of iterations

    Returns:
    x: Solution vector
    """
    n = len(A)
    x = [0 for _ in range(n)]  # Initial guess of the solution
    for iteration in range(max_iterations):
        x_new = x.copy()
        for i in range(n):
            sum_Ax = sum(A[i][j] * x_new[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - sum_Ax) / A[i][i]
            x_new[i] = round(x_new[i], 10)  # Rounding to handle floating-point precision

        # Convergence check
        if all(abs(x_new[i] - x[i]) <= tolerance for i in range(n)):
            return x_new, iteration  # Converged

        x = x_new

    raise Exception("Gauss-Seidel method did not converge within the maximum number of iterations")

num_nodes, num_edges, edges, fails, stops, start = read_input("input.txt")
P = createMatrix(num_nodes, edges, fails, stops)
b = create_vector_b(num_nodes, stops)
P2, b2 = P, b
P3, b3 = P, b


x = eliminacjaGaussaBezWyboru(P, b)
y = gauss_elimination_with_partial_pivoting(P2, b2)
z, ilosc = gauss_seidel(P3, b3)
#
#
# for i in range(len(P)):
#     for j in range(len(P[i])):
#         print(P[i][j], end=" ")
#     print("\n")
#
# print(b)
#
print("Eliminacja Gaussa bez wyboru elementu podstawowego:")
print(f'{x}')
print("Eliminacja Gaussa z czesciowym wyborem elementu podstawowego:")
print(f'{y}')
print("Metoda Gaussa-Seidela:")
print(f'{z}')