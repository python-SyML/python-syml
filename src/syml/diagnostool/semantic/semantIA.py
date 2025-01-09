from .label_embedding import LabelEmbedder
from .vizualization import plot_similarities
from .vizualization import plot_umap


class SementIA:
    def __init__(
        self,
        data,
        path="../python-syml/data/embeddings_{field_name}.pt",
        field_name="",
    ):
        self.data = data
        self.embedder = LabelEmbedder(data=self.data, field_name=field_name, path=path)

    def scatter_labels(self):
        return plot_umap(self.embedder.embeddings, self.embedder.labels, clusters=self.embedder.clustering.labels_cluster.astype(str))

    def heatmap_similiarities(self):
        return plot_similarities(self.embedder.similarities, self.embedder.labels)
