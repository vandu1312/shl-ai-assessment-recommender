import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# =====================================
# LOAD LIGHTWEIGHT MODEL
# =====================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu"
)

# =====================================
# LOAD DATASET
# =====================================

df = pd.read_csv(
    "data/shl_assessments.csv"
)

df = df.fillna("")

df = df.drop_duplicates(
    subset=["name"]
)

# =====================================
# CREATE SEARCH TEXT
# =====================================

df["search_text"] = (
    df["name"].astype(str)
    + " "
    + df["test_type"].astype(str)
)

# =====================================
# LIMIT DATASET SIZE FOR MEMORY
# =====================================

df = df.head(300)

# =====================================
# CREATE EMBEDDINGS ONCE
# =====================================

catalog_embeddings = model.encode(
    df["search_text"].tolist(),
    convert_to_numpy=True,
    show_progress_bar=False
)

# =====================================
# RETRIEVE FUNCTION
# =====================================

def retrieve_assessments(context):

    query_parts = []

    query_parts.extend(
        context.get("roles", [])
    )

    query_parts.extend(
        context.get("technical", [])
    )

    if context.get("personality"):

        query_parts.append(
            "personality behavioral communication"
        )

    if context.get("stakeholder"):

        query_parts.append(
            "stakeholder communication teamwork"
        )

    query = " ".join(query_parts)

    if not query.strip():

        return []

    # =====================================
    # QUERY EMBEDDING
    # =====================================

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        show_progress_bar=False
    )

    # =====================================
    # COSINE SIMILARITY
    # =====================================

    similarities = cosine_similarity(
        query_embedding,
        catalog_embeddings
    )[0]

    temp_df = df.copy()

    temp_df["score"] = similarities

    # =====================================
    # SORT RESULTS
    # =====================================

    results = (
        temp_df.sort_values(
            by="score",
            ascending=False
        )
        .head(10)
    )

    # =====================================
    # RETURN FORMAT
    # =====================================

    return results[
        ["name", "url", "test_type"]
    ].to_dict(orient="records")
