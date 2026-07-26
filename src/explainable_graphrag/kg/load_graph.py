from owlready2 import *


class DiabetesGraph:

    def __init__(self, path):

        self.onto = get_ontology(path).load()

    def classes(self):

        return list(self.onto.classes())

    def object_properties(self):

        return list(self.onto.object_properties())

    def individuals(self):

        return list(self.onto.individuals())