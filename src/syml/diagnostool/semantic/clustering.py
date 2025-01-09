import Levenshtein as lv
import numpy as np
from rapidfuzz import fuzz
from sklearn.cluster import AffinityPropagation
from sklearn.metrics.pairwise import cosine_similarity


class Clustering:
    def __init__(self, embeddings, data):
        self.embeddings = embeddings
        self.data = data
        self.get_clusters()

    def clusters_dict(self):
        clustered_sentences = {}
        for sentence_id, cluster_id in enumerate(self.labels_cluster):
            if f"cluster {cluster_id}" not in clustered_sentences.keys():
                clustered_sentences[f"cluster {cluster_id}"] = []

            clustered_sentences[f"cluster {cluster_id}"].append(self.data.index[sentence_id])

        self.clusters = clustered_sentences

    def get_similarity(self):
        sim_lev = np.zeros((len(self.data.index), len(self.data.index)))
        sim_fuzz = np.zeros((len(self.data.index), len(self.data.index)))

        for i, seq_1 in enumerate(self.data.index):
            for j, seq_2 in enumerate(self.data.index):
                sim_lev[i, j] = lv.ratio(seq_1, seq_2)
                sim_fuzz[i, j] = fuzz.partial_ratio(seq_1, seq_2, score_cutoff=75) / 100

        sim = (sim_lev + sim_fuzz + (1 + cosine_similarity(self.embeddings)) / 2) / 3

        self.similarity = sim

    def typo_clustering(self):
        model = AffinityPropagation(affinity="precomputed", max_iter=int(2e3), convergence_iter=100).fit(self.similarity)

        self.labels_cluster = model.labels_

    def get_clusters(self, *args, **kwargs):
        self.get_similarity()
        self.typo_clustering(*args, **kwargs)
        self.clusters_dict()
