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
                            nargs='*',
                            type=argparse.FileType('r'),
                            default=sys.stdin)
    return arg_parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    dot = graphviz.Graph(node_attr={'shape':'plaintext'})
    for geneology_file in args.geneology_data:
        try:
            geneology = yaml.load(geneology_file)
        except yaml.YAMLError as exc:
            print(exc)
            return 1
        draw_graph(dot, geneology)
    if args.verbose:
        print(dot.source)
    dot.render("geneology_chart.gv", view=True)
    return 0


def draw_graph(dot, graph):
    if "family_tree" in graph:
        fam = graph["family_tree"]
        for person_data in  fam:
            person = person_data["person"]
            if "name" in person:
                add_graph_node(dot, person)
                if "parents" in person:
                    for parent_data in person["parents"]:
                        parent = parent_data["parent"]
                        add_graph_node(dot, parent)
                        add_graph_edge(dot, parent, person)
                if "relations" in person:
                    layout = '{{rank=same;\n\t"{}";\n'.format(person["name"])
                    for spouse_data in person["relations"]:
                        spouse = spouse_data["person"]
                        add_graph_node(dot, spouse)
                        add_graph_edge(dot, person, spouse)
                        layout += '\t"{}";\n'.format(spouse["name"])
                    layout += "}\n"
                    dot.body.append(layout)
                if "children" in person:
                    for child_data in person["children"]:
                        child = child_data["child"]
                        add_graph_node(dot, child)
                        add_graph_edge(dot, person, child)



def add_graph_node(dot, person):
    dot.node(person['name'])


def add_graph_edge(dot, ancestor, decendent):
    dot.edge(ancestor['name'], decendent['name'])


if __name__ == '__main__':
    sys.exit(main(sys.argv))