import networkx as nx


class PathRetriever:

    def __init__(self, graph):

        self.graph = graph


    def get_paths(
            self,
            start_node,
            max_depth=3
    ):

        results = []


        for target in self.graph.nodes:

            if target == start_node:
                continue


            try:

                paths = nx.all_simple_paths(
                    self.graph,
                    source=start_node,
                    target=target,
                    cutoff=max_depth
                )


                for path in paths:

                    relations = []

                    for i in range(len(path)-1):

                        edge = self.graph[
                            path[i]
                        ][
                            path[i+1]
                        ]

                        relations.append(
                            edge.get(
                                "relation",
                                "related"
                            )
                        )


                    results.append(
                        {
                            "nodes": path,
                            "relations": relations
                        }
                    )


            except nx.NetworkXNoPath:
                pass


        return results