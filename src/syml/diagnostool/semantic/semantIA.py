from .label_embedding import LabelEmbedder
from .vizualization import plot_similarities
from .vizualization import plot_umap


class SementIA:
    def __init__(
        self,
        labels,
        path="",
        field_name="",
    ):
        self.labels = labels
        self.embedder = LabelEmbedder(labels=self.labels, field_name=field_name, path=path)

    def scatter_labels(self):
        return plot_umap(self.embedder.embeddings, self.embedder.labels, clusters=self.embedder.clustering.labels_cluster.astype(str))

    def heatmap_similiarities(self):
        return plot_similarities(self.embedder.similarities, self.embedder.labels)
