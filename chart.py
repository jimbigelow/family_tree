"""reads a family geneology in a yaml file and draws a chart"""


import argparse
import sys
import yaml
import graphviz


def parse_args(argv):
    sys.argv = argv
    arg_parser = argparse.ArgumentParser(prog=argv.pop(0),
                                         description="reads and created a "
                                                     "geneology charty")
    arg_parser.add_argument("-v", '--verbose', help="verbose mode",
                            default=False, action="store_true")
    arg_parser.add_argument('geneology',
                            help='the optional input file to process, '
                                 'defaults to stdin',
                            nargs='?',
                            type=argparse.FileType('r'),
                            default=sys.stdin)
    return arg_parser.parse_args(argv)

def add_nodes(nodes, dot):
    for node_def in nodes:
        if type(node_def) is str:
            dot.node(node_def)
        elif type(node_def) is dict:
            n = node_def.keys()[0]
            if node_def[n].has_key('name'):
                name = node_def[n]['name']
                del node_def[n]['name']
                dot.node(n, name, node_def[n] )
            else:
                dot.node(node_def.keys()[0], _attributes=node_def[n])
        else:
            raise ("unknown node type {}".format(type(node_def)))

def add_edges(edges, dot):
    for edge in edges:
        if type(edge) is str:
            start_pt = edge.split()[0]
            end_pt = edge.split()[1]
            dot.edge(start_pt, end_pt)
        elif type(edge) is dict:
            e = edge.keys()[0]
            start = e.split()[0]
            end   = e.split()[1]
            dot.edge(start, end, _attributes=edge[e])



def main(argv):
    args = parse_args(argv)

    try:
        graph = yaml.load(args.input)
    except yaml.YAMLError as exc:
        print(exc)
        return 1
    draw_graph(args, graph)
    return 0


def draw_graph(args, graph):
    dot = graphviz.Digraph()
    if "family_tree" in graph:
        pass
    # for kw in graph:
    #     if kw == "digraph":
    #         g = graph["digraph"]
    #         for g_kw in g:
    #             if g_kw == "nodes":
    #                 add_nodes(g["nodes"], dot)
    #             elif g_kw == "edges":
    #                 add_edges(g["edges"], dot)
    #             else:
    #                 dot.graph_attr[g_kw] = g[g_kw]
    #         if args.verbose:
    #             print(dot.source)
    #         name = "g"
    #         if "name" in g:
    #             name = g["name"]
    #         dot.render(name + ".gv", view=True)


if __name__ == '__main__':
    sys.exit(main(sys.argv))