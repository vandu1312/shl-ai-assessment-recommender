import pandas as pd

from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity


# =====================================
# LOAD MODEL
# =====================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
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
# CREATE EMBEDDINGS
# =====================================

catalog_embeddings = model.encode(
    df["search_text"].tolist(),
    convert_to_numpy=True
)


# =====================================
# RETRIEVE FUNCTION
# =====================================

def retrieve_assessments(context):

    query_parts = []

    query_parts.extend(
        context["roles"]
    )

    query_parts.extend(
        context["technical"]
    )

    if context["personality"]:
        query_parts.append(
            "personality behavioral communication"
        )

    if context["stakeholder"]:
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
        convert_to_numpy=True
    )

    # =====================================
    # COSINE SIMILARITY
    # =====================================

    similarities = cosine_similarity(
        query_embedding,
        catalog_embeddings
    )[0]

    df["score"] = similarities

    # =====================================
    # SORT RESULTS
    # =====================================

    results = (
        df.sort_values(
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