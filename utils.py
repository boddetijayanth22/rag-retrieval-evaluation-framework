import os
import chromadb

from config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
)

# Console Formatting

def print_header(title):
    """Prints a formatted section header."""

    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def print_separator():
    """Prints a separator line."""

    print("-" * 100)

# ChromaDB

def load_collection():
    """Returns the ChromaDB collection."""

    client = chromadb.PersistentClient(
        path=CHROMA_DB_PATH
    )

    return client.get_collection(COLLECTION_NAME)

# Matching Logic

def check_match(expected, document):
    """
    Checks whether the expected keyword(s)
    exist inside the retrieved document.
    """

    if isinstance(expected, str):
        expected = [expected]

    document = document.lower()

    return any(
        keyword.lower() in document
        for keyword in expected
    )

# Metrics

def calculate_metrics(correct, recall_hits, total):

    accuracy = (correct / total) * 100

    recall = (recall_hits / total) * 100

    return accuracy, recall

# Save Evaluation Report

def save_report(report_lines, chunk_size, overlap):

    os.makedirs("results", exist_ok=True)

    filename = (
        f"results/config_{chunk_size}_{overlap}.txt"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("\n".join(report_lines))

    return filename