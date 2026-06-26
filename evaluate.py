from utils import (
    print_header,
    print_separator,
    load_collection,
    check_match,
    calculate_metrics,
    save_report,
)

from config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    TOP_K,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

from test_queries import TEST_QUERIES

# Evaluate a single query

def evaluate_query(collection, test_case):

    results = collection.query(
        query_texts=[test_case["query"]],
        n_results=TOP_K
    )

    return {
        "documents": results["documents"][0],
        "distances": results["distances"][0],
        "metadatas": results["metadatas"][0]
    }

# Main Evaluation

def evaluate():

    print_header(" RETRIEVAL EVALUATION ")

    collection = load_collection()

    print(f"Collection Name : {COLLECTION_NAME}")
    print(f"Stored Chunks   : {collection.count()}")

    print()

    total_queries = len(TEST_QUERIES)

    correct_top1 = 0
    recall_hits = 0

    report_lines = []

    failure_log = []

    for test in TEST_QUERIES:

        query = test["query"]
        expected = test["expected"]
        topic = test["topic"]

        result = evaluate_query(
            collection,
            test
        )

        retrieved_docs = result["documents"]
        distances = result["distances"]
        metadatas = result["metadatas"]

        if not retrieved_docs:

            print(f" No results returned for query: {query}")

            continue

        top_doc = retrieved_docs[0]

        # Accuracy

        if check_match(expected, top_doc):

            status = "PASS"

            correct_top1 += 1

        else:

            status = "FAIL"

        # Recall@K

        hit = any(
            check_match(expected, doc)
            for doc in retrieved_docs
        )

        if hit:
            recall_hits += 1

        # Print Results

        print_separator()

        print(f"Topic      : {topic}")
        print(f"Query      : {query}")
        print(f"Expected   : {expected}")
        print(f"Result     : {status}")

        print("\n Retrieved Chunks:\n")

        for rank, (doc, distance, metadata) in enumerate(
            zip(
                retrieved_docs,
                distances,
                metadatas
            ),
            start=1
        ):

            print(f"Rank {rank}")

            print(f"Distance   : {distance:.4f}")

            print(f"Chunk ID   : {metadata['chunk_id']}")

            print(f"Source     : {metadata['source']}")

            print()

            print(doc[:180])

            print()

        report_lines.append("-" * 100)

        report_lines.extend([
            "-" * 100,
            f"Topic      : {topic}",
            f"Query      : {query}",
            f"Expected   : {expected}",
            f"Result     : {status}",
            f"Distance   : {distances[0]:.4f}",
            f"Chunk ID   : {metadatas[0]['chunk_id']}",
            ""
            ])

        if status == "FAIL":

            failure_log.append({

                "topic": topic,

                "query": query,

                "expected": expected,

                "retrieved": top_doc,

                "distance": distances[0],

                "chunk_id": metadatas[0]["chunk_id"],
                
                "source": metadatas[0]["source"]

            })

    accuracy, recall = calculate_metrics(
    correct_top1,
    recall_hits,
    total_queries
    )

    # Final Summary

    summary = f"""
    
    FINAL REPORT

    Chunk Size : {CHUNK_SIZE}
    Overlap    : {CHUNK_OVERLAP}

    Total Queries : {total_queries}

    PASS : {correct_top1}
    FAIL : {total_queries - correct_top1}

    Accuracy : {accuracy:.2f}%
    Recall@{TOP_K} : {recall:.2f}%
    """

    print(summary)

    report_lines.append(summary)

    # Save Report

    report_file = save_report(
    report_lines,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

    print(f"Report saved successfully:")
    print(report_file)

    # Failure Analysis

    if failure_log:

        print("\n" + "=" * 100)
        print(" FAILURE ANALYSIS ")
        print("=" * 100)

        for failure in failure_log:

            print(f"\n Topic      : {failure['topic']}")
            print(f"Query      : {failure['query']}")
            print(f"Expected   : {failure['expected']}")
            print(f"Chunk ID   : {failure['chunk_id']}")
            print(f"Distance   : {failure['distance']:.4f}")

            print("\n Retrieved Chunk:\n")

            print(failure["retrieved"][:300])

            print("-" * 100)

    else:

        print("\n No retrieval failures found!")
    
if __name__ == "__main__":
    evaluate()