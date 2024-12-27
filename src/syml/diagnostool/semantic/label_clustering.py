from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import torch as pt
import umap
from sentence_transformers import SentenceTransformer

from .utils import get_device


class LabelAnalysis:
    def __init__(
        self,
        labels=None,
        embedding_model="all-MiniLM-L6-v2",
        path="",
        field_name="",
    ):
        self._labels = labels
        self.field_name = field_name
        self.path = path
        self.device = get_device()
        self.embedding_model = self.init_model(embedding_model, device=self.device)
        self.embeddings = self.embed(labels=self.labels)

    def init_model(self, embedding_model, device):
        return SentenceTransformer(embedding_model, device=device)

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels):
        self._labels = labels
        self.embeddings = self.embed(labels=self.labels)

    def embed(self, labels=None):
        path = Path(self.path.format(field_name=self.field_name))
        if labels is None or np.all(labels == self.labels):
            labels = self.labels
        if (not hasattr(self, "embeddings")) or (self.embeddings is None) or np.any(labels != self.labels):
            if path.exists():
                embeds = pt.load(path)
                if embeds.shape[0] == len(labels):
                    return embeds
            embeds = self.embedding_model.encode(labels)
            pt.save(embeds, self.path.format(field_name=self.field_name))
            return embeds
        else:
            return self.embeddings

    def plot_umap(self, labels=None, n_components=2, n_neighbors=2, min_dist=0.1, metric="euclidean"):
        """
        Apply UMAP to a list of strings embedded using SpaCy and plot the result using Plotly.

        Parameters:
        strings (list of str): List of strings to be embedded.
        n_components (int): Number of dimensions to reduce to (2 or 3).
        n_neighbors (int): The size of local neighborhood (in terms of number of neighboring sample points) used for manifold approximation.
        min_dist (float): The effective minimum distance between embedded points.
        random_state (int): Determines the random number generation for initialization.
        """

        if labels is None:
            labels = self.labels
        else:
            self.labels = labels

        embeddings = self.embeddings

        # Apply UMAP
        reducer = umap.UMAP(n_components=n_components, n_neighbors=n_neighbors, min_dist=min_dist, metric=metric)
        reduced_data = reducer.fit_transform(embeddings)

        # Create a DataFrame for plotting
        if n_components == 2:
            df = pd.DataFrame(reduced_data, columns=["UMAP1", "UMAP2"])
            df["Label"] = labels
            fig = px.scatter(df, x="UMAP1", y="UMAP2", text="Label", title="UMAP 2D Plot")
        elif n_components == 3:
            df = pd.DataFrame(reduced_data, columns=["UMAP1", "UMAP2", "UMAP3"])
            df["Label"] = labels
            fig = px.scatter_3d(df, x="UMAP1", y="UMAP2", z="UMAP3", text="Label", title="UMAP 3D Plot")
        else:
            raise ValueError("n_components must be 2 or 3")

        return fig
