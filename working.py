from graph_io import *
from graph import *
from collections import *
import collections

source = "/Users/ammar/Desktop/Graph Project/SampleGraphsBasicColorRefinement/test_iter.grl"

def refine_colors(list_of_graphs):

    # initialization
    for graph in list_of_graphs:
        for v in graph.vertices:
            v.label = v.degree

    flag = True
    iterations = 0

    while flag:
        flag = False  # Reset change flag for this iteration
        color_neighborhood_map = defaultdict(list)
        for graph in list_of_graphs:
            for vertex in graph.vertices:
                neighbor_colors = sorted(n.label for n in vertex.neighbours)
                color_neighborhood_map[(vertex.label, tuple(neighbor_colors))].append(vertex)

        new_color = 0

        for group in color_neighborhood_map.values():
            new_color += 1
            for vertex in group:
                if vertex.label != new_color:
                    flag = True
                vertex.label = new_color
        iterations += 1

    color_distribution_groups = {}

    for index, graph in enumerate(list_of_graphs):
        color_distribution = tuple(sorted(Counter(vertex.label for vertex in graph.vertices).items()))
        if color_distribution in color_distribution_groups:
            color_distribution_groups[color_distribution].append(index)
        else:
            color_distribution_groups[color_distribution] = [index]
    potentially_isomorphic_groups = [group for group in color_distribution_groups.values()]
    return potentially_isomorphic_groups, iterations
    # signature_groups = {}
    # for idx, graph in enumerate(graphs):
    #     # Create a color distribution signature as a string
    #     color_counts = collections.Counter(vertex.label for vertex in graph.vertices)
    #     # Sort the labels and create a signature string: "label1:count1_label2:count2_..."
    #     signature = "_".join(f"{label}:{count}" for label, count in sorted(color_counts.items()))
        
    #     # Group graphs by their signatures
    #     if signature in signature_groups:
    #         signature_groups[signature].append(idx)
    #     else:
    #         signature_groups[signature] = [idx]
    
    # # Extract groups from the dictionary, these are lists of indices of potentially isomorphic graphs
    # isomorphic_graph_groups = list(signature_groups.values())

    # return isomorphic_graph_groups, iterations


# Fully changed
def discrete_check(graph):
    discrete = len(set(v.label for v in graph.vertices)) == len(graph.vertices)
    return discrete

def process(graphs):

    potentially_isomorphic_groups, iterations = refine_colors(graphs)
    final = list()
    for group in potentially_isomorphic_groups:
        graph = graphs[group[0]]

        _, iterations = refine_colors([graph])
        instance = []
        instance.append(group)
        instance.append(iterations)
        final.append(instance)
        final.append(discrete_check(graph))
    print(final)



with open(source, 'r') as file:
    graphs, options = load_graph(file, Graph, read_list=True)
process(graphs)

# from graph import Graph
# from graph_io import *
# from collections import OrderedDict

# def colour_refinement(graph: Graph):
#     # Colouring initialization based on vertex degree: v.label
#     for v in graph.vertices:
#         v.label = len(v.neighbours)
    
#     # Find the maximum initial label value to start new colours
#     colour_counter = max(v.label for v in graph.vertices) + 1
#     changed = True
#     iterations = 0

#     while changed:
#         changed = False
#         iterations += 1
#         print("iteration: ", iterations )

#         # Group vertices by their current label (colour)
#         colour_groups = {}
#         for v in graph.vertices:
#             if v.label in colour_groups:
#                 colour_groups[v.label].append(v)
#             else:
#                 colour_groups[v.label] = [v]
#         colour_groups = {k: colour_groups[k] for k in sorted(colour_groups)}
#         print("colors_groups: ", colour_groups)
#         for colour, vertices in colour_groups.items():
#             print("started with: ", vertices )
#             if len(vertices) > 1:
#                 # Create neighbour colour signature groups
#                 neighbour_colours = {}
#                 for v in vertices:
#                     signature = tuple(sorted([n.label for n in v.neighbours]))
#                     if signature in neighbour_colours:
#                         neighbour_colours[signature].append(v)
#                     else:
#                         neighbour_colours[signature] = [v]

#                 # Assign new colours if there is more than one unique signature
#                 if len(neighbour_colours) > 1:
#                     changed = True
#                     # Skip the first colour group to maintain the original colour
#                     first_signature = True
#                     for signature, sig_vertices in neighbour_colours.items():
#                         if first_signature:
#                             first_signature = False
#                             continue
#                         for sig_vertex in sig_vertices:
#                             print("changed ", sig_vertex.label, " to color ", colour_counter)
#                             sig_vertex.label = colour_counter
#                         colour_counter += 1

#     # Determine if the colouring is discrete
#     discrete = len(set(v.label for v in graph.vertices)) == len(graph.vertices)

#     # The output has been adjusted to match the requested format


#     return graph, discrete, iterations


# def compare_graphs_colour_refinement(graphs):
#     results = []
#     for graph in graphs:
#         coloured_graph, discrete = colour_refinement(graph)
#         results.append([coloured_graph, discrete])

#     # Compare the colour distributions to find potentially isomorphic graphs
#     isomorphic_sets = []
#     for i, result_i in enumerate(results):
#         for j, result_j in enumerate(results):
#             if i >= j:  # Avoid repeating comparisons
#                 continue
#             # Check if the two graphs have the same colour distribution
#             if len(result_i[0]) != len(result_j[0]):
#                 continue

#             # Sort the vertices based on their labels and degree (number of neighbours)
#             sorted_vertices1 = sorted(result_i[0], key=lambda v: (v.label, len(v.neighbours)))
#             sorted_vertices2 = sorted(result_j[0], key=lambda v: (v.label, len(v.neighbours)))

#             # Check if the sorted sequences of labels and incidences match
#             for v1, v2 in zip(sorted_vertices1, sorted_vertices2):
#                 if v1.label == v2.label and len(v1.neighbours) == len(v2.neighbours):
#                     isomorphic_sets.append((i, j, result_i[1], result_i[1]))


#     return isomorphic_sets


# def draw_graph(graph: Graph, file_name):
#     # for v in graph.vertices:
#     #     v.colornum = 
#     with open(file_name+".dot", 'w') as file:
#         write_dot(graph, file)
# # Ensure that for every label in Graph 0, 
# # there is an equal number of vertices with the same label in Graph 2.
# def check_label_number(vertices1, vertices2):
#     # Step 1: Vertex Label Matching
#     label_counts1 = {v.label: 0 for v in vertices1}
#     label_counts2 = {v.label: 0 for v in vertices2}

#     for v in vertices1:
#         label_counts1[v.label] += 1
#     for v in vertices2:
#         label_counts2[v.label] += 1

#     if label_counts1 != label_counts2:
#         return False, "Label distribution does not match."

#     # Step 2: Degree Matching (already considered as we use #incident for comparison)
#     # Assuming degree is correctly reflected by the #incident attribute

#     return True, "Graphs might be isomorphic based on labels and degrees."

# def verify_degree_distribution(vertices1, vertices2):
#     # Create a dictionary to store degree distributions for each label
#     degree_distribution1 = {}
#     degree_distribution2 = {}

#     # Fill the degree distributions for Graph 1
#     for v in vertices1:
#         label = v.label
#         degree = len(v.neighbours)  # Assuming 'neighbours' list/attribute exists and reflects the degree
#         if label not in degree_distribution1:
#             degree_distribution1[label] = []
#         degree_distribution1[label].append(degree)

#     # Fill the degree distributions for Graph 2
#     for v in vertices2:
#         label = v.label
#         degree = len(v.neighbours)
#         if label not in degree_distribution2:
#             degree_distribution2[label] = []
#         degree_distribution2[label].append(degree)

#     # Sort the lists to facilitate direct comparison
#     for label in degree_distribution1:
#         degree_distribution1[label].sort()
#     for label in degree_distribution2:
#         degree_distribution2[label].sort()

#     # Check if degree distributions match for each label
#     for label, degrees1 in degree_distribution1.items():
#         degrees2 = degree_distribution2.get(label, None)
#         if degrees2 is None or degrees1 != degrees2:
#             return False, f"Degree distribution does not match for label {label}."

#     return True, "Degree distributions match for all labels."

# def check_isomorphism(graphs):
#     results = []
#     for graph in graphs:
#         coloured_graph, discrete, iteration = colour_refinement(graph)
#         results.append([coloured_graph, discrete, iteration])

#     # Compare graphs
#     isomorphic_sets = []
#     for i, result_i in enumerate(results):
#         isomorphic_sets.append([[i], result_i[2], result_i[1]])
#         for j, result_j in enumerate(results):
#             if i >= j:  # Avoid repeating comparisons
#                 continue
#             # Ensure that for every label in Graph 0, there is an equal number 
#             # of vertices with the same label in Graph 2.
#             condition1 = check_label_number(result_i[0].vertices, result_j[0].vertices)

#             # Check tha both of thew will be whether discrete or both not
#             condition2 = (result_i[1] == result_j[1])
            
#             condition3 = verify_degree_distribution(result_i[0].vertices, result_j[0].vertices)
#             # Verify that vertices with the same label across both graphs also share the same degree (number of incidents)
#             if (condition1 == True and condition2 == True and condition3== True):
#                 isomorphic_sets[i][0].append(j)
#     return isomorphic_sets


# def colour_ref(path_file):
#     with open(path_file) as file:
#         g = load_graph(file, Graph, read_list=True)
    
#     graph_list = g[0]
#     # print(check_isomorphism(graph_list))
#     # print(compare_graphs_colour_refinement(graph_list))
#     # print(graph_list)

#     coloured_graph_0 = colour_refinement(graph_list[0])
#     coloured_graph_2 = colour_refinement(graph_list[4])
#     draw_graph(graph_list[4], "fil1qe.dot")
#     print("Graph 0: \n")
#     print(coloured_graph_0[0], "\n", coloured_graph_0[0].vertices, "\n", coloured_graph_0[0].edges)
    
#     print("Graph 2: \n")
#     print(coloured_graph_2[0], "\n", coloured_graph_2[0].vertices, "\n", coloured_graph_2[0].edges)

#     print(coloured_graph_2)

#     # Ensure that for every label in Graph 0, there is an equal number 
#     # of vertices with the same label in Graph 2.
#     print(check_label_number(coloured_graph_0[0].vertices, coloured_graph_2[0].vertices))

#     # Check tha both of thew will be whether discrete or both not
#     print(coloured_graph_0[1] == coloured_graph_2[1])

#     # Verify that vertices with the same label across both graphs also share the same degree (number of incidents)
#     print(verify_degree_distribution(coloured_graph_0[0].vertices, coloured_graph_2[0].vertices))

# colour_ref("/Users/ammar/Desktop/Graph Project/SampleGraphsBasicColorRefinement/colorref_largeexample_6_960.grl")












