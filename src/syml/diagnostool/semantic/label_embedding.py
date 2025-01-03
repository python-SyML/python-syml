from pathlib import Path

import numpy as np
import torch as pt
from sentence_transformers import SentenceTransformer

from .clustering import Clustering
from .utils import get_device


class LabelEmbedder:
    def __init__(
        self,
        data=None,
        embedding_model="all-MiniLM-L6-v2",
        path="",
        field_name="",
    ):
        self._data = data
        self._labels = data.index
        self.field_name = field_name
        self.path = path
        self.device = get_device()
        self.embedding_model = self.init_model(embedding_model, device=self.device)
        self.embeddings = self.embed(labels=self.labels)
        self.clustering = Clustering(self.embeddings, self.data)
        self._similarities = self.clustering.similarity

    def init_model(self, embedding_model, device):
        return SentenceTransformer(embedding_model, device=device)

    @property
    def data(self):
        return self._data

    @property
    def labels(self):
        return self._labels

    @property
    def similarities(self):
        return self._similarities

    @data.setter
    def data(self, new_data):
        self._data = new_data
        self._labels = new_data.index
        self.embeddings = self.embed(labels=self.labels)
        self.clustering = Clustering(self.embeddings, self.labels)
        self._similarities = self.clustering.similarity

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
