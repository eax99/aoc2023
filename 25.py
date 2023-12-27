# in part 1, we're given a graph that we know is 3-edge-connected:
# there exists a set of three edges that when removed cause the input graph
# to become disconnected, with two separate connected components. our task
# is to find those three edges.
import fileinput
from random import randrange
edges = set()
vertices = set()
for line in fileinput.input():
    line = line.rstrip()
    left, right = line.split(": ")
    vertices.add(left)
    for vertex in right.split():
        edges.add(frozenset([left, vertex]))
        vertices.add(vertex)
print(len(vertices), "vertices", len(edges), "edges")

def print_adjacency_matrix():
    global edges, vertices
    vs_sorted = sorted(vertices)
    vertices_to_numbers = {v:i for i, v in enumerate(vs_sorted)}
    numbers_to_vertices = {i:v for v, i in vertices_to_numbers.items()}
    print("   ", *vs_sorted, sep=" ")
    for i in range(len(vertices)):
        line_vertex = numbers_to_vertices[i]
        #neighbor_list = [
        #    ".1"[int(frozenset([line_vertex, v]) in edges)] for v in vs_sorted]
        neighbor_list = []
        for v in vs_sorted:
            if frozenset([line_vertex, v]) in edges:
                neighbor_list.append(v)
            else: neighbor_list.append("...")
        print(line_vertex, end=" ")
        print(*neighbor_list, sep=" ")
    print("   ", *vs_sorted, sep=" ")
#if len(vertices) == 15: print_adjacency_matrix()

# using https://en.wikipedia.org/wiki/Karger%27s_algorithm for part 1.
# we don't actually need to learn _what_ the three edges in the cut are,
# we only care about how big each of the connected components are.

# preparation for the algorithm: we turn the set of edges into a list of edges,
# because we now might have multiple edges between each pair of vertices.
# we also turn each vertex, which was before just a string holding the vertex's
# label, into a frozenset containing that label -- the idea is that when edges
# are combined, a new vertex is created, and that vertex will have as it's
# "label" a (frozen)set of the labels that were used to create it.
# that way we also keep track of how many original-graph vertices the new
# vertices correspond to, and at the end we also learn how big the two
# connected components are.
# (frozensets because normal sets aren't hashable and can't be set elements.)
k_edges = [set([frozenset([u]), frozenset([v])]) for u, v in edges]

# we won't store the vertices separately from the edges; we'll extract that
# information from the edge list when necessary.
def k_vertices(k_edges):
    vertices = set()
    for edgeset in k_edges:
        vertices.update(edgeset) 
    return vertices

while len(k_vertices(k_edges)) > 2:
    random_index = randrange(len(k_edges))
    random_edge = k_edges.pop(random_index)
    if len(random_edge) != 2 and type(random_edge) != tuple:
        print("random_edge", random_edge, "wasn't a tuple and wasn't of length 2")
        break
    #try:
    (u, v) = random_edge
#    print("looking at edge", random_edge)
    #except ValueError:
    #    print("ValueError; random_edge =", random_edge)
    #else:
    #    print("u =", u, "v =", v)

    # u and v are both frozensets that contain original graph vertex labels.
    # the new vertex will be a frozenset that contains both of those sets'
    # labels, and then we will replace u and v throughout the rest of the
    # graph with this new vertex.
    uv = u | v  # this will be a frozenset because u is a frozenset
#    print("merging edge", random_edge, ": replacing with", uv)
    # update the edge list by replacing references to u or v with uv
    for edge in k_edges:
        # edges themselves are sets, so we can update them in-place
        if u in edge and v in edge:
#            print("--> deleting edge", edge)
            del edge
            continue
        if u in edge:
#            print("--> updating edge", edge, end=" to ")
            edge.remove(u)
            edge.add(uv)
#            print(edge)
        if v in edge:
#            print("--> updating edge", edge, end=" to ")
            edge.remove(v)
            edge.add(uv)
#            print(edge)
#    try:
#        print("after replacing", u, v, "with", uv, "the graph has these vertices:", k_vertices(k_edges))
#    except ValueError:
#        print("ValueError; k_edges =", *k_edges, sep="\n  ")
#        break
#    print()

print("k_edges has", len(k_edges), "elements, which have", len(k_vertices(k_edges)), "vertices")
print("the vertices are:", *k_vertices(k_edges), sep="\n  ")
vlens = list(map(len, k_vertices(k_edges)))
print("and they have lengths:", *vlens, ", product =", vlens[0] * vlens[1])
# i get wildly varying results -- i suppose it's expected for a randomized
# algorithm, but i've gotten answers between 1*3=3 and 9*5=49, and 13*2=26,
# when the correct answer for the test input is 54.
# this approach isn't working.

