import random
import string

import pandas as pd
import torch


def get_device():
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    return device


def generate_typo(text, typo_type):
    """
    Generate a single typo for a given string based on the specified typo type.

    Parameters:
    text (str): The original string.
    typo_type (str): The type of typo to generate ('insertion', 'deletion', 'substitution', 'transposition').

    Returns:
    str: The string with the generated typo.
    """
    if len(text) == 0:
        return ""

    typo_text = text

    if typo_type == "insertion":
        pos = random.randint(0, len(typo_text))  # noqa: S311
        char = random.choice(string.ascii_lowercase)  # noqa: S311
        typo_text = typo_text[:pos] + char + typo_text[pos:]

    elif typo_type == "deletion":
        if len(typo_text) > 1:
            pos = random.randint(0, len(typo_text) - 1)  # noqa: S311
            typo_text = typo_text[:pos] + typo_text[pos + 1 :]

    elif typo_type == "substitution":
        if len(typo_text) > 0:
            pos = random.randint(0, len(typo_text) - 1)  # noqa: S311
            char = random.choice(string.ascii_lowercase)  # noqa: S311
            typo_text = typo_text[:pos] + char + typo_text[pos + 1 :]

    elif typo_type == "transposition":
        if len(typo_text) > 1:
            pos = random.randint(0, len(typo_text) - 2)  # noqa: S311
            typo_text = typo_text[:pos] + typo_text[pos + 1] + typo_text[pos] + typo_text[pos + 2 :]
    else:
        raise ValueError("Invalid typo type.")

    return typo_text


def generate_typos(text, num_typos=3):
    """
    Generate typos for a given string.

    Parameters:
    text (str): The original string.
    num_typos (int): The number of typos to generate.

    Returns:
    list of str: A list of strings with typos.
    """
    typos = []
    typo_types = ["insertion", "deletion", "substitution", "transposition"]

    for _ in range(num_typos):
        typo_text = generate_typo(text, random.choice(typo_types))  # noqa: S311
        typos.append(typo_text)

    return typos


def generate_typos_for_list(strings, n_typos=3):
    """
    Generate typos for a list of strings using Pandas `pd.apply`.

    Parameters:
    strings (list of str): The list of original strings.
    n_typos (int): The number of typos to generate for each string.

    Returns:
    pd.DataFrame: A DataFrame where each row contains the original string and its corresponding typos.
    """
    # Create a DataFrame from the list of strings
    df = pd.DataFrame(strings, columns=["Original"])

    # Apply the generate_typos function to each row
    df["Typos"] = df["Original"].apply(lambda x: generate_typos(x, num_typos=n_typos))

    # Explode the list of typos into separate rows
    df_exploded = df.explode("Typos").reset_index(drop=True)

    return df_exploded


def df_typo(labels, n_typos=5):
    return generate_typos_for_list(labels, n_typos=n_typos)["Typos"].unique()
