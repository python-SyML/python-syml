from sklearn.cluster import AgglomerativeClustering


class Clustering:
    def __init__(self, embeddings, labels):
        self.embeddings = embeddings
        self.labels = labels

    def init_clustering(self, n_clusters=None, distance_threshold=1.0):
        self.clustering_model = AgglomerativeClustering(n_clusters=n_clusters, distance_threshold=distance_threshold)

    def find_cluster(self):
        self.clustering_model.fit(self.embeddings)
        self.labels_cluster = self.clustering_model.labels_

        clustered_sentences = {}
        for sentence_id, cluster_id in enumerate(self.labels_cluster):
            if f"cluster {cluster_id}" not in clustered_sentences.keys():
                clustered_sentences[f"cluster {cluster_id}"] = []

            clustered_sentences[f"cluster {cluster_id}"].append(self.labels[sentence_id])

        self.clusters = clustered_sentences
