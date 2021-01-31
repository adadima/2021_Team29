from graphviz import Graph
from nsp2gc import *


def get_numerical_nodes(node_variable):
    return node_variable[1] + node_variable[4] + node_variable[7]

def get_compressed_numerical_nodes(node_variable):
    return node_variable[4] + node_variable[7]


GRAPH_ID = 0

def get_graph_colors(nurses):
    return {}


def build_graph(sample, adj_nodes, adj_edges, nurses):
    freq = {nurse: 0 for nurse in range(nurses)}
    for var, nurse in sample.items():
        freq[nurse] = freq.get(nurse, 0) + 1
        
    
    global GRAPH_ID
    dot = Graph(comment=f'nsp{GRAPH_ID}')
    
    for n in adj_nodes:
        numerical = get_numerical_nodes(n)
        dot.node(numerical, label=str(sample[n]))
        
    for e in adj_edges:
        dot.edge(get_numerical_nodes(e[0]), get_numerical_nodes(e[1]))
    
    dot.attr(label="\n".join([f"nurse {i} = {freq[i]} shifts" for i in freq]))

    filename = f'visualize_out/nsp{GRAPH_ID}.gv'
    GRAPH_ID += 1
    return dot, filename

def build_compact_graph(compressed_sample, adj_nodes, adj_edges, nurses):
    
    global GRAPH_ID
    dot = Graph(comment=f'nsp_compressed{GRAPH_ID}')
    
    for n in adj_nodes:
        numerical = get_compressed_numerical_nodes(n)
        dot.node(numerical, label=",".join([str(p) for p in compressed_sample[n[3:]]]))
    
    seen_edges = set()
    for e in adj_edges:
        n1 = get_compressed_numerical_nodes(e[0])
        n2 = get_compressed_numerical_nodes(e[1])
        if n1 == n2 or (n1, n2) in seen_edges or (n2, n1) in seen_edges:
            continue
        seen_edges.add((n1, n2))
        seen_edges.add((n2, n1))
        dot.edge(n1, n2)
    
    filename = f'visualize_out/nsp_compressed{GRAPH_ID}.gv'
    GRAPH_ID += 1
    return dot, filename


def compress_solution(sample, days, shifts, nurses_per_shift):
    compressed = {}
    for d in range(days):
        for s in range(shifts):
            
            day_and_shift = f"d{d}_s{s}"
            nurses = [sample[other_var] for other_var in [f"l{layer}_{day_and_shift}" for layer in range(nurses_per_shift)]]
            
            compressed[day_and_shift] = nurses
    return compressed

if __name__ == "__main__":
    
    adj = nsp_to_graph_coloring(15,2,3,3)
    
    adj_nodes, adj_edges = adj_to_nodes_and_edges(adj)
    
    sample = {'l0_d0_s0': 2, 'l0_d0_s1': 4, 'l0_d0_s2': 7, 'l0_d1_s0': 12, 'l0_d1_s1': 8, 'l0_d1_s2': 14, 'l1_d0_s0': 11, 'l1_d0_s1': 1, 'l1_d0_s2': 9, 'l1_d1_s0': 11, 'l1_d1_s1': 6, 'l1_d1_s2': 0, 'l2_d0_s0': 13, 'l2_d0_s1': 10, 'l2_d0_s2': 3, 'l2_d1_s0': 5, 'l2_d1_s1': 7, 'l2_d1_s2': 9}
    
    dot, filename = build_graph(sample, adj_nodes, adj_edges, 15)
    dot_compressed, filename_compressed = build_compact_graph(compress_solution(sample, 2,3,3), adj_nodes, adj_edges, 15)
    print(dot)
    dot.render(filename, view=True)
    dot_compressed.render(filename_compressed, view=True)