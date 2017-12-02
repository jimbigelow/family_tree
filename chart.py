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
    arg_parser.add_argument('geneology_data',
                            help='the optional input file to process, '
                                 'defaults to stdin',
                            nargs='?',
                            type=argparse.FileType('r'),
                            default=sys.stdin)
    return arg_parser.parse_args(argv)

def add_graph_node(dot, name):
    dot.node(name)


def add_graph_edge(dot, ancestor, decendent):
    dot.edge(ancestor, decendent)


def main(argv):
    args = parse_args(argv)

    try:
        graph = yaml.load(args.geneology_data)
    except yaml.YAMLError as exc:
        print(exc)
        return 1
    draw_graph(args, graph)
    return 0


def draw_graph(args, graph):
    dot = graphviz.Graph(node_attr={'shape':'plaintext'})
    if "family_tree" in graph:
        fam = graph["family_tree"]
        if "person" in fam:
            person = fam["person"]
            if "name" in person:
                add_graph_node(dot, person["name"])
                if "parents" in person:
                    for parent_data in person["parents"]:
                        parent = parent_data["parent"]
                        add_graph_node(dot, parent["name"])
                        add_graph_edge(dot, parent["name"], person["name"])
                if "relations" in person:
                    layout = '{{rank=same;\n\t"{}";\n'.format(person["name"])
                    for spouse_data in person["relations"]:
                        spouse = spouse_data["person"]
                        add_graph_node(dot, spouse["name"])
                        add_graph_edge(dot, person["name"], spouse["name"])
                        layout += '\t"{}";\n'.format(spouse["name"])
                        if "children" in spouse:
                            for child_data in spouse["children"]:
                                child = child_data["child"]
                                add_graph_node(dot, child['name'])
                                add_graph_edge(dot, spouse['name'],
                                               child['name'])
                                add_graph_edge(dot, person['name'],
                                               child['name'])
                    layout += "}\n"
                    dot.body.append(layout)

    if args.verbose:
        print(dot.source)
    dot.render("geneology_chart.gv", view=True)

if __name__ == '__main__':
    sys.exit(main(sys.argv))