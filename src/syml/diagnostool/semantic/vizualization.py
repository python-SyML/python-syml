import pandas as pd
import plotly.express as px
import umap


def plot_umap(embeddings, labels, clusters="red", n_components=2, n_neighbors=2, min_dist=0.1, metric="euclidean"):
    """
    Apply UMAP to a list of strings embedded using SpaCy and plot the result using Plotly.

    Parameters:
    strings (list of str): List of strings to be embedded.
    n_components (int): Number of dimensions to reduce to (2 or 3).
    n_neighbors (int): The size of local neighborhood (in terms of number of neighboring sample points) used for manifold approximation.
    min_dist (float): The effective minimum distance between embedded points.
    random_state (int): Determines the random number generation for initialization.
    """

    # Apply UMAP
    reducer = umap.UMAP(n_components=n_components, n_neighbors=n_neighbors, min_dist=min_dist, metric=metric)
    reduced_data = reducer.fit_transform(embeddings)

    # Create a DataFrame for plotting
    if n_components == 2:
        df = pd.DataFrame(reduced_data, columns=["UMAP1", "UMAP2"])
        df["Label"] = labels
        fig = px.scatter(df, x="UMAP1", y="UMAP2", text="Label", title="UMAP 2D Plot", color=clusters)
        fig.update_traces(marker={"size": 10})
    elif n_components == 3:
        df = pd.DataFrame(reduced_data, columns=["UMAP1", "UMAP2", "UMAP3"])
        df["Label"] = labels
        fig = px.scatter_3d(df, x="UMAP1", y="UMAP2", z="UMAP3", text="Label", title="UMAP 3D Plot")
    else:
        raise ValueError("n_components must be 2 or 3")

    return fig


def plot_similarities(similarities, labels, colors="RdBu_r"):
    fig = px.imshow(similarities, x=labels, y=labels, color_continuous_scale=colors)
    return fig
