from graph_io import *
from graph import *
from collections import *
import collections

def color_refinement(graphs):

    # initialization
    for graph in graphs:
        for v in graph.vertices:
            v.label = v.degree

    changed = True
    iterations = 0

    while changed:
        changed = False  
        colours_mapping = defaultdict(list)
        new_colour = 0
        
        for graph in graphs:
            for v in graph.vertices:
                neighbor_colours = sorted(n.label for n in v.neighbours)
                colours_mapping[(v.label, tuple(neighbor_colours))].append(v)
        for items in colours_mapping.values():
            new_colour += 1
            for vertex in items:
                if vertex.label != new_colour:
                    changed = True
                vertex.label = new_colour
        iterations += 1


    signature_groups = {}
    # Now after each graoh is coloured, we will create signature for each of them
    # The signature format will be: 
    # "color1:x_color2:y...", indicating x vertices share one color and y vertices has another color.
    for idx, graph in enumerate(graphs):
        color_counts = collections.Counter(vertex.label for vertex in graph.vertices)
        # "color1:2_color2:1", indicating two vertices share one color and one vertex has another color.
        signature = "_".join(f"{label}:{count}" for label, count in sorted(color_counts.items()))
        if signature in signature_groups:
            signature_groups[signature].append(idx)
        else:
            signature_groups[signature] = [idx]
    isomorphic_graph_groups = list(signature_groups.values())

    return isomorphic_graph_groups, iterations

def analyze_groups(graphs, isomorphic_groups):
    analysis_results = []

    for group in isomorphic_groups:
        first_graph_idx = group[0]
        first_graph = graphs[first_graph_idx]
        
        _, iteration_count = color_refinement([first_graph])
        # Discreteness check
        is_discrete = (len(set(v.label for v in first_graph.vertices)) == len(first_graph.vertices))
        
        analysis_results.append((group, iteration_count, is_discrete))

    return analysis_results

def start(graphs):
    isomorphic_groups, _ = color_refinement(graphs)
    results = analyze_groups(graphs, isomorphic_groups)
    return results

# Check algorithm
source = "/Users/ammar/Desktop/Graph/graph_isomorphism/SampleGraphsBasicColorRefinement/repair6.grl"
with open(source, 'r') as file:
    graphs, _ = load_graph(file, Graph, read_list=True)
print("Graups of isomorphc graphs: ")
print("Format: '[isomorphic graphs indexes], iterations, is_discrete'")
print(start(graphs))


