from config import CHUNK_SIZE, CHUNK_OVERLAP

def create_chunks(
    text,
    chunk_size=CHUNK_SIZE,
    overlap=CHUNK_OVERLAP
    ):

    """
    Split text into overlapping chunks.
    """

    words = text.split()

    chunks = []

    # Sliding window step
    step = chunk_size - overlap

    # Safety check
    if step <= 0:
        raise ValueError(
            "Overlap must be smaller than chunk size."
        )

    for i in range(0, len(words), step):

        chunk = words[i:i + chunk_size]

        if chunk:
            chunks.append(" ".join(chunk))

    return chunks

if __name__ == "__main__":

    from pdf_loader import load_pdf

    text = load_pdf()

    chunks = create_chunks(text)

    print("=" * 100)
    print("CHUNK INFORMATION")
    print("=" * 100)

    print(f"Chunk Size : {CHUNK_SIZE}")
    print(f"Overlap    : {CHUNK_OVERLAP}")
    print(f"Total Chunks : {len(chunks)}")

    print("\n")

    print("=" * 100)
    print("FIRST CHUNK")
    print("=" * 100)

    print(chunks[0])

    print("\n")

    print("=" * 100)
    print("LAST CHUNK")
    print("=" * 100)

    print(chunks[-1])