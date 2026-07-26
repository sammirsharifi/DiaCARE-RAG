from kg.load_graph import DiabetesGraph
from kg.build_graph import OntologyGraphBuilder
from kg.node_mapper import NodeMapper
from retrieval.sapbert_linker import SapBERTLinker
from retrieval.path_retriever import PathRetriever


#----------------Reading Ontology----------------

kg = DiabetesGraph("kg/diabetes_large.owl")

print(len(kg.classes()))

print(len(kg.object_properties()))

print(len(kg.individuals()))



#----------------Build Graph----------------


builder = OntologyGraphBuilder(
    kg.onto
)

G = builder.build()
mapper = NodeMapper(G)



      
print("------------------Graph Info Test---------------------")

print("Nodes :", G.number_of_nodes())

print("Edges :", G.number_of_edges())

print()
print("relations Example:")

count = 0
seen_rel=[]
for u, v, d in G.edges(data=True):

    if d["relation"] != "subClassOf" and d["relation"] not in seen_rel:

        print(u, "--", d["relation"], "-->", v)
        seen_rel.append(d["relation"])
        count += 1

    if count == 10:
        break

print("mapper Example:")
print(
            "73211009",
            " ---> ",
            mapper.id_to_label("73211009")
        )  



print("--------------------------------------")



#----------------sapBERT----------------


sapbert = SapBERTLinker(G)

result = sapbert.link(
    "obesity"
)

print("------------------sapBERT Test---------------------")

print(result)



link_result = sapbert.link(
    "obesity"
)


node_id = link_result["node"]


print(
    "Linked node:",
    node_id,
    link_result["label"]
)


retriever = PathRetriever(G)


paths = retriever.get_paths(
    node_id,
    max_depth=3
)


print(
    "Number of paths:",
    len(paths)
)

for p in paths[:10]:

    print("\nPATH")

    print(
        p["nodes"]
    )

    print(
        p["relations"]
    )


    