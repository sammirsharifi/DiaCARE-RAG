import networkx as nx


class OntologyGraphBuilder:

    def __init__(self, ontology):
        self.onto = ontology

    def build(self):

        G = nx.DiGraph()

        # -----------------------------
        # Add Classes
        # -----------------------------
        for cls in self.onto.classes():
            G.add_node(
                cls.name,
                node_type="Class"
            )

        # -----------------------------
        # Add Individuals
        # -----------------------------
        for ind in self.onto.individuals():

            label = ind.label.first() if ind.label else ind.name

            G.add_node(
                ind.name,
                label=label,
                node_type="Individual"
            )

        # -----------------------------
        # Add Object Properties
        # -----------------------------
        for ind in self.onto.individuals():

            for prop in ind.get_properties():

                if prop.name == "label":
                    continue

                try:

                    values = list(prop[ind])

                except:

                    continue

                for value in values:

                    if hasattr(value, "name"):

                        G.add_edge(
                            ind.name,
                            value.name,
                            relation=prop.name
                        )

        return G